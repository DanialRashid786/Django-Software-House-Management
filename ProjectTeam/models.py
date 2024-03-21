from django.db import models

# Create your models here.
from django.db import models
from datetime import datetime, date
import os
from tinymce.models import HTMLField
from autoslug import AutoSlugField
from django.contrib.auth.models import User


from django.contrib.auth.models import Group

from customer.models import *

import os
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.db.models.signals import pre_save

from SHMS import settings
from projectmanager.models import *
from projectmanager.widgets import MultiTagWidget
from django.core.validators import FileExtensionValidator

class Task(models.Model):
    project = models.ForeignKey(requestform, on_delete=models.CASCADE,related_name='tasks')
    name = models.CharField(max_length=100)
    description = models.TextField()
    TaskRequirementFile=models.FileField(upload_to='taskrequirement/',max_length=200,blank=True ,null=True,default=None)
    deadline = models.DateField()
    assigned_to = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)  # Individual team member assignment
    tags = models.CharField(max_length=100, blank=True, help_text='Enter tags separated by commas')

    category = models.CharField(max_length=50, blank=True, help_text='Write Category of task eg Backend,Frontend')
    status = models.CharField(max_length=20, choices=[("todo", "To Do"), ("in_progress", "In Progress"), ("completed", "Completed"),("to_review","To Review"),("needs_revision", "Needs Revision"),], default="To Do")


    date_created=models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # If you want to save tags as a list, you can split the input value here
        # For example: self.tags = self.tags.split(',')
        super().save(*args, **kwargs)

    @property
    def tag_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    def get_file_size(self):
        return f'{os.path.getsize(self.TaskRequirementFile.path) / (1024 * 1024):.2f} MB'



class Document(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to='taskdoc/',validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx'])])
    remarks = models.TextField(blank=True, null=True)

    date_created=models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.task.name