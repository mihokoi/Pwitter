from django.urls import path, include

from .views import dashboard, profile_list, profile, DashboardView
from . import views


app_name = "pwitter"

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path('profile_list/', profile_list, name="profile_list"),
    path('profile/<int:pk>', profile, name="profile"),
    path('accounts/logout/', views.logout_page.as_view(), name='logout-page')

]
