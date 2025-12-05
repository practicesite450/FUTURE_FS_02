from django.shortcuts import render
from .models import Product

def base(request):
    return render(request, 'products/base.html')

def index(request):
    return render(request, 'products/index.html')

def products1(request):
    products = Product.objects.all()
    return render(request, 'products/products1.html', {'products': products})
