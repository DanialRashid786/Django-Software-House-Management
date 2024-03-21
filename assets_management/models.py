from django.db import models
from datetime import datetime, date
from customer.models import projectmanagers


# Create your models here.
class Asset(models.Model):
    ASSET_TYPE_CHOICES = [
        ('Hardware', 'Hardware'),
        ('Software', 'Software'),
        ('Office Equipment', 'Office Equipment'),
        ('Other','Other'),
    ]
    asset_name = models.CharField(max_length=100)
    asset_type = models.CharField(
        max_length=20,
        choices=ASSET_TYPE_CHOICES,
        default='Hardware',
    )
    purchase_date = models.DateField()
    purchase_price = models.FloatField()
    serial_number = models.CharField(max_length=100,unique=True)
    notes = models.TextField(blank=True)
    date_created=models.DateTimeField(auto_now_add=True,null=True)
    
    def __str__(self):
        return self.asset_name




