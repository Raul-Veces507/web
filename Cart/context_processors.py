from .models import Cart, CartItem
from .views import _cart_id
import requests

def counter(request):
    cart_count=0

    try:
        cart=_cart_id(request)
        data ={
         "cart":cart,
           }        
        # Realizar una nueva solicitud a la API para obtener los detalles del producto
        url = f'http://192.168.88.136:3002/ecommer/rs/viewcart'
        response = requests.post(url, json=data)
         
        if response.status_code == 200:
            data_from_express_api = response.json()
            response = requests.post(url, json=data)  # Usar json=data en lugar de data=data
            cart_items = data_from_express_api['carrito']
            for cart_item in cart_items:
                cart_count += cart_item['quantity']

    except Cart.DoesNotExist:
            cart_count=0
    return dict(cart_count=cart_count)
