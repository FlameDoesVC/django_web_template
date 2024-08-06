from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, "index.html")

def checkout(request):
    return render(request, "checkout.html")

def product_details(request):
    return render(request, "product.html")

def login_view(request):
    return render(request, "login.html")