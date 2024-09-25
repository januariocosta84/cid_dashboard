from django.urls import path
from django.conf.urls.i18n import set_language
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
)

from .views import(
    HotLineAndWebView,
    DetailSubject,
      CreateReportWebView,
    #ReportWizardView,
      ViewAllReport,
      CreateReportWebCallView,
      ReportDetail,
      EditReport,
      EditReportComment,
      EditReportReview,
      SyncSubjectsView,
      DetailCall,
    )

urlpatterns = [
        #Call API from Web form to insert local database
    path('call-api/', SyncSubjectsView.as_view(), name= 'call-api'),
    
  
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
