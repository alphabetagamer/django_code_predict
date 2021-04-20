from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.home, name="site-home"),
    path("about/", views.about, name="about"),
    path("code/", views.code_here, name="code"),
    path("code/<int:id>/", views.problem, name="problem"),
]