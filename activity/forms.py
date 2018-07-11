from django import forms


class ActivityForm(forms.Form):
    username = forms.CharField(max_length=30,
        required=True, widget=forms.TextInput(attrs={'class' : 'form-control sign-up-input'}))