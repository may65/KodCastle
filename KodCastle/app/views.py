from django.shortcuts import render

# Create your views here.

def null(request):
    return render(request, 'null.html')#, {'products': products})

def test(request):
    # products = Product.objects.all()
    # return render(request, 'flower/product_list.html', {'products': products})
    return render(request, 'test.html')#, {'products': products})

def root(request):
    return render(request, 'root.html')

def int(request,id):
    return render(request, 'int.html')#, {'id': id})

def int_view(request, id):
    return render(request, 'int.html', {'id': id})
