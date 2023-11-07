from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Название категории")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Кактегорії"


class Post(models.Model):
    title = models.CharField(max_length=30, verbose_name="Заголовок", unique=True)
    content = models.TextField(verbose_name="Опис")
    published_date = models.DateTimeField(auto_created=True, verbose_name="Дата та час")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категорія")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    image = models.ImageField(default='default_image/900x300.png')
    price = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="цена")
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Пости"



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    group = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.user.username
