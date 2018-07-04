from django import forms
from .models import Board, BoardMember, Referral
from annoying.functions import get_object_or_None
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from .models import User
from django.shortcuts import reverse
from django.contrib.auth import logout, authenticate, login
from django.core.mail import send_mail

class BoardModalForm(forms.Form):



    board_name = forms.CharField(max_length=30,
        required=True, widget=forms.TextInput(attrs={'class' : 'form-control sign-up-input'}))

    def save_board(self, user):
        new_board = Board(name=self.cleaned_data.get('board_name'), owner=user)
        new_board.save()

    def update_board(self, board):
        board.name = self.cleaned_data.get('board_name')
        board.save()
        return board

    def archive_board(self, board):
        board.archived = True
        board.save()

class MembersModalForm(forms.Form):

    def __init__(self, *args, **kwargs):
        # This would allow the passing of variables to the clean method
        # Returns None if no value is passed
        self.board_id = kwargs.pop('board_id', None)
        super(MembersModalForm, self).__init__(*args, **kwargs)

    email = forms.CharField(max_length=100,
        required=True, widget=forms.TextInput(attrs={'class' : 'form-control sign-up-input'}))

    def invite(self, host, username, board):
        email = self.cleaned_data.get('email')
        # Creating New Referral
        new_referral = Referral(email=email)
        new_referral.generate_token()
        validation_url = (reverse('boards:user_validation', 
            kwargs={'token':new_referral.token}))

        # formatting string to send
        full_activation_link = f'{host}{validation_url}'
        full_message = ("{} has invited you to join '{}' board! \n" 
                "Click the link to join the board. \n{}").format(username,board.name,full_activation_link)
             
        send_mail(
            'Invitation Request',
            full_message,
            settings.EMAIL,
            [email],
            fail_silently=False,
        )

        # Passing in the instance so that the board member can save the board
        new_referral.board = board

        # Gets if the email has a user
        user = get_object_or_None(User, email=email)
        new_referral.user = user
        new_referral.save()

    def clean_email(self):
        # Checking if the email is already a board member or already invited
        email=self.data.get("email")
        exists = get_object_or_None(
                BoardMember, user__email=email, board__id=self.board_id)
        if exists:
            raise forms.ValidationError("This user is already a board member!")

        exists = get_object_or_None(
                Referral, email=email, board_member__board__id=self.board_id
            )
        if exists:
            raise forms.ValidationError("This user is already invited!")
        return email



class UserValidationForm(forms.Form):
    username = forms.CharField(max_length=20,
        required=True, widget=forms.TextInput(attrs={'class' : 'form-control sign-up-input'}))
    password = forms.CharField(
        required=True, widget=forms.PasswordInput(attrs={'class' : 'form-control sign-up-input'})
        )

    confirm_password = forms.CharField(
        required=True, widget=forms.PasswordInput(attrs={'class' : 'form-control sign-up-input'})
        )


    def save(self, *args, **kwargs):

        data = self.cleaned_data
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        new_user = User.objects.create_user(username, email, password)
        new_user.first_name = data["username"]
        new_user.last_name = [""]
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

    def login(self, request, user):
        login(request, user)
        return user


    def join_board(self, user, token):
        referral = get_object_or_None(Referral, token=token)
        if referral.board_member.user:
            board_member=referral.board_member
            board_member.is_confirmed = True
        else:
            board_member=referral.board_member
            board_member.is_confirmed = True
            board_member.user = user
        # cleaning all the referral tokens that was generated by the invite
        Referral.objects.filter(board_member=board_member).delete()
        board_member.save()
        return board_member.board.id