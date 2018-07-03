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

	def update(self, *args, **kwargs):
		data = self.cleaned_data
		board_name = data["board_name"]
		update_board = args[0]
		update_board.name = board_name
		update_board.save()
		return update_board

	def archive(self, *args, **kwargs):
		archive_board = args[0]
		archive_board.archived = True
		archive_board.save()


