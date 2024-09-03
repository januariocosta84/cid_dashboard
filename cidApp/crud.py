from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from cidApp.decorator_costum import GroupRequiredMixin
#from CidProject.cidApp.decorator_costum import GroupRequiredMixin
from .crud_form import AgencyForm
from .models import *
from django.core.paginator import Paginator
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth import get_user_model
from django.contrib import messages

class AgencyListView(GroupRequiredMixin, View):
    group_names = ['administrator']  # Specify the group(s) required
    def get(self, request, *args, **kwargs):
        id = request.user.id
        agencies = Agency.objects.all()
        paginator = Paginator(agencies, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        user_group = self.request.user.groups.values_list('name', flat=True)
        print(user_group)
        user_group = list(user_group)
        return render(request, 'agency/agency_list.html', {'agencies': agencies, 'id': id, 'page_obj': page_obj, 'user_group':user_group})
    
def agency_detail(request, pk):
    agency = get_object_or_404(Agency, pk=pk)
    return render(request, 'agency/agency_detail.html', {'agency': agency})

GroupRequiredMixin
def agency_create(request):
    group_names = ['administrator']  # Specify the group(s) required
    user_group = request.user.groups.values_list('name', flat=True)
    id = request.user.id
    user_group = list(user_group)
    if request.method == "POST":
        form = AgencyForm(request.POST)
        if form.is_valid():
            agency = form.save(commit=False)
            try:
                # Ensure that we get the actual user instance from the database
                user = AuthUser.objects.get(pk=request.user.pk)
                print("User type after fetching:", type(user))
                print("User instance after fetching:", user)
                agency.created_by = user
            except AuthUser.DoesNotExist:
                print("Error: User does not exist")
                return redirect('error_page')  # Handle this error appropriately
            
            agency.save()
            return redirect('agency-list')
        else:
            print("Form errors:", form.errors)
    else:
        form = AgencyForm()
    
    return render(request, 'agency/agency_form.html', {'form': form, 'id':id,'user_group':user_group})
def agency_update(request, pk):
    agency = get_object_or_404(Agency, pk=pk)
    print(agency)
    id = request.user.id
    if request.method == "POST":
        form = AgencyForm(request.POST, instance=agency)
        if form.is_valid():
            form.save()
            return redirect('agency-list')
    else:
        form = AgencyForm(instance=agency)
    return render(request, 'agency/agency_form.html', {'form': form, 'id':id})

def agency_delete(request, pk):
    id  = request.user.id
    agency = get_object_or_404(Agency, pk=pk)
    print("ID Tobe deleted",agency.id)
    if request.method == "POST":
        agency.delete()
        return redirect('agency-list')
    return render(request, 'agency/pagina_confirm_delete.html', {'agency': agency, 'id':id})





# """Add User Group"""

# def user_group_create(request):
#     if request.method == "POST":
#         form = AddUserForm(request.POST)
#         if form.is_valid():
#             agency = form.save(commit=False)
#             try:
#                 # Ensure that we get the actual user instance from the database
#                 user = AuthUser.objects.get(pk=request.user.pk)
#                 print("User type after fetching:", type(user))
#                 print("User instance after fetching:", user)
#                 agency.created_by = user
#             except AuthUser.DoesNotExist:
#                 print("Error: User does not exist")
#                 return redirect('error_page')  # Handle this error appropriately
            
#             agency.save()
#             return redirect('agency-list')
#         else:
#             print("Form errors:", form.errors)
#     else:
#         form = AddUserForm()
    
#     return render(request, 'users/user_group_form.html', {'form': form, 'id':1})


# """CRUD FOR USER GRUP TABLE BASE"""

# # Create Group
# def create_group(request):
#     id = request.user.id
#     if request.method == 'POST':
#         form = UserGroupForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Group created successfully.')
#             return redirect('group-list')
#     else:
#         form = UserGroupForm()
#     return render(request, 'users/group-form.html', {'form': form, 'id':id})

# # List Groups
# def group_list(request):
#     id = request.user.id
#     groups = AuthGroup.objects.all()
#     paginator = Paginator(groups, 6)
#     page_number =request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'users/group-list.html', {'groups': groups, 'id':id, 'page_obj':page_obj})

# # Update Group
# def update_group(request, pk):
#     id = request.user.id
#     group = get_object_or_404(AuthGroup, pk=pk)
#     if request.method == 'POST':
#         form = UserGroupForm(request.POST, instance=group)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Group updated successfully.')
#             return redirect('group-list')
#     else:
#         form = UserGroupForm(instance=group)
#     return render(request, 'users/group-form.html', {'form': form, 'id':id})

# # Delete Group
# def delete_group(request, pk):
#     group = get_object_or_404(AuthGroup, pk=pk)
#     if request.method == 'POST':
#         group.delete()
#         messages.success(request, 'Group deleted successfully.')
#         return redirect('group_list')
#     return render(request, 'group_confirm_delete.html', {'group': group})
    


# """Position List"""
# def create_position(request):
#     id = request.user.id
#     if request.method == 'POST':
#         form = UserGroupForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Group created successfully.')
#             return redirect('group-list')
#     else:
#         form = UserGroupForm()
#     return render(request, 'users/group-form.html', {'form': form, 'id':id})

# # List Groups
# def position_list(request):
#     id = request.user.id
#     position= Position.objects.all()
#     paginator = Paginator(position, 6)
#     page_number =request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'position/position_list.html', {'groups': position, 'id':id, 'page_obj':page_obj})

# # Update Group
# def update_group(request, pk):
#     id = request.user.id
#     group = get_object_or_404(AuthGroup, pk=pk)
#     if request.method == 'POST':
#         form = UserGroupForm(request.POST, instance=group)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Group updated successfully.')
#             return redirect('group-list')
#     else:
#         form = UserGroupForm(instance=group)
#     return render(request, 'users/group-form.html', {'form': form, 'id':id})

# # Delete Group
# def delete_group(request, pk):
#     group = get_object_or_404(AuthGroup, pk=pk)
#     if request.method == 'POST':
#         group.delete()
#         messages.success(request, 'Group deleted successfully.')
#         return redirect('group_list')
#     return render(request, 'group_confirm_delete.html', {'group': group})
    