from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.username

# Профиль можно объединить с User, но по заданию нужна отдельная модель Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # дополнительные поля, если нужно, пока оставим пустым
    # но можно дублировать bio/avatar/phone, но у нас уже есть в User
    # поэтому оставим как заглушку
    def __str__(self):
        return f"Profile of {self.user.username}"
