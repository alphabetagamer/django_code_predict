from django.shortcuts import render
from django.http import HttpResponse
from .models import code_page, progress
from django.contrib.auth.decorators import login_required


def home(request):
    # we use code_pr/home.html because it then looks for code_pr folder in templates folder
    return render(request, "code_pr/home.html")


# Create your views here.
def about(request):
    return render(request, "code_pr/about.html")


@login_required
def code_here(request):
    context = {"pages": code_page.objects.all()}
    return render(request, "code_pr/code.html", context)


@login_required
def problem(request, id=-1):
    if request.method == "POST":
        page_det = code_page.objects.filter(id=id)
        data = request.POST
        answer = data.get("answer")
        stat = False
        error = False
        result = code_check({"answer": answer, "questionType": page_det[0].title})
        if result == "correct answer":
            stat = True
        else:
            error = result
        try:
            prog = progress.objects.get(user=request.user, id_code=id)
            if prog.prog != "True":
                prog.prog = stat
                prog.save()
        except Exception as e:
            prog = progress(user=request.user, id_code=id, prog=stat)
            prog.save()
        context = {
            "page": page_det[0],
            "result": stat,
            "error": error,
            "answer": answer,
        }

        return render(request, "code_pr/problem_page.html", context)
    else:
        if id == -1:
            return render(request, "code_pr/404.html")
        else:
            page_det = code_page.objects.filter(id=id)
            lang = [i.id for i in code_page.objects.all()]
            lang = set(lang)
            context = {"page": page_det[0], "lang": lang}
            return render(request, "code_pr/problem_page.html", context)


### Sanvi code
def code_check(input_request):
    if input_request["questionType"] == "typecastingstring":
        try:
            assert input_request["answer"].find("str(3)") > -1
        except Exception as e:
            return "to typecast any integer to string in python, we should use str(input), so instead write str(3)"
        return "correct answer"
    elif input_request["questionType"] == "typecastingfloat":
        try:
            assert input_request["answer"].find("float(3)") > -1
        except Exception as e:
            return "to typecast any integer to float in python, we should use float(input), so instead write float(3)"
        return "correct answer"
    elif input_request["questionType"] == "lengthoflist":
        try:
            assert input_request["answer"].find("len(inlist)".lower()) > -1
        except Exception as e:
            return "to check the length of the list we should use len(input) function"
        return "correct answer"
    elif input_request["questionType"] == "appending":
        try:
            assert (
                input_request["answer"].find("append('apple')".lower()) > -1
                or input_request["answer"].find('append("apple")'.lower()) > -1
            )
        except Exception as e:
            return "to add the element in the list we should use append function"
        return "correct answer"
    elif input_request["questionType"] == "initialisetupleoneitem":
        try:
            assert (
                input_request["answer"]
                .replace(" ", "")
                .lower()
                .find("tuple(apple , )".replace(" ", "").lower())
                > -1
            )
        except Exception as e:
            return "to add the element in the list we should use append function"
        return "correct answer"
    elif input_request["questionType"] == "usingsets":
        try:
            assert (
                input_request["answer"]
                .replace(" ", "")
                .lower()
                .find("set(inlist)".replace(" ", "").lower())
                > -1
            )
        except Exception as e:
            return "to remove duplicates from list, we should use set(input)"
        return "correct answer"
    elif input_request["questionType"] == "dictionary":
        try:
            assert (
                input_request["answer"]
                .replace(" ", "")
                .lower()
                .find("car['model']".replace(" ", "").lower())
                > -1
                or input_request["answer"]
                .replace(" ", "")
                .lower()
                .find('car["model"]'.replace(" ", "").lower())
                > -1
            )
        except Exception as e:
            return "to access value of particular key in dictionary write it as dictionaryname[key]"
        return "correct answer"
