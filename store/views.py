from django.shortcuts import get_object_or_404, render,redirect
from django.contrib import messages
from Cart.views import _cart_id
from Departamento.models import Departamento
from category.models import categorias
from .models import Product
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .forms import ExcelUploadForm
import pandas as pd
from io import BytesIO
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
import requests
from Account.views import ListaCompra
from ribasmith.settings import URL_APIS
# Create your views here.
def store(request,depar):
    try:
        endpoint = 'Detapramento'
        url = f'{URL_APIS}{endpoint}'
     
        # Realizar una nueva solicitud a la API para obtener los detalles del producto
        # url = f'http://192.168.88.136:3002/ecommer/rs/Detapramento/'
        
        # id =request.POST.get('id')
        # session_data = dict(request.session)
        session_data = dict(request.session)
  
        if "valor_seleccionado" in session_data:
            bodega = session_data['valor_seleccionado']
        else:
             bodega=114100500
        data={
            'id':depar,
             "bodega":bodega
        }
      

        
        response = requests.post(url , json=data)
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
                'img':data_from_express_api['departamento']['img'],
                'Marca':data_from_express_api['Marca'],
                'filtradoCategoria':False,
                'start_page': start_page,
                'end_page': end_page,
                'depar':depar,
                'preciofiltrado':data_from_express_api['preciofiltrado']
               
                }
         
        else:
            # Manejar el caso en el que el producto no exista o haya un error en la API
            context = None

    except Exception as e:
        print(e)
        context = None

    return render(request, 'store/store.html', context) 


def FiltrarxPrecioDepartamento(request,depar,precio):
    try:
        endpoint = 'FiltrarxPrecioDepartamento'
        url = f'{URL_APIS}{endpoint}'
     
        # Realizar una nueva solicitud a la API para obtener los detalles del producto
        # url = f'http://192.168.88.136:3002/ecommer/rs/Detapramento/'
        
        # id =request.POST.get('id')
        # session_data = dict(request.session)
        session_data = dict(request.session)
  
        if "valor_seleccionado" in session_data:
            bodega = session_data['valor_seleccionado']
        else:
             bodega=114100500
        data={
            "departamentoid":depar,
            "precio":precio,
            "bodega":bodega
            }

        
        response = requests.post(url , json=data)
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
                'img':data_from_express_api['departamento']['img'],
                'Marca':data_from_express_api['Marca'],
                'filtradoCategoria':False,
                'start_page': start_page,
                'end_page': end_page,
                'depar':depar,
                'preciofiltrado':True,
                'fill':precio
               
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
        endpoint = 'Product'
        url = f'{URL_APIS}{endpoint}'
        session_data = dict(request.session)
        cart=_cart_id(request)

        if "valor_seleccionado" in session_data:
            bodega = session_data['valor_seleccionado']
        else:
             bodega=114100500

        if session_data:
             data={
             'id':product,
             "bodega":bodega,
             "cartid":cart,
             "userid":session_data['id'],
        }
    
        else:
             data={
            'id':product,
             "bodega":bodega,
             "cartid":cart,
        }
    
  

        # Realizar una nueva solicitud a la API para obtener los detalles del producto
        # url = f'http://192.168.88.136:3002/ecommer/rs/Product/{product}/'
        response = requests.post(url,json=data)
 
        data_from_express_api = response.json()

        if response.status_code == 200:
            session_data = dict(request.session)
            if session_data:
                 data ={
                "usuario":session_data['id']
                 }   

                 endpoint = 'listafavorito'
                 url = f'{URL_APIS}{endpoint}'
                #  url = f'http://192.168.88.136:3002/ecommer/rs/listafavorito'
   
                 response = requests.get(url, json=data)  # Usar json=data en lugar de data=data
                 resp = response.json()
   
                 if response.status_code == 200:
                     existingCart=resp['existingCart']
                     context={
                         'productos':data_from_express_api['productos'][0],
                          'Agregado':data_from_express_api['Agregado'],
  
                    
                         'lista':existingCart
                           }

            
             
                 else:
                      context={
                         'productos':data_from_express_api['productos'][0],
                          'Agregado':data_from_express_api['Agregado'],
                   
              
                         'lista':[]
                      }
            else:
                context={
               'productos':data_from_express_api['productos'][0],
               'Agregado':data_from_express_api['Agregado'],
          
           
               'list':[]
               
                }
                
  
         
        else:
            # Manejar el caso en el que el producto no exista o haya un error en la API
            context = None

    except Exception as e:
        print(e)
        context = None

    return render(request, 'store/product_detail.html', context) 



def search(request):
    
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
    try:
      
        endpoint = 'buscador'
        url = f'{URL_APIS}{endpoint}'
        session_data = dict(request.session)
  
        if "valor_seleccionado" in session_data:
            bodega = session_data['valor_seleccionado']
        else:
             bodega=114100500
        requestData = { "busqueda": keyword,"bodega":bodega }
      

        
        response = requests.post(url , json=requestData)
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
                'search':keyword,
                'start_page': start_page,
                'end_page': end_page,
                }
         
        else:
            # Manejar el caso en el que el producto no exista o haya un error en la API
            context = None

    except Exception as e:
        print(e)
        context = None

    return render(request, 'store/Search.html', context) 

def searchfillCategoria(request):
    if 'keyword' in request.GET:
        search=request.GET['keyword']
        categoria=request.GET['Cat']
    try:
      
        endpoint = 'fillbuscador'
        url = f'{URL_APIS}{endpoint}'
        session_data = dict(request.session)
  
        if "valor_seleccionado" in session_data:
            bodega = session_data['valor_seleccionado']
        else:
             bodega=114100500
        requestData = { "busqueda": search,"bodega":bodega,"category":categoria }
      

        
        response = requests.post(url , json=requestData)
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
                'search':search,
                'end_page': end_page,
                }
         
        else:
            # Manejar el caso en el que el producto no exista o haya un error en la API
            context = None

    except Exception as e:
        print(e)
        context = None

    return render(request, 'store/Search.html', context) 

def searchfillmarca(request):


    if 'keyword' in request.GET:
        search=request.GET['keyword']
        marca=request.GET['marca']
    try:
      
        endpoint = 'fillbuscador'
        url = f'{URL_APIS}{endpoint}'
        session_data = dict(request.session)
  
        if "valor_seleccionado" in session_data:
            bodega = session_data['valor_seleccionado']
        else:
             bodega=114100500
        requestData = { "busqueda": search,"bodega":bodega,"Marcasearch":marca }
      

        
        response = requests.post(url , json=requestData)
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
                'filtradoMarca':True,
                'start_page': start_page,
                'search':search,
                'end_page': end_page,
                }
         
        else:
            # Manejar el caso en el que el producto no exista o haya un error en la API
            context = None

    except Exception as e:
        print(e)
        context = None

    return render(request, 'store/Search.html', context) 






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
             



def products_by_category(request,depar,category_slug):

    try:
        endpoint = 'Filtradoxcategoria'
        url = f'{URL_APIS}{endpoint}'
        session_data = dict(request.session)
  
        if "valor_seleccionado" in session_data:
            bodega = session_data['valor_seleccionado']
        else:
             bodega=114100500
        data={
            'id':category_slug,
             "bodega":bodega
        }
   
        # Realizar una nueva solicitud a la API para obtener los detalles del producto
        # url = f'http://192.168.88.136:3002/ecommer/rs/Filtradoxcategoria/{category_slug}'

        response = requests.post(url,json=data)
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
                'depar':depar,
                'end_page': end_page,
                }
         
        else:
            # Manejar el caso en el que el producto no exista o haya un error en la API
            context = None

    except Exception as e:
        print(e)
        context = None
    return render(request,'store/store.html',context)







def products_by_category_marca(request,depar,category_slug,Marca_slug):
    try:

        endpoint = 'Filtradoxmarca'
        url = f'{URL_APIS}{endpoint}'
        session_data = dict(request.session)
  
        if "valor_seleccionado" in session_data:
            bodega = session_data['valor_seleccionado']
        else:
             bodega=114100500
     
        data ={
         "id":category_slug,
          "marca":Marca_slug,
          "bodega":bodega
           }
        # Realizar una nueva solicitud a la API para obtener los detalles del producto
        # url = f'http://192.168.88.136:3002/ecommer/rs/Filtradoxmarca'

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
                'depar':depar,
                'end_page': end_page,
                }
         
        else:
            # Manejar el caso en el que el producto no exista o haya un error en la API
            context = None

    except Exception as e:
        print(e)
        context = None
    return render(request,'store/store.html',context)

 


def obtenerinfoproduct(request):

        session_data = dict(request.session)
        try:
            if request.method=='POST':
                if "valor_seleccionado" in session_data:
                    bodega = session_data['valor_seleccionado']
                else:
                     bodega=114100500
                data ={
                 "item":request.POST['item'],
                 "bodega":bodega
                   }        
             
            # Realizar una nueva solicitud a la API para obtener los detalles del producto
            # url = f'http://192.168.88.136:3002/ecommer/rs/viewcart'
            endpoint = 'obtenerinfoproduct'
            url = f'{URL_APIS}{endpoint}'   
            response = requests.post(url, json=data)  # Usar json=data en lugar de data=data
        
            
            if response.status_code == 200:
                data_from_express_api = response.json()
                context = {
                    'productos':data_from_express_api
                }
                                
                return JsonResponse(context)

            else:
                context = {
                    
                }
                
                return JsonResponse(context)
    
    
        except Exception as e:
          
            context = None
            return JsonResponse(context)
    

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


def Seccion(request,seccion):

    try:
        endpoint = 'seccionesid'
        url = f'{URL_APIS}{endpoint}'
        session_data = dict(request.session)
  
        if "valor_seleccionado" in session_data:
            bodega = session_data['valor_seleccionado']
        else:
             bodega=114100500
     
        data ={
            'nombre':seccion,
             "bodega":bodega
           }
        # url = f'http://192.168.88.136:3002/ecommer/rs/seccionesid/'
        response = requests.post(url,json=data)
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
                'filtradoMarca':False,
                'seccion':seccion,
                'start_page': start_page,
                'end_page': end_page,
                }
         
        else:
            # Manejar el caso en el que el producto no exista o haya un error en la API
            context = None

    except Exception as e:
        print(e)
        print('error')
        context = None
    return render(request,'store/Secciones.html',context)



def SeccionfillCategoria(request,seccion,categoria):

    try:
      
        endpoint = 'fillsecciones'
        url = f'{URL_APIS}{endpoint}'
        session_data = dict(request.session)
  
        if "valor_seleccionado" in session_data:
            bodega = session_data['valor_seleccionado']
        else:
             bodega=114100500
        requestData = { "seccion": seccion,"bodega":bodega,"category":categoria }
      

        
        response = requests.post(url , json=requestData)
        print(response)
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
                'seccion':seccion,
                'end_page': end_page,
                }
         
        else:
            # Manejar el caso en el que el producto no exista o haya un error en la API
            context = None

    except Exception as e:
        print(e)
        context = None

    return render(request, 'store/Secciones.html', context) 

def Seccionfillmarca(request,seccion,marca):



    try:
      
        endpoint = 'fillsecciones'
        url = f'{URL_APIS}{endpoint}'
        session_data = dict(request.session)
  
        if "valor_seleccionado" in session_data:
            bodega = session_data['valor_seleccionado']
        else:
             bodega=114100500
        requestData = { "seccion": seccion,"bodega":bodega,"Marcasearch":marca }
      

        
        response = requests.post(url , json=requestData)
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
                'filtradoMarca':True,
                'start_page': start_page,
                'seccion':seccion,
                'end_page': end_page,
                }
         
        else:
            # Manejar el caso en el que el producto no exista o haya un error en la API
            context = None

    except Exception as e:
        print(e)
        context = None

    return render(request, 'store/Secciones.html', context) 

