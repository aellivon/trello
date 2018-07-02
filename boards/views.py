from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from .models import Board, BoardMember
from .forms import IndexModalForm
from annoying.functions import get_object_or_None
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseBadRequest
from django.shortcuts import reverse

class IndexView(TemplateView):
    """
        Views for the Sign Up Page
    """
    template_name = "boards/index.html"
    form = IndexModalForm
    def get(self, *args,** kwargs):
        if self.request.user.is_authenticated:
            context = self.form()
            username = self.kwargs.get('username')
            user = get_object_or_404(User,username=username)
            boards = BoardMember.objects.filter(user=user)
            # This code allows the template to count the current board
            count = 0
            for board in boards:
                board.count = count
                count+=1
                if count == 5:
                    count = 0
            return render(self.request, self.template_name, {'form':context, 'boards': boards})
        else:
            return HttpResponseRedirect(reverse('users:log_in'))
    
    def post(self, *args,** kwargs):
        if self.request.user.is_authenticated:
            form = self.form(self.request.POST)
            if form.is_valid():
                username = self.request.user.get_username()
                user = get_object_or_404(User,username=username)
                form.save(user)
                boards = BoardMember.objects.filter(user=user,archived=False)
                # This code allows the template to count the current board
                count = 0
                for board in boards:
                    board.count = count
                    count+=1
                    if count == 5:
                        count = 0
                return render(self.request, self.template_name, {'form':form, 'boards': boards})
        else:
            return HttpResponseRedirect(reverse('users:log_in'))

