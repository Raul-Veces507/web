from django.shortcuts import render

from store.models import Banner, Product


def home(request):
    banner=Banner.objects.all()
    product=Product.objects.filter(categoria_id=1)[:10] 
  
    context={
        'banner':banner,
        'product':product
    }
    return render(request,'home.html',context)