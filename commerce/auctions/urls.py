from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("createlisting/", views.createlisting, name="createlisting"),
    path("categories/", views.categoriespage, name="categoriespage"),
    path("watchlist/", views.watchlists, name="watchlist"),
    path("product/<slug:slug>/", views.listing_details, name= "listing_details"),
]
