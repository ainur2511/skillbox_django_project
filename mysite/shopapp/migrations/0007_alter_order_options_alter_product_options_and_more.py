# Generated by Django 5.0.1 on 2024-02-14 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0006_order_products'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name_plural': 'Orders'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['name', 'price']},
        ),
        migrations.AlterField(
            model_name='product',
            name='discount',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
