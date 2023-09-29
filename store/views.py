from django.shortcuts import get_object_or_404, render,redirect
from django.contrib import messages
from Departamento.models import Departamento
from category.models import categorias
from .models import Product
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .forms import ExcelUploadForm
import pandas as pd
from io import BytesIO
from django.http import HttpResponse
from django.db.models import Q
import requests
# Create your views here.
def store(request,depar):
    try:
        print(depar)
        # Realizar una nueva solicitud a la API para obtener los detalles del producto
        url = f'http://192.168.88.136:3002/ecommer/rs/Detapramento/{depar}/'
        response = requests.get(url)
        data_from_express_api = response.json()

        if response.status_code == 200:
            
           paginator=Paginator(data_from_express_api['productos'],36)
           page=request.GET.get('page')
           paged_prducts=paginator.get_page(page)
           product_count = len(data_from_express_api['productos'])
           current_page = paged_prducts.number
           start_page = max(current_page - 4, 1)  # Establece el rango de páginas visibles
           end_page = min(current_page + 4,paged_prducts.paginator.num_pages)
           context={
                'productos':paged_prducts,
                'products_count':product_count,
                'Categoria':data_from_express_api['categorias'],
                'Marca':data_from_express_api['Marca'],
                'filtradoCategoria':False,
                'start_page': start_page,
                'end_page': end_page,
                }
         
        else:
            # Manejar el caso en el que el producto no exista o haya un error en la API
            context = None

    except Exception as e:
        print(e)
        context = None

    return render(request, 'store/store.html', context) 



def product_detail(request,product):
    try:
        print(product)
        # Realizar una nueva solicitud a la API para obtener los detalles del producto
        url = f'http://192.168.88.136:3002/ecommer/rs/Product/{product}/'
        response = requests.get(url)
        data_from_express_api = response.json()
        print(data_from_express_api)

        if response.status_code == 200:
           context={
               'productos':data_from_express_api['productos'][0],
               'Categoria':data_from_express_api['productos'][0]
               
                }
         
        else:
            # Manejar el caso en el que el producto no exista o haya un error en la API
            context = None

    except Exception as e:
        print(e)
        context = None

    return render(request, 'store/product_detail.html', context) 



# def store(request,category_slug=None):
#       products=None
#       if category_slug!=None:
        
#         departamento=get_object_or_404(Departamento,id=category_slug)
#         products = Product.objects.filter(grupo__categoria__departamento_id=departamento.id)
#         categoriasfill = categorias.objects.filter(	departamento_id=departamento.id).order_by('id')
#         # print(products)
     
#         Marcas = set()
#         for product in products:
#            Marca = product.Marca
#            categoria = product.grupo.categoria.name
#            products_count=Product.objects.filter(Marca=Marca)
#            cantidad=products_count.count()
#            if Marca is not None and categoria is not None:

#              Marcas.add((Marca, categoria,cantidad))

#         marcas_lista = [{'Marca': Marca, 'Categoria': categoria,'Cantidad':cantidad} for Marca, categoria,cantidad in Marcas]

#         paginator=Paginator(products,36)
#         page=request.GET.get('page')
#         paged_prducts=paginator.get_page(page)
#         product_count=products.count()
#         current_page = paged_prducts.number
#         start_page = max(current_page - 4, 1)  # Establece el rango de páginas visibles
#         end_page = min(current_page + 4,paged_prducts.paginator.num_pages)
#       else:
#         categoriasfill = categorias.objects.all()
#         products=Product.objects.all().order_by('id')
#         Marcas = set()
#         for product in products:
#            Marca = product.Marca
#            categoria = product.grupo.categoria.name
#            if Marca is not None and categoria is not None:

#              Marcas.add((Marca, categoria))

#         marcas_lista = [{'Marca': Marca, 'Categoria': categoria,'Cantidad':cantidad} for Marca, categoria,cantidad in Marcas]
#         paginator=Paginator(products,36)
#         page=request.GET.get('page')
#         paged_prducts=paginator.get_page(page)
#         product_count=products.count()
#         current_page = paged_prducts.number
#         start_page = max(current_page - 4, 1)  # Establece el rango de páginas visibles
#         end_page = min(current_page + 4,paged_prducts.paginator.num_pages)
        
#       content={
#         'productos':paged_prducts,
#         'products_count':product_count,
#         'Marcas':marcas_lista,
#         'filtrado':False,
#         'start_page': start_page,
#         'end_page': end_page,
#         'categoriasfill':categoriasfill
            
#        }
#       return render(request,'store/store.html',content)
             



def products_by_category(request,category_slug):

    try:
   
        # Realizar una nueva solicitud a la API para obtener los detalles del producto
        url = f'http://192.168.88.136:3002/ecommer/rs/Filtradoxcategoria/{category_slug}'

        response = requests.get(url)
        data_from_express_api = response.json()

        if response.status_code == 200:
            
           paginator=Paginator(data_from_express_api['productos'],36)
           page=request.GET.get('page')
           paged_prducts=paginator.get_page(page)
           product_count = len(data_from_express_api['productos'])
           current_page = paged_prducts.number
           start_page = max(current_page - 4, 1)  # Establece el rango de páginas visibles
           end_page = min(current_page + 4,paged_prducts.paginator.num_pages)
           context={
                'productos':paged_prducts,
                'products_count':product_count,
                'Categoria':data_from_express_api['categorias'],
                'Marca':data_from_express_api['Marca'],
                'filtradoCategoria':True,
                'start_page': start_page,
                'end_page': end_page,
                }
         
        else:
            # Manejar el caso en el que el producto no exista o haya un error en la API
            context = None

    except Exception as e:
        print(e)
        context = None
    return render(request,'store/store.html',context)







def products_by_category_marca(request,category_slug,Marca_slug):
    try:
        data ={
         "id":category_slug,
          "marca":Marca_slug
           }
        # Realizar una nueva solicitud a la API para obtener los detalles del producto
        url = f'http://192.168.88.136:3002/ecommer/rs/Filtradoxmarca'

        response = requests.post(url, json=data)  # Usar json=data en lugar de data=data

        data_from_express_api = response.json()

        if response.status_code == 200:
            
           paginator=Paginator(data_from_express_api['productos'],36)
           page=request.GET.get('page')
           paged_prducts=paginator.get_page(page)
           product_count = len(data_from_express_api['productos'])
           current_page = paged_prducts.number
           start_page = max(current_page - 4, 1)  # Establece el rango de páginas visibles
           end_page = min(current_page + 4,paged_prducts.paginator.num_pages)
           context={
                'productos':paged_prducts,
                'products_count':product_count,
                'Categoria':data_from_express_api['categorias'],
                'Marca':data_from_express_api['Marca'],
                'filtradoCategoria':True,
                'filtradoMarca':True,
                'start_page': start_page,
                'end_page': end_page,
                }
         
        else:
            # Manejar el caso en el que el producto no exista o haya un error en la API
            context = None

    except Exception as e:
        print(e)
        context = None
    return render(request,'store/store.html',context)

 



#Administrador

def upload_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            archivo_excel = form.cleaned_data['archivo_excel']

            # Procesa el archivo Excel aquí
            try:
                # Lee el archivo Excel y realiza la importación
                df = pd.read_excel(archivo_excel)

                # Procesa los datos y crea instancias de Product
                for index, row in df.iterrows():
                    product = Product(
                        nombre=row['nombre'],
                        item=row['item'],
                        sku=row['sku'],
                        precio=row['precio'],
                        Impuesto=row['Impuesto'],
                        Size=row['Size'],
                        inventario=row['inventario'],
                        bodega=row['bodega'],
                        Marca=row['Marca'],
                        Detalle=row['Detalle'],
                        CodigoPeso=row['CodigoPeso'],
                        FactorConversion=row['FactorConversion'],
                        grupo_id=row['grupo_id']
                    )
                    product.save()

                # Muestra un mensaje de éxito
                messages.success(request, 'Importación exitosa desde Excel.')
            except Exception as e:
                # Si ocurre un error durante la importación, muestra un mensaje de error
                messages.error(request, f'Error durante la importación desde Excel: {str(e)}')

            return redirect('/admin/store/product/')  # Redirige a la lista de objetos del modelo

    else:
        form = ExcelUploadForm()

    return render(request, 'admin/upload_excel.html', {'form': form})


def checkout(request):
   return render(request, 'store/checkout.html')