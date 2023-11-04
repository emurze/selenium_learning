from django import forms

from apps.panel.models import Woman


class CreateEmailForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'email'})
    )


class CreateWomanForm(forms.Form):
    url = forms.CharField(max_length=1014, required=False)
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Enter description: [Hairstyle] · [Body shape] '
                               '· [Clothing] · Anything you want to show',
                'maxlength': 500,
                'cols': 0,
                'rows': 0,
            }
        )
    )

    class Meta:
        fields = ('url',)


class CreateWomanFileSystemForm(forms.ModelForm):
    class Meta:
        model = Woman
        fields = ('photo',)
