from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/upload/", views.upload_image, name="upload"),
    path("api/images-library/", views.get_image_library, name="images-library"),
]