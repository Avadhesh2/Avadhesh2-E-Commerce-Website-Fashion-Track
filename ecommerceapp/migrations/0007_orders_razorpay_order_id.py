# Generated by Django 4.2 on 2024-06-16 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceapp', '0006_remove_orders_razorpay_order_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='razorpay_order_id',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
