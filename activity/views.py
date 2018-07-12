from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseBadRequest
from django.urls import reverse_lazy
from django.db.models import Q
from django.core import serializers

from activity.models import Activity
from .forms import ActivityForm
from users.models import User
from boards.models import BoardMember

class ActivityView(LoginRequiredMixin,TemplateView):
    """
        Views for the User Activity Page
    """
    # Reverse lazy is needed since this code is before the Url coniguration
    # is loaded
    login_url = reverse_lazy('users:log_in')
    template_name = "activity/activity.html"

    def get(self, *args,** kwargs):
        context = {}
        user = self.request.user
        activity = Activity.objects.filter(
            Q(user=user)).order_by('-modified')
        context={'activities':activity, 'current_user' : self.request.user.username}

        return render(self.request, self.template_name,context)



   