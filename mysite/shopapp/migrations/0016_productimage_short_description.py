# Generated by Django 5.0.2 on 2024-02-22 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0015_productimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimage',
            name='short_description',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
