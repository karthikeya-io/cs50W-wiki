from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("createPage", views.create, name="create"),
    path("edit", views.edit, name="edit"),
    path("editpage", views.editpage, name="editpage"),
    path("randompage", views.randPage, name="randpage")

]
