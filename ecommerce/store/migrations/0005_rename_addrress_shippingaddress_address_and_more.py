# Generated by Django 5.0.1 on 2024-01-05 13:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_product_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='addrress',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='state',
            new_name='county',
        ),
    ]