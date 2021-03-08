from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/?P<str:name>/', views.EntryPage, name="EntryPage_Index"),
    path("wiki/<name>", views.EntryPage, name="EntryPage"),
    path('search/?P<str:name>/', views.Search, name="Search"), 
    path('new/', views.New, name="New"),
    path('random/', views.Random, name="Random"),

    path('edit/?P<str:name>/', views.Edit, name="Edit"),
    path('edit/', views.Edit, name="Edit")
    
   
]
