from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import FileExtensionValidator

from .models import Pweet, Profile, PweetReply
from django.contrib.auth.models import User

class PweetReplyForm(forms.ModelForm):
    reply_body = forms.CharField(required=True,
                           widget=forms.widgets.Textarea(
                               attrs={
                                   "placeholder": "Reply...",
                                   "class": "textarea is-success is-small",
                               }
                           ),
                           label="",
                           )

    class Meta:
        model = PweetReply
        exclude = ('created_at', 'likes')


class ChangeProfilepicForm(forms.ModelForm):
    user_image = forms.FileField()

    class Meta:
        model = Profile
        fields = ('user_image',)


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
    class Meta:
        model = User
        fields = ('username', 'email',)

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

# class PictureForm(forms.ModelForm):
#
#     class Meta:
#         model = Picture
#         exclude = ('user',)
