from rest_framework import serializers
from .models import Cart, CartItem

class CartItemSerializer(serializers.ModelSerializer):
    # Все поля продукта через SerializerMethodField
    product_id = serializers.SerializerMethodField()
    product_title = serializers.SerializerMethodField()
    product_price = serializers.SerializerMethodField()
    product_photo = serializers.SerializerMethodField()
    product_category = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    def get_product_id(self, obj):
        return obj.product.id if obj.product else None

    def get_product_title(self, obj):
        return obj.product.title if obj.product else None

    def get_product_price(self, obj):
        return obj.product.price if obj.product else None

    def get_product_photo(self, obj):
        if obj.product and obj.product.photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.product.photo.url)
            return obj.product.photo.url
        return None

    def get_product_category(self, obj):
        return obj.product.category.title if obj.product and obj.product.category else None

    def get_total_price(self, obj):
        return obj.total_price

    class Meta:
        model = CartItem
        fields = (
            'id',
            'product',
            'product_id',
            'product_title',
            'product_price',
            'product_photo',
            'product_category',
            'quantity',
            'total_price'
        )
        extra_kwargs = {
            'product': {'write_only': True}
        }

class CartSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    total_items = serializers.SerializerMethodField()

    def get_items(self, obj):
        request = self.context.get('request')
        return CartItemSerializer(obj.items.all(), many=True, context={'request': request}).data

    def get_total_price(self, obj):
        return obj.total_price

    def get_total_items(self, obj):
        return obj.total_items

    class Meta:
        model = Cart
        fields = ('id', 'user', 'items', 'total_price', 'total_items', 'created_at', 'updated_at')
        read_only_fields = ('user', 'created_at', 'updated_at')