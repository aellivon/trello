from django.shortcuts import render
from .models import User
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from .models import Board, BoardMember
from .forms import BoardModalForm
from annoying.functions import get_object_or_None
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseBadRequest
from django.shortcuts import reverse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(LoginRequiredMixin,TemplateView):
    """
        Views for the Index Page
    """
    login_url = reverse_lazy('users:log_in')
    template_name = "boards/index.html"
    form = BoardModalForm

    def get(self, *args,** kwargs):
        context = self.form()
        username = self.kwargs.get('username')
        user = get_object_or_404(User,username=username)
        boards = BoardMember.objects.filter(user=user,board__archived=False)
        return render(self.request, self.template_name, {'form':context, 'boards': boards})

    
    def post(self, *args,** kwargs):
        form = self.form(self.request.POST)
        username = self.request.user.get_username()
        user = get_object_or_404(User,username=username)
        if form.is_valid():
            form.save(user)
            boards = BoardMember.objects.filter(user=user,board__archived=False)
            return render(self.request, self.template_name, {'form':form, 'boards': boards})
        else:
             boards = BoardMember.objects.filter(user=user,board__archived=False)
        
        return render(self.request, self.template_name, {'form':form, 'boards': boards})


class BoardView(LoginRequiredMixin,TemplateView):
    login_url = reverse_lazy('users:log_in')
    template_name = "boards/boards.html"
    update_form = BoardModalForm

    def get(self, *args,** kwargs):
        update_form = self.update_form()
        board_id = self.kwargs.get('id')
        data = get_object_or_404(Board,pk=board_id)
        return render(self.request, self.template_name, {'update_form':update_form,'data':data})

    def post(self, *args,** kwargs):
        if 'EditModal' in self.request.POST:
            update_form = self.update_form(self.request.POST)
            username = self.request.user.get_username()
            user = get_object_or_404(User,username=username)
            board_id = self.kwargs.get('id')
            board = get_object_or_404(Board,pk=board_id)
            if board.owner == user:
                if update_form.is_valid():
                    board = update_form.update(board_id)
                    update_form = self.update_form()
                    return render(self.request, self.template_name, {'update_form':update_form,'data':board})
            return render(self.request, self.template_name, {'update_form':update_form,'data':board})
        else:
            return HttpResponseRedirect(reverse('users:log_in'))
