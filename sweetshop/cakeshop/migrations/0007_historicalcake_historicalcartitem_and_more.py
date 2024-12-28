# Generated by Django 5.0.6 on 2024-12-28 11:13

import django.db.models.deletion
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cakeshop', '0006_alter_order_id'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalCake',
            fields=[
                ('id', models.IntegerField(auto_created=True, db_index=True, help_text='Уникальный ID для торта')),
                ('title', models.CharField(help_text='Название торта', max_length=100, verbose_name='Название')),
                ('weight', models.IntegerField(help_text='Вес торта в граммах', verbose_name='Вес')),
                ('description', models.TextField(help_text='Описание торта', max_length=1000, verbose_name='Описание')),
                ('image', models.CharField(help_text='Изображение торта', max_length=100, verbose_name='Изображение')),
                ('price', models.DecimalField(decimal_places=2, help_text='Цена торта в руб.', max_digits=10, verbose_name='Цена')),
                ('created_at', models.DateField(blank=True, editable=False, verbose_name='Дата создания')),
                ('updated_at', models.DateField(blank=True, editable=False, verbose_name='Дата обновления')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical cake',
                'verbose_name_plural': 'historical cakes',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalCartItem',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Количество')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('cake', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='cakeshop.cake', verbose_name='Торт')),
                ('cart', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='cakeshop.cart', verbose_name='Корзина')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical cart item',
                'verbose_name_plural': 'historical cart items',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalIngredient',
            fields=[
                ('id', models.IntegerField(auto_created=True, db_index=True, help_text='Уникальный ID для ингредиента')),
                ('title', models.CharField(help_text='Название ингредиента', max_length=100, verbose_name='Название')),
                ('units', models.CharField(help_text='Наименование единиц измерения', max_length=10, verbose_name='Единицы измерения')),
                ('count', models.IntegerField(help_text='Количество ингредиента', verbose_name='Количество')),
                ('created_at', models.DateField(blank=True, editable=False, verbose_name='Дата создания')),
                ('updated_at', models.DateField(blank=True, editable=False, verbose_name='Дата обновления')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical ingredient',
                'verbose_name_plural': 'historical ingredients',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalOrder',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('execution_date', models.DateField(help_text='Дата доставки заказа клиенту', verbose_name='Дата доставки')),
                ('status', models.CharField(choices=[('О', 'Ожидается'), ('З', 'Завершён')], help_text='Статус заказа', max_length=1, verbose_name='Статус')),
                ('cost', models.DecimalField(decimal_places=2, help_text='Общая стоимость заказа', max_digits=10, verbose_name='Стоимость')),
                ('delivery_address', models.CharField(help_text='Адрес, по которому доставляется заказ', max_length=255, verbose_name='Адрес доставки')),
                ('created_at', models.DateField(blank=True, editable=False, verbose_name='Дата создания')),
                ('updated_at', models.DateField(blank=True, editable=False, verbose_name='Дата обновления')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'historical order',
                'verbose_name_plural': 'historical orders',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalReview',
            fields=[
                ('id', models.IntegerField(auto_created=True, db_index=True, help_text='Уникальный ID для отзыва')),
                ('review', models.TextField(help_text='Текст отзыва', max_length=1000, verbose_name='Отзыв')),
                ('created_at', models.DateField(blank=True, editable=False, verbose_name='Дата создания')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('cake', models.ForeignKey(blank=True, db_constraint=False, help_text='Торт, на который оставили отзыв', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='cakeshop.cake', verbose_name='Торт')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, db_constraint=False, help_text='Пользователь, оставивший отзыв', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'historical review',
                'verbose_name_plural': 'historical reviews',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
