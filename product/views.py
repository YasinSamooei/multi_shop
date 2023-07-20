from django.shortcuts import render
from django.views.generic import DetailView
from .models import Product
class ProductDetailView(DetailView):
    template_name="product/detail.html"
    model=Product