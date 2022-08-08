from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField

from .models import Pweet, Picture
from django.contrib.auth.models import Group, User


# class UserLoginForm(AuthenticationForm):
#
#     def __init__(self, *args, **kwargs):
#         super(UserLoginForm, self).__init__(*args, **kwargs)
#
#         username = UsernameField(widget=forms.TextInput(
#             attrs={'class': 'form-control', 'placeholder': '', 'id': 'hello'}
#         ))
#         password = forms.CharField(widget=forms.PasswordInput(
#             attrs={
#                 'class': 'form-control',
#                 'placeholder': '',
#                 'id': 'hi',
#             }
#         ))



class UserCreationForm(forms.ModelForm):
    class meta:
        model = User
        fields = ('email',)

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


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
        exclude = ("user", "picture", "likes")



class PictureForm(forms.ModelForm):

    class Meta:
        model = Picture
        exclude = ('user',)



