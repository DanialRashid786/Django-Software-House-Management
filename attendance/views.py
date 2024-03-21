import json
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
import requests
from customer.models import  *
from .models import *

from django.contrib.auth.models import User
from customadmin.decorators import *

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .forms import *
import datetime
import socket

# Create your views here.



@login_required(login_url='loginview')
@allowed_users(allowed_roles=['Project Manager'])
def mark_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            user = request.user
            if hasattr(user, 'projectmanagers'):
                project_manager = user.projectmanagers
                
                # Retrieve the user's IP address
                ip_address = get_client_ip(request)
                
                user_city = get_user_city(ip_address)
                # Get the current date
                current_date = date.today()
                
                # Check if attendance already marked for the current date and project manager
                if Attendance.objects.filter(projectmanager=project_manager, date=current_date).exists():
                    return redirect('errorpage')
                
                attendance = Attendance(
                    projectmanager=project_manager,
                    status=form.cleaned_data['status'],
                    ip_address=ip_address,
                    date=current_date,
                    area=user_city
                )
                attendance.save()  # Save the attendance record to the database
                return redirect('successpage')  # Redirect to a success page or another appropriate view
            else:
                # Handle the case where the user is not a project manager
                return HttpResponse('not_project_manager')
    else:
        form = AttendanceForm()
    
    return render(request, 'mark_attendance.html', {'form': form})


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR')
    return ip_address

def get_user_city(ip_address):
    ip_address='139.135.53.31'
    # ip_address='182.191.145.49'
    
    # Make a request to an IP geolocation service
    url = f'http://ip-api.com/json/{ip_address}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'success':
            return data['city']
    
    return None


@login_required(login_url='loginview')
@allowed_users(allowed_roles=['Project Manager'])
def successpage(request):
    return render(request , 'successpage.html')

@login_required(login_url='loginview')
@allowed_users(allowed_roles=['Project Manager'])
def errorpage(request):
    return render(request , 'errorpage.html')


