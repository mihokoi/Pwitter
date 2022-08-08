from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import profile_list, profile, DashboardView, SignedOutView
from . import views


app_name = "pwitter"

urlpatterns = [
    path("", login_required(DashboardView.as_view()), name="dashboard"),
    path('profile_list/', profile_list, name="profile_list"),
    path('profile/<int:pk>', profile, name="profile"),
    path('signed-out/', SignedOutView.as_view(), name='sign-out'),
    path('delete/<int:pk>', views.pweet_delete, name='pweet_delete'),
    path('/<int:pk>', views.like_view, name='like_pweet'),
    # path('login/', views.LoginView)
]
