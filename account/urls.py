from unicodedata import name
from . import views
from django.urls import path

app_name = "account"
urlpatterns = [
    path("register/",views.user_register,name="register"),
    path("login/",views.user_login,name="login"),
    path("logout/",views.user_logout,name="logout"),
]