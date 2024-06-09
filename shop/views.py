from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, "index.html")


def landing(request):
    return render(request, "landing.html")


def generic(request):
    return render(request, "generic.html")


def elements(request):
    return render(request, "elements.html")
