from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from .models import Board, BoardMember
from .forms import BoardModalForm
from annoying.functions import get_object_or_None
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseBadRequest
from django.shortcuts import reverse

class IndexView(TemplateView):
    """
        Views for the Index Page
    """
    template_name = "boards/index.html"
    form = BoardModalForm

    def show_boards(self, user):
        boards = BoardMember.objects.filter(user=user,board__archived=False)
        # This code allows the template to count the current board
        count = 0
        for board in boards:
            board.count = count
            count+=1
            if count == 5:
                count = 0
        return boards


    def get(self, *args,** kwargs):
        if self.request.user.is_authenticated:
            context = self.form()
            username = self.kwargs.get('username')
            user = get_object_or_404(User,username=username)
            boards = self.show_boards(user)
            return render(self.request, self.template_name, {'form':context, 'boards': boards})
        else:
            return HttpResponseRedirect(reverse('users:log_in'))
    
    def post(self, *args,** kwargs):
        if self.request.user.is_authenticated:
            form = self.form(self.request.POST)
            username = self.request.user.get_username()
            user = get_object_or_404(User,username=username)
            if form.is_valid():
                form.save(user)
                boards = self.show_boards(user)
                return render(self.request, self.template_name, {'form':form, 'boards': boards})
            else:
                boards = self.show_boards(user)
                return render(self.request, self.template_name, {'form':form, 'boards': boards})
        else:
            return HttpResponseRedirect(reverse('users:log_in'))


    

class BoardView(TemplateView):
    template_name = "boards/boards.html"
    form = BoardModalForm

    def get(self, *args,** kwargs):
        if self.request.user.is_authenticated:
            return render(self.request, self.template_name, {})
        else:
            return HttpResponseRedirect(reverse('users:log_in'))
    
    def post(self, *args,** kwargs):
        if self.request.user.is_authenticated:
            return render(self.request, self.template_name, {})
        else:
            return HttpResponseRedirect(reverse('users:log_in'))