from django.urls import path

from main import views

urlpatterns = [
    path("", views.MarkDown.as_view(), name="index"),
]
