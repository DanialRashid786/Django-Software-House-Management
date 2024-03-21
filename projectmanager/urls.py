from django.contrib import admin
from django.urls import path,include
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('login/manager-dashboard', projectmanager, name="projectmanager"),
    path('project/<int:project_id>/assign/', assign_project, name='assign_projects'),

    path('account/', accountSettings, name="account"),
    
    path('projects/', managersprojects, name="managersprojects"),
    path('projectcards/', projectscards, name="projectscards"),
    path('projecttasks/<pid>/<pname>', kanbanboard, name="Kanbanboard"),


    path('completedprojects/', completeprojects, name="completeprojects"),

    path('attendancelist/', attendancelist, name="attendancelist"),
    

    
    path('Teamregisterform/', Teamregister, name = 'registerteam'),

    path('deleteTeamDeveloper/<id>', deleteTeam, name='deleteTeam'),
    path('deleteTeamDesigner/<id>', deleteTeamDesigner, name='deleteTeamDesigner'),
    path('deleteTeamQA/<id>', deleteTeamQA, name='deleteTeamQA'),
    path('deleteTeamBusiness/<id>', deleteTeamBusiness, name='deleteTeamBusiness'),
    path('deleteTeamDevops/<id>', deleteTeamDevops, name='deleteTeamDevops'),


    path('projectTeams/', developersTeams, name='teams'),
    path('DesignerTeams/', designerTeams, name='Designerteams'),
    path('QATeams/', QATeam, name='QATeam'),
    path('BusinessAnalystTeam/', BusinessAnalystTeam, name='BusinessAnalystTeam'),
    path('DEVOPSTeam/', DEVOPS, name='DEVOPSTeam'),


    path("teamdetail/<slug>", teamdetail, name="teamdetail"),


    path('assigntask/', Mprojects, name="Mprojects"),
    path('Taskassign/<int:project_id>/newtask/', assign_task, name='assign_task'),
    path('alltask/', alltask, name="alltask"),
    

 path('projects/<project_id>/<project_name>/upload-completion-document/', upload_completion_document, name='upload_completion_document'),


path('view_Document/<int:task_id>/', ViewDocument.as_view(), name='View_document'),
path('download_Document/<int:task_id>/', DownloadDocument.as_view(), name='Download_document'),



path('update_project_status/', update_project_status, name="updateprojectstatus"),

#  path('Pm_update_task_status/', Pm_update_task_status, name="taskstatusPM"),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
