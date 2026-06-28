from rest_framework import serializers
from .models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )
    author_name = serializers.SerializerMethodField()

    def get_author_name(self, obj):
        return obj.author.username if obj.author else None

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('author', 'created_at', 'updated_at', 'views', 'purchases_count')