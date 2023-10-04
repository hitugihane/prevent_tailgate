from django.urls import path
from . import views

urlpatterns = [
  path ('login/',views.CustmLoginView.as_view(),name='login'),
  path ('home',views.HomeView.as_view(),name='home'),
   path('webcam/', views.WebcamView.as_view(), name='webcam'),
]