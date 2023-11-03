from django import forms


class CreateEmailForm(forms.Form):
    email = forms.EmailField()
