from django.db import models
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
# #User = settings.AUTH_USER_MODEL
# class User(AbstractUser):
#     email = models.EmailField(unique=True)


class Audit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=200)
    description = models.TextField()
    entity = models.CharField(max_length=200)
    entity_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Hotline(models.Model):
    type = models.CharField(max_length=250)
    file_path = models.CharField(max_length=250)
    file = models.CharField(max_length=250)
    created_at = models.TimeField(timezone.now())
    modify_at= models.TimeField(timezone.now())
    
    def __str__(self) -> str:
        return self.type
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Automatically create a CallAndWebForm instance
        CallAndWebForm.objects.create(
            hotline=self,
            webform=None,
            type='hotline',
            status=Status.objects.first()
        )

class WebForm(models.Model):
    place_birth = models.CharField(max_length=255)
    nationality = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)
    dob = models.DateField()
    approx_age = models.IntegerField()
    id_type = models.CharField(max_length=255)
    id_number = models.CharField(max_length=255)
    home_address = models.TextField()
    business_name = models.CharField(max_length=255)
    business_address = models.TextField()
    bin_tin = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    conveyance = models.CharField(max_length=255)
    related_name = models.CharField(max_length=255)
    status = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Automatically create a CallAndWebForm instance
        CallAndWebForm.objects.create(
            hotline=None,
            webform=self,
            type='webform',
            status=Status.objects.first()
        )
    
class Status(models.Model):
    name = models.CharField(max_length=250)
    def __str__(self) -> str:
        return self.name
    
class CallAndWebForm(models.Model):
    type  = models.CharField(max_length=250)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modify = models.DateTimeField(auto_now=True)
    hotline = models.ForeignKey(Hotline, on_delete=models.CASCADE, blank=True, null=True)
    webform = models.ForeignKey(WebForm, on_delete=models.CASCADE, blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.type
    def save(self, *args, **kwargs):
        # Ensure status is set to the first Status entry if not already set
        if not self.status_id:
            self.status = Status.objects.first()
        super().save(*args, **kwargs)
        
    
class Agency(models.Model):
    name = models.CharField(max_length=200,null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.name}'
class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name='staff_members')  
    date_joined = models.DateField(auto_now_add=True)
    full_name = models.CharField(max_length=250)
    email = models.EmailField(unique=True)
   

    def __str__(self):
        return self.user.username
    
# @receiver(post_save, sender=User)
# def create_staff_profile(sender, instance, created, **kwargs):
#     if created:
#         # Assuming you have a default agency or can determine it somehow
#         default_agency = Agency.objects.first()  # Replace with your logic to get the appropriate Agency

#         Staff.objects.create(
#             user=instance,
#             agency=default_agency,
#             full_name=instance.get_full_name(),
#             email=instance.email
#         )

class Nationality(models.Model):
    name = models.CharField(max_length=250,default="Timor Leste")
    def __str__(self) -> str:
        return self.name

gender_choice =  (
    ("Male", "Male"),
    ("Female", "Female"),
    ("Indeterminate", "Indeterminate"),
)
     
class Subject(models.Model):
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, default="", blank=True, null=True)
    gender = models.CharField(max_length=13, choices=gender_choice, default="Male",blank=True, null=True)
    pob = models.CharField(max_length=250,default="Dili",blank=True, null=True)
    dob = models.DateField(null=True, blank=True)
    nationality = models.ForeignKey(Nationality, on_delete=models.CASCADE, blank=True, null=True)
    identification = models.CharField(max_length=250,blank=True, null=True)
    Id_number = models.CharField(max_length=250,blank=True, null=True)
    home_add = models.CharField(max_length=250,blank=True, null=True)
    business_name = models.CharField(max_length=200,blank=True, null=True)
    business_address = models.CharField(max_length=200,blank=True, null=True)
    bin_or_tin = models.CharField(max_length=250,blank=True, null=True)
    phone_number = models.CharField(max_length=250,blank=True, null=True)
    description = models.TextField()
    conveyance_description = models.TextField()
    def __str__(self) -> str:
        return f'{self.id}'

choice_source = (
    ("Web Form", "Web Form"),
    ("Hotline", "Hotline"),
    ("Information other", "Information other"),
)

class Intial(models.Model):
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE,null=True, blank=True)
    source = models.CharField(max_length=250, choices=choice_source, default="Web Form")
    information_source = models.TextField(max_length=250, blank=True, null=True)
    
    def __str__(self) -> str:
        return f'{self.source}'
STATUS_CHOICES = (
        ("Incomplete", "Incomplete"),
        ("Completed", "Completed"),
        ("Closed", "Closed"),
        ("Disseminate", "Disseminate"),
        ("Archived", "Archived")
       # ("Disse")
)
       
class Report(models.Model):
    source = models.ForeignKey(CallAndWebForm, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='staff_report')
    Subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=True)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, blank=True, null=True)
    source_information_date = models.DateField(auto_now=True)
    initial= models.ForeignKey(Intial, on_delete=models.CASCADE, null=True, blank=True)
    information_other = models.TextField(max_length=250)
    file_attached = models.ForeignKey('FileAttch', on_delete=models.CASCADE, blank=True, null=True)
    report_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Incomplete")
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)
   
    
    def __str__(self):
        return f"Report by {self.user.username} and the ID is {self.id}"

    def save(self, *args, **kwargs):
        if self.source is None:
            other_source = CallAndWebForm.objects.filter(type='Information Source other').first()
            if other_source:
                self.source = other_source
        super().save(*args, **kwargs)    
 
evaluation = (
    ("A", "Always Reliable"),
    ("B", "Most Reliable"),
    ("C", "Fairly Reliable"),
    ("D", "Not Usual Reliable"),
    ("E", "Unreliable"),
    ("F", "Reliable Cannot be Judge"),
)

information = (
    ("1", "Confirmed by other Source"),
    ("2", "Probably True"),
    ("3", "Possible True"),
    ("4", "Doubtful"),
    ("5", "Improbable Not Confirmed"),
    ("6", "Truth Cannot be Judge"),
)

class TextAttach(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=250)
    information_source = models.CharField(max_length=250, choices=information, default="1")  # Adjusted max_length
    source_evaluation = models.CharField(max_length=250, choices=evaluation, default="A")  # Adjusted max_length
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
   
class FileAttch(models.Model):
    path = models.FileField(upload_to='media')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    metadata = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200)
   
class Comments(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ReportReviewed(models.Model):
    record = models.ForeignKey(Report, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    confirm = models.BooleanField(default=False)
  

    
    
    
    
