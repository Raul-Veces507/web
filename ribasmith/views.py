from itertools import zip_longest
from django.shortcuts import render
from category.models import categorias
import requests
from store.models import Banner, Product


# def home(request):
#     banner=Banner.objects.all()
#     product=Product.objects.filter(grupo_id=2)[:8] 
#     cat=categorias.objects.all()
#     context={
#         'banner':banner,
#         'product':product,
#         'categoria':cat
#     }
#     return render(request,'home.html',context)


def home(request):
    express_api_url = 'http://localhost:8000/api/mostrar'
    express_api_url2 = 'http://localhost:8000/api/mostrarcarrito'
    express_api_url3 = 'http://localhost:8000/api/totalcart'
    

    if request.method == 'POST':
        id = request.POST.get('id')
        name = request.POST.get('name')
        product_id = request.POST.get('product_id')
        img = request.POST.get('img')
        price = request.POST.get('price')

        data = {
            'id': id,
            'name': name,
            'product_id': product_id,
            'img': img,
            'price': price,
        }

        print(data)

        express_api_insert_url = 'http://localhost:8000/api/insertcart'

        try:
            response = requests.post(express_api_insert_url, json=data)  # Usar json=data en lugar de data=data

            if response.status_code == 200:
                print('datos insertados')
                
            else:
                print('error')
               
            

        except requests.exceptions.RequestException as e:
            
             print('Error en la petición:', e)
             return render(request, 'home.html', {'message': 'Error en la petición: ' + str(e)})
        
    
    
    try:
        response = requests.get(express_api_url)
        responses = requests.get(express_api_url2)
 
      
        if response.status_code == 200 and responses.status_code == 200 :
            data_from_express_api = response.json()
            data_from_express_api2 = responses.json()
            limited_data = data_from_express_api[:10]
            grouped_data = list(zip_longest(*[iter(limited_data)] * 4, fillvalue=None))
            context =  grouped_data
            
    
         
            return render(request, 'home.html', {'swip':context,'datas': limited_data, 'data':data_from_express_api2['productos'], 'total':data_from_express_api2['total']})

        else:
            return render(request, 'home.html', {'message': 'Error al obtener datos del API'})

    except requests.exceptions.RequestException as e:
        return render(request, 'home.html', {'message': str(e)})
    
