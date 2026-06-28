from django.db import models
from django.conf import settings
from products.models import Product


class Order(models.Model):
    """Заказ пользователя"""
    STATUS_CHOICES = (
        ('pending', 'В обработке'),
        ('confirmed', 'Подтверждён'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменён'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Контактная информация
    full_name = models.CharField(max_length=200, verbose_name='ФИО')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')
    address = models.TextField(verbose_name='Адрес доставки')
    comment = models.TextField(blank=True, verbose_name='Комментарий к заказу')

    # Итоговые суммы
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Заказ #{self.id} - {self.user.username}"

    def calculate_total(self):
        """Пересчёт общей суммы заказа"""
        total = sum(item.total_price for item in self.items.all())
        self.total_price = total + self.delivery_price
        self.save()
        return self.total_price


class OrderItem(models.Model):
    """Товар в заказе"""
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='order_items'
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена на момент заказа

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"

    @property
    def total_price(self):
        return self.price * self.quantity
