from django.urls import path,include
from .import views
from django.conf import settings
from django.conf.urls.static import static
from .views import *


urlpatterns = [

    path('customeraccount/', accountSettings, name="accountcustomer"),
    
    path('customerlogout/', customerlogout_view, name='customerlogout'),


    path('',views.home, name='homepage'),
    path("formsubmit/",views.contactfrom, name="contactfrom"),


    path("servicepage/",views.servicepage, name="servicepage"),
    path("servicedetail/<slug>",views.servicedetail, name="servicedetail"),
    path("perposalform/<pid>/<sname>",views.perposalrequest, name="perposalrequest"),

    path("career/",views.career_job, name="career"),
    path("careerdetails/<id>",views.career_details, name="career-details-page"),
    path("careerdetails/<int:id>/jobform/",views.job_proposal_request, name="jobrequest"),
    

    
    path("aboutus/",views.aboutus, name="aboutus"),

    path('portfoliodetails/<pid>', portfoliodetails, name='portfoliodetails'),
   
    
    path("projectlist/",views.project_list, name="projectlist"),
    

    
    path('technologies/', views.technologies, name="technology"),
    path('Our Mission-vision-values/', views.ourmission, name="ourmission"),


    path('OurWorkingCulture/', views.workingculture, name="workingculture"),

    path('whatwedo/', views.whatwedo, name="whatwedo"),


    

]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)