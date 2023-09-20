from django.shortcuts import get_object_or_404, render

from category.models import categorias
from .models import Product
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
# Create your views here.
def store(request,category_slug=None):
      categories=None
      products=None
      if category_slug!=None:
        print(category_slug)
        categories=get_object_or_404(categorias,id=category_slug)
        products=Product.objects.filter(categoria_id=categories.id).order_by('id')
        paginator=Paginator(products,5)
        page=request.GET.get('page')
        paged_prducts=paginator.get_page(page)
        product_count=products.count()
        product_count=products.count()
   
      else:
        products=Product.objects.all().order_by('id')
        paginator=Paginator(products,5)
        page=request.GET.get('page')
        paged_prducts=paginator.get_page(page)
        product_count=products.count()
        
      content={
        'productos':paged_prducts,
        'products_count':product_count,
            
       }
      return render(request,'store/store.html',content)
             
      