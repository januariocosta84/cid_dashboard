 
#from msilib.schema import File
from django import forms
# from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User,Group
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .models import Agency, Comments, FileAttch, Intial, Report, Staff, Subject, TextAttach, ReportReviewed
User = get_user_model()
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from admin_two_factor.models import TwoFactorVerification
# from django.contrib.auth.forms import PasswordResetForm,SetPasswordForm
# """User Registration form"""


# # class CreateTwoFactorForms(forms.ModelForm):
# #     class Meta:
# #         model = TwoFactorVerification
# #         fields =['user']

# class ResetPasswordForm(SetPasswordForm):
#     new_password1 = forms.CharField(
#         required=False,
#         widget=forms.PasswordInput,
#         label="New Password One"
#     )
#     new_password2 = forms.CharField(
#         required=False,
#         widget=forms.PasswordInput,
#         label="New Password Confirm One"
#     )
   
#     def clean(self):
#         cleaned_data = super().clean()
#         new_password1 = cleaned_data.get("new_password1")
#         new_password2 = cleaned_data.get("new_password2")

#         if new_password1 and new_password2:
#             if new_password1 != new_password2:
#                 raise forms.ValidationError("The two password fields didn’t match.")
#         return cleaned_data


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100,
                                 required=True,
                                 widget=forms.TextInput(attrs={'placeholder': _('First Name'),
                                                               'class': 'form-control',
                                                               }))
    last_name = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': _('Last Name'),
                                                              'class': 'form-control',
                                                              }))
    # username = forms.CharField(max_length=100,
    #                            required=True,
    #                            widget=forms.TextInput(attrs={'placeholder': 'Username',
    #                                                          'class': 'form-control',
    #                                                          }))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Email',
                                                           'class': 'form-control',
                                                           }))
    #permision = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    #agency = forms.ModelChoiceField(queryset=Agency.objects.all(), required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    

    class Meta:
        model =User
        fields = ['first_name', 'last_name', 'email','password1', 'password2']
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("This email is already taken. Please add another valid Email"))
        return email
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'autofocus': True,
            'placeholder': 'Email',
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': '******',
            'class': 'form-control',
            'data-toggle': 'password',
            'id': 'password',
        })
    )

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
                if not user.check_password(password):
                    raise forms.ValidationError(_('Invalid email or password'))
            except User.DoesNotExist:
                raise forms.ValidationError(_('Invalid email or password'))

        return super().clean()
    
# class CreateRecordsForm(forms.ModelForm):
#     class Meta:
#         model = Subjects
#         exclude = ['created_at', 'updated_at']

#     def __init__(self, *args, **kwargs):
#         super(CreateRecordsForm, self).__init__(*args, **kwargs)
#         for field_name, field in self.fields.items():
#             field.widget.attrs.update({'class': 'form-control'})
        
# class RecordsForm(forms.ModelForm):
#     class Meta:
#         model = Records
#         fields = '__all__'

# class ReferencesForm(forms.ModelForm):
#     class Meta:
#         model = References
#         fields = '__all__'

# class UserEditForm(forms.ModelForm):
#     class Meta:
#         model =Staff
#         fields = [ 'agency']
#     def __init__(self, *args, **kwargs):
#         super(UserEditForm, self).__init__(*args, **kwargs)
#         for field_name, field in self.fields.items():
#             field.widget.attrs.update({'class': 'form-control'})
    
class UserEditForm(forms.ModelForm):
   
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            
class AgencyForm(forms.Form):
   agency = forms.ModelChoiceField(
        queryset=Agency.objects.all(),
         empty_label=_("Select Agency"),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}, )
    )
   empty_field ='Select Agency'
   def __init__(self, *args, **kwargs):
        super(AgencyForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            
class GroupForm(forms.Form):
    groups = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label=_("Select Permision"),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
  
             
class StaffEditForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['agency']  # Add any other fields you want to edit
       
           
    def __init__(self, *args, **kwargs):
        super(StaffEditForm, self).__init__(*args, **kwargs)
        #self.fields['agency'].empty_label = "Select Agency"  # Set the initial option text
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'}) 
                  
class GroupEditForm(forms.Form):
    groups = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    def __init__(self, *args, **kwargs):
        super(GroupEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

            
class InitialForm(forms.ModelForm):
    class Meta:
        model = Intial 
        fields = ['source', 'information_source',]
        
    def __init__(self, *args, **kwargs):
        super(InitialForm, self).__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['information_source'].required = False

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject 
        fields = ('__all__')
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'description_subject': forms.Textarea(attrs={'rows': 4}),
            'cov_description':forms.Textarea(attrs={'rows': 4}),
            'address':forms.Textarea(attrs={'rows': 4}),
            'busaddress':forms.Textarea(attrs={'rows': 4})
                      
        }
    def __init__(self, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            field.required = False

class TextForm(forms.ModelForm):
    class Meta:
        model = TextAttach
        fields = ['text', 'information_source', 'source_evaluation']
        widgets = {
            'information_source': forms.RadioSelect,  # Use RadioSelect widget for cards
            'source_evaluation': forms.RadioSelect,
        }

    def __init__(self, *args, **kwargs):
        super(TextForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class': 'form-control'})
        # Optional: Add custom CSS class for card-style widgets
        self.fields['information_source'].widget.attrs.update({'class': 'card-radio'})
        self.fields['source_evaluation'].widget.attrs.update({'class': 'card-radio'})

             
class FileForm(forms.ModelForm):
    class Meta:
        model = FileAttch
        fields =['path']
    def __init__(self, *args, **kwargs):
        super(FileForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            field.required = False
            
class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = [
            'source',
            'user',
            'subject',
            'agency',
            #'source_information_date',
            'information_other',
            'report_by'
        ]
        widgets = {
           # 'source_information_date': forms.DateInput(attrs={'type': 'date'}),
            'information_other': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields =['comment']
    def __init__(self, *args, **kwargs):
        
        super(CommentForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReportReviewed
        fields = ['confirm']
        widgets = {
            'confirm': forms.CheckboxInput(attrs={
                'class': 'custom-control-input',
                'id': 'customSwitch1'  # 
            }),
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['confirm'].label = ''  # Optional: Remove default label
