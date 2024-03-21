import mimetypes
from django.shortcuts import get_object_or_404, render
from audioop import reverse
import os
from django.http import HttpResponse, JsonResponse
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from ProjectTeam.forms import projectteamForm
from customer.models import *
from projectmanager.models import *
from .models import *

from customadmin.decorators import allowed_users, admin_only, unauthenticated_user
from django.contrib.auth.models import Group
from django.contrib.auth.forms import *

from django.db.models import Count, F, ExpressionWrapper, DecimalField
from django.urls import reverse


from django.core.files.storage import FileSystemStorage
  
# Create your views here.

@login_required(login_url='loginview')
@allowed_users(allowed_roles=['Project Team'])
def projectteam(request):
    project_Team = request.user.team
    assigned_project = project_Team.assigned_projects_team.all()
    total_projects = assigned_project.count()
    
    context={
        'total_projects':total_projects,
        
    }
    return render(request,'PTdashboard.html',context)





@login_required(login_url='loginview')
@allowed_users(allowed_roles=['Project Team'])
def teamprojects(request):
    project_Team = request.user.team

    assigned_project = project_Team.assigned_projects_team.all().order_by('-id')
    context = {
        'assigned_project': assigned_project
    }
    return render(request, 'teamprojects.html', context)

@login_required(login_url="loginview")
@allowed_users(allowed_roles=['Project Team'])
def update_completion_status(request, assignment_id):
    if request.method == 'POST':
        assignment = ProjectAssignment.objects.get(id=assignment_id)
        completion_status = request.POST.get('completion_status') == 'on'  # Get the checkbox value
        assignment.completion_status = completion_status
        messages.success(request, 'Project Status update successfully')
        assignment.save()
        
		# Check if all project team members have completed their assignments
        all_completed = ProjectAssignment.objects.filter(project=assignment.project, completion_status=False).exists()
        if not all_completed:
            assignment.project.projectstatus = 'Complete'
            assignment.project.save()
        else:
            assignment.project.projectstatus = 'In Progress'
            assignment.project.save()
              

    return redirect('teamprojects')




@login_required(login_url='login')
@allowed_users(allowed_roles=['Project Team'])
def teamaccountSettings(request):
	team = request.user.team
	form = projectteamForm(instance=team)

	if request.method == 'POST':
		form = projectteamForm(request.POST, request.FILES, instance=team)
		if form.is_valid():
			form.save()
			messages.success(request, 'Account was updated successfully')
			return redirect('/teamaccount/')
	else:
		user = request.user
		form = projectteamForm(instance=team, initial={'first_name': user.first_name, 'last_name': user.last_name})
	context = {'form': form}
	return render(request, 'teamaccount_settings.html', context)



@login_required(login_url="loginview")
@allowed_users(allowed_roles=['Project Team'])  # Modify the allowed roles as needed
def teamtasks(request):
    team = request.user.team  # Assuming you have a 'team' field in your User model
    team_tasks = Task.objects.filter(assigned_to=team).order_by('-updated_at')
    return render(request, 'teamtasks.html', {'team_tasks': team_tasks})



@login_required(login_url="loginview")
@allowed_users(allowed_roles=['Project Team'])
def update_task_status(request):
    if request.method == 'POST':
        # Get parameters from the POST request
        task_id = request.POST.get('taskId')
        status = request.POST.get('status')

        # Get the task object
        task = get_object_or_404(Task, id=task_id)

        # Update the task status
        task.status = status
        task.save()

        return redirect('/tasklist/')
        

    # Return a JSON response indicating failure for invalid requests
    response_data = {'status': 'error', 'message': 'Invalid request.'}
    return JsonResponse(response_data)





@login_required(login_url='loginview')
@allowed_users(allowed_roles=['Project Team'])
def teamprojectscards(request):
    project_Team = request.user.team

    assigned_project = project_Team.assigned_projects_team.all().order_by('-id')
    total_projects = assigned_project.count()

    

    remaining_days = [] 
    for projects in assigned_project:
        projects.task_count = Task.objects.filter(project=projects.project , assigned_to=projects.team).count()

        projects.task_count = projects.task_count
        
        projects.completed_tasks = Task.objects.filter(project=projects.project, assigned_to=projects.team, status='completed').count()
        total_tasks = projects.task_count
        projects.completion_percentage = (projects.completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
        # completed_tasks = projects.tasks.filter(status='completed').count()
        # projects.completion_percentage = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0

        remaining_days = (projects.project.Project_Finnish_Date - datetime.now().date()).days
        projects.project.remaining_days = remaining_days  # Add remaining_days to the project instance

    context = {
        'assigned_project': assigned_project,
        'total_projects':total_projects,
    }
    return render(request, 'teamprojectcards.html', context)





@login_required(login_url="loginview")
@allowed_users(allowed_roles=['Project Team'])
def teamkanbanboard(request,pid,pname):

    project_team = request.user.team

    projectname = get_object_or_404(requestform, id=pid,project_title=pname)

    projecttask = Task.objects.filter(assigned_to=project_team,project=pid,project__project_title=pname,status="todo").order_by("-id")
    task_count = projecttask.count()

    projecttask1 = Task.objects.filter(assigned_to=project_team,project=pid,project__project_title=pname,status="in_progress").order_by("-id")
    task_count1 = projecttask1.count()

    projecttask2 = Task.objects.filter(assigned_to=project_team,project=pid,project__project_title=pname,status="to_review").order_by("-updated_at")
    task_count2 = projecttask2.count()

    projecttask3 = Task.objects.filter(assigned_to=project_team,project=pid,project__project_title=pname,status="completed").order_by("-updated_at")
    task_count3 = projecttask3.count()

    projecttask4 = Task.objects.filter(assigned_to=project_team,project=pid,project__project_title=pname,status="needs_revision").order_by("-id")
    task_count4 = projecttask4.count()

    bg_colors = ['bg-info', 'bg-success', 'bg-warning', 'bg-danger']
    remaining_days = []  # Initialize remaining_days as an empty list   
    for project in projecttask:
        remaining_days = (project.deadline - datetime.now().date()).days
        project.remaining_days = remaining_days

    for project in projecttask1:
        remaining_days = (project.deadline - datetime.now().date()).days
        project.remaining_days = remaining_days
    
    for project in projecttask2:
        remaining_days = (project.deadline - datetime.now().date()).days
        project.remaining_days = remaining_days
    
    for project in projecttask3:
        remaining_days = (project.deadline - datetime.now().date()).days
        project.remaining_days = remaining_days

    for project in projecttask4:
        remaining_days = (project.deadline - datetime.now().date()).days
        project.remaining_days = remaining_days


    if request.method == 'POST':
        # Get parameters from the POST request
        task_id = request.POST.get('task_id')
        status = request.POST.get('status')

        # Check if task_id is a valid positive integer
        if not task_id.isdigit():
            response_data = {'status': 'error', 'message': 'Invalid task ID.'}
            return JsonResponse(response_data)

        # Get the task object
        task = get_object_or_404(Task, id=task_id)

        # Update the task status
        task.status = status
        # Handle document upload
        uploaded_file = request.FILES.get('doc')
        if uploaded_file:
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)
            document = Document.objects.create(task=task, file=filename)
        task.save()

        url = reverse('teamKanbanboard',args=[pid, pname])
        return redirect(url)

        # return redirect('/tasklist/')
  

        # # Return a JSON response indicating failure for invalid requests
        # response_data = {'status': 'error', 'message': 'Invalid request.'}
        # return JsonResponse(response_data)
    

    data={
       'projecttask':projecttask,
       'projecttask1':projecttask1,
       'projecttask2':projecttask2,
       'projecttask3':projecttask3,
       'projecttask4':projecttask4,
       'bg_colors':bg_colors,
       'remaining_days':remaining_days,
       'projectname':projectname,
       'task_count':task_count,
       'task_count1':task_count1,
       'task_count2':task_count2,
       'task_count3':task_count3,
       'task_count4':task_count4,
    }

    return render(request, 'taskscards.html',data)




# Other imports
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
@method_decorator(login_required, name='dispatch')
class ViewDocumentView(View):
    def get(self, request, task_id, *args, **kwargs):
        task = get_object_or_404(Task, id=task_id)
        latest_document = task.documents.last()

        if latest_document:
            with open(latest_document.file.path, 'rb') as file:
                content_type, _ = mimetypes.guess_type(latest_document.file.name)
                response = HttpResponse(file.read(), content_type=content_type or 'application/octet-stream')
                response['Content-Disposition'] = f'inline; filename="{latest_document.file.name}"'
                return response
        else:
            return HttpResponse("No document available.")

@method_decorator(login_required, name='dispatch')
class DownloadDocumentView(View):
    def get(self, request, task_id, *args, **kwargs):
        task = get_object_or_404(Task, id=task_id)
        latest_document = task.documents.last()

        if latest_document:
            with open(latest_document.file.path, 'rb') as file:
                content_type, _ = mimetypes.guess_type(latest_document.file.name)
                response = HttpResponse(file.read(), content_type=content_type or 'application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{latest_document.file.name}"'
                return response
        else:
            return HttpResponse("No document available.")