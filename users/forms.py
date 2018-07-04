from django import forms
from django.conf import settings
from django.contrib.auth import (
    authenticate,
    login,
    logout,
)
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import reverse
from .models import User
from annoying.functions import get_object_or_None

class SignUpForm(forms.Form):
    """
    The form for the sign up page
    """
    first_name = forms.CharField(max_length=20,
        required=True, widget=forms.TextInput(attrs={'class' : 'form-control sign-up-input'}))
    last_name = forms.CharField(max_length=20,
        required=True, widget=forms.TextInput(attrs={'class' : 'form-control sign-up-input'}))
    username = forms.CharField(max_length=20,
        required=True, widget=forms.TextInput(attrs={'class' : 'form-control sign-up-input'}))
    email = forms.EmailField(
        required=True, widget=forms.TextInput(attrs={'class' : 'form-control sign-up-input'}))
    password = forms.CharField(
        required=True, widget=forms.PasswordInput(attrs={'class' : 'form-control sign-up-input'})
        )

    confirm_password = forms.CharField(
        required=True, widget=forms.PasswordInput(attrs={'class' : 'form-control sign-up-input'})
        )


    def save(self, *args, **kwargs):

        data = self.cleaned_data
        username = data["username"]
        email = data["email"]
        password = data["password"]
        new_user = User.objects.create_user(username, email, password)
        new_user.first_name = data["first_name"]
        new_user.last_name = data["last_name"]
        new_user.save()
        
        return new_user


    def clean_username(self, *args, **kwargs):
        username = self.data.get("username")
        user_with_the_same_username = User.objects.filter(username=username)        
        if user_with_the_same_username.count()==1:
            raise forms.ValidationError("This user already exists! Please choose another username.")
        
        return username

    def clean_password(self, *args, **kwargs):
        password = self.data.get("password")
        confirm_password = self.data.get("confirm_password")
        # Password Error
        if(password != confirm_password):
            raise forms.ValidationError("The password you entered doesn't match")
        return password 

    def clean_email(self, *args, **kwargs):
        email = self.data.get('email')
        duplicate_email = User.objects.filter(email=email)
        if duplicate_email.count() > 0:
            raise forms.ValidationError("This email already exists! Please choose another email.")
        return email

    
class UserLogInForm(forms.Form):
    username = forms.CharField(required=True,max_length=20
        ,widget=forms.TextInput(attrs={'class' : 'form-control input-center'}))

    password = forms.CharField(required=True,
        widget=forms.PasswordInput(attrs={'class' : 'form-control input-center'}))


    def login(self):
        data = self.cleaned_data
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        return user

    def clean(self, *args, **kwargs):
        # General Cleaning
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
           
        return super(UserLogInForm, self).clean(*args, **kwargs)
