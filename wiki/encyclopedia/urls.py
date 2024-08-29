from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.displayinfo, name="displayinfo"),
    path("random/", views.randompage, name="randompage"),
    path("createnewpage/", views.newpage, name="newpage"),
    path("editpage/", views.editpage, name = "editpage"),
    path("search/", views.search, name="search"),
]
