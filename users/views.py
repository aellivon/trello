import socket

from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseBadRequest
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.utils.http import urlsafe_base64_decode
from .forms import SignUpForm, UserLogInForm
from .models import Profile
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404

class SignUpView(TemplateView):
    """
        Views for the Sign Up Page
    """
    template_name = "users/sign_up.html"
    form = SignUpForm

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('users:home'))
        else:
            form = self.form()
            context = {'form': form}
            return render(self.request, self.template_name,context)

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse(''))
        else:
            form = self.form(self.request.POST)
            if form.is_valid():
                # Getting Host Name
                host = self.request.get_host()
                user = form.save(host)
                return HttpResponseRedirect(reverse('users:log_in'))
            else:
                args = {'form': form}
                return render(self.request, self.template_name, args)


class LogInView(TemplateView):

    template_name = "users/log_in.html"
    form = UserLogInForm

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('users:home'))
        else:
            form = self.form()
            context = {'form': form}
            return render(self.request, self.template_name,context)

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('users:home'))
        else:
            form = self.form(self.request.POST) 
            if form.is_valid():
                user = form.login()
                if user is not None:
                    login(self.request, user)
                    return HttpResponseRedirect(reverse('users:home'))
            context = {'form': form}

            return render(self.request, self.template_name, context)

class LogOutView(TemplateView):
    template_name = "users/log_in.html"

    def get(self, *args,** kwargs):
        logout(self.request)
        return HttpResponseRedirect(reverse('users:log_in'))

class IndexView(TemplateView):
    """
        Views for the Sign Up Page
    """
    template_name = "users/index.html"

    def get(self, *args,** kwargs):
        if self.request.user.is_authenticated:
            return render(self.request, self.template_name, {})
        else:
            return HttpResponseRedirect(reverse('users:log_in'))


