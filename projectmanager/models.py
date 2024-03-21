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


def delete_image(sender, instance, image_field, **kwargs):
    # Remove file from the storage
    image = instance.__getattribute__(image_field)
    if image and os.path.isfile(image.path):
        os.remove(image.path)

def delete_previous_image(sender, instance, old_image_field, **kwargs):
    if not instance.pk:
        return False

    try:
        old_image = sender.objects.get(pk=instance.pk).__getattribute__(old_image_field)
    except sender.DoesNotExist:
        old_image = None

    new_image = instance.__getattribute__(old_image_field)
    if old_image and old_image != new_image and os.path.isfile(old_image.path):
        os.remove(old_image.path)

    return True

# Create your models here.
class Team(models.Model):
    team_type_choices = [
        ('Developer', 'Developer'),
        ('Designer', 'Designer'),
        ('Business Analyst', 'Business Analyst'),
        ('QA Engineer', 'QA Engineer'),
        ('DEVOPS', 'DEVOPS'),
    ]
    user=models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    project_manager = models.ForeignKey(projectmanagers, on_delete=models.CASCADE)
    about=HTMLField(blank=True ,null=True)
    team_type=models.CharField(max_length=200,null=True,choices=team_type_choices,default='Developer')
    profileimage = models.ImageField(upload_to='team/',max_length=200,blank=True ,null=True)
    company=models.CharField(max_length=100,blank=True ,null=True)
    country=models.CharField(max_length=50,blank=True ,null=True)
    address=models.CharField(max_length=100,blank=True ,null=True)
    phone=models.CharField(max_length=12,blank=True ,null=True)
    TwitterProfile = models.URLField(max_length = 200,default="https://web.facebook.com/?_rdc=1&_rdr")
    FacebookProfile = models.URLField(max_length = 200,default="https://web.facebook.com/?_rdc=1&_rdr")
    InstagramProfile = models.URLField(max_length = 200,default="https://web.facebook.com/?_rdc=1&_rdr")
    LinkedinProfile = models.URLField(max_length = 200,default="https://web.facebook.com/?_rdc=1&_rdr")
    date_created=models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.username


@receiver(pre_delete, sender=Team)
def delete_customer_image(sender, instance, **kwargs):
    delete_image(sender, instance, 'profileimage', **kwargs)

@receiver(pre_save, sender=Team)
def delete_previous_customer_image(sender, instance, **kwargs):
    return delete_previous_image(sender, instance, 'profileimage', **kwargs)




class ProjectAssignment(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE,related_name='assigned_projects_team')
    project = models.ForeignKey(requestform, on_delete=models.CASCADE)
    date_created=models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)
    completion_status = models.BooleanField(default=False)  # New field for project completion status

    def __str__(self):
        return self.team.user.username
    

    def __str__(self):
        return f"Project Assign to {self.team.user.username} on {self.date_created}"
    
    def all_tasks_completed(self):
        return all(task.status == 'completed' for task in self.project.tasks.all())


    


