 
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User,Group
from .models import Records, Subjects, References
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm


from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

"""User Registration form"""
class RegisterForm(UserCreationForm):
    # fields we want to include and customize in our form
    first_name = forms.CharField(max_length=100,
                                 required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name',
                                                               'class': 'form-control',
                                                               }))
    last_name = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name',
                                                              'class': 'form-control',
                                                              }))
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Email',
                                                           'class': 'form-control',
                                                           }))
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
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


"""Login Form"""
class LoginForm(AuthenticationForm):
   username = forms.CharField(widget=forms.TextInput(attrs={'autofocus':True, 'placeholder':'Naran Utilizador ', 'class':'form-control'}))
   password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'********'}))


class CreateRecordsForm(forms.ModelForm):
    class Meta:
        model = Subjects
        exclude = ['created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super(CreateRecordsForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        
class RecordsForm(forms.ModelForm):
    class Meta:
        model = Records
        fields = '__all__'

class ReferencesForm(forms.ModelForm):
    class Meta:
        model = References
        fields = '__all__'

# class CombinedForm(forms.Form):
#     # Fields from Records
#     user = forms.ModelChoiceField(queryset=YourUserModel.objects.all())  # Replace YourUserModel with your actual User model
#     department = forms.ModelChoiceField(queryset=References.objects.filter(ref_type='department'), required=False)
#     information_source = forms.ModelChoiceField(queryset=References.objects.filter(ref_type='information_source'))
#     subject = forms.ModelChoiceField(queryset=Subjects.objects.all(), required=False)  # Replace Subjects with your actual Subject model
#     records_source = forms.ModelChoiceField(queryset=RecordsSource.objects.all(), required=False)  # Replace RecordsSource with your actual RecordsSource model
#     information_source_other = forms.CharField(widget=forms.Textarea, required=False)
#     description = forms.CharField(widget=forms.Textarea, required=False)
#     comment = forms.CharField(widget=forms.Textarea, required=False)
#     created_at = forms.DateTimeField(required=False)
#     updated_at = forms.DateTimeField(required=False)
#     status = forms.ModelChoiceField(queryset=References.objects.filter(ref_type='status'))

#     # Fields from References
#     parent = forms.ModelChoiceField(queryset=References.objects.all(), required=False)
#     ref_type = forms.CharField(max_length=200)
#     code = forms.CharField(max_length=50)
#     name = forms.CharField(max_length=200)
#     description = forms.CharField(widget=forms.Textarea, required=False)
#     order = forms.IntegerField(required=False)
#     created_at = forms.DateTimeField(required=False)
#     updated_at = forms.DateTimeField(required=False)