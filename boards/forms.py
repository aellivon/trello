from django import forms
from .models import Board, BoardMember

class BoardModalForm(forms.Form):
	board_name = forms.CharField(max_length=30,
        required=True, widget=forms.TextInput(attrs={'class' : 'form-control sign-up-input'}))

	def save(self, user):
		new_board = Board(name=self.cleaned_data('board_name'), owner=user)
		new_board.save()

	def update(self, board):
		board.name = self.cleaned_data('board_name')
		board.save()
		return board

	def archive(self, board):
		board.archived = True
		board.save()


