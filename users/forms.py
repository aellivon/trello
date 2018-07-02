from django import forms
from django.conf import settings
from django.contrib.auth import (
    authenticate,
    login,
    logout,
)
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.shortcuts import reverse
from .models import User
from .models import Profile
from django.core.mail import send_mail
from annoying.functions import get_object_or_None

class sign_up_form(forms.Form):
    """
    The form for the sign up page
    """
    first_name = forms.CharField(max_length=20,\
        required=True,widget=forms.TextInput(attrs={'class' : 'form-control sign_up_input'}))
    last_name = forms.CharField(max_length=20,\
        required=True,widget=forms.TextInput(attrs={'class' : 'form-control sign_up_input'}))
    username = forms.CharField(max_length=20,\
        required=True,widget=forms.TextInput(attrs={'class' : 'form-control sign_up_input'}))
    email = forms.EmailField(max_length=20,\
        required=True,widget=forms.TextInput(attrs={'class' : 'form-control sign_up_input'}))
    password = forms.CharField(\
        required=True,widget=forms.PasswordInput(attrs={'class' : 'form-control sign_up_input'})
        )

    confirm_password = forms.CharField(
        required=True,widget=forms.PasswordInput(attrs={'class' : 'form-control sign_up_input'})
        )


    def save(self, *args, **kwargs):

        data = self.cleaned_data
        username = data["username"]
        email = data["email"]
        password = data["password"]
        new_user = User.objects.create_user(username, email, password)
        new_user.first_name = data["first_name"]
        new_user.last_name = ["last_name"]
        new_user.save()
        # Default Token Django Generator
        token = default_token_generator.make_token(new_user)
        # Converting the id into base 64
        # Some issues from Django 2.0 
        uid = urlsafe_base64_encode(force_bytes(new_user.pk)).decode()
        # Getting Host Name
        host = args[0]
        # Getting url and filling it up with parameters
        validation_url = (reverse('users:user_validation', kwargs={'uidb64':uid,'token':token}))
        # formatting string to send
        full_activation_link = f'{host}{validation_url}'
        full_message = f"Click the link {full_activation_link} to activate the account {username}."



        new_profile = Profile(user=new_user)
        new_profile.initials = new_user.first_name[0] + new_user.last_name[0]
        new_profile.is_confirmed = False
        new_profile.bio = ''
        new_profile.save()
        
        send_mail(
            'Validating Your Account',
            full_message,
            'training.swift.aksun@gmail.com',
            [email],
            fail_silently=False,
        )

        return new_user

    def clean(self, *args, **kwargs):
        username = self.data.get("username")
        password = self.data.get("password")
        confirm_password = self.data.get("confirm_password")
        email = self.data.get('email')


        # Password Error
        if(password != confirm_password):
            raise forms.ValidationError("The password you entered doesn't match")



        user_with_the_same_username = User.objects.filter(username=username)
        duplicate_email = User.objects.filter(email=email)

        if user_with_the_same_username.count()==1:
            raise forms.ValidationError("This user already exists! Please choose another username.")

        # Uncomment this when final product rolls in
        
        if duplicate_email.count() > 0:
            raise forms.ValidationError("This email already exists! Please choose another email.")

        return super(sign_up_form, self).clean(*args, **kwargs)


class user_log_in_form(forms.Form):
    username = forms.CharField(required=True,max_length=20\
        ,widget=forms.TextInput(attrs={'class' : 'form-control InputCenter'}))

    password = forms.CharField(required=True,\
        widget=forms.PasswordInput(attrs={'class' : 'form-control InputCenter'}))


    def login(self):
        data = self.cleaned_data
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        return user

    def clean(self, *args, **kwargs):
        username = self.data.get("username")
        password = self.data.get("password")

        if username and password:
            user_with_the_same_username = User.objects.filter(username=username)

            if user_with_the_same_username.count()==1:
                user = user_with_the_same_username.first()
            else:
                raise forms.ValidationError("This user does not exists!")

            if not user.check_password(password):
                raise forms.ValidationError("Incorrect password")

            if not user.is_active:
                raise forms.ValidationError("This user is not active!")
            profile = Profile.objects.get(user=user)
            if profile.is_confirmed == False:
                raise forms.ValidationError("Please validate your account through your email first.")
        return super(user_log_in_form, self).clean(*args, **kwargs)


class user_validation_form(forms.Form):
    email = forms.CharField(required=True,max_length=20\
        ,widget=forms.TextInput(attrs={'class' : 'form-control InputCenter'}))

    def clean(self, *args, **kwargs):
        email = self.data.get("email")

        exists = get_object_or_None(User,email=email)
        if not exists:
            raise forms.ValidationError("This email hasn't been taken!")

        if exists:
            profile = get_object_or_None(Profile,user=exists)
            if profile.is_confirmed == True:
                raise forms.ValidationError("This email has already been confirmed!")

        return super(user_validation_form, self).clean(*args, **kwargs)

    def send_email(self,*args,**kwargs):
        data = self.cleaned_data
        email = data["email"]
        list_email = []
        list_email.append(email)
        new_user = get_object_or_None(User,email=email)
        # Default Token Django Generator
        token = default_token_generator.make_token(new_user)
        # Converting the id into base 64
        # Some issues from Django 2.0 
        uid = urlsafe_base64_encode(force_bytes(new_user.pk)).decode()
        # Getting Host Name
        host = args[0]
        # Getting url and filling it up with parameters
        validation_url = (reverse('users:user_validation', kwargs={'uidb64':uid,'token':token}))
        # formatting string to send
        full_activation_link = f'{host}{validation_url}'
        full_message = f"Click the link {full_activation_link} to activate the account {new_user.username}."

        
        send_mail(
            'Validating Your Account',
            full_message,
            'training.swift.aksun@gmail.com',
            list_email,
            fail_silently=False,
        )