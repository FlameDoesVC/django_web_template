from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("blank", views.blank, name="blank"),
    path("checkout", views.checkout, name="checkout"),
    path("product", views.product_details, name="product"),
    path("login", views.login, name="login"),
    path("signup", views.signup, name="signup"),
    path("logout", views.logout, name="logout"),
    path("add-to-cart", views.add_to_cart, name="add-to-cart"),
]