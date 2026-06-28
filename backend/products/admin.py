from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'category', 'is_published', 'author', 'created_at')
    list_filter = ('is_published', 'category', 'author')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at', 'views')
