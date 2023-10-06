from .models import Cart, CartItem
from .views import _cart_id
import requests
from decimal import Decimal



def counter(request, total=Decimal("0"), quantity=0, cart_items=None, taxt=Decimal("0"), grand_total=Decimal("0"), delivery=Decimal("3.50")):
    cart_count=0
    session_data = dict(request.session)
    
    if session_data:
        try:
            cart=_cart_id(request)
            data ={
             "cart":cart,
              "usuario":session_data['id']
               }        
            # Realizar una nueva solicitud a la API para obtener los detalles del producto
            url = f'http://192.168.88.136:3002/ecommer/rs/viewcart'
    
            response = requests.post(url, json=data)  # Usar json=data en lugar de data=data
            if response.status_code == 200:
                data_from_express_api = response.json()
                cart_items = data_from_express_api['carrito']
                
                array=[]
                for cart_item in cart_items:
                    precio = Decimal(str(cart_item['precio']))  # Convierte a Decimal
                    Descuento = Decimal(str(cart_item['Descuento'])) 
                    totaldes=precio-(Descuento * precio)
                    total += (totaldes * cart_item['quantity'])
                    cart_count += cart_item['quantity']
                    data={
                        'nombre':cart_item['nombre'],
                        'precio': precio-(Descuento * precio) ,
                        'quantity':cart_item['quantity'],
                        'item':cart_item['item'],
                        'total':cart_item['total']
                       
                    }
                    array.append(data)
    
                taxt = (Decimal("2") * total) / Decimal("100")
                grand_total = total + taxt + delivery
            
                context = {
                    'total': total,
                    'quantity': quantity,
                    'cart_items': array,
                    'cantidad':cart_count,
                    'taxt': taxt.quantize(Decimal("0.00")),
                    'grand_total': grand_total.quantize(Decimal("0.00"))
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
            data ={
             "cart":cart,
               }        
            # Realizar una nueva solicitud a la API para obtener los detalles del producto
            url = f'http://192.168.88.136:3002/ecommer/rs/viewcart'
    
            response = requests.post(url, json=data)  # Usar json=data en lugar de data=data
    
    
            if response.status_code == 200:
                data_from_express_api = response.json()
                cart_items = data_from_express_api['carrito']
                
                array=[]
                for cart_item in cart_items:
                    precio = Decimal(str(cart_item['precio']))  # Convierte a Decimal
                    Descuento = Decimal(str(cart_item['Descuento'])) 
                    totaldes=precio-(Descuento * precio)
                    total += (totaldes * cart_item['quantity'])
                    cart_count += cart_item['quantity']
                    data={
                        'nombre':cart_item['nombre'],
                        'precio': precio-(Descuento * precio) ,
                        'quantity':cart_item['quantity'],
                        'item':cart_item['item'],
                        'total':cart_item['total']
                       
                    }
                    array.append(data)
    
                taxt = (Decimal("2") * total) / Decimal("100")
                grand_total = total + taxt + delivery
            
                context = {
                    'total': total,
                    'quantity': quantity,
                    'cart_items': array,
                    'cantidad':cart_count,
                    'taxt': taxt.quantize(Decimal("0.00")),
                    'grand_total': grand_total.quantize(Decimal("0.00"))
                }
            else:
                    context = {
                          'cantidad':0,
                    }
    
    
        except Cart.DoesNotExist:
                cart_count=0
        return dict(cart_count=context)
    