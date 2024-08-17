from django.shortcuts import render, redirect
from django.template.defaulttags import register
from django.template.defaultfilters import stringfilter
from django.contrib.auth import authenticate, login as lgin, logout as lgout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import SignupForm, LoginForm
from .models import Cart, CartItem, Order, OrderItem, Product, ShippingAddress


@register.filter(name="split")
def split(value, key):
	value.split("key")
	return value.split(key)

@register.filter(name="in")
@stringfilter
def in_filter(value, key):
	return value in key

@register.filter(name="mult")
def mult(value, key):
	return value * key


def get_cart(request):
	try:
		cart = Cart.objects.get(user=request.user)
		# print(cart.items.all())
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
	return render(request, "index.html", {"active": "home"})


@login_required
def checkout(request):
	cart = get_cart(request)
	if not cart:
		return redirect("cart")
	cart_items = cart.items.all()
	if not cart_items:
		return redirect("cart")
	total = 0
	for item in cart_items:
		total += item.product.price * item.quantity

	shipping_address = ShippingAddress.objects.filter(user=request.user).order_by("-last_used").first()

	if request.method == "POST":
		# check if shipping address id exists in the request
		if request.POST.get("shipping_address_id") and ShippingAddress.objects.filter(id=request.POST["shipping_address_id"]).exists():
			shipping_address = ShippingAddress.objects.get(id=request.POST["shipping_address_id"])
		else:
			shipping_address = ShippingAddress()
			shipping_address.user = request.user
			shipping_address.first_name = request.POST["first_name"]
			shipping_address.last_name = request.POST["last_name"]
			shipping_address.address = request.POST["address"]
			shipping_address.city = request.POST["city"]
			shipping_address.country = request.POST["country"]
			shipping_address.zip_code = request.POST["zip_code"]
			shipping_address.telephone = request.POST["tel"]
			shipping_address.save()
		order = Order()
		order.user = request.user
		order.slug = Order.generate_slug()
		order.total = total
		order.shipping_address = shipping_address
		order.notes = request.POST["notes"]
		order.payment_method = request.POST["payment"]
		order.save()
		for item in cart_items:
			order_item = OrderItem()
			order_item.order = order
			order_item.product = item.product
			order_item.size = item.size
			order_item.color = item.color
			order_item.quantity = item.quantity
			order_item.save()
		cart.items.all().delete()
		cart.delete()
		return redirect(f"/order/{order.slug}")
	else:
		return render(request, "checkout.html", {"cart": cart, "items": cart_items, "total": total, "shipping_address": shipping_address})
	
@login_required
def orderlist(request):
	orders = Order.objects.filter(user=request.user)
	return render(request, "orderlist.html", {"orders": orders})

def order(request, id):
	try:
		order = Order.objects.get(slug=id)
	except Order.DoesNotExist:
		# return redirect("index")
		# return 404
		return render(request, "404.html", status=404)
	
	# if order.user != request.user:
	# 	return
	
	items = order.items.all()
	return render(request, "order.html", {"order": order, "items": items})


def products(request):
	category = request.GET.get("c")
	if not category:
		category = "all"
	if category != "all":
		products = Product.objects.filter(category__name__icontains=category)
	else:
		products = Product.objects.all()
	page_obj = paginate_products(request, products)
	return render(request, "productlist.html", {"page_obj": page_obj, "selected_category": category, "active": category})


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
		{"page_obj": page_obj, "query": query, "selected_category": category, "active": category},
	)


@login_required
def cart(request):
	cart = get_cart(request)
	if not cart:
		return render(request, "cart.html", {"cart": None, "items": None})
	items = cart.items.order_by("added_at").all()
	return render(request, "cart.html", {"cart": cart, "items": items})

@login_required
def update_cart_item(request, item_id):
	cart = get_cart(request)
	cart_item = CartItem.objects.get(id=item_id)
	if cart_item.cart != cart:
		return redirect("cart")

	if request.GET.get("action") == "increment":
		cart_item.quantity += 1
		cart_item.save()
		return redirect("cart")
	if request.GET.get("action") == "decrement":
		cart_item.quantity -= 1
		if cart_item.quantity < 0:
			cart_item.delete()
		else:
			cart_item.save()
		return redirect("cart")
	
	if request.GET.get("action") == "delete":
		cart_item.delete()
		return redirect("cart")
	
	print(request.POST)
	# cart_item.size = request.POST["size"][0]
	# cart_item.color = request.POST["color"][0]
	# cart_item.quantity = request.POST["quantity"][0]
	cart_item.size = request.POST.get("size")
	cart_item.color = request.POST.get("color")
	cart_item.quantity = request.POST.get("quantity")
	cart_item.save()
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
	cart_item = CartItem.objects.filter(cart=cart, product=product, size=size, color=color)
	if cart_item:
		cart_item = cart_item.first()
		cart_item.quantity += int(quantity)
		cart_item.save()
	else:
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
				return redirect("index")
			else:
				form.add_error(None, "Invalid username or password")
	else:
		form = LoginForm()
	return render(
		request, "login.html", {"form": form, "query_str": request.GET.urlencode()}
	)


def signup(request):
	if request.method == "POST":
		form = SignupForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect("login")
	else:
		form = SignupForm()
	return render(request, "signup.html", {"form": form, "query_str": request.GET.urlencode()})


def logout(request):
	lgout(request)
	if request.GET.get("next"):
		return redirect(request.GET["next"])
	return redirect("index")


def blank(request):
	return render(request, "productlist.html")
