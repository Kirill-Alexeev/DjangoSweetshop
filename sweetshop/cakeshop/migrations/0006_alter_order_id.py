# Generated by Django 5.0.6 on 2024-12-25 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cakeshop', '0005_alter_ordercake_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
