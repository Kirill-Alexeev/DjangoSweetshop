from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Ingredient(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True, help_text="Уникальный ID для ингредиента")
    title = models.CharField(verbose_name='Название', max_length=100, help_text="Название ингредиента")
    units = models.CharField(verbose_name='Единицы измерения', max_length=10, help_text="Наименование единиц измерения")
    count = models.IntegerField(verbose_name='Количество', help_text="Количество ингредиента")
    created_at = models.DateField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateField(verbose_name='Дата обновления', auto_now=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("ingredient-detail", args=[str(self.id)])


class Cake(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True, help_text="Уникальный ID для торта")
    title = models.CharField(verbose_name='Название', max_length=100, help_text="Название торта")
    weight = models.IntegerField(verbose_name='Вес', help_text="Вес торта в граммах")
    description = models.TextField(verbose_name='Описание', max_length=1000, help_text="Описание торта")
    image = models.CharField(verbose_name='Изображение', max_length=100, help_text="Изображение торта")
    price = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2, help_text="Цена торта в руб.")
    ingredients = models.ManyToManyField(Ingredient, verbose_name='Ингредиенты', help_text="Ингредиенты используемые для приготовления")
    created_at = models.DateField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateField(verbose_name='Дата обновления', auto_now=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("cake-detail", args=[str(self.id)])


class Review(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True, help_text="Уникальный ID для отзыва")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', help_text="Пользователь, оставивший отзыв")
    cake = models.ForeignKey(Cake, on_delete=models.CASCADE, verbose_name='Торт', help_text="Торт, на который оставили отзыв")
    review = models.TextField(verbose_name='Отзыв', max_length=1000, help_text="Текст отзыва")
    created_at = models.DateField(verbose_name='Дата создания', auto_now_add=True)

    class Meta:
        ordering = ['cake']

    def __str__(self):
        return f"Отзыв от {self.user.username} на {self.cake.title}"

    def get_absolute_url(self):
        return reverse("cake-detail", args=[str(self.cake.id)])


class Order(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True, help_text="Уникальный ID для заказа")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', help_text="")
    execution_date = models.DateField(verbose_name='Дата доставки', help_text="Дата доставки заказа клиенту")
    status = models.CharField(verbose_name='Статус', max_length=1, choices=[('О', 'Ожидается'), ('З', 'Завершён')], help_text="Статус заказа")
    cost = models.DecimalField(verbose_name='Стоимость', max_digits=10, decimal_places=2, help_text="Общая стоимость заказа")
    cakes = models.ManyToManyField(Cake, verbose_name='Торты', through="OrderCake", help_text="Торты добавленные в заказ")
    delivery_address = models.CharField(verbose_name='Адрес доставки', max_length=255, help_text="Адрес, по которому доставляется заказ")
    created_at = models.DateField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateField(verbose_name='Дата обновления', auto_now=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"Заказ #{self.id} для {self.user.username}"


class OrderCake(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True, help_text="Уникальный ID")
    order = models.ForeignKey(Order, verbose_name='Заказ', on_delete=models.CASCADE)
    cake = models.ForeignKey(Cake, verbose_name='Торт', on_delete=models.CASCADE)
