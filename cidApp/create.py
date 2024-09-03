from django.urls import reverse_lazy
from .lib import *
from django.contrib.auth.models import User,Group
from .forms import *

class UserCreateView(CreateView):
    model = User
    form_class = AdminUserCreationForm
    login_url ='login'
    template_name = 'dashboard/registration/user_form.html'
    success_url = reverse_lazy('user_list')



