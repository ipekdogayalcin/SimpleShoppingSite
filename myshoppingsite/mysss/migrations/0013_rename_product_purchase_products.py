# Generated by Django 4.2.1 on 2024-04-04 22:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysss', '0012_remove_purchase_shipping_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchase',
            old_name='product',
            new_name='products',
        ),
    ]