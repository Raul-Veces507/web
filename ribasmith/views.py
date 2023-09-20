from django.shortcuts import render
from category.models import categorias

from store.models import Banner, Product


def home(request):
    banner=Banner.objects.all()
    product=Product.objects.filter(categoria_id=1)[:10] 
    cat=categorias.objects.all()
    context={
        'banner':banner,
        'product':product,
        'categoria':cat
    }
    return render(request,'home.html',context)