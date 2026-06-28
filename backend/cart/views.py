from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from products.models import Product

class CartViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartSerializer

    def get_cart(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart

    def list(self, request):
        cart = self.get_cart()
        serializer = self.get_serializer(cart, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add_item(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        if not product_id:
            return Response(
                {'error': 'product_id обязателен'},
                status=status.HTTP_400_BAD_REQUEST
            )

        product = get_object_or_404(Product, id=product_id)

        if not product.is_published:
            return Response(
                {'error': 'Товар не доступен для покупки'},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart = self.get_cart()
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()

        serializer = CartItemSerializer(cart_item, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def update_item(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')

        if not product_id or quantity is None:
            return Response(
                {'error': 'product_id и quantity обязательны'},
                status=status.HTTP_400_BAD_REQUEST
            )

        quantity = int(quantity)
        if quantity <= 0:
            return self.remove_item(request)

        cart = self.get_cart()
        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
        cart_item.quantity = quantity
        cart_item.save()

        serializer = CartItemSerializer(cart_item, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def remove_item(self, request):
        product_id = request.data.get('product_id')

        if not product_id:
            return Response(
                {'error': 'product_id обязателен'},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart = self.get_cart()
        deleted, _ = CartItem.objects.filter(cart=cart, product_id=product_id).delete()

        if deleted:
            return Response(
                {'message': 'Товар удалён из корзины'},
                status=status.HTTP_200_OK
            )
        return Response(
            {'error': 'Товар не найден в корзине'},
            status=status.HTTP_404_NOT_FOUND
        )

    @action(detail=False, methods=['post'])
    def clear(self, request):
        cart = self.get_cart()
        cart.items.all().delete()
        return Response(
            {'message': 'Корзина очищена'},
            status=status.HTTP_200_OK
        )