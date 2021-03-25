from django.shortcuts import render
from django.http import HttpResponse
from .models import code_page


def home(request):
    # we use code_pr/home.html because it then looks for code_pr folder in templates folder
    return render(request, "code_pr/home.html")


# Create your views here.
def about(request):
    return render(request, "code_pr/about.html")


def code_here(request):
    context = {"pages": code_page.objects.all()}
    return render(request, "code_pr/code.html", context)


def problem(request, id=-1):
    if id == -1:
        return render(request, "code_pr/404.html")
    else:
        page_det = code_page.objects.filter(id=id)
        lang = [i.id for i in code_page.objects.all()]
        lang = set(lang)
        context = {"page": page_det[0], "lang": lang}
        return render(request, "code_pr/problem_page.html", context)
