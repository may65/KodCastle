from django.shortcuts import render

# Create your views here.
def test(request):
    """Отображает список товаров."""
    # products = Product.objects.all()
    # return render(request, 'flower/product_list.html', {'products': products})
    return render(request, 'test.html')#, {'products': products})

def root(request):
    """Отображает список товаров."""
    # products = Product.objects.all()
    # return render(request, 'flower/product_list.html', {'products': products})
    return render(request, 'test.html')#, {'products': products})