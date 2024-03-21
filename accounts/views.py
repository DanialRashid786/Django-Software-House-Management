import json
from django.shortcuts import render,redirect
from django.http import BadHeaderError, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse_lazy
from customer.models import  *
from .models import *

from django.contrib.auth.models import User
from customadmin.decorators import allowed_users, admin_only, unauthenticated_user

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

import uuid
from django.conf import settings
from django.core.mail import send_mail

def register_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            if User.objects.filter(username=username).exists():
                messages.success(request, 'Username is taken.')
                return redirect('/customerregister/')

            if User.objects.filter(email=email).exists():
                messages.success(request, 'Email is taken.')
                return redirect('/customerregister/')

            user_obj = User.objects.create(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()

            group = Group.objects.get(name='Customer')
            group.user_set.add(user_obj)

            auth_token = str(uuid.uuid4())
            profile_obj = Customer.objects.create(user=user_obj, auth_token=auth_token)
            profile_obj.save()

            # Attempt to send the email
            try:
                send_mail_after_registration(email, auth_token)
                return redirect('/token')
            except BadHeaderError:
                # Email sending failed due to a bad header
                # Delete the created user object
                user_obj.delete()
                messages.error(request, 'Failed to send verification email. Please try again later.')
                return redirect('/customerregister/')
            except Exception as e:
                # Handle other exceptions that might occur during email sending
                user_obj.delete()
                messages.error(request, 'An error occurred while sending the email. Please try again later.')
                return redirect('/customerregister/')

        except Exception as e:
            print(e)

    return render(request, 'customerregister.html')


def success(request):
    return render(request , 'success.html')


def token_send(request):
    return render(request , 'token_send.html')



def verify(request , auth_token):
    try:
        profile_obj = Customer.objects.filter(auth_token = auth_token).first()
    

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/loginpage/')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('/loginpage/')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/')

def error_page(request):
    return  render(request , 'error.html')



def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )





from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)

class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    success_url = reverse_lazy('accounts:password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'