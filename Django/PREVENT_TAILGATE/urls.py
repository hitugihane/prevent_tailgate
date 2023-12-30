from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('camera/', views.FaceDetector.as_view(), name='camera'),
]