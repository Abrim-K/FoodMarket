from django.db import models
from django.conf import settings

class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True, unique=True)

    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.FileField(upload_to='products/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)
    purchases_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title