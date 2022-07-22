from django import forms
from .models import Pweet


class PweetForm(forms.ModelForm):
    body = forms.CharField(required=True,
                           widget=forms.widgets.Textarea(
                               attrs={
                                   "placeholder": "Pweet something...",
                                   "class": "textarea is-success is-medium",
                               }
                           ),
                           label="",
                           )

    class Meta:
        model = Pweet
        exclude = ("user",)
