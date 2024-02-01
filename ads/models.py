from django.db import models


# Create your models here.


class Location(models.Model):
    name = models.CharField(max_length=50)
    lat = models.DecimalField(max_digits=8, decimal_places=6)
    lng = models.DecimalField(max_digits=8, decimal_places=6)

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"
        ordering = ["name"]

    def __str__(self):
        return self.name


class User(models.Model):
    class Role(models.TextChoices):
        ADMIN = "admin", "Администратор"
        MEMBER = "member", "Пользователь"
        MODERATOR = "moderator", "Модератор"

    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    username = models.CharField(unique=True, max_length=20, null=True, blank=True)
    password = models.CharField(max_length=40)
    role = models.CharField(max_length=9, choices=Role.choices, default=Role.MEMBER)
    age = models.PositiveSmallIntegerField()
    locations = models.ManyToManyField(Location)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["username"]

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Ads(models.Model):
    name = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField()
    description = models.TextField(null=True)
    is_published = models.BooleanField()
    images = models.ImageField(upload_to="ads/", null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    def __str__(self):
        return self.name
