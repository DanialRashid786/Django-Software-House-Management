# Generated by Django 4.1.3 on 2023-12-10 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0008_alter_customer_address_alter_customer_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestform',
            name='Project_Budget',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
