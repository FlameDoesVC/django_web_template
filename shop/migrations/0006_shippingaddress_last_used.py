# Generated by Django 5.0.6 on 2024-08-16 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_alter_product_image_order_orderitem_shippingaddress_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='last_used',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
