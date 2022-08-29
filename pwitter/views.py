from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .models import Profile, Picture, Pweet, PweetReply
from .forms import PweetForm, NewUserForm, ChangeProfilepicForm, PweetReplyForm
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



class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):
        pweet_form = PweetForm(request.POST or None)
        reply_form = PweetReplyForm(request.POST or None)
        return render(request, self.template_name, {'pweet_form': pweet_form,
                                                    'reply_form': reply_form})

    def post(self, request, *args, **kwargs):
        pweet_form = PweetForm(request.POST, request.FILES)
        reply_form = PweetReplyForm(request.POST)
        if pweet_form.is_valid():
            pweet = pweet_form.save(commit=False)
            pweet.user = request.user
            pweet.save()
            image = Picture(user=request.user, picture=pweet.pweet_image, pweet_id=pweet.pk)
            image.save()
            return redirect('pwitter:dashboard')
        elif reply_form.is_valid():
            reply = reply_form.save(commit=False)
            reply.user = self.request.user
            reply_form.save()
            return redirect('pwitter:dashboard')

        print(request.POST)
        return render(request, self.template_name, {'pweet_form': pweet_form,
                                                    'reply_form': reply_form})

@login_required
def pweet_delete(request, pk):
    pweet = get_object_or_404(Pweet, pk=pk)
    if request.user.username == pweet.user.username:
        if request.method == 'POST':
            pweet.delete()
            return redirect('/')
        return render(request, 'dashboard.html')



@login_required
def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, "profile_list.html", {"profiles": profiles})


class ProfileDetail(LoginRequiredMixin, View):
    template_name = 'profile.html'

    def get_object(self):
        try:
            obj = Profile.objects.get(pk=self.kwargs['pk'])
        except Profile.DoesNotExist:
            raise Http404('Profile not found!')
        return obj

    def get_context_data(self, **kwargs):
        kwargs['profile'] = self.get_object()
        if 'change_profile_pic_form' not in kwargs:
            kwargs['change_profile_pic_form'] = ChangeProfilepicForm()
        return kwargs

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        ctxt = {}

        if 'follow' in request.POST:
            profile_ = Profile.objects.get(pk=self.get_object().pk)
            current_user_profile = request.user.profile
            data = request.POST
            action = data.get("follow")
            if action == "follow":
                current_user_profile.follows.add(profile_)
            elif action == "unfollow":
                current_user_profile.follows.remove(profile_)
            current_user_profile.save()

        elif 'change_profile_pic_form' in request.POST:
            change_profile_pic_form = ChangeProfilepicForm(request.POST, request.FILES, instance=request.user.profile)

            if change_profile_pic_form.is_valid():
                prof = change_profile_pic_form
                prof.user_image = request.FILES
                prof.save()


            else:
                ctxt['change_profile_pic_form'] = change_profile_pic_form
        return render(request, self.template_name, self.get_context_data(**ctxt))



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
