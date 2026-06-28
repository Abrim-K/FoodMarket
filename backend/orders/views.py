from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Order, OrderItem
from .serializers import OrderSerializer, CreateOrderSerializer
from cart.models import Cart


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all().order_by('-created_at')
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        # Получаем корзину пользователя
        cart = get_object_or_404(Cart, user=request.user)

        # Проверяем, что корзина не пуста
        if not cart.items.exists():
            return Response(
                {'error': 'Корзина пуста'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Создаём заказ
        order = Order.objects.create(
            user=request.user,
            full_name=data['full_name'],
            phone=data['phone'],
            email=data['email'],
            address=data['address'],
            comment=data.get('comment', ''),
            delivery_price=0
        )

        # Переносим товары из корзины в заказ
        total = 0
        for cart_item in cart.items.all():
            order_item = OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            total += order_item.total_price

            product = cart_item.product
            product.purchases_count += cart_item.quantity
            product.save(update_fields=['purchases_count'])

        # Обновляем общую сумму заказа
        order.total_price = total
        order.save()

        # Очищаем корзину
        cart.items.all().delete()

        # Возвращаем созданный заказ
        order_serializer = self.get_serializer(order)
        return Response(order_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Отмена заказа (пользователь)"""
        order = self.get_object()

        # Проверяем, что пользователь владелец заказа или админ
        if order.user != request.user and not request.user.is_staff:
            return Response(
                {'error': 'Вы не можете отменить этот заказ'},
                status=status.HTTP_403_FORBIDDEN
            )

        if order.status not in ['pending', 'confirmed']:
            return Response(
                {'error': 'Заказ не может быть отменён'},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = 'cancelled'
        order.save()
        return Response({'message': 'Заказ отменён'})

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Обновление статуса заказа (только для администратора)"""
        if not request.user.is_staff:
            return Response(
                {'error': 'Доступ запрещён'},
                status=status.HTTP_403_FORBIDDEN
            )

        order = self.get_object()
        new_status = request.data.get('status')

        if new_status not in dict(Order.STATUS_CHOICES):
            return Response(
                {'error': 'Некорректный статус'},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = new_status
        order.save()
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Удаление заказа (только для администратора)"""
        if not request.user.is_staff:
            return Response(
                {'error': 'Доступ запрещён. Только для администратора.'},
                status=status.HTTP_403_FORBIDDEN
            )

        order = self.get_object()
        order.delete()
        return Response(
            {'message': f'Заказ #{order.id} успешно удалён'},
            status=status.HTTP_200_OK
        )
