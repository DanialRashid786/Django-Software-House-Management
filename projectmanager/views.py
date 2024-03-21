from audioop import reverse
import mimetypes
import os
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from ProjectTeam.models import Task
from customer.forms import *
from customer.models import *
from .models import *

from projectmanager.forms import  *
from customadmin.decorators import allowed_users, admin_only, unauthenticated_user
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm  
from django.db.models import Count
from django.urls import reverse

@login_required(login_url='loginview')
@allowed_users(allowed_roles=['Project Manager'])
def projectmanager(request):
    project_manager = request.user.projectmanagers  # Assuming you have set the related_name for the ForeignKey

    # Get the count of projects assigned to the project manager
    assigned_projects_count = requestform.objects.filter(assigned_to=project_manager).count()
    completedproject = requestform.objects.filter(assigned_to=project_manager, projectstatus='Complete').count()
    total_team_members = Team.objects.filter(project_manager=project_manager).count



    # # Calculate the total number of team members
    projects = requestform.objects.filter(assigned_to=project_manager)
    # tasks = Task.objects.filter(project__assigned_to=project_manager)

    # Get the tasks for the selected project (if a project is selected)
    tasks = []
    selected_project = None
    if request.method == 'POST':
        project_id = request.POST.get('project')
        selected_project = requestform.objects.get(pk=project_id)
        tasks = Task.objects.filter(project=selected_project, project__assigned_to=project_manager)

    # Calculate task completion metrics for the selected project
    team_performance = {"todo": 0, "in_progress": 0, "completed": 0, "to_review":0,"needs_revision": 0}
    for task in tasks:
        status = task.get_status_display()
        if status == "To Do":
            team_performance["todo"] += 1
        elif status == "In Progress":
            team_performance["in_progress"] += 1
        elif status == "Completed":
            team_performance["completed"] += 1

        elif status == "To Review":
            team_performance["to_review"] += 1
        elif status == "Needs Revision":
            team_performance["needs_revision"] += 1

    team_counts = Team.objects.filter(project_manager=project_manager).values('team_type').annotate(count=Count('team_type'))

    
    # Count the number of completed projects for each team assigned to the project manager
    

    # Get all teams associated with the project manager
    teams = Team.objects.filter(project_manager=project_manager)

    # Calculate the count of completed projects for each team
    team_completed_projects = []
    for team in teams:
        completed_projects_count = ProjectAssignment.objects.filter(
            team=team,
            completion_status=True
        ).count()
        team_completed_projects.append({
            'team_name': team.user.username,
            'completed_projects_count': completed_projects_count,
            'team_type':team.team_type
        })
    

    context={
        'project_manager': project_manager,
        'assigned_projects_count': assigned_projects_count,
        'completedproject':completedproject,
        'total_team_members':total_team_members,

        'projects':projects,
        'selected_project': selected_project,
        'team_performance': team_performance,
        'team_counts':team_counts,
        'team_completed_projects': team_completed_projects
    }
    return render(request,'PMdashboard.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Project Manager'])
def accountSettings(request):
    manager = request.user.projectmanagers
    form = projectmanagerForm(instance=manager)

    if request.method == 'POST':
        form = projectmanagerForm(request.POST, request.FILES, instance=manager)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account was updated successfully')
            return redirect('/account/')
    else:
        user = request.user
        form = projectmanagerForm(instance=manager, initial={'first_name': user.first_name, 'last_name': user.last_name})
        # 'email':user.email

    context = {'form': form}
    return render(request, 'account_settings.html', context)






        


# //////////////////////////////////////project team//////////////////////////////

@login_required(login_url="loginview")
@allowed_users(allowed_roles=['Project Manager'])
def Teamregister(request):
    manager = request.user.projectmanagers

    form = projectteam() 
    if request.method == 'POST':
        form = projectteam(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='Project Team')
            group.user_set.add(user)
            Teams = Team.objects.create(
                user=user,
                project_manager= manager,
                team_type=form.cleaned_data.get('team_type'),
                company=form.cleaned_data.get('company'),
                country=form.cleaned_data.get('country'),
            )
            messages.success(request, 'Account was created for ' + username)
            return redirect('/login/manager-dashboard')
        
    else:
        form = projectteam()
    context = {'form2':form}    
    return render(request, 'registerTeam.html', context)


# /////////////////////////////////DELETE TEAMS///////////////////////////
# Developer team delete
@login_required(login_url="loginview")
@allowed_users(allowed_roles=['Project Manager'])
def deleteTeam(request, id):
  deleteT = User.objects.get(id=id)
  deleteT.delete()
  messages.info(request, "Delete Account Successfully")
  return redirect('teams')

# Designer team delete
@login_required(login_url="loginview")
@allowed_users(allowed_roles=['Project Manager'])
def deleteTeamDesigner(request, id):
  deleteT = User.objects.get(id=id)
  deleteT.delete()
  messages.info(request, "Delete Account Successfully")
  return redirect('Designerteams')

# QA team delete
@login_required(login_url="loginview")
@allowed_users(allowed_roles=['Project Manager'])
def deleteTeamQA(request, id):
  deleteT = User.objects.get(id=id)
  deleteT.delete()
  messages.info(request, "Delete Account Successfully")
  return redirect('deleteTeamQA')

# Business team delete
@login_required(login_url="loginview")
@allowed_users(allowed_roles=['Project Manager'])
def deleteTeamBusiness(request, id):
  deleteT = User.objects.get(id=id)
  deleteT.delete()
  messages.info(request, "Delete Account Successfully")
  return redirect('BusinessAnalystTeam')


# Devops team delete
@login_required(login_url="loginview")
@allowed_users(allowed_roles=['Project Manager'])
def deleteTeamDevops(request, id):
  deleteT = User.objects.get(id=id)
  deleteT.delete()
  messages.info(request, "Delete Account Successfully")
  return redirect('DEVOPSTeam')

# /////////////////////////////////DELETE TEAMS END///////////////////////////



#/////////////////Developes Team Page////////////////
@login_required(login_url="loginview")
@allowed_users(allowed_roles=['Project Manager'])
def developersTeams(request):
    # projectTeam=Team.objects.all().order_by('-id')
    projectTeam = Team.objects.filter(project_manager=request.user.projectmanagers,team_type="Developer")
    user=User.objects.all().order_by('-id')
    context={
        'projectTeam':projectTeam,
        'user':user,
        
    }
    return render(request,'DevelopersTeamspage.html',context)



#/////////////////Designer Team Page////////////////
@login_required(login_url="loginview")
@allowed_users(allowed_roles=['Project Manager'])
def designerTeams(request):
    # projectTeam=Team.objects.all().order_by('-id')
    projectTeam = Team.objects.filter(project_manager=request.user.projectmanagers,team_type="Designer")
    user=User.objects.all().order_by('-id')
    context={
        'projectTeam':projectTeam,
        'user':user,
        
    }
    return render(request,'DesignersTeamspage.html',context)


#/////////////////QA Engineer Team Page////////////////
@login_required(login_url="loginview")
@allowed_users(allowed_roles=['Project Manager'])
def QATeam(request):
    # projectTeam=Team.objects.all().order_by('-id')
    projectTeam = Team.objects.filter(project_manager=request.user.projectmanagers,team_type="QA Engineer")
    user=User.objects.all().order_by('-id')
    context={
        'projectTeam':projectTeam,
        'user':user,
        
    }
    return render(request,'QATeamsPage.html',context)


#/////////////////Business Analyst Team Page////////////////
@login_required(login_url="loginview")
@allowed_users(allowed_roles=['Project Manager'])
def BusinessAnalystTeam(request):
    # projectTeam=Team.objects.all().order_by('-id')
    projectTeam = Team.objects.filter(project_manager=request.user.projectmanagers,team_type="Business Analyst")
    user=User.objects.all().order_by('-id')
    context={
        'projectTeam':projectTeam,
        'user':user,
        
    }
    return render(request,'BusinessAnalyst.html',context)



#/////////////////DEVOPS engineer Teams Page////////////////
@login_required(login_url="loginview")
@allowed_users(allowed_roles=['Project Manager'])
def DEVOPS(request):
    # projectTeam=Team.objects.all().order_by('-id')
    projectTeam = Team.objects.filter(project_manager=request.user.projectmanagers,team_type="DEVOPS")
    user=User.objects.all().order_by('-id')
    context={
        'projectTeam':projectTeam,
        'user':user,
        
    }
    return render(request,'BusinessAnalyst.html',context)



# ///////////Team Details//////////////

@login_required(login_url="loginview")
@allowed_users(allowed_roles=['Project Manager'])
def teamdetail(request,slug):
    teams=Team.objects.get(user_id=slug)
    user=User.objects.get(id=slug)
    # update data of project managers
    if request.method == "POST":
       
        teams.profileimage=request.FILES['profileimage']
            
        user.username=request.POST.get('username')
        teams.about=request.POST.get('about')
        teams.company=request.POST.get('company')
        teams.job=request.POST.get('job')
        teams.country=request.POST.get('country')
        teams.address=request.POST.get('address')
        teams.phone=request.POST.get('phone')
        user.email=request.POST.get('email')
        teams.TwitterProfile=request.POST.get('TwitterProfile')
        teams.FacebookProfile=request.POST.get('FacebookProfile')
        teams.InstagramProfile=request.POST.get('InstagramProfile')
        teams.LinkedinProfile=request.POST.get('LinkedinProfile')
    
        teams.save()
        user.save()
        messages.info(request, "Profile Updated Successfully")
        return redirect('projectmanager')

    data={
        'teams':teams,
        'user':user
    } 
    return render(request,'teamdetails.html', data) 




from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

def assign_project(request, project_id):
    project = get_object_or_404(requestform, id=project_id)
    project_manager = project.assigned_to
    teams = Team.objects.filter(project_manager=project_manager)
    assigned_teams = ProjectAssignment.objects.filter(project=project).values_list('team', flat=True)

    if request.method == 'POST':
        team_ids = request.POST.getlist('teams')
        assignment_deleted = False  # Flag variable to track if any assignment is deleted

        # Get the existing project assignments for the project
        existing_assignments = ProjectAssignment.objects.filter(project=project)

        # Iterate over existing assignments
        for assignment in existing_assignments:
            team_id = str(assignment.team.id)

            # Check if the team ID is not in the submitted team IDs list
            if team_id not in team_ids:
                assignment.delete()  # Delete the assignment
                assignment_deleted = True  # Set the flag variable
                messages.success(request, f"The project '{project.project_title}' has been unassigned from team '{assignment.team.user.username} ({assignment.team.team_type})'.")

        # Iterate over the submitted team IDs
        for team_id in team_ids:
            team = Team.objects.get(id=team_id)

            # Check if the project has already been assigned to the team
            if ProjectAssignment.objects.filter(team=team, project=project).exists():
                messages.warning(request, f"The project '{project.project_title}' is already assigned to the team '{team.user.username} ({team.team_type})'.")
                continue

            assignment = ProjectAssignment.objects.create(team=team, project=project)

        if not assignment_deleted:
            messages.success(request, f"The project '{project.project_title}' has been successfully assigned to the selected teams.")

        return redirect('/projects/')  # Redirect to the project manager's dashboard

    return render(request, 'assign_project1.html', {'project': project, 'teams': teams, 'assigned_teams': assigned_teams})





@login_required(login_url="loginview")
@allowed_users(allowed_roles=['Project Manager'])
def attendancelist(request):
    project_manager = request.user.projectmanagers

    # Get the assigned projects for the project manager
    attendancelist = project_manager.attendancelist.all().order_by('-id')

    data = {
        'attendancelist': attendancelist,
    }

    return render(request, 'attendancelist.html', data)




@login_required(login_url="loginview")
@allowed_users(allowed_roles=['Project Manager'])
def completeprojects(request):
	# if not request.user.is_staff:
	# 	return redirect('managersprojects')
		
	# assigned_projects = requestform.objects.filter(assigned_to=request.user.id)
	project_manager = request.user.projectmanagers

    # Get the assigned projects for the project manager
	assigned_projects = project_manager.assigned_projects.filter(projectstatus__in=["Complete", "Delivered"]).order_by('-updated_at')
    
    


	return render(request, 'completedproject.html',{'assigned_projects': assigned_projects})



@login_required(login_url="loginview")
@allowed_users(allowed_roles=['Project Manager'])
def Mprojects(request):
	# if not request.user.is_staff:
	# 	return redirect('managersprojects')
		
	# assigned_projects = requestform.objects.filter(assigned_to=request.user.id)
	project_manager = request.user.projectmanagers

    # Get the assigned projects for the project manager
	assigned_projects = project_manager.assigned_projects.filter(projectstatus="In Progress").order_by('-id')
	return render(request, 'assigntask.html',{'assigned_projects': assigned_projects})




@login_required(login_url="loginview")
@allowed_users(allowed_roles=['Project Manager'])
def assign_task(request, project_id):
    project = get_object_or_404(requestform, id=project_id)
    project_manager = request.user.projectmanagers
    # assigned_projects = project_manager.assigned_projects.filter(projectstatus="In Progress").order_by('-id')

    assigned_projects = ProjectAssignment.objects.filter(project=project)


    if request.method == 'POST':
        team_id = request.POST.get('team')
        name = request.POST.get('name')
        description = request.POST.get('description')
        TaskRequirementFile=request.FILES['Requirement']
        tags = request.POST.get('tags')
        category = request.POST.get('category')
        deadline = request.POST.get('deadline')

        try:
            team = Team.objects.get(id=team_id)
            # Create the task assignment
            task = Task.objects.create(
                project=project,
                name=name,
                description=description,
                TaskRequirementFile=TaskRequirementFile,
                tags=tags,
                category=category,
                deadline=deadline,
                assigned_to=team,
                status='todo'  # Set the default status as 'todo'
            )
            return redirect('alltask')
        except Team.DoesNotExist:
            return HttpResponseBadRequest("Invalid team ID. Task assignment failed.")
    else:
        # Handle GET request, render the template with the assigned projects and teams
        return render(request, 'task.html', {'assigned_projects': assigned_projects})
    

@login_required(login_url="loginview")
@allowed_users(allowed_roles=['Project Manager'])
def alltask(request):
    project_manager = request.user.projectmanagers
    assigned_tasks = Task.objects.filter(project__assigned_to=project_manager).order_by('-id')

    project_choices = [(project.id, project.project_title) for project in requestform.objects.filter(assigned_to=project_manager.id)]

    team_member_choices = [(team.id, team.user.username) for team in Team.objects.filter(project_manager=project_manager.id)]

    form = TaskFilterForm(request.POST or None)
    form.fields['project'].choices = [('', 'All')] + project_choices
    form.fields['team_member'].choices = [('', 'All')] + team_member_choices

    if request.method == 'POST' and form.is_valid():
        project_id = form.cleaned_data.get('project')
        team_member_id = form.cleaned_data.get('team_member')
        status = form.cleaned_data.get('status')

        # Apply filters based on form data
        if project_id:
            assigned_tasks = assigned_tasks.filter(project_id=project_id)
        if team_member_id:
            assigned_tasks = assigned_tasks.filter(assigned_to=team_member_id)
        if status:
            assigned_tasks = assigned_tasks.filter(status=status)

    return render(request, 'tasklist.html', {'assigned_tasks': assigned_tasks, 'form': form})





def upload_completion_document(request, project_id,project_name):
    project = get_object_or_404(requestform, id=project_id,project_title=project_name)

    documents_uploaded = ProjectCompletionDocument.objects.filter(project=project).exists()

    project_documents = ProjectCompletionDocument.objects.filter(project_id=project_id)

    if request.method == 'POST':
        form = ProjectCompletionDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            completion_document = form.save(commit=False)
            completion_document.project = project
            completion_document.save()
            # Handle successful upload, redirect to a success page, etc.
    else:
        form = ProjectCompletionDocumentForm()

    return render(request, 'upload_completion_document.html', {'form': form, 'project': project,'documents_uploaded': documents_uploaded,'project_documents':project_documents})





@login_required(login_url="loginview")
@allowed_users(allowed_roles=['Project Manager'])
def managersprojects(request):
	# if not request.user.is_staff:
	# 	return redirect('managersprojects')
		
	# assigned_projects = requestform.objects.filter(assigned_to=request.user.id)
	project_manager = request.user.projectmanagers

    # Get the assigned projects for the project manager
	assigned_projects = project_manager.assigned_projects.filter(projectstatus="In Progress").order_by('-id')
	return render(request, 'managersprojects.html',{'assigned_projects': assigned_projects})


@login_required(login_url="loginview")
@allowed_users(allowed_roles=['Project Manager'])
def projectscards(request):
    project_manager = request.user.projectmanagers

    # Get the assigned projects for the project manager
    projectcard = project_manager.assigned_projects.order_by('-updated_at')
    total_projects = projectcard.count()
    remaining_days = [] 
    for project in projectcard:
        total_tasks = project.tasks.count()
        completed_tasks = project.tasks.filter(status='completed').count()
        project.completion_percentage = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0

        remaining_days = (project.Project_Finnish_Date - datetime.now().date()).days
        project.remaining_days = remaining_days  # Add remaining_days to the project instance

        # Get all teams associated with the project
        teams = ProjectAssignment.objects.filter(project=project)

        # Check if all teams have completion_status=True
        all_teams_completed = all(team.completion_status for team in teams)

        # Set the all_teams_completed flag in the project instance
        project.all_teams_completed = all_teams_completed
        

    return render(request, 'projectcards.html', {'projectcard': projectcard,'total_projects':total_projects})




@login_required(login_url="loginview")
@allowed_users(allowed_roles=['Project Manager'])
def update_project_status(request):
    if request.method == 'POST':
        # Get parameters from the POST request
        projectid = request.POST.get('taskid')
        status = request.POST.get('status')

        # Get the task object
        projectstatu = get_object_or_404(requestform, id=projectid)

        # Update the task status
        projectstatu.projectstatus = status
        projectstatu.save()

        return redirect('/completedprojects/')
        

    # Return a JSON response indicating failure for invalid requests
    response_data = {'status': 'error', 'message': 'Invalid request.'}
    return JsonResponse(response_data)







@login_required(login_url="loginview")
@allowed_users(allowed_roles=['Project Manager'])
def kanbanboard(request,pid,pname):

    project_manager = request.user.projectmanagers

    projectname = get_object_or_404(requestform, id=pid,project_title=pname)

    projecttask = Task.objects.filter(project__assigned_to=project_manager,project=pid,project__project_title=pname,status="todo").order_by("-date_created")
    task_count = projecttask.count()

    projecttask1 = Task.objects.filter(project__assigned_to=project_manager,project=pid,project__project_title=pname,status="in_progress").order_by("-updated_at")
    task_count1 = projecttask1.count()

    projecttask2 = Task.objects.filter(project__assigned_to=project_manager,project=pid,project__project_title=pname,status="to_review").order_by("-updated_at")
    task_count2 = projecttask2.count()


    projecttask3 = Task.objects.filter(project__assigned_to=project_manager,project=pid,project__project_title=pname,status="completed").order_by("-updated_at")
    task_count3 = projecttask3.count()

    projecttask4 = Task.objects.filter(project__assigned_to=project_manager,project=pid,project__project_title=pname,status="needs_revision").order_by("-updated_at")
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
        task.save()

        url = reverse('Kanbanboard',args=[pid, pname])
        return redirect(url)

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

    return render(request, 'projecttasks.html',data)



from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
@method_decorator(login_required, name='dispatch')
class ViewDocument(View):
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
class DownloadDocument(View):
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
        

        
        

    