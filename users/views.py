import socket

from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseBadRequest
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.utils.http import urlsafe_base64_decode
from .forms import sign_up_form, user_log_in_form, user_validation_form
from .models import Profile
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404

class sign_up_view(TemplateView):
    """
        Views for the Sign Up Page
    """
    template_name = "users/sign_up.html"

    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('users:home'))
        else:
            form = sign_up_form()
            context = {'form': form}
            return render(self.request, self.template_name,context)

    def post(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse(''))
        else:
            form = sign_up_form(self.request.POST)
            if form.is_valid():
                # Getting Host Name
                host = self.request.get_host()
                user = form.save(host)
                return HttpResponseRedirect(reverse('users:log_in'))
            else:
                args = {'form': form}
                return render(self.request, self.template_name, args)


class log_in_view(TemplateView):

    template_name = "users/log_in.html"

    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('users:home'))
        else:
            form = user_log_in_form()
            context = {'form': form}
            return render(self.request, self.template_name,context)

    def post(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('users:home'))
        else:
            form = user_log_in_form(self.request.POST) 
            if form.is_valid():
                user = form.login()
                if user is not None:
                    login(self.request, user)
                    return HttpResponseRedirect(reverse('users:home'))
            context = {'form': form}

            return render(self.request, self.template_name, context)

class user_validation(TemplateView):
    template_name = "users/user_validation.html"

    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('users:home'))
        else:
            uidb64 = self.kwargs.get('uidb64')
            token = self.kwargs.get('token')
            form = user_validation_form()
            if uidb64 is not None and token is not None:
                try:
                    # This line could throw some errors when someone randomly types
                    uid = urlsafe_base64_decode(uidb64).decode()
                    user = get_object_or_404(User,pk=uid)
                    filtered_profile = get_object_or_404(Profile,user=user)

                    if default_token_generator.check_token(user, token) and filtered_profile.is_confirmed == False:
                        filtered_profile.is_confirmed = True
                        filtered_profile.save()
                        return render(self.request, self.template_name, {'form': form,'success': True})
                    else:
                        return render(self.request, self.template_name, {'form': form,'success': False})
                except:
                    return render(self.request, self.template_name, {'form': form,'success': False})

        return render(self.request, self.template_name, {'form': form,'success': False})

    def post(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('users:home'))
        else:
            form = user_validation_form(self.request.POST) 
            if form.is_valid():
                host = self.request.get_host()
                user = form.send_email(host)
                return render(self.request, self.template_name, {'form': form,'success': False})
            context = {'form': form}

            return render(self.request, self.template_name, {'form': form,'success': False})



class log_out_view(TemplateView):
    template_name = "users/log_in.html"

    def get(self,*args,**kwargs):
        logout(self.request)
        return HttpResponseRedirect(reverse('users:log_in'))

class index_view(TemplateView):
    """
        Views for the Sign Up Page
    """
    template_name = "users/index.html"

    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return render(self.request, self.template_name, {})
        else:
            return HttpResponseRedirect(reverse('users:log_in'))