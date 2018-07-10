import socket
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseBadRequest
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.utils.http import urlsafe_base64_decode
from .forms import SignUpForm, UserLogInForm
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from .mixins import ThrowHomeIfLoggedInMixIn


class SignUpView(ThrowHomeIfLoggedInMixIn,TemplateView):
    # This mix in throws home if not logged in
    """
        Views for the Sign Up Page
    """
    template_name = "users/sign_up.html"
    form = SignUpForm

    def get(self, *args, **kwargs):
        form = self.form()
        context = {'form': form}
        return render(self.request, self.template_name,context)

    def post(self, *args, **kwargs):
        form = self.form(self.request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect(reverse('users:log_in'))
        else:
            args = {'form': form}
            return render(self.request, self.template_name, args)


class LogInView(ThrowHomeIfLoggedInMixIn,TemplateView):
    # This mix in throws home if not logged in
    template_name = "users/log_in.html"
    form = UserLogInForm

    def get(self, *args, **kwargs):
        form = self.form()
        context = {'form': form}
        return render(self.request, self.template_name,context)

    def post(self, *args, **kwargs):
        form = self.form(self.request.POST) 
        if form.is_valid():
            user = form.login()
            if user is not None:
                login(self.request, user)
                return HttpResponseRedirect(reverse('boards:home', kwargs={ 
                        'username': self.request.user.get_username() 
                    }))
        context = {'form': form}
        return render(self.request, self.template_name, context)


class LogOutView(TemplateView):
    """
        This view is for simply logging out the user
    """
    template_name = "users/log_in.html"

    def get(self, *args,** kwargs):
        logout(self.request)
        return HttpResponseRedirect(reverse('users:log_in'))


