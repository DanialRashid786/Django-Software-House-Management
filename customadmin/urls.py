from django.contrib import admin
from django.urls import path,include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    
    path('registerform/', register, name = 'register'),

    path('loginpage/', loginviews, name="loginview"),
    path('logout/', logout_view, name="logout"),

    path('login/admin-dashboard/', admindashboard, name="dashboard"),

   
    path('services/', service, name="service"),
    path('servicesdetail/', servicedetails, name="servicedetails"),


    path('messages/', customermessages, name="messages"),
    path('message/read/<int:message_id>/', mark_message_as_read, name='mark_message_as_read'),

    path('projectrequests/', projectrequests, name="projectrequests"),

    path('delete/<idservice>', delete, name='delete'),

    path('addservice/', add_service, name='addservice'),

    path('edit/<serviceid>', serviceupdate, name='edit'),

    path('editservicedetails/<servicedetailid>', servicedetailsupdate, name='servicedetailupdate'),

    path('status-update/<statusid>', statusupdate, name='status'),




    path('projectmanagers/', projectmanagerspage, name='projectmanagers'),


    path('projectmanagerform/', projectmanagerform, name='projectmanagerform'),

    # path('addprojectmanagersDB/', addprojectmanager, name='addprojectmanager'),

    path("managersdetail/<slug>", managersdetail, name="managersdetail"),

    path('deletemanager/<id>', deletemanager, name='deletemanager'),

    


    path('acceptedprojectlist/', acceptedprojects, name="acceptedprojectlist"),

    path('completedprojectlist/', completeprojects, name="completeprojectlist"),
    

    path('customers/', customertable, name="customertable"),




    path('assign_project/<proposal_id>', assign_project, name='assign_project'),


    # path('change_password/<int:pk>/', change_password, name='change_password'),

    
    path('AllTeamlist/', Teamlist, name="Teamlist"),

    path('managers-attendance/', managerattendance, name = 'managerattendance'),



    path('Careerpage/', Careerpage, name='Careerpage'),
    path("jobdetails/<id>", careersdetail, name="careersdetail"),
    path('deletecareer/<id>', deletecareer, name='deletecareer'),
    path('newcareers/', Addcareers, name='addcareers'),
    path('requestcareer/', careertable, name='requestcareer'),


    path('project/cards/', adminprojectscards, name='adminprojectscards'),




    
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
