from django import forms
from .models import Agency
from django.contrib.auth.models import User as AuthUser

class AgencyForm(forms.ModelForm):
    class Meta:
        model = Agency
        fields =['name']
        
        def __init__(self, *args, **kwargs):
            super(AgencyForm, self).__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs.update({'class': 'form-control'})

# class AddUserForm(forms.Form):
#     user = forms.ModelChoiceField(
#         queryset=CustomUser.objects.all(),
#         required=True,
#         widget=forms.Select(attrs={'class': 'form-control'})
#     )
    
    
# class UserGroupForm(forms.Form):
#     class Meta:
#         model =CustomUser
#         fields = ['name']
#     def __init__(self, *args, **kwargs):
#             super(UserGroupForm, self).__init__(*args, **kwargs)
#             for field_name, field in self.fields.items():
#                 field.widget.attrs.update({'class': 'form-control'})