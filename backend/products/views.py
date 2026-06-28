from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from .permissions import IsAuthorOrAdminOrReadOnly
from .pagination import ProductPagination


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = None


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_published=True)
    serializer_class = ProductSerializer
    permission_classes = [IsAuthorOrAdminOrReadOnly]
    pagination_class = ProductPagination

    def get_queryset(self):
        # Базовый queryset
        if self.action == 'list':
            queryset = Product.objects.filter(is_published=True)
        else:
            if self.request.user and self.request.user.is_staff:
                queryset = Product.objects.all()
            else:
                queryset = Product.objects.filter(is_published=True)

        # Применяем фильтры только для list и all
        if self.action in ['list', 'all']:
            search = self.request.query_params.get('search', '')
            category = self.request.query_params.get('category', '')
            min_price = self.request.query_params.get('min_price', '')
            max_price = self.request.query_params.get('max_price', '')
            sort = self.request.query_params.get('sort', '')

            if search:
                queryset = queryset.filter(
                    Q(title__icontains=search) |
                    Q(description__icontains=search)
                )

            if category:
                queryset = queryset.filter(category_id=category)

            if min_price:
                try:
                    queryset = queryset.filter(price__gte=float(min_price))
                except (ValueError, TypeError):
                    pass

            if max_price:
                try:
                    queryset = queryset.filter(price__lte=float(max_price))
                except (ValueError, TypeError):
                    pass

            if sort == 'price_asc':
                queryset = queryset.order_by('price')
            elif sort == 'price_desc':
                queryset = queryset.order_by('-price')
            elif sort == 'newest':
                queryset = queryset.order_by('-created_at')
            elif sort == 'oldest':
                queryset = queryset.order_by('created_at')
            elif sort == 'popular':
                queryset = queryset.order_by('-purchases_count')

        return queryset

    def list (self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """Получение товара с увеличением счётчика просмотров"""
        instance = self.get_object()
        instance.views += 1
        instance.save(update_fields=['views'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAdminUser])
    def all(self, request):
        """Эндпоинт для администратора с пагинацией"""
        queryset = Product.objects.all()

        search = request.query_params.get('search', '')
        category = request.query_params.get('category', '')
        min_price = request.query_params.get('min_price', '')
        max_price = request.query_params.get('max_price', '')
        sort = request.query_params.get('sort', '')

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )

        if category:
            queryset = queryset.filter(category_id=category)

        if min_price:
            try:
                queryset = queryset.filter(price__gte=float(min_price))
            except (ValueError, TypeError):
                pass

        if max_price:
            try:
                queryset = queryset.filter(price__lte=float(max_price))
            except (ValueError, TypeError):
                pass

        if sort == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort == 'price_desc':
            queryset = queryset.order_by('-price')
        elif sort == 'newest':
            queryset = queryset.order_by('-created_at')
        elif sort == 'oldest':
            queryset = queryset.order_by('created_at')
        elif sort == 'popular':
            queryset = queryset.order_by('-purchases_count')

        # Применяем пагинацию
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        print("=== ПОЛУЧЕННЫЕ ДАННЫЕ ===")
        print("FILES:", request.FILES)
        print("DATA:", request.data)
        print("POST:", request.POST)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("ОШИБКИ ВАЛИДАЦИИ:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAdminUser])
    def all(self, request):
        queryset = Product.objects.all()

        search = request.query_params.get('search', '')
        category = request.query_params.get('category', '')
        min_price = request.query_params.get('min_price', '')
        max_price = request.query_params.get('max_price', '')
        sort = request.query_params.get('sort', '')

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )

        if category:
            queryset = queryset.filter(category_id=category)

        if min_price:
            try:
                queryset = queryset.filter(price__gte=float(min_price))
            except (ValueError, TypeError):
                pass

        if max_price:
            try:
                queryset = queryset.filter(price__lte=float(max_price))
            except (ValueError, TypeError):
                pass

        if sort == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort == 'price_desc':
            queryset = queryset.order_by('-price')
        elif sort == 'newest':
            queryset = queryset.order_by('-created_at')
        elif sort == 'oldest':
            queryset = queryset.order_by('created_at')
        elif sort == 'popular':
            queryset = queryset.order_by('-purchases_count')

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        print("=== ОБНОВЛЕНИЕ ===")
        print("FILES:", request.FILES)
        print("DATA:", request.data)

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            print("ОШИБКИ ВАЛИДАЦИИ:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # Увеличиваем счётчик просмотров
        instance.views += 1
        instance.save(update_fields=['views'])

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def view(self, request, pk=None):
        """Увеличение счётчика просмотров"""
        product = self.get_object()
        product.views += 1
        product.save(update_fields=['views'])
        return Response({'views': product.views})