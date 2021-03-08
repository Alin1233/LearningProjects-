from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing", views.listing, name="listing"),
    path("listing/<int:pk>", views.page, name="page"),
    path("close/<int:pk>", views.listing_actions, name="listing_actions"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("cat", views.cat, name="cat")
]
