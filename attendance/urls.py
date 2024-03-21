from django.urls import path,include
from .import views
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from .models import *
from customer.models import *


urlpatterns = [

   
   path('mark-attendance/', mark_attendance, name='mark_attendance'),

   path('attendance-marked', successpage, name='successpage'),
   path('attendance_already_marked', errorpage, name='errorpage'),


]
