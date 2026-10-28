from django.db import models

class Location(models.Model):
    address = models.CharField(max_length=200, verbose_name="Адрес")
    working_hours = models.CharField(max_length=100, default="08:00 - 23:00", verbose_name="Часы работы")
    def __str__(self): return self.address

class Operator(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='operators', verbose_name="Локация")
    name = models.CharField(max_length=100, verbose_name="Имя оператора")
    phone = models.CharField(max_length=20, verbose_name="Номер телефона")
    def __str__(self): return f"{self.name} ({self.location.address})"

class Product(models.Model):
    CATEGORY_CHOICES = [('coffee', 'Кофе'), ('drink', 'Напитки'), ('food', 'Еда')]
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Состав")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Цена")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='coffee', verbose_name="Категория")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Фото")
    is_seasonal = models.BooleanField(default=False, verbose_name="Сезонное")
    is_new = models.BooleanField(default=False, verbose_name="Новинка")
    class Meta: ordering = ['name']
    def __str__(self): return self.name

class Order(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя клиента")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    address = models.CharField(max_length=250, verbose_name="Адрес доставки")
    items_summary = models.TextField(blank=True, null=True, verbose_name="Состав заказа")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")
    is_processed = models.BooleanField(default=False, verbose_name="Обработан")
    def __str__(self): return f"Заказ {self.name} - {self.phone}"

class SupportMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя клиента", blank=True, default="Гость")
    message = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата")
    is_read = models.BooleanField(default=False, verbose_name="Прочитано")
    def __str__(self): return f"Сообщение от {self.name}"

class Review(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='reviews', verbose_name="Локация")
    name = models.CharField(max_length=100, verbose_name="Имя клиента")
    text = models.TextField(verbose_name="Текст отзыва")
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=5, verbose_name="Оценка")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата")
    def __str__(self): return f"Отзыв от {self.name} ({self.rating}★)"
