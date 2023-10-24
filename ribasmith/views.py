from itertools import zip_longest
from django.http import JsonResponse
from django.shortcuts import render
from category.models import categorias
import requests
from store.models import Banner, Product
from ribasmith.settings import URL_APIS

def home(request):

    try:       
        endpoint = 'seccionesid'
        url = f'{URL_APIS}{endpoint}'
        session_data = dict(request.session)
  
        if "valor_seleccionado" in session_data:
            bodega = session_data['valor_seleccionado']
        else:
             bodega=114100500
     
        data ={
            'id':1,
             "bodega":bodega
           }
        # Realizar una nueva solicitud a la API para obtener los detalles del producto
        # url = f'http://192.168.88.136:3002/ecommer/rs/seccionesid/1'
        response = requests.post(url,json=data)
        if response.status_code == 200:
           data_from_express_api = response.json()
           productos=data_from_express_api['productos'][:10]
          
  
           context = {
                'productos': productos
            }
           
        else:
            # Manejar el caso en el que el producto no exista o haya un error en la API
            context = None

    except Exception as e:
        print(e)
        context = None

    return render(request, 'home.html',context) 
  
  

def verbodega(request):
     try:
        # Realizar una nueva solicitud a la API para obtener los detalles del producto
        url = f'http://192.168.88.136:3005/ecommer/rs/obtenerbodega'
        response = requests.get(url)

        if response.status_code == 200:
           data_from_express_api = response.json()
           return JsonResponse({'status': 'obtenido', 'message': data_from_express_api['bodega']})
             
        else:
            return JsonResponse({'status': 'fallido', 'message': []}) # Manejar el caso en el que el producto no exista o haya un error en la API
            

     except Exception as e:
        print(e)
        context = None

        return render(request, 'home.html',context)    