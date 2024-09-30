import base64
import os
from django.db import models
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
import pyotp

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
    created_at = models.DateTimeField(default=timezone.now)
    modify_at = models.DateTimeField(default=timezone.now)
    origin_date = models.DateTimeField(blank=True, null=True)

    
    def __str__(self) -> str:
        return self.type
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        CallAndWebForm.objects.create(
            hotline=self,
            webform=None,
            type='hotline',
            status=Status.objects.first()
        )

class WebForm(models.Model):
     # Personal information
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    middle_name = models.CharField(max_length=250, blank=True, null=True)
    nick_name = models.CharField(max_length=250, blank=True, null=True)
    description_subject = models.CharField(max_length=250, blank=True, null=True)
    business_name = models.CharField(max_length=100, blank=True, null=True)
    
    # Contact information
    address = models.CharField(max_length=250, blank=True, null=True)
    post_code = models.CharField(max_length=250, blank=True, null=True)
    country = models.CharField(max_length=250, blank=True, null=True)
    phone_num = models.CharField(max_length=250, blank=True, null=True)
    
    # Transportation information
    vehicle = models.CharField(max_length=250, blank=True, null=True)
    routing = models.CharField(max_length=250, blank=True, null=True)
    ferry = models.CharField(max_length=250, blank=True, null=True)
    vessel = models.CharField(max_length=250, blank=True, null=True)
    cargo = models.CharField(max_length=250, blank=True, null=True)
    other_trans = models.CharField(max_length=250, blank=True, null=True)
    
    # Personal details
    approx_age = models.IntegerField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=250, blank=True, null=True)
    
    # Event details
    any_other = models.CharField(max_length=250, blank=True, null=True)
    what = models.CharField(max_length=250, blank=True, null=True)
    location = models.CharField(max_length=250, blank=True, null=True)
    quando = models.DateField(blank=True, null=True)
    how_happen = models.CharField(max_length=250, blank=True, null=True)
    how_long = models.IntegerField(blank=True, null=True)
    
    # Additional information
    other_infor = models.CharField(max_length=250, blank=True, null=True)
    your_connection = models.CharField(max_length=250, blank=True, null=True)
    still_connect = models.CharField(max_length=250, blank=True, null=True)
    
    # Involvement details
    how_did = models.CharField(max_length=250, blank=True, null=True)
    others_know_information = models.BooleanField(default=False, blank=True, null=True)
    how_many = models.IntegerField(blank=True, null=True)
    affect_information = models.BooleanField(default=False, blank=True, null=True)
    
    # Anonymous details
    if_yes = models.CharField(max_length=250, blank=True, null=True)
    prefer_anonymous = models.BooleanField(default=False, blank=True, null=True)
    an_first_name = models.CharField(max_length=250, blank=True, null=True)
    an_last_name = models.CharField(max_length=250, blank=True, null=True)
    an_middle_name = models.CharField(max_length=250, blank=True, null=True)
    an_phone_number = models.CharField(max_length=250, blank=True, null=True)
    an_email = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    # Call preference
    ligar = models.BooleanField(blank=True, null=True)
    
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

gender_choice = (
    (_("Male"), _("Male")),
    (_("Female"), _("Female")),
    (_("Indeterminate"), _("Indeterminate")),
)
     
class Subject(models.Model):
       # Personal information
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    gender = models.CharField(max_length=13,choices=gender_choice, default="Male")
    nationality = models.CharField(max_length=250, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    pob = models.CharField(max_length=250, blank=True, null=True)
    identification = models.CharField(max_length=250, blank=True, null=True)
    idNumber = models.CharField(max_length=250, blank=True,null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
   # middle_name = models.CharField(max_length=250, blank=True, null=True)
   # nick_name = models.CharField(max_length=250, blank=True, null=True)
    business_name = models.CharField(max_length=100, blank=True, null=True)
    # Contact information
    busaddress = models.CharField(max_length=250, null=True,blank=True)
    bin_tin = models.CharField(max_length=250, null=True, blank=True)
    phone_num = models.CharField(max_length=250, blank=True, null=True)
    description_subject = models.CharField(max_length=250, blank=True, null=True)
    post_code = models.CharField(max_length=250, blank=True, null=True)
    country = models.CharField(max_length=250, blank=True, null=True)
    coveyance = models.CharField(max_length=250, blank=True,null=True)
    cov_description = models.CharField(max_length=250, blank=True, null=True)
    # # Transportation information
    # vehicle = models.CharField(max_length=250, blank=True, null=True)
    # routing = models.CharField(max_length=250, blank=True, null=True)
    # ferry = models.CharField(max_length=250, blank=True, null=True)
    # vessel = models.CharField(max_length=250, blank=True, null=True)
    # cargo = models.CharField(max_length=250, blank=True, null=True)
    # other_trans = models.CharField(max_length=250, blank=True, null=True)
    
    # # Personal details
    # approx_age = models.IntegerField(blank=True, null=True)
    
    
    
    # # Event details
    # any_other = models.CharField(max_length=250, blank=True, null=True)
    # what = models.CharField(max_length=250, blank=True, null=True)
    # location = models.CharField(max_length=250, blank=True, null=True)
    # quando = models.DateField(blank=True, null=True)
    # how_happen = models.CharField(max_length=250, blank=True, null=True)
    # how_long = models.IntegerField(blank=True, null=True)
    
    # # Additional information
    # other_infor = models.CharField(max_length=250, blank=True, null=True)
    # your_connection = models.CharField(max_length=250, blank=True, null=True)
    # still_connect = models.CharField(max_length=250, blank=True, null=True)
    
    # # Involvement details
    # how_did = models.CharField(max_length=250, blank=True, null=True)
    # others_know_information = models.BooleanField(default=False, blank=True, null=True)
    # how_many = models.IntegerField(blank=True, null=True)
    # affect_information = models.BooleanField(default=False, blank=True, null=True)
    
    # # Anonymous details
    # if_yes = models.CharField(max_length=250, blank=True, null=True)
    # prefer_anonymous = models.BooleanField(default=False, blank=True, null=True)
    # an_first_name = models.CharField(max_length=250, blank=True, null=True)
    # an_last_name = models.CharField(max_length=250, blank=True, null=True)
    # an_middle_name = models.CharField(max_length=250, blank=True, null=True)
    # an_phone_number = models.CharField(max_length=250, blank=True, null=True)
    # an_email = models.CharField(max_length=250, blank=True, null=True)
    
    # # Call preference
    # ligar = models.BooleanField(blank=True, null=True)
    
    # # Created date
    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name or "Subject"


choice_source = (
    ("Web Form", _("Web Form")),
    ("Hotline", _("Hotline")),
    ("Information other", _("Information other")),
)

class Intial(models.Model):
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE,null=True, blank=True)
    source = models.CharField(max_length=250, choices=choice_source, default="Web Form")
    information_source = models.TextField(max_length=250, blank=True, null=True)
    
    def __str__(self) -> str:
        return f'{self.source}'
STATUS_CHOICES = (
        ("Incomplete", _("Incomplete")),
        ("Completed", _("Completed")),
        ("Closed", _("Closed")),
        ("Disseminate", _("Disseminate")),
        ("Archived", _("Archived"))
       # ("Disse")
)
       
class Report(models.Model):
    source = models.ForeignKey(CallAndWebForm, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='staff_report')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=True, null=True, default=None, related_name='subject_report')
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
    ("A", _("Always Reliable")),
    ("B", _("Most Reliable")),
    ("C", _("Fairly Reliable")),
    ("D", _("Not Usual Reliable")),
    ("E", _("Unreliable")),
    ("F", _("Reliable Cannot be Judge")),
)

information = (
    ("1", _("Confirmed by other Source")),
    ("2", _("Probably True")),
    ("3", _("Possible True")),
    ("4", _("Doubtful")),
    ("5", _("Improbable Not Confirmed")),
    ("6", _("Truth Cannot be Judge")),
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
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ReportReviewed(models.Model):
    record = models.ForeignKey(Report, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    confirm = models.BooleanField(default=False)
  

####MFA user model

class UserMFA(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mfa', blank=True, null=True)
    is_mfa_enabled = models.BooleanField(default=False)
    secret_key = models.CharField(max_length=16, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.secret_key:
            self.secret_key = base64.b32encode(os.urandom(10)).decode('utf-8')
        super().save(*args, **kwargs)

    def get_totp_uri(self):
        return f'otpauth://totp/cid:{self.user.username}?secret={self.secret_key}&issuer=cidApp'

    def verify_token(self, token):
        totp = pyotp.TOTP(self.secret_key)
        return totp.verify(token)   
    
    
@receiver(post_save, sender=User)
def create_user_mfa(sender, instance, created, **kwargs):
    if created:
        UserMFA.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_mfa(sender, instance, **kwargs):
    instance.mfa.save()