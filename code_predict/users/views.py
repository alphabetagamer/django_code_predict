from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request, f"Account created for {username}! You can now login."
            )
            return redirect("login")
    # we use code_pr/home.html because it then looks for code_pr folder in templates folder
    else:
        form = UserRegisterForm()

    return render(request, "users/register.html", {"form": form})


# Create your views here.
