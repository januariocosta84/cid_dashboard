from django.http import HttpResponseNotAllowed, HttpResponseRedirect, HttpResponseServerError
from django.urls import reverse
from .lib import *
"""Protection view"""
class GroupRequiredMixin(AccessMixin):
    group_names = []
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not any(group.name in self.group_names for group in request.user.groups.all()):
            return HttpResponseForbidden("Ita Laiha Permisaun Atu Hare Pagina ida ne")
        return super().dispatch(request, *args, **kwargs)
