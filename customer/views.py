import json
from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from customer.models import  *

from django.contrib.auth.models import User
from customadmin.decorators import allowed_users, admin_only, unauthenticated_user

from django.contrib.auth import authenticate, login, logout


from .forms import *

from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm as DjangoPasswordChangeForm



def handling_404(request,exception):
    return render(request,'404.html',{})

def custom_500(request):
    return render(request, '500.html', status=500)


def customerlogout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("homepage")




# Create your views here.

def home(request):
    newData=services.objects.filter(display_on_screen=True)[0:6]
    myportfolio=portfolio.objects.all().order_by('id')
    about_entry = AboutUs.objects.filter(display_on_screen=True).first()
    dataStrategies = DataUtilizationStrategies.objects.filter(display_on_screen=True).order_by('created_at')[0:9]

    faqs = FAQ.objects.filter(display_on_screen=True).order_by('created_at')[0:6]
    if request.method == 'POST':
        form = RequestSessionform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Session Request Submit Successfully') 
            return redirect('/')  # Redirect to a success page
    else:
        form = RequestSessionform()
    data={
        'newData':newData,
        'myportfolio':myportfolio,
        'form':form,
        'about_entry':about_entry,
        'dataStrategies':dataStrategies,
        'faqs':faqs,
    }
    return render(request,'index.html',data)  
    

def servicedetail(request,slug):
    newData=services.objects.filter(display_on_screen=True)
    service=services.objects.get(title_slug=slug,display_on_screen=True)
    datadec = service.SitedServices if service.SitedServices else []
    names = datadec.split(',')
    data={
        'service':service,
        'datadec':names,
        'newData':newData,
    } 
    return render(request,'servicedetail.html', data) 




def servicepage(request):
    newData=services.objects.filter(display_on_screen=True)
    data={
        'newData':newData
    }
    return render(request,'services.html',data) 

 


def contactfrom(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        subject=request.POST.get('subject')
        message=request.POST.get('message')

        en=contactus(name=name,email=email,subject=subject,message=message)
        en.save()
    messages.success(request,'Message Send Successfully') 
    return HttpResponseRedirect("/") 


@login_required(login_url="loginview")
@allowed_users(allowed_roles=['Customer'])
def perposalrequest(request, pid, sname):
    newData=services.objects.filter(display_on_screen=True)
    service = services.objects.get(id=pid, service_title=sname,display_on_screen=True)
    customer = request.user.customer

    if request.method == 'POST':
        formset = ProjectProposalFormSet(request.POST, request.FILES, instance=customer)
        if formset.is_valid() and formset.has_changed():
            # # Check if the user has an accepted or completed project
            # existing_requests = formset.queryset.filter(
            #     projectstatus__in=['In Progress',]
            # )

            # if existing_requests.exists():
            #     return JsonResponse({'status': False, 'error': 'You cannot submit a new request until your existing project is completed'})

            instances = formset.save(commit=False)
            for proposal_request in instances:
                proposal_request.servicetype = service
                proposal_request.save()

            # Assuming your form submission is successful
            return JsonResponse({'status': True, 'message': 'Form submitted successfully.'})
        else:
            # Form is not valid, collect form errors and return them
            form_errors = {}
            for form in formset:
                form_errors.update({f"{key}": error for key, error in form.errors.items()})
            
            return JsonResponse({'status': False, 'errors': form_errors})
    else:
        formset = ProjectProposalFormSet(instance=None)

    return render(request, 'requestproject.html', {'formset': formset, 'service': service,'newData':newData})




    



@login_required(login_url="loginview")
@allowed_users(allowed_roles=['Customer'])
def accountSettings(request):
    customer = request.user.customer
    user = request.user

    if request.method == 'POST':
        # Profile Update Form
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            new_email = form.cleaned_data['email']

            if new_email != user.email and User.objects.filter(email=new_email).exists():
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                customer.phone = form.cleaned_data['phone']
                customer.address = form.cleaned_data['address']
                if 'profileimage' in request.FILES:
                    customer.profileimage = request.FILES['profileimage']
                customer.save()
                user.save()
                messages.error(request, 'Email already exists. Please choose a different one.')
                messages.success(request, 'Profile updated successfully')
                return redirect(reverse('accountcustomer'))
            else:
                # Handle the update for each field
                user.email = form.cleaned_data['email']
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                customer.phone = form.cleaned_data['phone']
                customer.address = form.cleaned_data['address']
                if 'profileimage' in request.FILES:
                    customer.profileimage = request.FILES['profileimage']
                customer.save()
                user.save()

                messages.success(request, 'Profile updated successfully')
                return redirect(reverse('accountcustomer'))
        else:
            # If the form is not valid, you might want to handle it accordingly
            messages.error(request, 'Invalid form data. Please correct the errors.')
        

        # Password Change Form
        passwordform = PasswordChangeForm(request.POST)
        if passwordform.is_valid():
            current_password = passwordform.cleaned_data['current_password']
            new_password = passwordform.cleaned_data['new_password']
            repeat_new_password = passwordform.cleaned_data['repeat_new_password']

            if not user.check_password(current_password):
                messages.error(request, 'Incorrect current password.')
            elif new_password != repeat_new_password:
                messages.error(request, 'New passwords do not match.')
            else:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, customer)
                messages.success(request, 'Password changed successfully')
                return redirect(reverse('loginview'))


    else:
        # Initial form rendering
        form = CustomerForm(instance=customer, initial={'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name})
        passwordform = PasswordChangeForm()

    context = {'form1': form, 'passwordform': passwordform}
    return render(request, 'customer_settings.html', context)


# @login_required(login_url="loginview")
# @allowed_users(allowed_roles=['Customer'])
# def change_password(request):
#     if request.method == 'POST':
#         passwordform = PasswordChangeForm(request.POST)
#         if passwordform.is_valid():
#             current_password = passwordform.cleaned_data['current_password']
#             new_password = passwordform.cleaned_data['new_password']
#             repeat_new_password = passwordform.cleaned_data['repeat_new_password']

#             # Check if the current password is correct
#             if not request.user.check_password(current_password):
#                 messages.error(request, 'Incorrect current password.')
#             elif new_password != repeat_new_password:
#                 messages.error(request, 'New passwords do not match.')
#             else:
#                 # Update the user's password
#                 request.user.set_password(new_password)
#                 request.user.save()

#                 # Update the session to reflect the password change
#                 update_session_auth_hash(request, request.user)

#                 messages.success(request, 'Password changed successfully.')
#                 return redirect('profile')  # Redirect to the user's profile page after password change
#     else:
#         passwordform = PasswordChangeForm()

#     return render(request, 'customer_settings.html', {'passwordform': passwordform})







def portfoliodetails(request,pid):
    details = portfolioDetails.objects.get(portfolio_id=pid)
    
    context = {
       'details':details
    }
    return render(request, 'portfolio-details.html', context)


from django.db.models import Prefetch

@login_required(login_url="loginview")
@allowed_users(allowed_roles=['Customer'])
def project_list(request):
    customer = request.user.customer
    projects = requestform.objects.filter(customer=customer).order_by('-id')

    projects = projects.prefetch_related(Prefetch('documents', queryset=ProjectCompletionDocument.objects.all(), to_attr='project_documents'))

    context = {
       'projects': projects,
       

    }
    return render(request, 'project_list.html',context)





# /////////////////Career///////////////////
def career_job(request):
    newData=services.objects.filter(display_on_screen=True)[0:6]
    careers = Career.objects.all().order_by('-id')
    new_data = services.objects.all()[0:6]
    data = {
        'careers': careers,
        'new_data': new_data,
        'newData':newData,
    }
    return render(request, 'career.html', data)  

def career_details(request, id):
    newData=services.objects.filter(display_on_screen=True)[0:6]
    career_detail = Career.objects.get(id=id)
    responsibilities_list = eval(career_detail.Responsibilities)
    requirements_list = eval(career_detail.Requirements)
    data = {
        'career_detail': career_detail,
        'responsibilities_list': responsibilities_list,
        'requirements_list': requirements_list,
        'newData':newData,
    }
    return render(request, 'careerdetails.html', data)   

def job_proposal_request(request, id):
    newData=services.objects.filter(display_on_screen=True)[0:6]
    career = get_object_or_404(Career, id=id)


    if request.method == 'POST':
        name = request.POST['Name']
        email = request.POST['Email']
        phone_number = request.POST['Phone_number']
        about = request.POST['About']
        cv = request.FILES['CV']

        # Custom validation: Check if the email is unique for the given JobTitle
        existing_applications = CareerForm.objects.filter(JobTitle=career, Email=email)
        if existing_applications.exists():
            messages.error(request, 'You have already applied with this email for this job.')
            return redirect('jobrequest',id=id)

        # You can add any other custom validation checks here if needed

        # Create and save the CareerForm instance
        career_form = CareerForm.objects.create(
            Name=name,
            Email=email,
            Phone_number=phone_number,
            About=about,
            CV=cv,
            JobTitle=career,
        )
        messages.success(request, 'Request Successfully submitted')
        return redirect('jobrequest', id=id)
    else:
        return render(request, 'jobrequest.html', {'career': career,'newData':newData,})
# /////////////////Career End///////////////////




def technologies(request):
    technology = Technologies.objects.filter(display_on_screen=True)
    newData=services.objects.filter(display_on_screen=True)[0:6]
    data={
        'technology':technology,
        'newData':newData
    }
    return render(request,'technology.html',data) 



def workingculture(request):
    ourculture = OurCulture.objects.filter(display_on_screen=True)
    newData=services.objects.filter(display_on_screen=True)[0:6]
    data={
        'newData':newData,
        'ourculture':ourculture
    }
    return render(request,'culture.html',data)


def ourmission(request):
    ourcore = OurCore.objects.filter(display_on_screen=True).first()
    newData=services.objects.filter(display_on_screen=True)[0:6]
    data={
        'newData':newData,
        'ourcore':ourcore
    }
    return render(request,'mission.html',data)


def whatwedo(request):
    whatwedo = Whatwedo.objects.filter(display_on_screen=True)
    whatsetsusapart = WhatSetsUsApart.objects.filter(display_on_screen=True)
    newData=services.objects.all()[0:6]
    if request.method == 'POST':
        form = RequestSessionform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Session Request Submit Successfully') 
            return redirect('/')  # Redirect to a success page
    else:
        form = RequestSessionform()
    data={
        'whatwedo':whatwedo,
        'whatsetsusapart':whatsetsusapart,
        'form':form,
        'newData':newData
    }
    return render(request,'whatwedo.html',data)


def aboutus(request):
    about_entry = AboutUs.objects.filter(display_on_screen=True).first()
    newData=services.objects.all()[0:6]
    data={
        'about_entry':about_entry,
        'newData':newData
    }
    return render(request,'aboutus.html', data) 


