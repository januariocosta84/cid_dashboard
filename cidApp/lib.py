"""Protection view"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseForbidden
from django.views.generic import CreateView