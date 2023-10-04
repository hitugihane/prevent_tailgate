from django.shortcuts import render

# Create your views here.

#======import======

from django.contrib.auth.views import LoginView
from django.urls import path,reverse_lazy

from django.views.generic import TemplateView
#==================

#======Views=======

class CustmLoginView(LoginView):
  template_name = 'login.html'
  redirect_authenticated_user = True

  def get_success_url(self):
        return reverse_lazy('home')


class HomeView(TemplateView):
  template_name="home.html"

class WebcamView(TemplateView):
    template_name = "webcam.html"