# Generated by Django 5.0.6 on 2024-07-25 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='quabtity',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='digital',
            field=models.BooleanField(default=True, null=True),
        ),
    ]
