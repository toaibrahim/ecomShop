
from unicodedata import name
from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path("",views.HomeView.as_view(),name="index"),
    path("product/",views.Products.as_view(),name="product"),

    path("product_details/<slug>",views.product_details,name="product_details"),
    
    path("cart/",views.OrderSummery.as_view(),name="cart"),
    path("cart/add_to_cart/<slug>",views.add_to_cart,name="add_to_cart"),
    path("cart/remove_cart/<slug>",views.remove_from_cart,name="remove_from_cart"),
    path("cart/remove_from_cart_totally/<slug>",views.remove_from_cart_totally,name="remove_from_cart_totally"),

    
    path("checkout/",views.CheckoutView.as_view(),name="checkout"),
    path("payment/<payment_option>",views.PaymentView.as_view(),name="payment"),
    

    path("wishlist/",views.wishlist,name="wishlist"),
    path("wishlist/add_to_wishlist/<slug>",views.add_to_wishlist,name="add_to_wishlist"),
    path("wishlist/remove_from_wishlist/<slug>",views.remove_from_wishlist,name="remove_from_wishlist"),

    path("contact/",views.contact,name="contact"),
    path("search/",views.search,name="search"),

    path("blog/",views.Blogpost.as_view(),name="blog"),
    path("blog_details/<id>",views.blog_details,name="blog_details"),

    path("my_account/",views.my_account,name="my_account"),



]