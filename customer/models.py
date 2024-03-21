from datetime import datetime, date
import os
from django.db import models
from tinymce.models import HTMLField
from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.db.models.signals import pre_save
from django.core.exceptions import ValidationError

from SHMS import settings
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _


def delete_image(sender, instance, image_field, **kwargs):
    # Remove file from the storage
    image = instance.__getattribute__(image_field)
    if image and os.path.isfile(image.path):
        os.remove(image.path)

def delete_previous_image(sender, instance, old_image_field, **kwargs):
    if not instance.pk:
        return False

    try:
        old_image = sender.objects.get(pk=instance.pk).__getattribute__(old_image_field)
    except sender.DoesNotExist:
        old_image = None

    new_image = instance.__getattribute__(old_image_field)
    if old_image and old_image != new_image and os.path.isfile(old_image.path):
        os.remove(old_image.path)

    return True





class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address=models.CharField(max_length=50,null=True, blank=True)
    phone=models.CharField(max_length=50,null=True, blank=True)
    profileimage = models.ImageField(upload_to='customers/',max_length=200,blank=True ,null=True)

    auth_token = models.CharField(max_length=100 )
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.user.username
    
    def change_password(self, new_password):
        self.user.set_password(new_password)
        self.user.save()


@receiver(pre_delete, sender=Customer)
def delete_customer_image(sender, instance, **kwargs):
    delete_image(sender, instance, 'profileimage', **kwargs)

@receiver(pre_save, sender=Customer)
def delete_previous_customer_image(sender, instance, **kwargs):
    return delete_previous_image(sender, instance, 'profileimage', **kwargs)


# ****************************************************************************************


# Create your models here.
class projectmanagers(models.Model):
    user=models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    id=models.BigAutoField(primary_key=True)
    profileimage = models.ImageField(upload_to='projectmanagers/',max_length=200,blank=True ,null=True)
    about=HTMLField()
    company=models.CharField(max_length=100)
    job=models.CharField(max_length=50)
    country=models.CharField(max_length=50)
    address=models.CharField(max_length=100)
    phone=models.CharField(max_length=12)
    TwitterProfile = models.URLField(max_length = 200)
    FacebookProfile = models.URLField(max_length = 200)
    InstagramProfile = models.URLField(max_length = 200)
    LinkedinProfile = models.URLField(max_length = 200)
    date_created=models.DateTimeField(auto_now_add=True,null=True)
    # updated_at = models.DateTimeField(auto_now=True)
    
    # Job_slug = AutoSlugField(populate_from='user',unique=True,null=True,)
    def __str__(self):
        return f"{self.user.username}  ( {self.job} )"
    

@receiver(pre_delete, sender=projectmanagers)
def delete_customer_image(sender, instance, **kwargs):
    delete_image(sender, instance, 'profileimage', **kwargs)

@receiver(pre_save, sender=projectmanagers)
def delete_previous_customer_image(sender, instance, **kwargs):
    return delete_previous_image(sender, instance, 'profileimage', **kwargs)




# ************************************************
# Create your models here.
class services(models.Model):
    id=models.BigAutoField(primary_key=True)
    service_title=models.CharField(max_length=50)
    service_desc=models.TextField()
    serviceimage = models.ImageField(upload_to='services/',max_length=200,blank=True ,null=True,default=None)

    servicedetail_desc=models.TextField()
    image_desc = models.ImageField(upload_to='servicedetails/',max_length=200,blank=True ,null=True,default=None)
    Sited_Services_title=models.CharField(max_length=50,default='no data')
    SitedServices=models.JSONField()
    
    image_Sited_Services = models.ImageField(upload_to='servicedetails/',max_length=200,blank=True ,null=True,default=None)

    title_slug = AutoSlugField(populate_from='service_title',unique=True,null=True,)

    display_on_screen = models.BooleanField(default=True)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.service_title

#*****************************************************
@receiver(pre_delete, sender=services)
def delete_customer_image(sender, instance, **kwargs):
    delete_image(sender, instance, 'serviceimage', **kwargs)

@receiver(pre_delete, sender=services)
def delete_customer_image(sender, instance, **kwargs):
    delete_image(sender, instance, 'image_desc', **kwargs)
    
@receiver(pre_delete, sender=services)
def delete_customer_image(sender, instance, **kwargs):
    delete_image(sender, instance, 'image_Sited_Services', **kwargs)


@receiver(pre_save, sender=services)
def delete_previous_customer_image(sender, instance, **kwargs):
    return delete_previous_image(sender, instance, 'serviceimage', **kwargs) 

@receiver(pre_save, sender=services)
def delete_previous_customer_image(sender, instance, **kwargs):
    return delete_previous_image(sender, instance, 'image_desc', **kwargs)

@receiver(pre_save, sender=services)
def delete_previous_customer_image(sender, instance, **kwargs):
    return delete_previous_image(sender, instance, 'image_Sited_Services', **kwargs)                   
# ****************************************************





class requestform(models.Model):
    STATUS=(
        ('Rejected','Rejected'),
        ('Accepted','Accepted'),
        ('Pending','Pending'),
    )
    pstatus=(
        ('Delivered','Delivered'),
        ('In Progress','In Progress'),
        ('Complete','Complete')
    )

    payment=(
        ('Paid','Paid'),
        ('UnPaid','Unpaid'),
    )
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    servicetype=models.ForeignKey(services,on_delete=models.PROTECT)
    phone_number=models.IntegerField()
    project_title=models.CharField(max_length=50)
    requirementfile=models.FileField(upload_to='requirement_Doc/',max_length=200,validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx'])])
    Project_Budget=models.DecimalField(max_digits=10, decimal_places=2)

    Project_Start_Date = models.DateField(blank=True,null=True)
    Project_Finnish_Date = models.DateField(blank=True,null=True)

    assigned_to = models.ForeignKey(projectmanagers, on_delete=models.PROTECT, related_name='assigned_projects', null=True, blank=True)
   
    ShortDesc=models.TextField(null=True, blank=True)

    created_at=models.DateField(auto_now_add=True, auto_now=False,blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    status=models.CharField(max_length=200,null=True,choices=STATUS,default='Pending')

    projectstatus=models.CharField(max_length=200,null=True,choices=pstatus,default='In Progress')

    paymentstatus=models.CharField(max_length=200,null=True,choices=payment,default='Unpaid')

    payment_transaction_id = models.CharField(max_length=255, null=True, blank=True)
    
    def clean(self):
        super().clean()

        if self.Project_Start_Date and self.Project_Finnish_Date:
            if self.Project_Finnish_Date < self.Project_Start_Date:
                raise ValidationError("Project finish date cannot be earlier than project start date.")
    def get_file_size(self):
        return f'{os.path.getsize(self.requirementfile.path) / (1024 * 1024):.2f} MB'
    
    def __str__(self):
        return self.project_title
    def save(self, *args, **kwargs):
    # Define the maximum word limit for ShortDesc field
        max_word_limit = 50  # Adjust this value according to your requirements

        # Check if ShortDesc is not None before splitting
        if self.ShortDesc:
            # Truncate the description if it exceeds the word limit
            words = self.ShortDesc.split()
            truncated_description = ' '.join(words[:max_word_limit])

            self.ShortDesc = truncated_description

        super(requestform, self).save(*args, **kwargs)
    


@receiver(pre_delete, sender=requestform)
def delete_customer_image(sender, instance, **kwargs):
    delete_image(sender, instance, 'requirementfile', **kwargs)

@receiver(pre_save, sender=requestform)
def delete_previous_customer_image(sender, instance, **kwargs):
    return delete_previous_image(sender, instance, 'requirementfile', **kwargs)




class ProjectCompletionDocument(models.Model):
    project = models.ForeignKey(requestform, on_delete=models.CASCADE,related_name='documents')
    document = models.FileField(upload_to='completion_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def get_file_size(self):
        return f'{os.path.getsize(self.document.path) / (1024 * 1024):.2f} MB'
    
    def __str__(self):
        return self.project.project_title
  
@receiver(pre_delete, sender=ProjectCompletionDocument)
def delete_customer_image(sender, instance, **kwargs):
    delete_image(sender, instance, 'document', **kwargs)

@receiver(pre_save, sender=ProjectCompletionDocument)
def delete_previous_customer_image(sender, instance, **kwargs):
    return delete_previous_image(sender, instance, 'document', **kwargs)




class contactus(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=254)
    subject=models.CharField(max_length=50)
    message=HTMLField()
    is_read = models.BooleanField(default=False) 
    created_at=models.DateField(auto_now_add=True, auto_now=False,blank=True)
   

    def __str__(self):
        return self.subject
    





    # ///////////////////////////////Portfolio Section///////////////////////////

portfolioType=[
    ('filter-Business','Business Intelligence'),
    ('filter-Research','Research Consultancy'),
    ('filter-AI','Artificial Intelligence'),    
]
class portfolio(models.Model):  
    data_filter = models.CharField(choices=portfolioType, max_length=50)
    Image_Title=models.CharField(max_length=50,help_text="Enter your image Title")
    portfolio_Image = models.ImageField(upload_to='portfolio/',max_length=200)

    def __str__(self):
            return self.Image_Title

@receiver(pre_delete, sender=portfolio)
def delete_customer_image(sender, instance, **kwargs):
    delete_image(sender, instance, 'portfolio_Image', **kwargs)

@receiver(pre_save, sender=portfolio)
def delete_previous_customer_image(sender, instance, **kwargs):
    return delete_previous_image(sender, instance, 'portfolio_Image', **kwargs)



class portfolioDetails(models.Model):
    portfolio=models.OneToOneField(portfolio,on_delete=models.CASCADE)
    Category=models.CharField(max_length=50,help_text="Enter Project Category")
    Client=models.CharField(max_length=50)
    Projectdate =models.DateField()
    ProjectURL = models.URLField(max_length=200,default="www.example.com")
    Description=models.TextField(help_text="Portfolio Details",default="Write portfolio Details")
    projectImage = models.ImageField(upload_to='portfolioDetails/',max_length=200)

    def __str__(self):
            return self.Category

@receiver(pre_delete, sender=portfolioDetails)
def delete_customer_image(sender, instance, **kwargs):
    delete_image(sender, instance, 'projectImage', **kwargs)

@receiver(pre_save, sender=portfolioDetails)
def delete_previous_customer_image(sender, instance, **kwargs):
    return delete_previous_image(sender, instance, 'projectImage', **kwargs)




class Career(models.Model):
    JOB_STATUS_CHOICES = (
        ('Open', 'Open'),
        ('Closed', 'Closed')
    )

    JobTitle = models.CharField(max_length=50, help_text="Web Development")
    JobDetail = models.CharField(max_length=150, help_text="Permanent | Islamabad | Software / IT Engineer")
    JobStatus = models.CharField(max_length=10, choices=JOB_STATUS_CHOICES, default='Open')

    JobDescription = models.TextField(help_text="Short Job Description")
    JobDescriptionImage = models.ImageField(upload_to='career/', max_length=200)

    Responsibilities = models.TextField(default="['a', 'b']")
    ResponsibilitiesImage = models.ImageField(upload_to='career/', max_length=200)

    Requirements = models.TextField(default="['a', 'b']")
    MinimumExperience = models.CharField(max_length=50, help_text="1 Year")
    JobCategory = models.CharField(max_length=50, help_text="Web Developer")
    Department = models.CharField(max_length=50, help_text="Backend Development")
    JobType = models.CharField(max_length=50, help_text="Permanent")
    Location = models.CharField(max_length=100, help_text="Comsats University Sahiwal")
    
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.JobTitle


@receiver(pre_delete, sender=Career)
def delete_customer_image(sender, instance, **kwargs):
    delete_image(sender, instance, 'JobDescriptionImage', **kwargs)

@receiver(pre_save, sender=Career)
def delete_previous_customer_image(sender, instance, **kwargs):
    return delete_previous_image(sender, instance, 'JobDescriptionImage', **kwargs)




class CareerForm(models.Model):
    STATUS_CHOICES = (
        ('In Process', 'In Process'),
        ('Rejected', 'Rejected'),
        ('Accepted', 'Accepted')
    )
    JobTitle = models.ForeignKey(Career, on_delete=models.CASCADE, related_name='job_applications')
    Name = models.CharField(max_length=50)
    Email = models.EmailField()
    Phone_number = models.CharField(max_length=12)
    About = models.TextField()
    
    CV = models.FileField(
        upload_to='jobcv/',
        max_length=200,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])]
    )

    RequestStatus = models.CharField(max_length=12, choices=STATUS_CHOICES, default='In Process')

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Name

    def get_file_size(self):
        return f'{os.path.getsize(self.CV.path) / (1024 * 1024):.2f} MB'
    
    def clean(self):
        # Custom validation to check if the email is unique for the given JobTitle
        existing_applications = CareerForm.objects.filter(JobTitle=self.JobTitle, Email=self.Email)
        if self.pk is None:
            # If the form is being saved as a new instance
            if existing_applications.exists():
                raise ValidationError('You have already applied with this email for this job.')
        else:
            # If the form is being updated, make sure the email is still unique
            if existing_applications.exclude(pk=self.pk).exists():
                raise ValidationError('You have already applied with this email for this job.')
            

@receiver(pre_delete, sender=CareerForm)
def delete_customer_image(sender, instance, **kwargs):
    delete_image(sender, instance, 'CV', **kwargs)

@receiver(pre_save, sender=CareerForm)
def delete_previous_customer_image(sender, instance, **kwargs):
    return delete_previous_image(sender, instance, 'CV', **kwargs)





class RequestSession(models.Model):
    name = models.CharField(max_length=30)
    Email = models.EmailField()
    phone=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    Comments=models.TextField()

    
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return self.name
    


# ///////////////What we do//////////////////
class Whatwedo(models.Model):
    title = models.CharField(max_length=50)
    icon_image = models.ImageField(upload_to='Whatwedo_icons/')
    description = models.TextField(max_length=280)

    display_on_screen = models.BooleanField(default=True)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
@receiver(pre_delete, sender=Whatwedo)
def delete_customer_image(sender, instance, **kwargs):
    delete_image(sender, instance, 'icon_image', **kwargs)

@receiver(pre_save, sender=Whatwedo)
def delete_previous_customer_image(sender, instance, **kwargs):
    return delete_previous_image(sender, instance, 'icon_image', **kwargs)

# ///////What Sets Us Apart//////////

class WhatSetsUsApart(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='WhatSetsUsApart/')
    description = models.TextField(max_length=430)

    display_on_screen = models.BooleanField(default=True)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

@receiver(pre_delete, sender=WhatSetsUsApart)
def delete_customer_image(sender, instance, **kwargs):
    delete_image(sender, instance, 'image', **kwargs)

@receiver(pre_save, sender=WhatSetsUsApart)
def delete_previous_customer_image(sender, instance, **kwargs):
    return delete_previous_image(sender, instance, 'image', **kwargs)



#////////////about us////////////

class AboutUs(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=600)
    sentences = models.JSONField()
    image = models.ImageField(upload_to='about_images/')

    display_on_screen = models.BooleanField(default=True)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

@receiver(pre_delete, sender=AboutUs)
def delete_customer_image(sender, instance, **kwargs):
    delete_image(sender, instance, 'image', **kwargs)

@receiver(pre_save, sender=AboutUs)
def delete_previous_customer_image(sender, instance, **kwargs):
    return delete_previous_image(sender, instance, 'image', **kwargs)


class OurCore(models.Model):
    section = models.CharField(max_length=50,default="MISSION, VISION, AND VALUES")

    MissionTitle = models.CharField(max_length=100,default="Our Mission")
    MissionImage = models.ImageField(upload_to='OurCore/')
    MissionContent = models.TextField(max_length=400)

    VisionTitle = models.CharField(max_length=100,default="Our Vision")
    VisionImage = models.ImageField(upload_to='OurCore/')
    VisionContent = models.TextField(max_length=400)


    ValuesTitle = models.CharField(max_length=100,default="Our Values")
    ValuesImage = models.ImageField(upload_to='OurCore/')
    ValuesContent = models.JSONField()


    display_on_screen = models.BooleanField(default=True)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.section
    

@receiver(pre_delete, sender=OurCore)
def delete_customer_image(sender, instance, **kwargs):
    delete_image(sender, instance, 'MissionImage', **kwargs)

@receiver(pre_delete, sender=OurCore)
def delete_customer_image(sender, instance, **kwargs):
    delete_image(sender, instance, 'VisionImage', **kwargs)

@receiver(pre_delete, sender=OurCore)
def delete_customer_image(sender, instance, **kwargs):
    delete_image(sender, instance, 'ValuesImage', **kwargs)

@receiver(pre_save, sender=OurCore)
def delete_previous_customer_image(sender, instance, **kwargs):
    return delete_previous_image(sender, instance, 'MissionImage', **kwargs)

@receiver(pre_save, sender=OurCore)
def delete_previous_customer_image(sender, instance, **kwargs):
    return delete_previous_image(sender, instance, 'VisionImage', **kwargs)

@receiver(pre_save, sender=OurCore)
def delete_previous_customer_image(sender, instance, **kwargs):
    return delete_previous_image(sender, instance, 'ValuesImage', **kwargs)


class OurCulture(models.Model):
   
    Title = models.CharField(max_length=50)
    Content = models.TextField(max_length=600)
    Image = models.ImageField(upload_to='OurCulture/')

    display_on_screen = models.BooleanField(default=True)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Title

@receiver(pre_delete, sender=OurCulture)
def delete_customer_image(sender, instance, **kwargs):
    delete_image(sender, instance, 'Image', **kwargs)

@receiver(pre_save, sender=OurCulture)
def delete_previous_customer_image(sender, instance, **kwargs):
    return delete_previous_image(sender, instance, 'Image', **kwargs)    


class Technologies(models.Model):
    title = models.CharField(max_length=100)
    image_url = models.URLField()
    description = models.TextField(max_length=500)

    Site_url=models.URLField(null=True,blank=True)


    display_on_screen = models.BooleanField(default=True)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    


class DataUtilizationStrategies(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField(max_length=600)
    Image = models.ImageField(upload_to='DataUtilization/')

    display_on_screen = models.BooleanField(default=True)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
@receiver(pre_delete, sender=DataUtilizationStrategies)
def delete_customer_image(sender, instance, **kwargs):
    delete_image(sender, instance, 'Image', **kwargs)

@receiver(pre_save, sender=DataUtilizationStrategies)
def delete_previous_customer_image(sender, instance, **kwargs):
    return delete_previous_image(sender, instance, 'Image', **kwargs)  



class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = HTMLField()

    display_on_screen = models.BooleanField(default=True)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question