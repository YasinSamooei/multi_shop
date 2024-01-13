from django.shortcuts import render
from django.views.generic import DetailView,ListView
from .models import Product
from django.db.models import Q

class ProductDetailView(DetailView):
    template_name="product/detail.html"
    model=Product
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        request = self.request
        product = self.get_object()

        product_categories = product.category.all()

        suggested_products = Product.objects.filter(
            Q(category__in=product_categories) &
            ~Q(id=product.id)  # Exclude the current video from the results
        ).order_by('?').distinct()[:5]

        context = {
                "product": product,
                "suggested_products": suggested_products,
            }



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
