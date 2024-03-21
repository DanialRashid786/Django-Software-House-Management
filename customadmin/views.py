from audioop import reverse
import io
import os
from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect, get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from attendance.models import Attendance
from customer.models import *
from projectmanager.forms import  projectmanagerForm
from projectmanager.models import ProjectAssignment, Team
from .decorators import allowed_users, admin_only, unauthenticated_user
from django.contrib.auth.models import Group
from django.contrib.auth.forms import *
from .forms import * 
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.db.models.functions import TruncMonth

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

from django.shortcuts import render
import base64
import io
from django.db.models import Count


# /////////////////////////////////Dashboard/////////////////////////////////////////
@login_required(login_url="loginview")
@admin_only
def admindashboard(request):
    service = services.objects.all()
    servicecount = service.count()

    mydata = requestform.objects.filter(status='Pending')
    requestcount = mydata.count()

    tprojects = requestform.objects.filter(projectstatus__in=['Complete', 'Delivered'])
    projectcount = tprojects.count()

    dprojects = requestform.objects.filter(projectstatus__in=['Delivered'])
    dcount = dprojects.count()

    inprogress = requestform.objects.filter(projectstatus='In Progress', status='Accepted')
    projectinprogress = inprogress.count()

    clients=Customer.objects.filter(is_verified='True')
    totalclient=clients.count()

    managers = projectmanagers.objects.all()
    managerscount = managers.count()

    group = Group.objects.get(name='Customer')
    users = group.user_set.all()
    customercount = users.count()

    
     # Retrieve the data
    request_forms = requestform.objects.all()

    # Pie chart of request form status
    status_counts = request_forms.values('status').annotate(count=models.Count('status'))
    status_labels = [entry['status'] for entry in status_counts]
    status_counts = [entry['count'] for entry in status_counts]

    # Create the pie chart
    plt.pie(status_counts, labels=status_labels, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.title('Project Request Status')

    # Convert plot to image in memory
    image_stream = io.BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()

    # Encode the image stream as base64
    image_stream.seek(0)
    pie_image = base64.b64encode(image_stream.getvalue()).decode('utf-8')



    # Bar chart of service type
    service_types = requestform.objects.values('servicetype__service_title').annotate(count=models.Count('servicetype'))

    labels = [entry['servicetype__service_title'] for entry in service_types]
    counts = [entry['count'] for entry in service_types]

    # Define custom colors for the bars
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'yellow']

    plt.bar(labels, counts, color=colors)
    plt.xlabel('Service Type')
    plt.ylabel('Number of Services')
    plt.title('Service Type Distribution')

    if counts:  # Check if counts is not empty
        for i, count in enumerate(counts):
          plt.text(i, count, str(count), ha='center', va='bottom')

         # Set y-axis ticks to whole numbers
        plt.yticks(range(int(max(counts)) + 1))
    else:
        print("The counts list is empty.")

    # Save the chart to a file-like object
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Convert the chart image to a base64-encoded string
    chart_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    revenue_monthly = requestform.objects.filter(paymentstatus='Paid').annotate(revenue_month=TruncMonth('Project_Finnish_Date')).values('revenue_month').annotate(total_budget=Sum('Project_Budget'))

    paid_projects_budget = requestform.objects.filter(paymentstatus='Paid').aggregate(total_budget=Sum('Project_Budget'))
    total_budget_amount = paid_projects_budget['total_budget'] or 0



    team_types = [choice[0] for choice in Team.team_type_choices]
    team_type_counts = [Team.objects.filter(team_type=team_type).count() for team_type in team_types]



    
   

    context = {
        'servicecount': servicecount,
        'requestcount': requestcount,
        'projectcount': projectcount,
        'dcount':dcount,
        'managers':managers,
        'managerscount': managerscount,
        'customercount': customercount,
        'chart_image': chart_image,
        'pie_image': pie_image,
        'projectinprogress':projectinprogress,
        'totalclient':totalclient,
        'total_budget_amount':total_budget_amount,
        'revenue_monthly':revenue_monthly,

        'team_types': team_types,
        'team_type_counts': team_type_counts,

   

       
    }
    piechart(request)
    return render(request, 'dashboard.html', context)



@login_required(login_url="loginview")
@admin_only
def piechart(request):
    
     # Retrieve the data
    request_forms = requestform.objects.all()

    # Pie chart of request form status
    status_counts = request_forms.values('status').annotate(count=models.Count('status'))
    status_labels = [entry['status'] for entry in status_counts]
    status_counts = [entry['count'] for entry in status_counts]

    # Create the pie chart
    plt.pie(status_counts, labels=status_labels, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.title('Project Request Status')

    # Convert plot to image in memory
    image_stream = io.BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()

    # Encode the image stream as base64
    image_stream.seek(0)
    pie_image = base64.b64encode(image_stream.getvalue()).decode('utf-8')


    context = {
        
        'pie_image': pie_image,
    }

    return render(request, 'dashboard.html', context)


# /////////////////////////////////Dashboard End/////////////////////////////////////////




# Create your views here.
@login_required(login_url="loginview")
@allowed_users(allowed_roles=['admin'])
def register(request):

    form = CustomUserCreationForm() 
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='Project Manager')
            group.user_set.add(user)
            projectmanager = projectmanagers.objects.create(
                user=user,
                company=form.cleaned_data.get('company'),
                job=form.cleaned_data.get('job'),
                country=form.cleaned_data.get('country'),
            )
            messages.success(request, 'Account was created for ' + username)
            return redirect('projectmanagers')
        
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})



@unauthenticated_user
def loginviews(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request, 'User not found.')
            return redirect('/loginpage/')

        customer_group = Group.objects.get(name='Customer')
        if customer_group in user_obj.groups.all():
            profile_obj = Customer.objects.filter(user=user_obj).first()

            if not profile_obj.is_verified:
                messages.success(request, 'Profile is not verified. Check your email.')
                return redirect('/loginpage/')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/login/admin-dashboard/')
        else:
            messages.info(request, 'Username or password is incorrect')

    return render(request, 'login.html')




def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("loginview")








# ////////////services views/////////////////////////////
@login_required(login_url="loginview")
@allowed_users(allowed_roles=['admin'])
def service(request):
    obj=services.objects.all().order_by('id')
    return render(request,'servicestable.html',{'obj':obj})  

@login_required(login_url="loginview")
@allowed_users(allowed_roles=['admin'])
def servicedetails(request):
    obj=services.objects.all().order_by('id')
    return render(request,'servicesdetail.html',{'obj':obj})     

# ////////////services views end/////////////////////////////      
@login_required(login_url="loginview")
@allowed_users(allowed_roles=['admin'])
def customermessages(request):
    obj = contactus.objects.all().order_by('-created_at')
    message = contactus.objects.annotate(new_messages=Count('id')).all().order_by('-created_at').filter(is_read=False)
    new_message_count = contactus.objects.filter(is_read=False).count()

    return render(request, 'messages.html', {'obj': obj, 'message': message, 'new_message_count': new_message_count})


from django.shortcuts import get_object_or_404, redirect

@login_required(login_url="loginview")
@allowed_users(allowed_roles=['admin'])
def mark_message_as_read(request, message_id):
    message = get_object_or_404(contactus, id=message_id)
    message.is_read = True
    message.save()

    # Redirect back to the 'messages' page or any other desired page
    return redirect('messages')
# def customermessages(request):
#     obj=contactus.objects.all().order_by('-created_at')
#     message = contactus.objects.annotate(new_messages=Count('id')).all().order_by('-created_at')
#     return render(request,'messages.html',{'obj':obj,'message':message})



@login_required(login_url="loginview")
@allowed_users(allowed_roles=['admin'])
def projectrequests(request):
    obj=requestform.objects.filter(status__in=["Pending", "Rejected"]).order_by('-id')
    return render(request,'perposal-requests.html',{'obj':obj})   


# ////////////////////services CRUD///////////////////////////
@login_required(login_url="loginview")
@allowed_users(allowed_roles=['admin'])
def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Add Service Successfully")
            return redirect('service')  # Redirect to the service list page after successfully adding a service
    else:
        form = ServiceForm()

    return render(request, 'addservice.html', {'form': form})  


@login_required(login_url="loginview")
@allowed_users(allowed_roles=['admin'])
def delete(request, idservice):
  member = services.objects.get(id=idservice)
  member.delete()
  messages.info(request, "Delete data Successfully")
  return redirect('service')


@login_required(login_url="loginview")
@allowed_users(allowed_roles=['admin'])
def serviceupdate(request,serviceid):
    service=services.objects.get(id=serviceid)
    
    if request.method == "POST":
    
      
        # service.serviceimage=request.FILES['serviceimage']
        if 'serviceimage' in request.FILES:
            service.serviceimage = request.FILES['serviceimage'] 

        service.service_title=request.POST.get('service_title')
        service.service_desc=request.POST.get('service_desc')
        service.save()
        messages.info(request, "Update data Successfully")
        return redirect('service')


    context={
        'service':service
    }
    return render(request,'updateservice.html',context) 

# //////////////service details update/////////////////////

@login_required(login_url="loginview")
@allowed_users(allowed_roles=['admin'])
def servicedetailsupdate(request,servicedetailid):
    service=services.objects.get(id=servicedetailid)
    
    if request.method == "POST":
        
            if 'image_desc' in request.FILES:
                service.image_desc=request.FILES['image_desc']


            if 'image_Sited_Services' in request.FILES:
                service.image_Sited_Services=request.FILES['image_Sited_Services']     
             
          
            service.servicedetail_desc=request.POST.get('servicedetail_desc')
            service.Sited_Services_title=request.POST.get('Sited_Services_title')
            service.SitedServices=request.POST.get('Sited_Services')

            service.save()
            messages.info(request, "Update data Successfully")
            return redirect('servicedetails')


    context={
        'service':service
    }
    return render(request,'updateservicedetails.html',context) 

# ////////////////////services CRUD END///////////////////////////


# /////////////////////proposal status update////////////////
@login_required(login_url="loginview")
@allowed_users(allowed_roles=['admin'])
def statusupdate(request,statusid):
    status=requestform.objects.get(id=statusid)
    
    if request.method == "POST":
            status.status=request.POST.get('status')
            status.Project_Budget=request.POST.get('Project_Budget')
    
            status.save()
            messages.info(request, "Status Update Successfully")
            if status.status=="Accepted":
                return redirect('acceptedprojectlist')
            else:
                return redirect('projectrequests')


    context={
        'status':status
    }
    return render(request,'perposalstatus.html',context)



# /////////////////////project managers///////////////////////////////////////

@login_required(login_url="loginview")
@allowed_users(allowed_roles=['admin'])
def projectmanagerspage(request):
    projectmanager=projectmanagers.objects.all().order_by('-id')
    user=User.objects.all().order_by('-id')
    context={
        'projectmanager':projectmanager,
        'user':user,
        
    }
    return render(request,'projectmanagers.html',context)

# form to add new project manager
@login_required(login_url="loginview")
def projectmanagerform(request):
    return render(request,'formprojectmanager.html')  



@login_required(login_url="loginview")
@allowed_users(allowed_roles=['admin'])
def managersdetail(request,slug):
    managers=projectmanagers.objects.get(user_id=slug)
    user=User.objects.get(id=slug)
    # update data of project managers
    if request.method == "POST":
        if 'profileimage' in request.FILES:
            managers.profileimage=request.FILES['profileimage']
            
        user.username=request.POST.get('username')
        managers.about=request.POST.get('about')
        managers.company=request.POST.get('company')
        managers.job=request.POST.get('job')
        managers.country=request.POST.get('country')
        managers.address=request.POST.get('address')
        managers.phone=request.POST.get('phone')
        user.email=request.POST.get('email')
        managers.TwitterProfile=request.POST.get('TwitterProfile')
        managers.FacebookProfile=request.POST.get('FacebookProfile')
        managers.InstagramProfile=request.POST.get('InstagramProfile')
        managers.LinkedinProfile=request.POST.get('LinkedinProfile')
    
        managers.save()
        user.save()
        messages.info(request, "Profile Updated Successfully")
        return redirect('projectmanagers')

    data={
        'managers':managers,
        'user':user
    } 
    return render(request,'projectmanagerdetails.html', data) 


@login_required(login_url="loginview")
@allowed_users(allowed_roles=['admin'])
def deletemanager(request, id):
  deleteM = User.objects.get(id=id)
  deleteM.delete()
  messages.info(request, "Delete data Successfully")
  return redirect('projectmanagers')




@login_required(login_url="loginview")
@allowed_users(allowed_roles=['admin'])
def acceptedprojects(request):
    obj=requestform.objects.filter(status="Accepted", projectstatus="In Progress").order_by('-updated_at')
    return render(request,'acceptedProjectslist.html',{'obj':obj})      






@login_required(login_url="loginview")
@allowed_users(allowed_roles=['admin'])
def customertable(request):
    group = Group.objects.get(name='Customer')
    users = group.user_set.all()
    customer = Customer.objects.filter(user__in=users)
    # customer=Customer.objects.all()
    
    context={
        'customer':customer,
        'users':users,
        
    }
    return render(request,'customerlist.html',context)






@login_required(login_url="loginview")
@allowed_users(allowed_roles=['admin'])
def assign_project(request, proposal_id):
    proposal = get_object_or_404(requestform, id=proposal_id)

    if not request.user.is_staff:
        messages.error(request, 'You are not authorized to assign projects.')
        return redirect('acceptedprojectlist')

    if request.method == 'POST':
        assigned_to_id = request.POST.get('assigned_to')
        status = request.POST.get('status')
        proposal.Project_Finnish_Date = request.POST.get('finnish')
        proposal.Project_Start_Date = request.POST.get('start')
        # Check if ShortDesc exists in POST data
        short_desc = request.POST.get('short_desc')
        if short_desc:
            proposal.ShortDesc = short_desc

        if status != "Accepted":
            
                # Delete existing project assignments if the project manager is changed
            existing_assignments = ProjectAssignment.objects.filter(project=proposal)
            for assignment in existing_assignments:
                team_id = str(assignment.team.id)

                # Check if the team ID is not in the submitted team IDs list
                if team_id not in request.POST.getlist('teams'):
                    assignment.delete()
            proposal.assigned_to = None
            proposal.Project_Start_Date = None
            proposal.Project_Finnish_Date = None
            proposal.ShortDesc = None
            proposal.status = status
            proposal.save()
            messages.success(request, 'Project unassigned successfully!')
            return redirect('acceptedprojectlist')

        project_manager_changed = False

        if assigned_to_id and proposal.status == "Accepted":
            project_manager = get_object_or_404(projectmanagers, user_id=assigned_to_id)

            if proposal.assigned_to != project_manager:
                # Delete existing project assignments if the project manager is changed
                existing_assignments = ProjectAssignment.objects.filter(project=proposal)
                for assignment in existing_assignments:
                    team_id = str(assignment.team.id)

                    # Check if the team ID is not in the submitted team IDs list
                    if team_id not in request.POST.getlist('teams'):
                        assignment.delete()

                proposal.assigned_to = project_manager
                proposal.Project_Start_Date = request.POST.get('start')
                proposal.Project_Finnish_Date = request.POST.get('finnish')
                project_manager_changed = True
        
        proposal.status = status

        try:
            # Perform validation on selected fields
            proposal.full_clean(exclude=['paymentstatus'])  # Exclude fields you don't want to validate
        except ValidationError as e:
            for field, errors in e.message_dict.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
            return redirect('assign_project', proposal_id)

        proposal.save()

        if project_manager_changed:
            messages.success(request, 'Project assigned successfully!')
        else:
            messages.success(request, 'Updated successfully!')

        return redirect('acceptedprojectlist')

    project_managers = projectmanagers.objects.all()
    return render(request, 'assign_project.html', {'proposal': proposal, 'project_managers': project_managers})










# ///////////////////////////////List of Teams//////////////////////////////////

#/////////////////Developes Team Page////////////////
@login_required(login_url="loginview")
@allowed_users(allowed_roles=['admin'])
def Teamlist(request):
    
    group = Group.objects.get(name='Project Team')
    users = group.user_set.all()
    projectTeam = Team.objects.filter(user__in=users)

    project_manager=projectmanagers.objects.all()
    
    
    context={
        'projectTeam':projectTeam,
        'users':users,
        'project_manager':project_manager,
        
    }
    return render(request,'teamlist.html',context)



@login_required(login_url="loginview")
@allowed_users(allowed_roles=['admin'])
def managerattendance(request):
    managersattendance = Attendance.objects.all().order_by('-date')
    return render(request,'manager-attendance.html',{'managersattendance':managersattendance})  


from django.db.models import Prefetch
@login_required(login_url="loginview")
@allowed_users(allowed_roles=['admin'])
def completeprojects(request):
    # obj=requestform.objects.filter(projectstatus="Complete").order_by('-updated_at')
    # obj = requestform.objects.filter(projectstatus="Complete").select_related('documents').order_by('-updated_at')
    obj = requestform.objects.filter(projectstatus__in=['Complete', 'Delivered']).order_by('-updated_at')
    
    # Prefetch related documents for each requestform instance
    obj = obj.prefetch_related(Prefetch('documents', queryset=ProjectCompletionDocument.objects.all(), to_attr='project_documents'))
    return render(request,'completeproject.html',{'obj':obj})   




@login_required(login_url="loginview")
@allowed_users(allowed_roles=['admin'])
def Careerpage(request):
    allcareer=Career.objects.all().order_by('-id')
    context={
        'allcareer':allcareer,

    }
    return render(request,'careerlist.html',context)


@login_required(login_url="loginview")
@allowed_users(allowed_roles=['admin'])
def careersdetail(request, id):
    careerdetail = get_object_or_404(Career, id=id)

    if request.method == 'POST':
        careerform = CareerFormdata(request.POST, request.FILES, instance=careerdetail)
        if careerform.is_valid():
            careerform.save()
            # Handle the successful update, such as redirecting to a success page
            messages.success(request, 'Career Update Successfully')
            return redirect('careersdetail',careerdetail.id)  # Replace 'success_page_name' with the URL name of your success page
    else:
        careerform = CareerFormdata(instance=careerdetail)

    data = {
        'careerdetail': careerdetail,
        'careerform': careerform
    } 
    return render(request, 'careersdetails.html', data)

@login_required(login_url="loginview")
@allowed_users(allowed_roles=['admin'])
def deletecareer(request, id):
  deleteC = Career.objects.get(id=id)
  deleteC.delete()
  messages.info(request, "Delete Career Successfully")
  return redirect('Careerpage')



def Addcareers(request):
    if request.method == 'POST':
        formcareer = CareerFormdata(request.POST, request.FILES)
        if formcareer.is_valid():
            formcareer.save()
            # Redirect to a success page after successful form submission
            return redirect('Careerpage')  # Replace 'success_page_name' with the URL name of your success page
    else:
        formcareer = CareerFormdata()

    data = {
        'formcareer': formcareer,
    }
    return render(request, 'careeradd.html', data)


@login_required(login_url="loginview")
@allowed_users(allowed_roles=['admin'])
def careertable(request):
    obj=CareerForm.objects.all().order_by('-id')
    return render(request,'careerRequests.html',{'obj':obj})  






@login_required(login_url="loginview")
@allowed_users(allowed_roles=['admin'])
def adminprojectscards(request):
    projectcard = requestform.objects.exclude(assigned_to=None).order_by('-id')
    total_projects = projectcard.count()

    for project in projectcard:
        total_tasks = project.tasks.count()
        completed_tasks = project.tasks.filter(status='completed').count()
        project.completion_percentage = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0

        # Check if Project_Finnish_Date is not None before calculating remaining_days
        if project.Project_Finnish_Date:
            remaining_days = (project.Project_Finnish_Date - datetime.now().date()).days
            project.remaining_days = remaining_days
        else:
            project.remaining_days = None  # or any other default value you want to set for cases where Project_Finnish_Date is None

        # Get all teams associated with the project
        teams = ProjectAssignment.objects.filter(project=project)

        # Check if all teams have completion_status=True
        all_teams_completed = all(team.completion_status for team in teams)

        # Set the all_teams_completed flag in the project instance
        project.all_teams_completed = all_teams_completed

    return render(request, 'adminprojectcards.html', {'projectcard': projectcard, 'total_projects': total_projects})