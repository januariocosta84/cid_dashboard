from django.urls import path
from django.conf.urls.i18n import set_language

#Built in library for auth views
from django.contrib.auth import views as auth_views
from .crud import(
    AgencyListView,
    agency_create,
    agency_update,
    agency_delete,
)
from .user_management import(
    Login_View,
    Logout_View,
    RegisterUsers,
    UserListsView,
    EditUserView,
    DeleteUserView,
)

from .views import(
    HotLineAndWebView,
    DetailSubject,
      CreateReportWebView,
      ViewAllReport,
      CreateReportWebCallView,
      ReportDetail,
      EditReport,
      EditReportComment,
      EditReportReview,
      SyncSubjectsView,
      DetailCall,
      EnableMFAView,
      DisableMFAView,
      MFAVerificationView,
    )

urlpatterns = [
        #Call API from Web form to insert local database
    #path('call-api/', SyncSubjectsView.as_view(), name= 'call-api'),
    path('<int:user_id>/enable-mfa/', EnableMFAView.as_view(), name='enable-mfa'),
    path('<int:user_id>/disable-mfa/', DisableMFAView.as_view(), name='disable-mfa'),
    path('mfa-verify/', MFAVerificationView.as_view(), name='verify-mfa'),
    
        #Hotline and Subjectdetail webview
    path('', HotLineAndWebView.as_view(), name='records'),
    
    path('call-details/<int:pk>/', DetailCall.as_view(), name='detail_call'),
    path('subject_details/<int:pk>/', DetailSubject.as_view(), name='detail_subject'),
    
        #User Managament

    path('login/', Login_View.as_view(), name='login'),
    path('logout/', Logout_View.as_view(), name='logout'),
    path('<int:pk>/edit-user/', EditUserView.as_view(), name='change'),
    path('users/user-list/', UserListsView.as_view(), name='user-list'),
    path('new/add-account/', RegisterUsers.as_view(), name='user-register'),
    path('<int:pk>/delete-user/',DeleteUserView.as_view(), name='delete-user' ),
    
    
        #CRUD URL Agency
    path('agency-create/',agency_create, name= 'create-agency' ),
    path('agency-list/',AgencyListView.as_view(), name ='agency-list'),
    path('<int:pk>/agency-update/', agency_update, name ='agency-update'),
    path('<int:pk>/agency-delete/', agency_delete, name ='agency-delete'),
    
    
    #CRUD URL REPORT
    path('report-list/', ViewAllReport.as_view(), name='report-list'),
    path('add/new-report/',CreateReportWebView.as_view(), name='new-report'),
    path('add/new-report/<int:web_id>/',CreateReportWebCallView.as_view(), name ='report-web'),
     
    #CRUD for Report 
    
    path('<pk>/report-details', ReportDetail.as_view(), name='report-detail'),
    path('report/<int:report_id>/', EditReport.as_view(), name='edit_report'),
    path('report-comment/<int:report_id>/', EditReportComment.as_view(), name='comment_report'),
    
    path('report-review/<int:report_id>/',EditReportReview.as_view(), name='review_report'),
    
    
    
    # Reset password in case users forgot the password
    
    path("password_reset/",auth_views.PasswordResetView.as_view(
        template_name ='users/reset_email_password.html'
        ), name='reset_password'),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name = 'users/password_reset_done.html'
            ), name='password_reset_done'
    ),
    path(
        "reset/<uidb64>/<token>/",
         auth_views.PasswordResetConfirmView.as_view(
             template_name ='users/password_reset_confirm.html'
             ), name='password_reset_confirm'
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name ='users/password_reset_complete.html'
            ), name='password_reset_complete'
    ),
    
]

# #from .views import insert_subject
# urlpatterns = [
#     path('', RecordView.as_view(), name='records' ),
#     ##CRUD user Group
#     path('groups/', group_list, name='group-list'),
#     path('create-group/', create_group,name='create-group'),
#     path('<int:pk>/update-group/', update_group, name = 'update-group'),
#     path('user-group/', user_group_create, name='user-group'),
    
#     ##CRUD Position
#     path('postion/', position_list, name='position-list'),
    
#     #CRUD URL Agency
#     path('agency-create/',agency_create, name= 'create-agency' ),
#     path('agency-list/',agency_list, name ='agency-list'),
#     path('<int:pk>/agency-update/', agency_update, name ='agency-update'),
#     path('<int:pk>/agency-delete/', agency_delete, name ='agency-delete'),
    
#     #TWO Factor
#     path('two_factor/', TwoStepVerification.as_view(), name='two_factor'),
    
#     path('record/', IndexView.as_view(), name='home'),
#     path('new/add-account/', RegisterUsers.as_view(), name='register'),
#     path('users/user-list/', UserListsView.as_view(), name='user-list'),
#     path('<int:id>/change-password/', ChangePasswordView.as_view(), name='change'),
#     path('user/<int:pk>/update/', ResetPasswordView.as_view(), name='user_reset_password'),
   
#     path('logout/', Logout_View.as_view(), name='logout'),
#     path('search/', SearchForm.as_view(), name='search'),
#     path('record_details/<int:pk>/',DetailRecordResource.as_view(), name='record_detail' ),
#     path('subject_details/<int:pk>/', DetailSubject.as_view(), name='detail_subject'),
#     #path('test', insert_subject, name='teste')
#    # path('create-record/', CreateRecords.as_view(), name='create_record_form'),
   
# ]