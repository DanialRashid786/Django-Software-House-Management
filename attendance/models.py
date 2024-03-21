from datetime import datetime, date
import os
from django.db import models
from tinymce.models import HTMLField
from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


import os
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.db.models.signals import pre_save

from SHMS import settings
from customer.models import *

# Create your models here.

class Attendance(models.Model):
    projectmanager = models.ForeignKey(projectmanagers, on_delete=models.CASCADE,related_name='attendancelist')
    date = models.DateField(default=date.today)
    status = models.CharField(max_length=10, choices=(
        ('present', 'Present'),
        ('absent', 'Absent'),
    ))
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    area=models.CharField(max_length=20,blank=True, null=True)

    def __str__(self):
        return f"Attendance for {self.projectmanager.user.username} on {self.date}"