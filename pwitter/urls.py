import allauth.account.views
from django.urls import path
from .views import profile_list, DashboardView, ProfileDetail
from . import views


app_name = "pwitter"

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path('profile_list/', profile_list, name="profile_list"),
    path('profile/<int:pk>', ProfileDetail.as_view(), name="profile"),
    path('accounts/logout/', allauth.account.views.LogoutView.as_view(), name='sign-out'),
    path('delete/<int:pk>', views.pweet_delete, name='pweet_delete'),
    path('/<int:pk>', views.like_view, name='like_pweet'),
    path('/reply/<int:pk>', views.reply_like_view, name='like_reply'),
    path('register', views.register_request, name='register'),
]
