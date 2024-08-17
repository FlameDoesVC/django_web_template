from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("blank", views.blank, name="blank"),
    path("checkout", views.checkout, name="checkout"),
    path("orders", views.orderlist, name="orders"),
    path("order/<uuid:id>", views.order, name="order"),
    path("products", views.products, name="products"),
    path("product/<int:id>", views.product_details, name="product"),
    path("search", views.search, name="search"),
    path("login", views.login, name="login"),
    path("signup", views.signup, name="signup"),
    path("logout", views.logout, name="logout"),
    path("cart", views.cart, name="cart"),
    path("add-to-cart", views.add_to_cart, name="add-to-cart"),
	path("update-cart-item/<int:item_id>", views.update_cart_item, name="update-cart-item"),
]
