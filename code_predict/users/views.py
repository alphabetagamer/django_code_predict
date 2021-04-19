import code_predict
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from code_pr.models import progress, code_page


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


@login_required
def profile(request):
    data = progress.objects.filter(user=request.user)
    temp = []
    txt = ""
    if data:
        for pro in data:
            details = code_page.objects.get(id=pro.id_code)
            if pro.prog != "False":
                txt = "Done"
            else:
                txt = "Attempted but not passed"
            temp.append({"title": details.title, "status": txt, "id": pro.id_code})
    return render(
        request,
        "users/profile.html",
        {
            "progress": temp,
            "user": request.user,
        },
    )


# Create your views here.
