from django.shortcuts import render,redirect
from .models import Profile
from .forms import PweetForm



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
    return render(request, "dashboard.html", {"form": form})


def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, "profile_list.html", {"profiles": profiles})


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

