from django.contrib.auth import logout
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import TemplateView
from .models import Profile, Picture, Pweet
from .forms import PweetForm
from django.views.generic import View, ListView

def like_view(request, pk):
    if request.method == 'POST':
        pweet = get_object_or_404(Pweet, pk=pk)
        print(pweet)
        pweet.likes.add(request.user)
        print(pweet.likes.all())
        return redirect('/')
    return render(request, 'dashboard.html')


class DashboardView(View):
    form_class = PweetForm
    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            pweet = form.save(commit=False)
            pweet.user = request.user
            pweet.save()
            image = Picture(user=request.user, picture=pweet.pweet_image, pweet_id=pweet.pk)
            image.save()
            return redirect('pwitter:dashboard')
        return render(request, self.template_name, {'form': form})

def pweet_delete(request, pk):
    pweet = get_object_or_404(Pweet, pk=pk)
    if request.method == 'POST':
        pweet.delete()
        return redirect('/')
    return render(request, 'dashboard.html')


@login_required
def dashboard(request):
    if request.method =="GET":
        form = PweetForm(request.POST or None)
    if request.method == "POST":
        form = PweetForm(request.POST or None)
        if form.is_valid():
            pweet = form.save(commit=False)
            pweet.user = request.user
            pweet.save()
            return redirect("pwitter:dashboard")
        else:
            return redirect("pwitter:dashboard")
    return render(request, "dashboard.html", {"form": form})


@login_required
def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, "profile_list.html", {"profiles": profiles})


@login_required
def profile(request, pk):
    if not hasattr(request.user, 'profile'):
        missing_profile = Profile(user=request.user)
        missing_profile.save()

    profile = Profile.objects.get(pk=pk)
    if request.method == "POST":
        current_user_profile = request.user.profile
        data = request.POST
        action = data.get("follow")
        if action == "follow":
            current_user_profile.follows.add(profile)
        elif action == "unfollow":
            current_user_profile.follows.remove(profile)
        current_user_profile.save()
    return render(request, "profile.html", {"profile": profile})


class SignedOutView(TemplateView):
    template_name = 'registration/signed_out.html'

    def get(self, request: HttpRequest):
        logout(request)
        return render(request, self.template_name)
