

from django.contrib import admin
from django.contrib.admin.sites import site
from .models import *
# Register your models here.

admin.site.register(Task)

admin.site.register(Document)


