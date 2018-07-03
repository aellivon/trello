from django import forms
from .models import Board, BoardMember

class BoardModalForm(forms.Form):
	board_name = forms.CharField(max_length=30,
        required=True, widget=forms.TextInput(attrs={'class' : 'form-control sign-up-input'}))

	def save(self, *args, **kwargs):
		data = self.cleaned_data
		board_name = data["board_name"]
		user = args[0]
		new_board = Board(name=board_name,owner=user)
		new_board.save()

		new_board_member = BoardMember(user=user,board=new_board)
		new_board_member.is_confirmed = True
		new_board_member.save()

