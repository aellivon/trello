from django.shortcuts import render
from .models import User
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, View
from .models import Board, BoardMember, Referral, Column, Card, CardComment, CardMember
from .forms import BoardModalForm, MembersModalForm, UserValidationForm
from annoying.functions import get_object_or_None
from django.http import (HttpResponse, HttpResponseRedirect,
    HttpResponseBadRequest, JsonResponse)
from django.shortcuts import reverse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import AJAXBoardMixIn, AJAXCardMixIn, BoardPermissionMixIn
from users.mixins import ThrowHomeIfLoggedInMixIn
from django.contrib.auth import logout, authenticate, login
from django.http import JsonResponse
import json as simplejson
from django.core import serializers
from django.db.models import Max
import dateutil.parser
import pytz


class IndexView(LoginRequiredMixin,TemplateView):
    """
        Views for the Index Page
    """
    # Reverse lazy is needed since this code is before the Url coniguration
    # is loaded
    login_url = reverse_lazy('users:log_in')
    template_name = "boards/index.html"
    form = BoardModalForm

    def get(self, *args,** kwargs):
        context = self.form()
        username = self.kwargs.get('username')
        user = get_object_or_404(User,username=username)
        boards = BoardMember.objects.filter(
            user=user,board__archived=False,is_confirmed=True).order_by('-pk')
        return render(self.request, self.template_name,
            {'form':context, 'boards': boards, 'current_user' : username}
        )

    
    def post(self, *args,** kwargs):
        form = self.form(self.request.POST)
        username = self.request.user.get_username()
        user = get_object_or_404(User,username=username)
        if form.is_valid():
            form.save_board(user)
            boards = BoardMember.objects.filter(
                user=user,board__archived=False,is_confirmed=True).order_by('-pk')
            form = self.form()
            return render(self.request, self.template_name,
                {'form':form, 'boards': boards, 'current_user' : username}
            )
        else:
             boards = BoardMember.objects.filter(
                user=user,board__archived=False,is_confirmed=True)
        
        return render(self.request, self.template_name, 
            {'form':form, 'boards': boards, 'current_user' : username}
        )


class BoardView(LoginRequiredMixin, TemplateView):
    # Reverse lazy is needed since this code is before the Url coniguration
    # is loaded
    login_url = reverse_lazy('users:log_in')
    template_name = "boards/boards.html"
    board_form = BoardModalForm
    member_form = MembersModalForm


    def get(self, *args,** kwargs):
        board_form = self.board_form()
        member_form = self.member_form()
        board_id = self.kwargs.get('id')
        username = self.request.user.get_username()
        access = get_object_or_404(BoardMember,user__username=username,
            is_confirmed=True,board__id=board_id)
        board = get_object_or_404(Board,pk=board_id)
        board_member = BoardMember.objects.filter(
            board__id=board_id)
        referral = Referral.objects.filter(
            board_member__board__id=board_id).exclude(
                board_member__user=board.owner)
        columns = Column.objects.filter(
            board__id=board_id,archived=False).order_by('position')
        card = Card.objects.filter(
            column__board__id=board_id,archived=False)
        owner = False
        if board.owner == self.request.user:
            owner = True
        return render(self.request, self.template_name,
            {
                'board_form': board_form, 'member_form': member_form,
                'board':board, 'current_user' : username, 'message_box': None,
                'owner' : owner, 'board_member' : board_member, 'columns' : columns,
                'referral' : referral, 'cards': card, 'owner_instance' : board.owner
            }
        )


    def post(self, *args,** kwargs):
        board_id = self.kwargs.get('id')
        username = self.request.user.get_username()
        access = get_object_or_404(BoardMember,user__username=username,
            is_confirmed=True,board__id=board_id)
        board = get_object_or_404(Board,pk=board_id)
        columns = Column.objects.filter(
            board__id=board_id,archived=False).order_by('position')
        owner = False
        board_member = BoardMember.objects.filter(
            board__id=board_id)
        referral = Referral.objects.filter(
            board_member__board__id=board_id).exclude(
            board_member__user=board.owner)
        card = Card.objects.filter(
            column__board__id=board_id,archived=False)
        if board.owner == self.request.user:
            owner = True
        # Edit Board Form
        if 'EditModal' in self.request.POST:
            member_form = self.member_form()
            board_form = self.board_form(self.request.POST)
            if owner == True:
                if board_form.is_valid():
                    board = board_form.update_board(board)
                    board_form = self.board_form()
                    return render(self.request, self.template_name,
                        {
                            'board_form': board_form, 'member_form': member_form,
                            'board':board, 'current_user' : username,
                            'message_box':None, 'owner' : owner,
                            'board_member' : board_member, 'columns' : columns,
                            'referral': referral, 'cards': card,
                            'owner_instance' : board.owner
                        }
                    )
            # Failing validation will render this template below
            return render(self.request, self.template_name,
                {
                 'board_form': board_form, 'member_form': member_form,
                 'board':board, 'current_user' : username,
                 'message_box':None, 'owner' : owner,
                 'board_member' : board_member, 'columns' : columns, 
                 'referral' : referral, 'cards': card, 
                 'owner_instance' : board.owner
                }
            )
        # Archiving Board Form
        elif 'ArchiveBoardModal' in self.request.POST:
            board_form = self.board_form()
            member_form = self.member_form()
            if owner == True:
                board = board_form.archive_board(board)
                return HttpResponseRedirect(reverse('boards:home' , 
                    kwargs={'username': username 
                }))
            # Failing validation will render template below
            return render(self.request, self.template_name,
                {
                    'board_form': board_form, 'member_form': member_form,
                    'board':board, 'current_user' : username,
                    'message_box': None, 'owner' : owner, 'board_member' : board_member,
                     'columns' : columns, 'referral':referral, 'cards': card,
                     'owner_instance' : board.owner
                }
            )
        # Inviting a member form
        elif 'AddMemberModal' in self.request.POST:
            member_form = self.member_form(self.request.POST , board_id=board_id)
            board_form = self.board_form()

            if member_form.is_valid():
                host = self.request.get_host()
                member_form.invite(host, username, board)
                # This function creates an object define the values of the message box modal
                # Currently limited on one button since I don't need multiple buttons
                message_box = {
                        'title' : 'Success', 'message': 'The user is successfully invited',
                        'button' : 'OK'
                    }
                return render(self.request, self.template_name,
                    {
                       'board_form': board_form, 'member_form': member_form,
                       'board':board, 'current_user' : username,
                        'message_box':message_box, 'owner' : owner,
                        'board_member' : board_member, 'columns' : columns,
                        'referral' : referral, 'cards': card,
                        'owner_instance' : board.owner
                    }
                )

            # Falls here if the validation failed
            return render(self.request, self.template_name,
                {
                   'board_form': board_form, 'member_form': member_form,
                   'board':board, 'current_user' : username,
                   'message_box':None, 'owner' : owner,
                    'board_member' : board_member, 'columns' : columns,
                    'referral' : referral, 'cards': card,
                    'owner_instance' : board.owner
                }
            )
        elif 'RemoveMemberModal' in self.request.POST:
            stacked_id_to_remove = self.request.POST.getlist('remove_member')
            member_form = self.member_form()
            board_form = self.board_form()
            member_form.remove_members(stacked_id_to_remove)
            return render(self.request, self.template_name,
                {
                   'board_form': board_form, 'member_form': member_form,
                   'board':board, 'current_user' : username,
                   'message_box':None, 'owner' : owner, 'board_member' : board_member,
                    'columns' : columns, 'referral' : referral, 'cards': card,
                    'owner_instance' : board.owner
                }
            )
        elif 'LeaveConfirmationModal' in self.request.POST:
            member_form = self.member_form()
            board_form = self.board_form()
            user_id = self.request.user.id
            member_form.remove_member(user_id, board)
            return HttpResponseRedirect(reverse('boards:home' , 
                kwargs={'username': username 
            }))




# ajax implementation

class GetBoardDetails(LoginRequiredMixin, BoardPermissionMixIn , AJAXBoardMixIn, View):

    login_url = reverse_lazy('users:log_in')
    def get(self, *args, **kwargs):
        data = self.return_board()
        return JsonResponse(data)

class AddColumnView(LoginRequiredMixin, BoardPermissionMixIn, AJAXBoardMixIn, View):

    login_url = reverse_lazy('users:log_in')
    def post(self, *args, **kwargs):
        title = self.request.POST.get('title')
        board_id = self.kwargs.get('id')

        board = get_object_or_404(Board,pk=board_id)
        max_position=Column.objects.filter(archived=False).aggregate(Max('position'))
        to_add_position = 1 
        maximum_exists = max_position.get('position__max')
        if  maximum_exists:
            to_add_position =   maximum_exists + 1
        new_column = Column(board=board,name=title,position=to_add_position)
        new_column.save()
        data = self.return_board()
        # needs to be changed
        return JsonResponse(data)



class UpdateColumnView(LoginRequiredMixin, BoardPermissionMixIn, AJAXBoardMixIn, View):

    login_url = reverse_lazy('users:log_in')
    def post(self, *args, **kwargs):
        title = self.request.POST.get('title')
        to_update_id = self.request.POST.get('id')
        column=get_object_or_404(Column,id=to_update_id)
        column.name = title
        column.save()
        data = self.return_board()
        # needs to be changed
        return JsonResponse(data)


class ArchiveColumnView(LoginRequiredMixin, BoardPermissionMixIn, AJAXBoardMixIn, View):

    login_url = reverse_lazy('users:log_in')
    def post(self, *args, **kwargs):
        to_update_id = self.request.POST.get('id')
        column=get_object_or_404(Column,id=to_update_id)
        column.archived = True
        column.save()
        data = self.return_board()
        # needs to be changed
        return JsonResponse(data)


class AddCardView(LoginRequiredMixin, BoardPermissionMixIn, AJAXBoardMixIn, View):

    login_url = reverse_lazy('users:log_in')
    def post(self, *args, **kwargs):
        name = self.request.POST.get('name')
        column_id = self.request.POST.get('id')
        column = get_object_or_404(Column,pk=column_id)
        new_card = Card(name=name,column=column)
        new_card.save()
        data = self.return_board()
        return JsonResponse(data)

class GetCardDetails(LoginRequiredMixin, BoardPermissionMixIn, AJAXCardMixIn, View):

    login_url = reverse_lazy('users:log_in')
    def get(self, *args, **kwargs):
        data=self.return_card()
        return JsonResponse(data)

class UpdateCardTitle(LoginRequiredMixin, BoardPermissionMixIn, AJAXCardMixIn, View):

    login_url = reverse_lazy('users:log_in')
    def post(self, *args, **kwargs):
        name =  self.request.POST.get('title')
        card_id = self.request.POST.get('card_id')
        card = get_object_or_404(Card, pk=card_id)
        card.name = name
        card.save()
        data=self.return_card()
        return JsonResponse(data)

class UpdateCardDescription(LoginRequiredMixin, BoardPermissionMixIn, View):

    login_url = reverse_lazy('users:log_in')
    def post(self, *args, **kwargs):
        description =  self.request.POST.get('description')
        card_id = self.request.POST.get('card_id')
        card = get_object_or_404(Card, pk=card_id)
        card.description = description
        card.save()
        return HttpResponse('success!')



class AddCommentCard(LoginRequiredMixin, BoardPermissionMixIn, AJAXCardMixIn, View):

    login_url = reverse_lazy('users:log_in')
    def post(self, *args, **kwargs):
        comment =  self.request.POST.get('comment')
        card_id = self.request.POST.get('card_id')
        if comment != "":
            card = get_object_or_404(Card, pk=card_id)
            new_comment = CardComment(card=card, user=self.request.user, comment=comment)
            new_comment.save()
        data=self.return_card()
        return JsonResponse(data)

class DeleteComment(LoginRequiredMixin, BoardPermissionMixIn, AJAXCardMixIn, View):

    login_url = reverse_lazy('users:log_in')
    def post(self, *args, **kwargs):
        comment_id = self.request.POST.get('comment_id')
        CardComment.objects.get(pk=comment_id).delete()
        data=self.return_card()
        return JsonResponse(data)

class AssignMembers(LoginRequiredMixin, BoardPermissionMixIn, AJAXCardMixIn, View):

    login_url = reverse_lazy('users:log_in')
    def post(self, *args, **kwargs):
        selected = self.request.POST.getlist('selected[]')
        not_selected = self.request.POST.getlist('not_selected[]')
        card_id = self.request.POST.get('card_id')
        card_instance = get_object_or_404(Card,pk=card_id)
        for element in selected:
            board_member = get_object_or_404(BoardMember,user__pk=element)
            new_card_member= CardMember(board_member=board_member,card=card_instance)
            new_card_member.save()

        for element in not_selected:
            CardMember.objects.filter(board_member__user__id=element).delete()

        
        data=self.return_card()
        return JsonResponse(data)

class GetMembers(LoginRequiredMixin, BoardPermissionMixIn, View):

    login_url = reverse_lazy('users:log_in')
    def get(self, *args, **kwargs):
        card_id = self.request.GET.get('card_id')
        card_member = CardMember.objects.filter(
            card__pk=card_id)
        serialized_card_member = serializers.serialize('json', card_member)
        data = {'card_member' : serialized_card_member}
        return JsonResponse(data)

class DueDate(LoginRequiredMixin, BoardPermissionMixIn, View):

    login_url = reverse_lazy('users:log_in')
    def get(self, *args, **kwargs):
        card_id = self.request.GET.get('card_id')
        card = [get_object_or_404(Card,pk=card_id)]
        serialized_card = serializers.serialize('json', card)
        data = {'card' : serialized_card}
        return JsonResponse(data)

    def post(self, *args, **kwargs):
        card_id = self.request.POST.get('card_id')
        card = get_object_or_404(Card,pk=card_id)
        try:
            parsed_date = dateutil.parser.parse(self.request.POST.get('due_date'))
        except Exception as e:
            return HttpResponse(e)

        card.due_date = parsed_date
        card.save()
        return HttpResponse('success!')

class ArhiveCard(LoginRequiredMixin, BoardPermissionMixIn, AJAXBoardMixIn, View):

    login_url = reverse_lazy('users:log_in')
    def post(self, *args, **kwargs):
        print('hi')
        card_id = self.request.POST.get('card_id')
        card = get_object_or_404(Card, pk=card_id)
        card.archived = True
        card.save()
        data = self.return_board()
        return JsonResponse(data)


class UserValidationView(TemplateView):
    """
        Views for the User Validation Page
    """
    template_name = "boards/user_validation.html"
    form = UserValidationForm

    def get(self, *args, **kwargs):
        token = self.kwargs.get('token')
        referral = get_object_or_404(Referral, token=token)
        board = referral.board_member.board
        email = referral.email
        form = self.form()
        if referral:
            # Checking if the user exists
            user = get_object_or_None(User, email=referral.email)
            if user:
                proceed = False
                # Check if the user is already logged in
                if not self.request.user.is_authenticated:
                    user = form.login(self.request, user=user)
                    proceed = True
                else:
                    if self.request.user.email == email:
                        user = self.request.user
                        proceed = True
                       
                if proceed:
                    # falls short when the logged in user is not the same referral email
                    return render(self.request, self.template_name,
                        {'form':form, 'email' : email, 'board': board , 'account' : True}
                    )
            else:
                return render(self.request, self.template_name,
                    {'form':form, 'email' : email, 'board': board, 'account' : False}
                ) 
        return HttpResponseBadRequest()

    def post(self, *args, **kwargs):
        form = self.form(self.request.POST)
        user = self.request.user
        token = self.kwargs.get('token')
        referral = get_object_or_404(Referral, token=token)
        board = referral.board_member.board
        email = referral.email
        if 'JoinBoard' in self.request.POST:
            # User Is Already Registered

            board_id = form.join_board(user, token)
            return HttpResponseRedirect(reverse('boards:board' , kwargs={'id':board_id  }))
        elif 'ReferralSignUp' in self.request.POST:
            if form.is_valid():
                user = form.save(email)
                user = form.login(self.request, user=user)
                board_id = form.join_board(user,token)
                return HttpResponseRedirect(reverse('boards:board' , kwargs={'id':board_id  }))
            else:
                return render(self.request, self.template_name,
                    {'form':form, 'email' : email, 'board': board , 'success': True , 'account' : False}
                ) 
        return HttpResponseBadRequest()

