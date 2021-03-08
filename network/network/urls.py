
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:id>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("edit/<int:id>", views.edit, name="edit"),

    #Api Routes
    path ("like", views.like, name="like"),
    path ("profile/like", views.like, name="like"),
    path ("like/<int:post_id>", views.like_nr, name="like_nr"),
    path("profile/like/<int:post_id>", views.like_nr, name="like_nr")
]
