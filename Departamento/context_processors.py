
from django.shortcuts import redirect, render
from itertools import zip_longest
from .models import Departamento
from store.models import  Product
import requests

def menu_links(request):
    url='http://192.168.88.136:3002/ecommer/rs/Detapramentos'
    try:
        response = requests.get(url)
    
 
      
        if response.status_code == 200 :
            data_from_express_api = response.json()
            limited_data = data_from_express_api
            grouped_data = list(zip_longest(*[iter(limited_data)] * 4, fillvalue=None))
            context =  grouped_data
            
    
            return dict(links= limited_data['departamento'])
            

        else:
            return render(request, 'home.html', {'message': 'Error al obtener datos del API'})

    except requests.exceptions.RequestException as e:
        return render(request, 'home.html', {'message': str(e)})
