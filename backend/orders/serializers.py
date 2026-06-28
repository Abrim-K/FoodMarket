from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title', read_only=True)
    product_photo = serializers.SerializerMethodField()
    product_id = serializers.IntegerField(source='product.id', read_only=True)

    def get_product_photo(self, obj):
        if obj.product and obj.product.photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.product.photo.url)
            return obj.product.photo.url
        return None

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'product_id', 'product_title', 'product_photo', 'quantity', 'price', 'total_price')
        read_only_fields = ('total_price',)


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Order
        fields = (
            'id', 'user', 'created_at', 'updated_at', 'status', 'status_display',
            'full_name', 'phone', 'email', 'address', 'comment',
            'total_price', 'delivery_price', 'items'
        )
        read_only_fields = ('user', 'created_at', 'updated_at', 'total_price')


class CreateOrderSerializer(serializers.Serializer):
    """Сериализатор для создания заказа из корзины"""
    full_name = serializers.CharField(max_length=200)
    phone = serializers.CharField(max_length=20)
    email = serializers.EmailField()
    address = serializers.CharField()
    comment = serializers.CharField(required=False, allow_blank=True)