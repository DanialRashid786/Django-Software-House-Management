from django.contrib import admin
from django.urls import path,include
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    
    path('login/team-dashboard', projectteam, name="projectteam"),

    path('teamprojects/', teamprojects, name="teamprojects"),

    path('teamaccount/', teamaccountSettings, name="teamaccount"),

    path('update_completion_status/<int:assignment_id>/', update_completion_status, name='update_completion_status'),

    path('tasklist/', teamtasks, name='teamtasks'),

    path('update_task_status/', update_task_status, name='update_task_status'),

  

     path('teamprojectscards/', teamprojectscards, name="teamprojectscards"),

      path('teamprojecttasks/<pid>/<pname>', teamkanbanboard, name="teamKanbanboard"),


path('view_document/<int:task_id>/', ViewDocumentView.as_view(), name='view_document'),
    path('download_document/<int:task_id>/', DownloadDocumentView.as_view(), name='download_document'),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
