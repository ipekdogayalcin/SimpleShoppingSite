# Generated by Django 4.2.1 on 2024-04-06 13:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysss', '0014_purchase_card_credentials_purchase_cvc_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='card_credentials',
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='cvc',
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='expiry_month',
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='expiry_year',
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='shipping_address',
        ),
    ]
