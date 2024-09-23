"""
URL configuration for CidProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from django.views.static import serve
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User
# from django_otp.admin import OTPAdminSite
# from django_otp.plugins.otp_totp.models import TOTPDevice
# from django_otp.plugins.otp_totp.admin import TOTPDeviceAdmin

# class OTPAdmin(OTPAdminSite):
#     pass

# admin_site = OTPAdmin(name='OTPAdmin')
# admin_site.register(User)
# admin_site.register(TOTPDevice, TOTPDeviceAdmin)
#from two_factor.urls import urlpatterns as tf_urls
urlpatterns = i18n_patterns(
     path('admin/', admin.site.urls),
    #path('two_factor/', include(('admin_two_factor.urls', 'admin_two_factor'), namespace='two_factor-one')),
    path('', include('cidApp.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT}),
    prefix_default_language=True,
    #path('mfa/', include(tf_urls)),
)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   
