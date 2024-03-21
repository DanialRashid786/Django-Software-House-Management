from django.contrib import admin
from django.contrib.admin.sites import site
from customer.models import *
# from customer.models import services

class signupcustomerform(admin.ModelAdmin):
    list_display=('id','user','address','phone','profileimage','is_verified','created_at')

admin.site.register(Customer, signupcustomerform) 


class servicesindex(admin.ModelAdmin):
    list_display=('service_title','service_desc', 'serviceimage','title_slug','display_on_screen','created_at','updated_at')

admin.site.register(services, servicesindex)    



class contactusform(admin.ModelAdmin):
    list_display=('name','email','subject','message')

admin.site.register(contactus, contactusform)   


class requestproject(admin.ModelAdmin):
    list_display=('id','customer_id','customer','servicetype','phone_number','project_title','requirementfile','Project_Budget','assigned_to','Project_Start_Date','Project_Finnish_Date','created_at','updated_at')

admin.site.register(requestform, requestproject)  

admin.site.register(ProjectCompletionDocument)  


class Projectmanagers(admin.ModelAdmin):
    list_display=('id','user_id','user','company','job','country','address','date_created')

admin.site.register(projectmanagers, Projectmanagers) 


class myportfolio(admin.ModelAdmin):
    list_display=('id','data_filter','Image_Title','portfolio_Image')
admin.site.register(portfolio,myportfolio) 

class portfolioDetail(admin.ModelAdmin):
    list_display=('id','Client','Category','ProjectURL', 'Description','projectImage','Projectdate')
admin.site.register(portfolioDetails,portfolioDetail)



class CareerAdmin(admin.ModelAdmin):
    list_display = ('id', 'JobTitle', 'JobDetail', 'JobStatus', 'created_at', 'updated_at')

admin.site.register(Career, CareerAdmin)
admin.site.register(CareerForm)



class requestsession(admin.ModelAdmin):
    list_display=('id','name','Email','phone','city','Comments','created_at','updated_at')
admin.site.register(RequestSession,requestsession) 




class Whatwedosession(admin.ModelAdmin):
    list_display = ('id', 'title', 'display_on_screen', 'created_at', 'updated_at')
    list_filter = ('display_on_screen',)  # Optional: Add filtering options
    search_fields = ('title',)  # Optional: Add search functionality
admin.site.register(Whatwedo,Whatwedosession)


class WhatSetsUsApartAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'display_on_screen', 'created_at', 'updated_at')
    list_filter = ('display_on_screen',)  # Optional: Add filtering options
    search_fields = ('title',)  # Optional: Add search functionality

admin.site.register(WhatSetsUsApart, WhatSetsUsApartAdmin)

class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'display_on_screen', 'created_at', 'updated_at')
    list_filter = ('display_on_screen',)  # Optional: Add filtering options
    search_fields = ('title',)  # Optional: Add search functionality

admin.site.register(AboutUs, AboutUsAdmin)

class OurCoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'section', 'display_on_screen', 'created_at', 'updated_at')
    list_filter = ('display_on_screen',)  # Optional: Add filtering options
    search_fields = ('section',)  # Optional: Add search functionality
admin.site.register(OurCore, OurCoreAdmin)

class OurCultureAdmin(admin.ModelAdmin):
    list_display = ('id', 'Title', 'display_on_screen', 'created_at', 'updated_at')
    list_filter = ('display_on_screen',)  # Optional: Add filtering options
    search_fields = ('Title',)  # Optional: Add search functionality
admin.site.register(OurCulture, OurCultureAdmin)


class TechnologiesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'display_on_screen', 'created_at', 'updated_at')
    list_filter = ('display_on_screen',)  # Optional: Add filtering options
    search_fields = ('title',)  # Optional: Add search functionality

admin.site.register(Technologies, TechnologiesAdmin)



class DataStrategies(admin.ModelAdmin):
    list_display = ('id', 'title', 'display_on_screen', 'created_at', 'updated_at')
admin.site.register(DataUtilizationStrategies,DataStrategies)



class faq(admin.ModelAdmin):
    list_display = ('id', 'question', 'display_on_screen', 'created_at', 'updated_at')
    list_filter = ('display_on_screen',)  # Optional: Add filtering options
    search_fields = ('question',)  # Optional: Add search functionality

admin.site.register(FAQ, faq)
