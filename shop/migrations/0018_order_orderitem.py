# Generated by Django 5.0.6 on 2024-08-16 17:45

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0017_remove_orderitem_order_remove_orderitem_product_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('total', models.DecimalField(decimal_places=2, max_digits=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('notes', models.TextField()),
                ('payment_method', models.CharField(max_length=255)),
                ('shipping_address', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='shop.shippingaddress')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=10)),
                ('color', models.CharField(max_length=10)),
                ('quantity', models.IntegerField(default=1)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='items', to='shop.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='shop.product')),
            ],
        ),
    ]
