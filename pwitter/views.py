from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView
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

    # def detail(self, request, id):
    #     pweet = get_object_or_404(Pweet, id=id)
    #     replies = pweet.replies.all()
    #     return render(request, 'detail.html', {'pweet': pweet, 'replies': replies})
    #
    # def replyComment(self, request, id):
    #     replies = PweetReply.objects.get(id=id)
    #     if request.method == "POST":
    #         replier_name = request.user
    #         reply_body = request.POST.get('reply_body')
    #
    #         newReply = PweetReply(user=replier_name, reply_body=reply_body)

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
            reply_form.user = request.user
            # reply_form.pweet =
            reply_form.save()

            reply.save()
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



# @login_required
# def dashboard(request):
#     if request.method =="GET":
#         form = PweetForm(request.POST or None)
#     if request.method == "POST":
#         form = PweetForm(request.POST or None)
#         if form.is_valid():
#             pweet = form.save(commit=False)
#             pweet.user = request.user
#             pweet.save()
#             return redirect("pwitter:dashboard")
#         else:
#             return redirect("pwitter:dashboard")
#     return render(request, "dashboard.html", {"form": form})


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
        # if 'follow_form' not in kwargs:
        #     kwargs['follow_form'] = Profile.objects.get(pk=self.get_object().pk)
        #     # kwargs['follow_form'] = ChangeProfileFollowForm()
        # print(kwargs)
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

        # if 'follow_form' in request.POST:
        #     change_profile_follow = ChangeProfileFollowForm(request.POST, instance=request.user.profile)
        #     if change_profile_follow.is_valid():
        #         change = change_profile_follow
        #         change.follows.add

        elif 'change_profile_pic_form' in request.POST:
            change_profile_pic_form = ChangeProfilepicForm(request.POST, request.FILES, instance=request.user.profile)

            if change_profile_pic_form.is_valid():
                prof = change_profile_pic_form
                prof.user_image = request.FILES
                prof.save()


            else:
                ctxt['change_profile_pic_form'] = change_profile_pic_form
        return render(request, self.template_name, self.get_context_data(**ctxt))




# @login_required
# def profile(request, pk):
#     if not hasattr(request.user, 'profile'):
#         missing_profile = Profile(user=request.user)
#         missing_profile.save()
#
#     profile = Profile.objects.get(pk=pk)
#     # if request.method == "POST" and "changeprofilepicform" in request.POST:
#     #     form = ChangeProfilepicForm(request.POST)
#     #     if form.is_valid():
#     #         profile_ = form.save(commit=False)
#     #         profile_.save()
#     #         return redirect("pwitter:profile")
#     #     else:
#     #         return redirect("pwitter:profile")
#     print(request.POST)
#     if request.method == "POST":
#         current_user_profile = request.user.profile
#         data = request.POST
#         print(data)
#         print("kutaz")
#         action = data.get("follow")
#         if action == "follow":
#             current_user_profile.follows.add(profile)
#         elif action == "unfollow":
#             print(data)
#             current_user_profile.follows.remove(profile)
#         current_user_profile.save()
#     return render(request, "profile.html", {"profile": profile})




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
