from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as lgin, logout as lgout
from django.contrib.auth.decorators import login_required
from .forms import CartItemForm, SignupForm, LoginForm
from .models import Cart, Product

def get_cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except:
        cart = Cart(user=request.user)
        cart.save()
    return cart

# Create your views here.
def index(request):
    cart = get_cart(request)
    return render(request, "index.html", {'cart': cart})

@login_required
def checkout(request):
    return render(request, "checkout.html")

def product_details(request, id):
    product = Product.objects.get(id=id)
    if (not product):
        return redirect('index')
    
    return render(request, "product.html")

def add_to_cart(request):
    if request.method == 'POST':
        form = CartItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(f'products/{form.cleaned_data["product"].id}')
    return redirect('index')

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                lgin(request, user)
                try:
                    if request.session["redirect_uri"]:
                        return redirect(request.session["redirect_uri"])
                except:
                    return redirect('index')
                return redirect('index')
    else:
        form = LoginForm()
    return render(request, "login.html", {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, "signup.html", {'form': form})

def logout(request):
    lgout(request)
    return redirect('login')

def blank(request):
    return render(request, "checkout.html")
