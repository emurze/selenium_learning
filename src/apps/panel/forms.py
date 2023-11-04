from django import forms


class CreateEmailForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'email'})
    )


class CreateWomanForm(forms.Form):
    url = forms.CharField(max_length=1014)

    class Meta:
        fields = ('url',)
