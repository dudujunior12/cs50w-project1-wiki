from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/", views.wiki, name="wiki"),
    path("wiki/<str:qname>", views.entry, name="entry"),
    path("result/", views.result, name="result"),
    path("new-page/", views.new_page, name="new-page"),
    path("random/", views.random, name="random"),
    path("edit/", views.edit, name="edit"),
]
