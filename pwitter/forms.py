from django import forms
from .models import Pweet, Picture
from .widgets import PictureWidget

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
        exclude = ("user", "picture")



class PictureForm(forms.ModelForm):

    class Meta:
        model = Picture
        exclude = ('user',)



