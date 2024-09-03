from django.contrib import admin
from .models import Status, Hotline, Subject, WebForm, CallAndWebForm, Staff, Agency, Report, Comments, Intial


admin.site.register(Status)
admin.site.register(Hotline)
admin.site.register(WebForm)
admin.site.register(CallAndWebForm)
admin.site.register(Staff)
admin.site.register(Agency)
admin.site.register(Report)
admin.site.register(Subject)
admin.site.register(Comments)
admin.site.register(Intial)