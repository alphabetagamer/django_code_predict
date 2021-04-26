from django.shortcuts import render
from django.http import HttpResponse
from .models import code_page, progress
from django.contrib.auth.decorators import login_required
from django.db.models import Q


def home(request):
    # we use code_pr/home.html because it then looks for code_pr folder in templates folder
    result = []
    if request.method == "POST":
        query = str(request.POST.get("query"))
        result = list(
            code_page.objects.filter(Q(title__contains=query) | Q(desc__contains=query))
        )
        print(query)
    context = {"result": result}
    return render(request, "code_pr/home.html", context=context)


# Create your views here.
def about(request):
    return render(request, "code_pr/about.html")


@login_required
def code_here(request):
    context = {"pages": code_page.objects.all()}

    try:
        switch = code_page.objects.get(title="Type Casting Float")
    except code_page.DoesNotExist:
        temp = code_page(
            title="Typecast Integer to String",
            desc="Typecast a number (3) to String",
            content="https://www.youtube.com/embed/GMMuxLVgxTs",
        )
        temp.save()
        temp = code_page(
            title="Type Casting Float",
            desc="Typecast a number (3) to Float",
            content="https://www.youtube.com/embed/GMMuxLVgxTs",
        )
        temp.save()
        temp = code_page(
            title="Length Of List",
            desc="Find the Length of a list",
            content="https://www.youtube.com/embed/lnTq2kjUzhw",
        )
        temp.save()
        temp = code_page(
            title="Appending",
            desc="Append to a list",
            content="https://www.youtube.com/embed/lnTq2kjUzhw",
        )
        temp.save()
        temp = code_page(
            title="Initialise Tuple One Item",
            desc="Initialize a tuple item",
            content="https://www.youtube.com/embed/lv_Z6loukOs",
        )
        temp.save()
        temp = code_page(
            title="Using Sets",
            desc="Learn about using Sets",
            content="https://www.youtube.com/embed/2u_ZExcNBzA",
        )
        temp.save()
        temp = code_page(
            title="Dictionary",
            desc="Learn about Dictionary",
            content="https://www.youtube.com/embed/z7z_e5-l2yE",
        )
        temp.save()

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
            print(page_det[0])
            return render(request, "code_pr/problem_page.html", context)


def code_check(input_request):
    if (
        input_request["questionType"] == "typecastingstring"
        or input_request["questionType"] == "Typecast Integer to String"
    ):
        try:
            assert input_request["answer"].find("str(3)") > -1
        except Exception as e:
            return "to typecast any integer to string in python, we should use str(input), so instead write str(3)"
        return "correct answer"
    elif input_request["questionType"] == "Type Casting Float":
        try:
            assert input_request["answer"].find("float(3)") > -1
        except Exception as e:
            return "to typecast any integer to float in python, we should use float(input), so instead write float(3)"
        return "correct answer"
    elif input_request["questionType"] == "Length Of List":
        try:
            assert input_request["answer"].find("len(".lower()) > -1
        except Exception as e:
            return "to check the length of the list we should use len(input) function"
        return "correct answer"
    elif input_request["questionType"] == "Appending":
        try:
            assert (
                input_request["answer"].find("append('apple')".lower()) > -1
                or input_request["answer"].find('append("apple")'.lower()) > -1
            )
        except Exception as e:
            return "to add the element in the list we should use append function"
        return "correct answer"
    elif input_request["questionType"] == "Initialise Tuple One Item":
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
    elif input_request["questionType"] == "Using Sets":
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
    elif input_request["questionType"] == "Dictionary":
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
