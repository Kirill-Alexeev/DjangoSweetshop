# Generated by Django 5.0.6 on 2024-12-20 20:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.IntegerField(help_text='Уникальный ID для ингредиента', primary_key=True, serialize=False)),
                ('title', models.CharField(help_text='Название ингредиента', max_length=100, verbose_name='Название')),
                ('units', models.CharField(help_text='Наименование единиц измерения', max_length=10, verbose_name='Единицы измерения')),
                ('count', models.IntegerField(help_text='Количество ингредиента', verbose_name='Количество')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateField(auto_now=True, verbose_name='Дата обновления')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Cake',
            fields=[
                ('id', models.IntegerField(help_text='Уникальный ID для торта', primary_key=True, serialize=False)),
                ('title', models.CharField(help_text='Название торта', max_length=100, verbose_name='Название')),
                ('weight', models.IntegerField(help_text='Вес торта в граммах', verbose_name='Вес')),
                ('description', models.TextField(help_text='Описание торта', max_length=1000, verbose_name='Описание')),
                ('image', models.ImageField(help_text='Изображение торта', upload_to='cakes/', verbose_name='Изображение')),
                ('price', models.DecimalField(decimal_places=2, help_text='Цена торта в руб.', max_digits=10, verbose_name='Цена')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateField(auto_now=True, verbose_name='Дата обновления')),
                ('ingredients', models.ManyToManyField(help_text='Ингредиенты используемые для приготовления', to='cakeshop.ingredient', verbose_name='Ингредиенты')),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.IntegerField(help_text='Уникальный ID для заказа', primary_key=True, serialize=False)),
                ('execution_date', models.DateField(help_text='Дата доставки заказа клиенту', verbose_name='Дата доставки')),
                ('status', models.CharField(choices=[('О', 'Ожидается'), ('З', 'Завершён')], help_text='Статус заказа', max_length=1, verbose_name='Статус')),
                ('cost', models.DecimalField(decimal_places=2, help_text='Общая стоимость заказа', max_digits=10, verbose_name='Стоимость')),
                ('delivery_address', models.CharField(help_text='Адрес, по которому доставляется заказ', max_length=255, verbose_name='Адрес доставки')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateField(auto_now=True, verbose_name='Дата обновления')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='OrderCake',
            fields=[
                ('id', models.IntegerField(help_text='Уникальный ID', primary_key=True, serialize=False)),
                ('cake', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cakeshop.cake', verbose_name='Торт')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cakeshop.order', verbose_name='Заказ')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='cakes',
            field=models.ManyToManyField(help_text='Торты добавленные в заказ', through='cakeshop.OrderCake', to='cakeshop.cake', verbose_name='Торты'),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.IntegerField(help_text='Уникальный ID для отзыва', primary_key=True, serialize=False)),
                ('review', models.TextField(help_text='Текст отзыва', max_length=1000, verbose_name='Отзыв')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('cake', models.ForeignKey(help_text='Торт, на который оставили отзыв', on_delete=django.db.models.deletion.CASCADE, to='cakeshop.cake', verbose_name='Торт')),
                ('user', models.ForeignKey(help_text='Пользователь, оставивший отзыв', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'ordering': ['cake'],
            },
        ),
    ]
