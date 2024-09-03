from typing import Any
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from cidApp.forms import CommentForm, FileForm, InitialForm, ReportForm, SubjectForm, TextForm, ReviewForm
from .models import CallAndWebForm, Comments, Intial, Report, Staff, Status, Subject,WebForm, TextAttach
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from formtools.wizard.views import SessionWizardView
from django.shortcuts import get_object_or_404
from django.contrib.auth.views import LoginView
from .decorator_costum import GroupRequiredMixin
from django.http import JsonResponse
from django.core.paginator import Paginator,PageNotAnInteger, EmptyPage

class HotLineAndWebView(LoginRequiredMixin,GroupRequiredMixin,TemplateView):
    template_name = 'dashproject/pages/call_web_page.html'
    group_names =['administrator']
    login_url ='login'
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =super().get_context_data(**kwargs)
        print(self.request.user.email)
        context['id']= self.request.user.id
        context['records_count']= CallAndWebForm.objects.filter(status__name="Report Waiting").count()
        context['call_web'] = CallAndWebForm.objects.all()
        print(context['call_web'])
        user_group = self.request.user.groups.values_list('name', flat=True)
        print(user_group)
        context['user_group'] = list(user_group)
        return context 
    
class ViewAllReport(LoginRequiredMixin,TemplateView):
    template_name ='dashproject/pages/report_page.html'
    subject_form =  SubjectForm
    report_form = ReportForm
    login_url ='login'
    group_names =['administrator','staff']
    paginate_by =3   # Number of reports per page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id']= self.request.user.id
        print(context['id'])
        context['report_count'] = Report.objects.count()
        
        # Pagination logic
        reports_list = Report.objects.all().order_by('-status')
        paginator = Paginator(reports_list,self.paginate_by)
        page = self.request.GET.get('page')
        
        try:
            report = paginator.page(page)
        except PageNotAnInteger:
            report = paginator.page(1)
        except EmptyPage:
            report = paginator.page(paginator.num_pages)
            
        context['report'] = report    
        context['reports'] =  Report.objects.all().order_by('-status')
        user_group = self.request.user.groups.values_list('name', flat=True)
        print(user_group)
        context['user_group'] = list(user_group)
        context['subject_form'] = self.subject_form
        context['report_form'] = self.report_form
        return context


    
class CreateReportWebCallView(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    template_name = 'dashproject/pages/report.html'
    group_names = ['administrator']
    login_url = 'login'
    initial_form = InitialForm
    subject_form = SubjectForm
    text_form = TextForm
    file_form = FileForm
    comments_form = CommentForm
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        web_id =self.kwargs.get('web_id')
        context = super().get_context_data(**kwargs)
        context['call_web'] = CallAndWebForm.objects.all()
        context['id'] = self.request.user.id
        user_group = self.request.user.groups.values_list('name', flat=True)
        context['user_group'] = list(user_group)
        context['subject_form'] = self.subject_form()
        context['initial_form'] = self.initial_form()
        context['text_form'] = self.text_form()
        context['file_form'] = self.file_form()
        context['comment_form']= self.comments_form()
        context['view_id']= web_id
        ##ida ne ba status
        if 'report_id' in self.request.session:
            report = get_object_or_404(Report, id=self.request.session['report_id'])
            print(report)
            context['text_list'] = TextAttach.objects.filter(report=report)
            context['report_status'] = self.request.session.get('report_status', 'On Creating')
            context['report_id'] = self.request.session.get('report_id', 'Unique ID will be created')
        else:
            context['report_status'] = 'No report found'
            context['report_id'] = 'Unique ID will be created'

            
        return context

    def get_report(self, report_id):
        """ Helper method to retrieve the report """
        return Report.objects.get(id=report_id)
    
    def get_web_call(self,call_id):
        return CallAndWebForm.objects.get(id=call_id)
    
    def post(self, request, *args, **kwargs):
        web_id = self.kwargs.get('web_id')
        user_id = request.user.id
        staff = get_object_or_404(Staff, user_id=user_id)
        agency = staff.agency
        print(web_id)
       # print("Bug info",call_web)
        if 'initial_form' in request.POST:
            return self.handle_initial_form(request, agency, web_id)
        elif 'subject_form' in request.POST:
            return self.handle_subject_form(request)
        elif 'text_form' in request.POST:
            return self.handle_text_form(request)
        elif 'file_form' in request.POST:
            return self.handle_file_form(request)

        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def handle_initial_form(self, request, agency, web_id):
        form = self.initial_form(request.POST)
        
        if form.is_valid():
            initial_instance = form.save(commit=False)
            initial_instance.agency = agency
            initial_instance.save()
            request.session['initial_id'] = initial_instance.id

            report = Report.objects.create(
                source =self.get_web_call(web_id),
                user=request.user,
                initial=initial_instance,
                agency=agency,
                status="Incomplete",
                information_other=initial_instance.information_source
            )
            call_web = self.get_web_call(web_id)
            reported_status = Status.objects.get(name="Reported")  # Use 'name' instead of 'status'
            call_web.status = reported_status
            call_web.save()
            
            request.session['report_id'] = report.id
            request.session['report_status'] = report.status
           # request.session['report_created'] = report.created_at
            messages.success(request, f'New Initial has added')
            return redirect(f"{reverse('new-report')}?tab=subjects")

    def handle_subject_form(self, request):
        form = self.subject_form(request.POST)
        if form.is_valid():
            subject_instance = form.save()
            initial_id = request.session.get('initial_id')
            request.session['subject_id'] = subject_instance.id

            report = self.get_report(request.session.get('report_id'))
            report.Subject = subject_instance
            report.save()
            messages.success(request, f'New Subject has added successfully to {request.session.get('report_id')} Report ID')
            return redirect(f"{reverse('new-report')}?tab=text")

    def handle_text_form(self, request):
        form = self.text_form(request.POST)
        if form.is_valid():
            text_instance = form.save(commit=False)
            text_instance.user = request.user
            text_instance.report= self.get_report(request.session.get('report_id'))
            text_instance.save()
            request.session['text_id'] = text_instance.id
            #report.save()
            messages.success(request, f'New Subject has added successfully to {request.session.get('report_id')} Report ID')
            return redirect(f"{reverse('new-report')}?tab=text")
        else:
            print("Errorr")
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
  

    
    
class CreateReportWebView(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    template_name = 'dashproject/pages/report.html'
    group_names = ['administrator']
    login_url = 'login'
    initial_form = InitialForm
    subject_form = SubjectForm
    text_form = TextForm
    file_form = FileForm
    comments_form = CommentForm
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
        context['comment_form']= self.comments_form()
        ##ida ne ba status
        if 'report_id' in self.request.session:
            report = get_object_or_404(Report, id=self.request.session['report_id'])
            print(report)
            context['text_list'] = TextAttach.objects.filter(report=report)
            context['report_status'] = self.request.session.get('report_status', 'On Creating')
            context['report_id'] = self.request.session.get('report_id', 'Unique ID will be created')
        else:
            context['report_status'] = 'No report found'
            context['report_id'] = 'Unique ID will be created'

            
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
            request.session['report_status'] = report.status
           # request.session['report_created'] = report.created_at
            messages.success(request, f'New Initial has added')
            return redirect(f"{reverse('new-report')}?tab=subjects")

    def handle_subject_form(self, request):
        form = self.subject_form(request.POST)
        if form.is_valid():
            subject_instance = form.save()
            initial_id = request.session.get('initial_id')
            request.session['subject_id'] = subject_instance.id

            report = self.get_report(request.session.get('report_id'))
            report.Subject = subject_instance
            report.save()
            messages.success(request, f'New Subject has added successfully to {request.session.get('report_id')} Report ID')
            return redirect(f"{reverse('new-report')}?tab=text")

    def handle_text_form(self, request):
        form = self.text_form(request.POST)
        if form.is_valid():
            text_instance = form.save(commit=False)
            text_instance.user = request.user
            text_instance.report= self.get_report(request.session.get('report_id'))
            text_instance.save()
            request.session['text_id'] = text_instance.id
            #report.save()
            messages.success(request, f'New Subject has added successfully to {request.session.get('report_id')} Report ID')
            return redirect(f"{reverse('new-report')}?tab=text")
        else:
            print("Errorr")
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

class EditReport(LoginRequiredMixin,GroupRequiredMixin,View):
    group_names = ['administrator']
    login_url = 'login'
    def get(self,request,*args, **kwargs):
        report_id = kwargs.get('report_id')
        report = get_object_or_404(Report, id= report_id)
        comments = Comments.objects.filter(report= report)
        text_list = TextAttach.objects.filter(report=report)
        for i in comments:
            print(i.comment)
        print(report.status)
        initial_form = InitialForm(instance = report.initial)
        try:
            subject_form = SubjectForm(instance=report.Subject)
        except AttributeError:
            subject_form = SubjectForm()
        file_form = FileForm(instance= report.file_attached)
        id =self.request.user.id
        comments_form = CommentForm()
        text_form = TextForm()
        context={
            'initial_form':initial_form,
            'subject_form': subject_form,
            'text_form':text_form,
            'file_form':file_form,
            'id':self.request.user.id,
            'report_id':report_id,
            'report_status':report.status,
            'report_created':report.created_at,
            'comments_form': comments_form,
            'comments':comments,
            'text_list':text_list,
        }
        
        return render(request, 'dashproject/pages/report_edit.html', context)
     
    def post(self, request, *args, **kwargs):
        report_id = kwargs.get('report_id')
        report = get_object_or_404(Report, id=report_id)

        if 'initial_form' in request.POST:
            initial_form = InitialForm(request.POST, instance=report.initial)
            if initial_form.is_valid():
                initial_form.save()
                return redirect(f'/report/{report_id}/?tab=subjects')  # Include report_id in the URL

        elif 'subject_form' in request.POST and request.method=='POST':
            if report.Subject_id is None:
                subject_form = SubjectForm(request.POST)
                if subject_form.is_valid():
                    subjects=subject_form.save()
                    report.Subject = subjects
                    report.status="Incomplete"
                    report.save()
                    return redirect(f'/report/{report_id}/?tab=text')  # Include report_id in the URL
            else:
                subject_form = SubjectForm(request.POST, instance=report.Subject)
                if subject_form.is_valid():
                    subject_form.save()
                    report.status = "Incomplete"
                    report.save()
                    return redirect(f'/report/{report_id}/?tab=text')   # Include report_id in the URL
                
        elif 'text_form' in request.POST:
            text_form = TextForm(request.POST)
            if text_form.is_valid():
                text = text_form.save(commit=False)
                text.user = request.user
                text.report = report  # Link the text to the report
                text.save()
                report.status = "Incomplete"
                report.save()
                return redirect(f'/report/{report_id}/?tab=text')  # Redirect to text tab

        elif 'file_form' in request.POST:
            file_form = FileForm(request.POST, request.FILES, instance=report.file_attached)
            if file_form.is_valid():
                file = file_form.save(commit=False)
                file.user_id = self.request.user.id
                report.file_attached= file
                file.save()
                report.status ="Completed"
                report.save()
                return redirect('report-list')  # Include report_id in the URL
            
class EditReportComment(LoginRequiredMixin,GroupRequiredMixin,View):
    group_names = ['administrator']
    login_url = 'login'
    def get(self,request,*args, **kwargs):
        report_id = kwargs.get('report_id')
        report = get_object_or_404(Report, id= report_id)
        comments = Comments.objects.filter(report= report)
        text_list = TextAttach.objects.filter(report=report)
        for i in comments:
            print(i.comment)
        print(report.status)
        initial_form = InitialForm(instance = report.initial)
        try:
            subject_form = SubjectForm(instance=report.Subject)
        except AttributeError:
            subject_form = SubjectForm()
        file_form = FileForm(instance= report.file_attached)
        
        id =self.request.user.id
        comments_form = CommentForm()
        text_form =TextForm()
        user_group = self.request.user.groups.values_list('name', flat=True)
        context={
            'initial_form':initial_form,
            'subject_form': subject_form,
            'text_form':text_form,
            'file_form':file_form,
            'id':self.request.user.id,
            'report_id':report_id,
            'report_status':report.status,
            'report_created':report.created_at,
            'comments_form': comments_form,
            'comments':comments,
            'text_list':text_list,
            'user_group':list(user_group),
        }
        
        return render(request, 'dashproject/pages/report_edit_comment.html', context)
    
    def post(self, request, *args, **kwargs):
        report_id = kwargs.get('report_id')
        report = get_object_or_404(Report, id=report_id)
        comments_form = CommentForm(request.POST)
        if comments_form.is_valid():
                coments =comments_form.save(commit=False)
                coments.report_id =report_id
                coments.user_id =self.request.user.id
                coments.save()
                messages.success(request, f'New Comment added to ID {report.id} ')
                return redirect(f'/report-comment/{report_id}/?tab=comments')  # Include report_id in the URL

        # Fallback to reload the page with forms and errors if any form was invalid
        return self.get(request, *args, **kwargs)

class EditReportReview(LoginRequiredMixin,GroupRequiredMixin,View):
    group_names = ['administrator']
    login_url = 'login'
    def get(self,request,*args, **kwargs):
        report_id = kwargs.get('report_id')
        report = get_object_or_404(Report, id= report_id)
        comments = Comments.objects.filter(report= report)
        text_list = TextAttach.objects.filter(report=report)
        user_group = self.request.user.groups.values_list('name', flat=True)
        for i in comments:
            print(i.comment)
        print(report.status)
        initial_form = InitialForm(instance = report.initial)
        try:
            subject_form = SubjectForm(instance=report.Subject)
        except AttributeError:
            subject_form = SubjectForm()
        file_form = FileForm(instance= report.file_attached)
        
        id =self.request.user.id
        comments_form = CommentForm()
        text_form =TextForm()
        reviewed = ReviewForm()
        context={
            'initial_form':initial_form,
            'subject_form': subject_form,
            'text_form':text_form,
            'file_form':file_form,
            'id':self.request.user.id,
            'report_id':report_id,
            'report_status':report.status,
            'report_created':report.created_at,
            'comments_form': comments_form,
            'comments':comments,
            'text_list':text_list,
            'user_group':list(user_group),
            'reviewed':reviewed,
        }
        
        return render(request, 'dashproject/pages/report_edit_review.html', context)
    
    def post(self, request, *args, **kwargs):
        report_id = kwargs.get('report_id')
        report = get_object_or_404(Report, id=report_id)
        comments_form = CommentForm(request.POST)
        reviewed = ReviewForm(request.POST)
        if reviewed.is_valid():
                reviewed=reviewed.save(commit=False)
                reviewed.record_id =report_id
                reviewed.updated_by =self.request.user
                report.status ="Closed"
                reviewed.save()
                report.save()
                messages.success(request, f'The Id number {report.id} Has reviewed successfuly')
                return redirect('report-list')  
        return self.get(request, *args, **kwargs)


