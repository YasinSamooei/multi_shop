from django.shortcuts import render
from django.views.generic import TemplateView

#HomeView
class Home(TemplateView):
    template_name="home/index.html"
    
