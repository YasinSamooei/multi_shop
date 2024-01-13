from product.models import Category,Product

def categories(request):
    """
    To have categories
    """
    categories = Category.objects.all()

    recent_products = Product.objects.all()[:6]

    context = {"categories": categories , "recent_products":recent_products}

    return context
