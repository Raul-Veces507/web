from .models import Cart, CartItem
from .views import _cart_id
import requests
from decimal import Decimal
from ribasmith.settings import URL_APIS


def counter(request, total=Decimal("0"), quantity=0, cart_items=None, taxt=Decimal("0"), grand_total=Decimal("0"), delivery=Decimal("3.50")):
    cart_count=0
    session_data = dict(request.session)
    if session_data:
        try:
            cart=_cart_id(request)
            
            if "valor_seleccionado" in session_data:
                bodega = session_data['valor_seleccionado']
            else:
                 bodega=114100500
            
            data ={
             "cart":cart,
              "usuario":session_data['id'],
              "bodega":bodega
               }   
            endpoint = 'viewcart'
            url = f'{URL_APIS}{endpoint}'     
            # Realizar una nueva solicitud a la API para obtener los detalles del producto
            # url = f'http://192.168.88.136:3002/ecommer/rs/viewcart'
    
            response = requests.post(url, json=data)  # Usar json=data en lugar de data=data
            if response.status_code == 200:
                data_from_express_api = response.json()
                cart_items = data_from_express_api['carrito']
            
                for cart_item in cart_items:
                  
                    if cart_item['inventario'] >= 0 and cart_item['item_a_reemplazar'] is not None:
                         cart_count += cart_item['quantity']
                    if cart_item['inventario'] > 0: 
                       cart_count += cart_item['quantity']

                context = {

                    'cantidad':cart_count,

                }
            else:
                    context = {
                          'cantidad':0,
                    }

           
    
    
        except Cart.DoesNotExist:
                cart_count=0
        return dict(cart_count=context)
    

    else:
        try:
            cart=_cart_id(request)
            
            if "valor_seleccionado" in session_data:
                bodega = session_data['valor_seleccionado']
            else:
                 bodega=114100500
            
            data ={
             "cart":cart,
         
              "bodega":bodega
               }   
            endpoint = 'viewcart'
            url = f'{URL_APIS}{endpoint}'  
    
            response = requests.post(url, json=data)  # Usar json=data en lugar de data=data
    
    
            if response.status_code == 200:
                data_from_express_api = response.json()
                cart_items = data_from_express_api['carrito']
                
            
                for cart_item in cart_items:
               
                    if cart_item['inventario'] >= 0 and cart_item['item_a_reemplazar'] is not None:
                         cart_count += cart_item['quantity']
                    if cart_item['inventario'] > 0: 
                       cart_count += cart_item['quantity']
            
                context = {

                    'cantidad':cart_count,
   
                }
            else:
                    context = {
                          'cantidad':0,
                    }
    
    
        except Cart.DoesNotExist:
                cart_count=0
        return dict(cart_count=context)
    