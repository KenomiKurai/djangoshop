from django.urls import path
from . import views


urlpatterns = [
    path("", views.gallery, name="gallery"),
    path("uploads/", views.uploads, name="uploads"),
    ]