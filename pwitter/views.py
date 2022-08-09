from django.contrib.auth import logout, login
from django.http import HttpRequest, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .models import Profile, Picture, Pweet, PweetReply
from .forms import PweetForm, NewUserForm
from django.views.generic import View
from django.contrib import messages


def like_view(request, pk):
    if request.method == 'POST':
        pweet = get_object_or_404(Pweet, pk=pk)
        pweet.likes.add(request.user)
        return redirect('/')
    return render(request, 'dashboard.html')


def reply_like_view(request, pk):
    if request.method == 'POST':
        reply = get_object_or_404(PweetReply, pk=pk)
        reply.likes.add(request.user)
        return redirect('pwitter:dashboard')
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

@login_required
def pweet_delete(request, pk):
    pweet = get_object_or_404(Pweet, pk=pk)
    if request.user.username == pweet.user.username:
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


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('pwitter:dashboard')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name='registration/register.html', context={"register_form":form})


class SignedOutView(TemplateView):
    template_name = 'registration/signed_out.html'

    def get(self, request: HttpRequest):
        logout(request)
        return render(request, self.template_name)
