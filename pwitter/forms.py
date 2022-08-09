from django import forms
from django.contrib.auth.forms import UserCreationForm



from .models import Pweet, Picture
from django.contrib.auth.models import User


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


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



