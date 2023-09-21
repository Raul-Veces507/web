from django.shortcuts import get_object_or_404, render

from category.models import categorias
from .models import Product
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
# Create your views here.
def store(request,category_slug=None):
      categories=None
      products=None
      if category_slug!=None:
        
        categories=get_object_or_404(categorias,id=category_slug)
        products=Product.objects.filter(categoria_id=categories.id).order_by('id')
        Marcas = set()
        for product in products:
           Marca = product.Marca
           categoria = product.categoria_id
           if Marca is not None and categoria is not None:

             Marcas.add((Marca, categoria))

        marcas_lista = [{'Marca': Marca, 'Categoria': categoria} for Marca, categoria in Marcas]

        paginator=Paginator(products,36)
        page=request.GET.get('page')
        paged_prducts=paginator.get_page(page)
        product_count=products.count()
        current_page = paged_prducts.number
        start_page = max(current_page - 4, 1)  # Establece el rango de páginas visibles
        end_page = min(current_page + 4,paged_prducts.paginator.num_pages)
      else:
        products=Product.objects.all().order_by('id')
        
        paginator=Paginator(products,24)
        page=request.GET.get('page')
        paged_prducts=paginator.get_page(page)
        product_count=products.count()
        
      content={
        'productos':paged_prducts,
        'products_count':product_count,
        'Marcas':marcas_lista,
        'filtrado':False,
        'start_page': start_page,
        'end_page': end_page,
            
       }
      return render(request,'store/store.html',content)
             
def products_by_category_marca(request,category_slug,Marca_slug):
      try:
      
          categories=None
          products=None
      except Exception as e:
          raise e
      if category_slug!=None:
        categories=get_object_or_404(categorias,id=category_slug)
        products=Product.objects.filter(categoria_id=categories.id,Marca=Marca_slug).order_by('id')
      
        Marcas = set()
        for product in products:
           Marca = product.Marca
           categoria = product.categoria_id
           if Marca is not None and categoria is not None:

             Marcas.add((Marca, categoria))

        marcas_lista = [{'Marca': Marca, 'Categoria': categoria} for Marca, categoria in Marcas]

        paginator=Paginator(products,36)
        page=request.GET.get('page')
        paged_prducts=paginator.get_page(page)
        product_count=products.count()
        product_count=products.count()
   
      else:
        products=Product.objects.all().order_by('id')
        paginator=Paginator(products,24)
        page=request.GET.get('page')
        paged_prducts=paginator.get_page(page)
        product_count=products.count()
      content={
        'productos':paged_prducts,
        'products_count':product_count,
        'Marcas':marcas_lista,
        'filtrado':True
            
       }
      return render(request,'store/store.html',content)



def product_detail(request,category_slug,product_slug):
    print(product_slug)
    try:
        single_product=Product.objects.get(item=product_slug)

    except Exception as e:
        raise e


    context={
        'single_product': single_product,
    }

    return render(request, 'store/product_detail.html',context)