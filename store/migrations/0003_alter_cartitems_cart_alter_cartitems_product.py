# Generated by Django 4.0.6 on 2022-08-30 09:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_cart_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitems',
            name='cart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.cart'),
        ),
        migrations.AlterField(
            model_name='cartitems',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.product'),
        ),
    ]
