from django.shortcuts import render
from django.views.generic import DetailView,ListView
from .models import Product

class ProductDetailView(DetailView):
    template_name="product/detail.html"
    model=Product


class ProductsListView(ListView):
    template_name='product/products_list.html'
    queryset=Product.objects.all()

    def get_context_data(self, **kwargs):
        request= self.request
        colors=request.GET.getlist('color')
        sizes=request.GET.getlist('size')
        min_price=request.GET.get('min_price')
        max_price=request.GET.get('max_price')

        queryset=Product.objects.all()
        if colors:
            queryset=queryset.filter(Color__title__in=colors).distinct()
        if sizes:
            queryset=queryset.filter(size__title__in=sizes).distinct()
        if min_price and max_price:
            queryset=queryset.filter(price__lte=max_price,price__gte=min_price).distinct()

        context= super(ProductsListView,self).get_context_data()
        context['object_list']=queryset
        return context
