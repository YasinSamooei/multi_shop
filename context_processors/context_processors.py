from product.models import Category

def categories(request):
    """
    To have categories
    """
    categories = Category.objects.all()


    context = {"categories": categories}

    return context
