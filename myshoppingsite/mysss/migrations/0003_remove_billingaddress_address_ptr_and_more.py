# Generated by Django 4.2.1 on 2024-03-01 14:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mysss', '0002_product_description_product_in_stock_product_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billingaddress',
            name='address_ptr',
        ),
        migrations.RemoveField(
            model_name='billingaddress',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='order',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='order',
            name='shippingaddress',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='order',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='product',
        ),
        migrations.RemoveField(
            model_name='orderpayment',
            name='billingaddress',
        ),
        migrations.RemoveField(
            model_name='orderpayment',
            name='order',
        ),
        migrations.RemoveField(
            model_name='product',
            name='description',
        ),
        migrations.RemoveField(
            model_name='product',
            name='in_stock',
        ),
        migrations.AddField(
            model_name='customer',
            name='user',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='product',
            name='color',
            field=models.CharField(choices=[('Red', 'Red'), ('Blue', 'Blue'), ('Green', 'Green'), ('Pink', 'Pink'), ('Purple', 'Purple'), ('Black', 'Black'), ('Orange', 'Orange'), ('Yellow', 'Yellow'), ('Beige', 'Beige'), ('Multicolored', 'Multicolored')], default='', max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='image_url',
            field=models.URLField(default=None),
        ),
        migrations.AddField(
            model_name='product',
            name='item_type',
            field=models.CharField(choices=[('Clothing', 'Clothing'), ('Electronics', 'Electronics'), ('Books', 'Books')], default=None, max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='material',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.DeleteModel(
            name='Address',
        ),
        migrations.DeleteModel(
            name='BillingAddress',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
        migrations.DeleteModel(
            name='OrderPayment',
        ),
    ]
