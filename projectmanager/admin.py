
from django.contrib import admin
from django.contrib.admin.sites import site
from .models import *
# Register your models here.
class addteam(admin.ModelAdmin):
    list_display=('id','user','user_id','project_manager','team_type','profileimage','company','country','address','phone','date_created','updated_at')

admin.site.register(Team, addteam)


admin.site.register(ProjectAssignment)
