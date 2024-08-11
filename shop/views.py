from django.shortcuts import render, redirect
from django.template.defaulttags import register
from django.contrib.auth import authenticate, login as lgin, logout as lgout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import SignupForm, LoginForm
from .models import Cart, CartItem, Product


@register.filter(name="split")
def split(value, key):
    value.split("key")
    return value.split(key)


def get_cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        print(cart.items.all())
    except Exception:
        cart = None
    return cart


def paginate_products(request, products):
    page = request.GET.get("page", 1)
    paginator = Paginator(products, 10)
    try:
        products = paginator.get_page(page)
    except PageNotAnInteger:
        products = paginator.get_page(1)
    except EmptyPage:
        products = paginator.get_page(paginator.num_pages)
    return products


# Create your views here.
def index(request):
    return render(request, "index.html")


@login_required
def checkout(request):
    return render(request, "checkout.html")


def products(request):
    products = Product.objects.all()
    page_obj = paginate_products(request, products)
    return render(request, "productlist.html", {"page_obj": page_obj})


def product_details(request, id):
    product = Product.objects.get(id=id)
    if not product:
        return redirect("index")

    return render(request, "product.html", {"product": product})


def search(request):
    query = request.GET.get("q")
    category = request.GET.get("c")
    if category != "all":
        products = Product.objects.filter(
            title__icontains=query, category__name__icontains=category
        )
    else:
        products = Product.objects.filter(title__icontains=query)
    page_obj = paginate_products(request, products)
    return render(
        request,
        "productlist.html",
        {"page_obj": page_obj, "query": query, "selected_category": category},
    )


@login_required
def cart(request):
    cart = get_cart(request)
    items = cart.items.all()
    return render(request, "cart.html", {"cart": cart, "items": items})


@login_required
def remove_from_cart(request):
    cart = get_cart(request)
    cart_item = CartItem.objects.get(id=request.GET["item"])
    cart_item.delete()
    return redirect("cart")


@login_required
def add_to_cart(request):
    cart = get_cart(request)
    if not cart:
        cart = Cart.objects.create(user=request.user)
    product = Product.objects.get(id=request.GET["product"])
    size = request.GET["size"]
    color = request.GET["color"]
    quantity = request.GET["qty"]
    cart_item = CartItem.objects.create(
        cart=cart, product=product, size=size, color=color, quantity=quantity
    )
    return redirect("cart")
    # form = CartItemForm(request.POST)
    # if form.is_valid():
    #     cart = get_cart(request)
    #     if not cart:
    #         cart = Cart.objects.create(user=request.user)
    #     cart_item = CartItem()
    #     cart_item.cart = cart
    #     cart_item.product = form.cleaned_data["product"]
    #     cart_item.size = form.cleaned_data["size"]
    #     cart_item.color = form.cleaned_data["color"]
    #     cart_item.quantity = form.cleaned_data["quantity"]
    #     cart_item.save()
    #     return redirect("cart")
    #     # return redirect(f'products/{form.cleaned_data["product"].id}')
    # else:
    #     print(form.errors)
    #     return redirect("products")


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                lgin(request, user)
                if request.GET.get("next"):
                    return redirect(request.GET["next"])
                try:
                    if request.session["redirect_uri"]:
                        return redirect(request.session["redirect_uri"])
                except:
                    return redirect("index")
                return redirect("index")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = SignupForm()
    return render(request, "signup.html", {"form": form})


def logout(request):
    lgout(request)
    return redirect("login")


def blank(request):
    return render(request, "productlist.html")
