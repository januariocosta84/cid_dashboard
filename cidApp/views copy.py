# from django.shortcuts import redirect, render, resolve_url
# from django.views import View
from typing import Any
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from cidApp.forms import FileForm, InitialForm, ReportForm, SubjectForm, TextForm
from .models import CallAndWebForm, Intial, Report, Staff, Subject,WebForm, TextAttach
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from formtools.wizard.views import SessionWizardView
from django.shortcuts import get_object_or_404
# #from .models import Records,RecordsSource
# from django.urls import reverse_lazy
# from .lib import *
# from django.contrib.auth.models import User,Group
# from .forms import *
# #from cidApp.forms import CreateRecordsForm
# from django.http import JsonResponse
# from django.views.generic import ListView
# from django.contrib import admin
from django.contrib.auth.views import LoginView
# from django.contrib.auth import get_user_model
# from django.contrib.auth import logout
from .decorator_costum import GroupRequiredMixin
# import requests
# from django.contrib.auth import authenticate, login
# from urllib.parse import parse_qsl
# from django.contrib.auth import authenticate
from django.http import JsonResponse
# from django.views import View
# from django.views.decorators.csrf import csrf_exempt
# from admin_two_factor.utils import set_expire
# from two_factor .views import LoginView

class HotLineAndWebView(LoginRequiredMixin,GroupRequiredMixin,TemplateView):
    template_name = 'dashproject/pages/call_web_page.html'
    group_names =['administrator']
    login_url ='login'
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =super().get_context_data(**kwargs)
        print(self.request.user.email)
        context['id']= self.request.user.id
        context['call_web'] = CallAndWebForm.objects.all()
        print(context['call_web'])
        user_group = self.request.user.groups.values_list('name', flat=True)
        print(user_group)
        context['user_group'] = list(user_group)
        return context 
    
# class ReportWebView(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
#     template_name = 'dashproject/pages/report.html'
#     group_names = ['administrator']
#     login_url = 'login'
#     initial_form = InitialForm
#     subject_form = SubjectForm
#     text_form   =TextForm
#     file_form = FileForm

#     def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
#         context = super().get_context_data(**kwargs)
#         context['call_web'] = CallAndWebForm.objects.all()
#         context['id'] = self.request.user.id
#         user_group = self.request.user.groups.values_list('name', flat=True)
#         context['user_group'] = list(user_group)
#         context['subject_form'] = self.subject_form()
#         context['initial_form'] = self.initial_form()
#         context['text_form'] = self.text_form()
#         context['file_form'] = self.file_form()
#         return context

#     def get(self, request, *args, **kwargs):
#         context = self.get_context_data(**kwargs)
#         return render(request, self.template_name, context)

#     def post(self, request, *args, **kwargs):
#         if 'initial_form' in request.POST:
#             initial_form = self.initial_form(request.POST)
#             if initial_form.is_valid():
#                 initial_instance = initial_form.save()
            
#                 request.session['initial_id'] = initial_instance.id
                
#                 return redirect(f"{reverse('report')}?tab=subjects")

#         elif 'subject_form' in request.POST:
#             subject_form = self.subject_form(request.POST)
#             if subject_form.is_valid():
#                 subject_instance = subject_form.save()
#                 initial_instance = None
#                 initial_id = request.session.get('initial_id')
#                 if initial_id:
#                     initial_instance = Intial.objects.get(id=initial_id)
#                 print(initial_instance.source)
#                 # Create a report
#                 Report.objects.create(
#                     user=request.user,
#                     Subject=subject_instance,
#                     intial=initial_instance,
#                     report_by=request.user,
#                     information_other=initial_instance.source ,  # Replace with actual data if needed
#                 )

#                 # Clear the initial instance from session after report creation
#                 request.session.pop('initial_id', None)

#                 return redirect(f"{reverse('report')}?tab=text")
#         elif 'text_form' in request.POST:
#             text_form  = self.text_form(request.POST)
#             if text_form.is_valid():
#                 text_instance = text_form.save()
#                 request.session['text_id']= text_instance.id
#             return redirect(f"{reverse('report')}?tab=text")
        
#         elif 'file_form' in request.POST:
#             file_form  = self.text_form(request.POST)
#             if file_form.is_valid():
#                 text_instance = text_form.save()
#                 request.session['text_id']= text_instance.id
#             return redirect(f"{reverse('report')}?tab=text")
#         context = self.get_context_data(**kwargs)
#         return render(request, self.template_name, context)

class ReportWebView(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    template_name = 'dashproject/pages/report.html'
    group_names = ['administrator']
    login_url = 'login'
    initial_form = InitialForm
    subject_form = SubjectForm
    text_form = TextForm
    file_form = FileForm

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['call_web'] = CallAndWebForm.objects.all()
        context['id'] = self.request.user.id
        user_group = self.request.user.groups.values_list('name', flat=True)
        context['user_group'] = list(user_group)
        context['subject_form'] = self.subject_form()
        context['initial_form'] = self.initial_form()
        context['text_form'] = self.text_form()
        context['file_form'] = self.file_form()
        return context

    def get_report(self, report_id):
        """ Helper method to retrieve the report """
        return Report.objects.get(id=report_id)

    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        staff = get_object_or_404(Staff, user_id=user_id)
        agency = staff.agency
        if 'initial_form' in request.POST:
            return self.handle_initial_form(request, agency)
        elif 'subject_form' in request.POST:
            return self.handle_subject_form(request)
        elif 'text_form' in request.POST:
            return self.handle_text_form(request)
        elif 'file_form' in request.POST:
            return self.handle_file_form(request)

        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def handle_initial_form(self, request, agency):
        form = self.initial_form(request.POST)
        if form.is_valid():
            initial_instance = form.save(commit=False)
            initial_instance.agency = agency
            initial_instance.save()
            request.session['initial_id'] = initial_instance.id

            report = Report.objects.create(
                user=request.user,
                initial=initial_instance,
                agency=agency,
                status="Incomplete",
                information_other=initial_instance.information_source
            )
            request.session['report_id'] = report.id
            return redirect(f"{reverse('report')}?tab=subjects")

    def handle_subject_form(self, request):
        form = self.subject_form(request.POST)
        if form.is_valid():
            subject_instance = form.save()
            initial_id = request.session.get('initial_id')
            request.session['subject_id'] = subject_instance.id

            report = self.get_report(request.session.get('report_id'))
            report.Subject = subject_instance
            report.save()
            return redirect(f"{reverse('report')}?tab=text")

    def handle_text_form(self, request):
        form = self.text_form(request.POST)
       
        if form.is_valid():
            print(form)
            print("Form Data:", form.cleaned_data)  # Debug: Print cleaned dat
            text_instance = form.save(commit=False)
            text_instance.user = request.user
            text_instance.save()
            request.session['text_id'] = text_instance.id

            report = self.get_report(request.session.get('report_id'))
            report.save()
            return redirect(f"{reverse('report')}?tab=attach")
        else:
            print(form.errors)  # Handle this more gracefully in production

    def handle_file_form(self, request):
        form = self.file_form(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save(commit=False)
            file_instance.user = request.user
            file_instance.metadata = 'Default'
            file_instance.name = 'default'
            file_instance.save()

            report = self.get_report(request.session.get('report_id'))
            report.file_attached = file_instance
            report.status = "Completed"
            report.save()

            request.session.pop('initial_id', None)
            request.session.pop('subject_id', None)
            request.session.pop('text_id', None)
            request.session.pop('report_id', None)
            return redirect('report-list')
  

class ReportDetail(DetailView):
    model = Report
    template_name ='dashproject/pages/detail_report.html'
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =super().get_context_data(**kwargs)
        context['']=''
        return context
      
class ViewAllReport(LoginRequiredMixin,TemplateView):
    template_name ='dashproject/pages/report_page.html'
    subject_form =  SubjectForm
    report_form = ReportForm
  
    login_url ='login'
    group_names =['administrator']
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id']= self.request.user.id
        print(context['id'])
        context['report_count'] = Report.objects.count()
        context['reports'] =  Report.objects.all().order_by('-created_at')
        user_group = self.request.user.groups.values_list('name', flat=True)
        print(user_group)
        context['user_group'] = list(user_group)
        context['subject_form'] = self.subject_form
        context['report_form'] = self.report_form
       
        return context

    def post(self, request, *args, **kwargs):
        form = self.subject_form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('view_all_report'))  # Adjust this to your desired redirect URL
        else:
            return self.render_to_response(self.get_context_data(subject_form=form))

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())
    
class DetailSubject(DetailView,):
    login_url ='login'
    model = WebForm
    #template_name = 'dashproject/base/detail_subject.html'
    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            detail_webform = self.get_object()
            data = {
                 'name': detail_webform.first_name,
                'last_name': detail_webform.last_name,
                'nationality': detail_webform.nationality,
                # Add other necessary fields here
                'gender': detail_webform.gender,
                'dob': detail_webform.dob,
                'approx_age': detail_webform.approx_age,
                'id_type': detail_webform.id_type,
                'id_number': detail_webform.id_number,
                'home_address': detail_webform.home_address,
                'business_name': detail_webform.business_name,
                'business_address': detail_webform.business_address,
                'bin_tin': detail_webform.bin_tin,
                'telephone': detail_webform.telephone,
                'description': detail_webform.description,
                'created_at': detail_webform.created_at,
                'updated_at': detail_webform.updated_at,
                'conveyance_description': detail_webform.description,
                'status': detail_webform.status,
            }
            print(data)
            return JsonResponse(data)
        else:
            return super().get(request, *args, **kwargs)




class ReportWizardView(SessionWizardView):
    form_list = [InitialForm, SubjectForm]
    template_name = 'dashproject/pages/report.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id'] = self.request.user.id
        return context

    def get(self, request, *args, **kwargs):
        form = self.get_form(step=self.steps.current)
        context = self.get_context_data(form=form, **kwargs)
        return self.render_to_response(context)
    
    def done(self, form_list, **kwargs):
        return HttpResponse("Forms are submitted")

# class DetailRecordResource(LoginRequiredMixin,DetailView):
#     login_url ='login'
#     model =R
#     template_name = 'dashproject/pages/detail_subject.html'
#     def get(self, request, *args, **kwargs):
#         if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#             record_source = self.get_object()
#             print(record_source)
#             data = {
#                 'name': record_source.uri,
#                 # 'last_name':record_source.last_name,
#                 # 'gender':record_source.gender,
                
#                 # Add other necessary fields here
#             }
#             print(data)
#             return JsonResponse(data)
#         else:
#             return super().get(request, *args, **kwargs)
        

# class SearchForm(LoginRequiredMixin,ListView):
#     model = Records
#     template_name = 'dashproject/pages/search_form.html'
#     context_object_name = 'results'
    
#     def get_queryset(self):
#         query = self.request.GET.get('search', '')
#         if query:
#             return Records.objects.filter(subject__first_name__icontains=query)
#         return Records.objects.none()

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user_group = self.request.user.groups.values_list('name', flat=True)
#         print(user_group)
#         context['id']= self.request.user.id
#         context['user_group'] = list(user_group)
#         query = self.request.GET.get('search', '')
#         if query:
#             context['records_count'] = Records.objects.filter(subject__first_name__icontains=query).count()
#         else:
#             context['records_count'] = 0
#         context['query'] = query
#         return context


# # def insert_subject(request):
# #     url = 'https://fakestoreapi.com/products'
# #     response = requests.get(url)
# #     content = response.json()
    
# #     all_products = content
# #     print(all_products)
    
# #     create_obj = []
# #     for product in all_products:
# #         if not Product.objects.filter(code=product['id']).exists():
# #             create_obj.append(Product(
# #                 code=product['id'],
# #                 title=product['title'],
# #                 price=product['price'],
# #                 description=product['description'],
# #                 category=product['category'],
# #                 image=product['image'],
# #                 rating_rate=product['rating']['rate'],
# #                 rating_count=product['rating']['count']
# #             ))
    
# #     if create_obj:
# #         Product.objects.bulk_create(create_obj)

# #     product_data = Product.objects.all()

# #     return render(request, 'cart/product.html', {"product_data": product_data})

# class TwoStepVerification(View):
#     def post(self, request):
#         params = dict(parse_qsl(request.body.decode()))
#         username = params.get('username', None)
#         password = params.get('password', None)
#         if not username or not password:
#             return JsonResponse({'is_valid': False, 'message': 'required username/password'})

#         user = authenticate(request=request, username=username, password=password)
#         if user and user.is_staff:
#             if hasattr(user, 'two_step') and user.two_step.is_active:
#                 request.session['pre_two_step_user_id'] = user.id
#                 return JsonResponse({'is_valid': True, 'message': 'ok'})
#         return JsonResponse({'is_valid': False, 'message': 'maybe something wrong'})
#     @csrf_exempt
#     def put(self, request):
#         params = dict(parse_qsl(request.body.decode()))
#         code = params.get('code', None)
#         username = params.get('username', None)
#         password = params.get('password', None)
#         if not username or not password:
#             return JsonResponse({'is_valid': False, 'message': 'required username/password'})
#         if not code:
#             return JsonResponse({'is_valid': False, 'message': 'provide a valid code. The code is required.'})

#         user = authenticate(request=request, username=username, password=password)
#         if user and user.is_staff:
#             if hasattr(user, 'two_step') and user.two_step.is_active:
#                 if user.two_step.is_verify(code):
#                     request.session['two_step_%s' % user.id] = {'expire': set_expire().get('time')}
#                     login(request, user)  # Log the user in after successful verification
#                     return JsonResponse({'is_valid': True, 'message': 'ok'})
#                 else:
#                     return JsonResponse({'is_valid': False, 'message': 'please provide a valid code'})

#         return JsonResponse({'is_valid': False, 'message': 'something wrong happened'})
