
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include("pwitter.urls")),
    path('admin/', admin.site.urls),
]
