# Generated by Django 4.1.3 on 2023-12-01 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_rename_sited_services_services_sitedservices'),
    ]

    operations = [
        migrations.AlterField(
            model_name='services',
            name='servicedetail_desc',
            field=models.TextField(),
        ),
    ]
