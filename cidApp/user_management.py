from django.shortcuts import get_object_or_404, redirect, render, resolve_url
from django.views import View
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _

from cidApp.decorator_costum import GroupRequiredMixin
from cidApp.forms import(
    AgencyForm, GroupEditForm, GroupForm, LoginForm, RegisterForm, StaffEditForm, User, UserEditForm,
) 
from django.contrib.auth.forms import PasswordResetForm,SetPasswordForm
from cidApp.models import Agency, Staff

"""User Create"""
class RegisterUsers(LoginRequiredMixin, View):
    form_class = RegisterForm
    group_regist = GroupForm
    staff_regist = AgencyForm
    template_name = 'users/register.html'
    initial = {'key': 'value'}

    def get_context_data(self, **kwargs):
        context = {}
        context['users'] = User.objects.all()
        user_group = self.request.user.groups.values_list('name', flat=True)
        context['user_group'] = list(user_group)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['id'] = request.user.id
        form = self.form_class(initial=self.initial)
        groups_form = self.group_regist()
        staff_form = self.staff_regist()

        context['form'] = form
        context['groups_form'] = groups_form
        context['staff_form'] = staff_form

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        groups_form = self.group_regist(request.POST)
        staff_form = self.staff_regist(request.POST)
        if form.is_valid() and groups_form.is_valid() and staff_form.is_valid():
            user = form.save(commit=False)
            user.save()

            # Assign group to user
            group = groups_form.cleaned_data['groups']
            user.groups.add(group)
            
            #Assign Agency to user
            agency = staff_form.cleaned_data['agency']
            email= form.cleaned_data['email']
            first_name = form.cleaned_data['first_name'] 
            last_name = form.cleaned_data['last_name'] 
            full_name =f'{first_name} {last_name}'
            Staff.objects.create(
            user=user,
            agency= agency,
            full_name=full_name,
            email=email
             )

            username = form.cleaned_data.get('username')
            messages.success(request, _('Account created for {username}'))
            return redirect('user-list')

        context = self.get_context_data(**kwargs)
        context['form'] = form
        context['groups_form'] = groups_form
        context['staff_form'] = staff_form
        context['id'] =request.user.id
        return render(request, self.template_name, context)
    
"""User EDIT"""
class EditUserView(GroupRequiredMixin, View):
    group_names = ['administrator']  
    def get(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        print("user id",user.id)
        staff = get_object_or_404(Staff, user=user)
        user_edit_form = UserEditForm(instance=user)
        staff_edit_form = StaffEditForm(instance=staff)
        form = SetPasswordForm(user)
        #user_groups = user.groups.all()  # Fetch the user's groups
        id = request.user.id
        user_group = self.request.user.groups.values_list('name', flat=True)
        return render(request, 'users/reset_password.html', {
            'form': form,
            'user_edit_form': user_edit_form,
            'staff_edit_form': staff_edit_form,
            'user': user,
            'user_group': list(user_group),
            'id': user.id
        })

    def post(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        staff = get_object_or_404(Staff, user=user)
        user_edit_form = UserEditForm(request.POST, instance=user)
        staff_edit_form = StaffEditForm(request.POST, instance=staff)
        password_change_requested = 'new_password1' in request.POST and 'new_password2' in request.POST and request.POST['new_password1'] and request.POST['new_password2']
        form = SetPasswordForm(user, request.POST) if password_change_requested else None

        if user_edit_form.is_valid() and staff_edit_form.is_valid() and (not password_change_requested or (form and form.is_valid())):
            user_edit_form.save()
            staff_edit_form.save()
            if password_change_requested:
                form.save()
            
            messages.success(request, _("User information has been updated"))
            return redirect('user-list')
        
        user_groups = user.groups.all()  # Fetch the user's groups
        return render(request, 'users/reset_password.html', {
            'form': form,
            'user_edit_form': user_edit_form,
            'staff_edit_form': staff_edit_form,
            'user': user,
            'user_group': user_groups,
            'id': user.id
        })
        
class Login_View(LoginView):
    form_class = LoginForm
    template_name = 'dashproject/account/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(resolve_url('/'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Check if the user has MFA enabled after successful password authentication
        user = form.get_user()
        print("KOKO atu hare saida mak mosu iha ne",user)
        
        if user.mfa.is_mfa_enabled:
            # Store the user ID in the session temporarily until MFA is verified
            self.request.session['mfa_user_id'] = user.id
            
            # Redirect to the MFA verification page
            return redirect('verify-mfa')  # This should point to your MFA verification view URL

        # No MFA, proceed to normal success URL
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Hei: {self.request.user.first_name} You are successfully logged in"))
        return resolve_url('/')
    
    def form_invalid(self, form):
        messages.error(self.request, _("Warning: UNAUTHORIZED ACCESS TO THIS SYSTEM MAY CONSTITUTE A CRIMINAL OFFENCE."))
        return super().form_invalid(form)
          
# class Login_View(LoginView):
#     form_class = LoginForm
#     template_name = 'dashproject/account/login.html'

#     def dispatch(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return redirect(resolve_url('/'))
#         return super().dispatch(request, *args, **kwargs)

#     def get_success_url(self):
#         messages.success(self.request, _("Hei: {self.request.user.first_name} You are successfully logged in"))
#         return resolve_url('/')

#     def form_invalid(self, form):
#         messages.error(self.request, _("Warning: UNAUTHORIZED ACCESS TO THIS SYSTEM MAY CONSTITUTE A CRIMINAL OFFENCE."))
#         return super().form_invalid(form)

class Logout_View(View):
    def get(self,request):
        logout(self.request)
        messages.info(request, _("Logged out successfully! bye bye"))
        return redirect ('login',permanent=True)

class UserListsView(LoginRequiredMixin,GroupRequiredMixin,View):
    paginate_by =6
    #model = get_user_model
    group_names = ['administrator']
    template_name = 'users/user-list.html'
    login_url = '/login/'  # Define the login URL or get it from your settings
    def get_context_data(self, **kwargs):
        context = {}
        context['users'] =User.objects.all()
        user_group = self.request.user.groups.values_list('name', flat=True)
        print(user_group)
        user_list = User.objects.all()
        paginator = Paginator(user_list, 6)

        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['user_group'] = list(user_group)
        return context

    def get(self, request, *args, **kwargs):
        self.request = request  # Make the request object available in get_context_data
        context = self.get_context_data(**kwargs)
        context['id']= self.request.user.id
        if isinstance(context, dict):
            return render(request, self.template_name, context)
        else:
            return context
        
