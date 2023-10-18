from django.shortcuts import get_object_or_404, redirect, render
from Cart.models import Cart, CartItem
from store.models import Product
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal
from django.contrib import messages
from django.http import JsonResponse
from Account.auth import verificar_autenticacion
import requests
import json
from ribasmith.settings import GOOGLE_MAPS_API_KEY
# Create your views here.

def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart

def add_cart(request,product_id):
        session_data = dict(request.session)
        if session_data:
         try:
             cart=_cart_id(request)
             data ={
              "cart":cart,
               "quantity":1,
               "product":product_id,
               "usuario":session_data['id']
                }  
                   
             # Realizar una nueva solicitud a la API para obtener los detalles del producto
             url = f'http://192.168.88.136:3002/ecommer/rs/carrito'
     
             response = requests.post(url, json=data)  # Usar json=data en lugar de data=data
     
             data_from_express_api = response.json()
             referer = request.META.get('HTTP_REFERER')
       
     
             if response.status_code == 200:
                 
              if referer=='http://127.0.0.1:8000/cart/':
                  return JsonResponse({'status': 'carrito', 'message': 'Error al agregar el producto al carrito'})
              else:
                 return JsonResponse({'status': 'success', 'message': 'Producto agregado al carrito correctamente'})
               
           
     
             #    return JsonResponse({'status': 'success', 'message': 'Producto agregado al carrito correctamente'})
                 
             else:
                 return JsonResponse({'status': 'error', 'message': 'Error al agregar el producto al carrito'})
     
         except Exception as e:
             
             context = None
             return JsonResponse({'status': 'error', 'message': 'Error interno del servidor'})
        else:
          try:
              cart=_cart_id(request)
              data ={
               "cart":cart,
                "quantity":1,
                "product":product_id
                 }  
                    
              # Realizar una nueva solicitud a la API para obtener los detalles del producto
              url = f'http://192.168.88.136:3002/ecommer/rs/carrito'
      
              response = requests.post(url, json=data)  # Usar json=data en lugar de data=data
      
              data_from_express_api = response.json()
              referer = request.META.get('HTTP_REFERER')
        
      
              if response.status_code == 200:
                  
               if referer=='http://127.0.0.1:8000/cart/':
                   return JsonResponse({'status': 'carrito', 'message': 'Error al agregar el producto al carrito'})
               else:
                  return JsonResponse({'status': 'success', 'message': 'Producto agregado al carrito correctamente'})
                
            
      
              #    return JsonResponse({'status': 'success', 'message': 'Producto agregado al carrito correctamente'})
                  
              else:
                  return JsonResponse({'status': 'error', 'message': 'Error al agregar el producto al carrito'})
      
          except Exception as e:
              
              context = None
              return JsonResponse({'status': 'error', 'message': 'Error interno del servidor'})
      
    # product=Product.objects.get(id=product_id)
    # try:
    #     cart=Cart.objects.get(cart_id=_cart_id(request))
    # except Cart.DoesNotExist:
    #     cart=Cart.objects.create(
    #         cart_id=_cart_id(request)
    #     )
    # cart.save()

    # try:
    #     cart_item=CartItem.objects.get(product=product, cart=cart)
    #     cart_item.quantity +=1
    #     cart_item.save()
    # except CartItem.DoesNotExist:
    #     cart_item=CartItem.objects.create(
    #         product=product,
    #         quantity=1,
    #         cart=cart
    #     )
    #     cart_item.save()
    # return redirect('cart')


def add_cart_comentatario(request):
     if request.method=='POST':
      Comentario=request.POST['Comentario']
      Newproduct=request.POST['Newproduct']
      item=request.POST['item']
      session_data = dict(request.session)
      if session_data:
            try:
              cart=_cart_id(request)
              data ={
               "cart":cart,
                "quantity":1,
                "product":item,
                "usuario":session_data['id'],
                "Comentario":Comentario,
                "ItemRemplazo":Newproduct
                 }   
              
              # Realizar una nueva solicitud a la API para obtener los detalles del producto
              url = f'http://192.168.88.136:3002/ecommer/rs/carrito'

              response = requests.post(url, json=data)  # Usar json=data en lugar de data=data

              data_from_express_api = response.json()
              referer = request.META.get('HTTP_REFERER')


              if response.status_code == 200:
             
                  return JsonResponse({'status': 'success', 'message': 'Producto agregado al carrito correctamente'})
              else:
                  return JsonResponse({'status': 'error', 'message': 'Error al agregar el producto al carrito'})


            except Exception as e:
            
              context = None
              return JsonResponse({'status': 'error', 'message': 'Error interno del servidor'})
            
      else:
            try:
              cart=_cart_id(request)
              data ={
               "cart":cart,
                "quantity":1,
                "product":item,
                "Comentario":Comentario,
                "ItemRemplazo":Newproduct
                 }   
              # Realizar una nueva solicitud a la API para obtener los detalles del producto
              url = f'http://192.168.88.136:3002/ecommer/rs/carrito'

              response = requests.post(url, json=data)  # Usar json=data en lugar de data=data

              data_from_express_api = response.json()
              referer = request.META.get('HTTP_REFERER')


              if response.status_code == 200:
                  messages.success(request,' Producto Agregado con exito')
                  return redirect(referer)

              else:
                  return JsonResponse({'status': 'error', 'message': 'Error al agregar el producto al carrito'})


            except Exception as e:
            
              context = None
              return JsonResponse({'status': 'error', 'message': 'Error interno del servidor'})  



def add_cart_detail(request):
   if request.method=='POST':
      
      
      
      cantidad=request.POST['cantidad']
      item=request.POST['item']
      session_data = dict(request.session)
      if session_data:
            try:
              cart=_cart_id(request)
              data ={
               "cart":cart,
                "quantity":cantidad,
                "product":item,
                "usuario":session_data['id']
                 }   
              # Realizar una nueva solicitud a la API para obtener los detalles del producto
              url = f'http://192.168.88.136:3002/ecommer/rs/carrito'

              response = requests.post(url, json=data)  # Usar json=data en lugar de data=data

              data_from_express_api = response.json()
              referer = request.META.get('HTTP_REFERER')


              if response.status_code == 200:
                  messages.success(request,' Producto Agregado con exito')
                  return redirect(referer)

              else:
                  return JsonResponse({'status': 'error', 'message': 'Error al agregar el producto al carrito'})


            except Exception as e:
            
              context = None
              return JsonResponse({'status': 'error', 'message': 'Error interno del servidor'})
            
      else:
            try:
              cart=_cart_id(request)
              data ={
               "cart":cart,
                "quantity":cantidad,
                "product":item
                 }   
              # Realizar una nueva solicitud a la API para obtener los detalles del producto
              url = f'http://192.168.88.136:3002/ecommer/rs/carrito'

              response = requests.post(url, json=data)  # Usar json=data en lugar de data=data

              data_from_express_api = response.json()
              referer = request.META.get('HTTP_REFERER')


              if response.status_code == 200:
                  messages.success(request,' Producto Agregado con exito')
                  return redirect(referer)

              else:
                  return JsonResponse({'status': 'error', 'message': 'Error al agregar el producto al carrito'})


            except Exception as e:
            
              context = None
              return JsonResponse({'status': 'error', 'message': 'Error interno del servidor'})
          


def cart(request, total=Decimal("0"), quantity=0, cart_items=None, taxt=Decimal("0"), grand_total=Decimal("0"), delivery=Decimal("3.50")):
    
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
    
                for cart_item in cart_items:
    
                    Descuento = Decimal(str(cart_item['Descuento'])) 
                    total += (Descuento * cart_item['quantity'])
    
                taxt = (Decimal("2") * total) / Decimal("100")
                grand_total = total + taxt 
            
                context = {
                    'total': total,
                    'quantity': quantity,
                    'cart_items': cart_items,
                    'taxt': taxt.quantize(Decimal("0.00")),
                    'grand_total': grand_total.quantize(Decimal("0.00"))
                }
              
                return render(request, 'store/cart.html', context)
    
                
            else:
                pass
                return render(request, 'store/cart.html', context)
    
    
        except Exception as e:
           
            context = None
            return render(request, 'store/cart.html',context)
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
    
                for cart_item in cart_items:
    
                    Descuento = Decimal(str(cart_item['Descuento'])) 
                    total += (Descuento * cart_item['quantity'])
    
                taxt = (Decimal("2") * total) / Decimal("100")
                grand_total = total + taxt 
            
                context = {
                    'total': total,
                    'quantity': quantity,
                    'cart_items': cart_items,
                    'taxt': taxt.quantize(Decimal("0.00")),
                    'grand_total': grand_total.quantize(Decimal("0.00"))
                }
              
                return render(request, 'store/cart.html', context)
    
                
            else:
                pass
                return render(request, 'store/cart.html', context)
    
    
        except Exception as e:
            
            context = None
            return render(request, 'store/cart.html',context)


    
    # try:
    #     cart=Cart.objects.get(cart_id=_cart_id(request))
    #     cart_items=CartItem.objects.filter(cart=cart,is_active=True)
    #     for cart_item in cart_items:
    #         total +=(cart_item.product.precio*cart_item.quantity)
    #         quantity +=cart_item.quantity

    #     taxt = (Decimal("2") * total) / Decimal("100")
    #     grand_total = total + taxt + delivery
    # except ObjectDoesNotExist :
    #     pass
  
    # context={
    #     'total':total,
    #     'quantity':quantity,
    #     'cart_items':cart_items,
    #     'taxt':taxt.quantize(Decimal("0.00")),
    #     'grand_total':grand_total.quantize(Decimal("0.00"))

    # }
    # return render(request, 'store/cart.html',context)


def viewfiltcart(request, total=Decimal("0"), quantity=0, cart_items=None, taxt=Decimal("0"), grand_total=Decimal("0"), delivery=Decimal("3.50")):

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
             
                for cart_item in cart_items:
                    Descuento = Decimal(str(cart_item['Descuento'])) 
                    total += (Descuento * cart_item['quantity'])
                    
    
    
                taxt = (Decimal("2") * total) / Decimal("100")
                grand_total = total + taxt + delivery
            
                context = {
                    'total': total,
                    'quantity': quantity,
                    'cart_items': cart_items,
                    'taxt': taxt.quantize(Decimal("0.00")),
                    'grand_total': grand_total.quantize(Decimal("0.00"))
                }
                return JsonResponse(context)
    
                
            elif response.status_code == 404:
                context = {
                    
                }
                
                return JsonResponse(context)
            else:
                context = {
                    
                }
                
                return JsonResponse(context)
    
    
        except Exception as e:
          
            context = None
            return JsonResponse(context)
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
             
                for cart_item in cart_items:
                    Descuento = Decimal(str(cart_item['Descuento'])) 
                    total += (Descuento * cart_item['quantity'])
                    
    
    
                taxt = (Decimal("2") * total) / Decimal("100")
                grand_total = total + taxt + delivery
            
                context = {
                    'total': total,
                    'quantity': quantity,
                    'cart_items': cart_items,
                    'taxt': taxt.quantize(Decimal("0.00")),
                    'grand_total': grand_total.quantize(Decimal("0.00"))
                }
                return JsonResponse(context)
    
                
            elif response.status_code == 404:
                context = {
                    
                }
                
                return JsonResponse(context)
            else:
                context = {
                    
                }
                
                return JsonResponse(context)
    
    
        except Exception as e:
     
            context = None
            return JsonResponse(context)
    

def remove_cart(request, product_id):
    session_data = dict(request.session)
    if session_data:
        try:
            cart=_cart_id(request)
            data ={
             "cart":cart,
             "product":product_id,
              "usuario":session_data['id']
               }        
            # Realizar una nueva solicitud a la API para obtener los detalles del producto
            url = f'http://192.168.88.136:3002/ecommer/rs/restarcarrito'
     
            response = requests.post(url, json=data)  # Usar json=data en lugar de data=data
            referer = request.META.get('HTTP_REFERER')
     
            if response.status_code == 200:
                
                 if referer=='http://127.0.0.1:8000/cart/':
                   return redirect(referer)
                 else:
                   
                     return JsonResponse({'status': 'success', 'message': 'Producto Eliminado del carrito'})
     
                
            else:
            
                return JsonResponse({'status': 'error', 'message': 'Error al Eliminar el producto del carrito'})
     
     
        except Exception as e:
          
            context = None
            return JsonResponse({'status': 'error', 'message': 'Error interno del servidor'})

    else:
        try:
            cart=_cart_id(request)
            data ={
             "cart":cart,
             "product":product_id
               }        
            # Realizar una nueva solicitud a la API para obtener los detalles del producto
            url = f'http://192.168.88.136:3002/ecommer/rs/restarcarrito'
     
            response = requests.post(url, json=data)  # Usar json=data en lugar de data=data
            referer = request.META.get('HTTP_REFERER')
     
            if response.status_code == 200:
                
                 if referer=='http://127.0.0.1:8000/cart/':
                   return redirect(referer)
                 else:
                   
                     return JsonResponse({'status': 'success', 'message': 'Producto Eliminado del carrito'})
     
                
            else:
             
                return JsonResponse({'status': 'error', 'message': 'Error al Eliminar el producto del carrito'})
     
     
        except Exception as e:
       
            context = None
            return JsonResponse({'status': 'error', 'message': 'Error interno del servidor'})

     
    # cart=Cart.objects.get(cart_id=_cart_id(request))
    # product=get_object_or_404(Product,id=product_id)
    # cart_item=CartItem.objects.get(product=product,cart=cart)

    # if cart_item.quantity>1:
    #     cart_item.quantity -= 1
    #     cart_item.save()
    # else:
    #     cart_item.delete()
    # return redirect('cart')


def remove_cart_item(request, product_id):
    # cart=Cart.objects.get(cart_id=_cart_id(request))
    # product=get_object_or_404(Product,id=product_id)
    # cart_item=CartItem.objects.get(product=product,cart=cart)
    # cart_item.delete()
    # return redirect('cart')

    session_data = dict(request.session)
    if session_data:
        try:
            cart=_cart_id(request)
            data ={
             "cart":cart,
             "product":product_id,
             "usuario":session_data['id']
               }        
            # Realizar una nueva solicitud a la API para obtener los detalles del producto
            url = f'http://192.168.88.136:3002/ecommer/rs/eliminarproductcarrito'

            response = requests.post(url, json=data)  # Usar json=data en lugar de data=data
            referer = request.META.get('HTTP_REFERER')

            if response.status_code == 200:
            
                 if referer=='http://127.0.0.1:8000/cart/':
                
                     return redirect(referer)
                 else:
                
                     return JsonResponse({'status': 'success', 'message': 'Producto Eliminado del carrito'})



            else:
                return JsonResponse({'status': 'error', 'message': 'Error al Eliminar el producto del carrito'})



        except Exception as e:
           
            context = None
            return JsonResponse({'status': 'error', 'message': 'Error interno del servidor'})
    else:
        try:
            cart=_cart_id(request)
            data ={
             "cart":cart,
             "product":product_id
               }        
            # Realizar una nueva solicitud a la API para obtener los detalles del producto
            url = f'http://192.168.88.136:3002/ecommer/rs/eliminarproductcarrito'

            response = requests.post(url, json=data)  # Usar json=data en lugar de data=data
            referer = request.META.get('HTTP_REFERER')

            if response.status_code == 200:
               
                 if referer=='http://127.0.0.1:8000/cart/':
                
                     return redirect(referer)
                 else:
                
                     return JsonResponse({'status': 'success', 'message': 'Producto Eliminado del carrito'})



            else:
                return JsonResponse({'status': 'error', 'message': 'Error al Eliminar el producto del carrito'})



        except Exception as e:
           
            context = None
            return JsonResponse({'status': 'error', 'message': 'Error interno del servidor'})


def EliminarCarrtioCompleto(request):
    session_data = dict(request.session)
    if session_data:
        try:
            cart=_cart_id(request)
            data ={
             "cart":cart,
             "usuario":session_data['id']
               }        
            # Realizar una nueva solicitud a la API para obtener los detalles del producto
            url = f'http://192.168.88.136:3002/ecommer/rs/EliminarCarrtioCompleto'
    
            response = requests.post(url, json=data)  # Usar json=data en lugar de data=data
            referer = request.META.get('HTTP_REFERER')
    
            if response.status_code == 200:
              
                 if referer=='http://127.0.0.1:8000/cart/':
                    
                     return JsonResponse({'status': 'carrito', 'message': 'Producto Eliminado del carrito'})
                 else:
                  
                     return JsonResponse({'status': 'success', 'message': 'Producto Eliminado del carrito'})
    
                
            else:
              
                return JsonResponse({'status': 'error', 'message': 'Error al Eliminar el producto del carrito'})
    
    
        except Exception as e:
      
            context = None
            return JsonResponse({'status': 'error', 'message': 'Error interno del servidor'})
    else:
        try:
            cart=_cart_id(request)
            data ={
             "cart":cart,
               }        
            # Realizar una nueva solicitud a la API para obtener los detalles del producto
            url = f'http://192.168.88.136:3002/ecommer/rs/EliminarCarrtioCompleto'
    
            response = requests.post(url, json=data)  # Usar json=data en lugar de data=data
            referer = request.META.get('HTTP_REFERER')
    
            if response.status_code == 200:
               
                 if referer=='http://127.0.0.1:8000/cart/':
                 
                     return JsonResponse({'status': 'carrito', 'message': 'Producto Eliminado del carrito'})
                 else:
                 
                     return JsonResponse({'status': 'success', 'message': 'Producto Eliminado del carrito'})
    
                
            else:
                
                return JsonResponse({'status': 'error', 'message': 'Error al Eliminar el producto del carrito'})
    
    
        except Exception as e:
           
            context = None
            return JsonResponse({'status': 'error', 'message': 'Error interno del servidor'})



def checkout(request, total=Decimal("0"), quantity=0, cart_items=None, taxt=Decimal("0"), grand_total=Decimal("0"), delivery=Decimal("3.50")):
        # Verifica la autenticación usando la función personalizada
    resultado_redireccion = verificar_autenticacion(request)

    if resultado_redireccion is not None:
        # Si la función devuelve una redirección, redirige al usuario a la página de inicio de sesión
        return resultado_redireccion
    
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
                Direccion = data_from_express_api['Direccion']
                  
              
                
                for cart_item in cart_items:
                    Descuento = Decimal(str(cart_item['Descuento'])) 
    
                    total += (Descuento * cart_item['quantity'])
    
                taxt = (Decimal("2") * total) / Decimal("100")
                grand_total = total + taxt + delivery
                semigrand_total = total + taxt 
                context = {
                    'total': total,
                    'quantity': quantity,
                    'cart_items': cart_items,
                    'taxt': taxt.quantize(Decimal("0.00")),
                   'semigrand_total': semigrand_total.quantize(Decimal("0.00")),
                    'grand_total': grand_total.quantize(Decimal("0.00")),
                    'Direccion':Direccion
                }
                return render(request, 'store/checkout.html', context)
    
                
            else:
                pass
                return render(request, 'store/checkout.html', context)
    
    
    
        except Exception as e:
            
            context = None
            return render(request, 'store/checkout.html',context)
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
                
                for cart_item in cart_items:
                    Descuento = Decimal(str(cart_item['Descuento'])) 
    
                    total += (Descuento * cart_item['quantity'])
    
                taxt = (Decimal("2") * total) / Decimal("100")
                grand_total = total + taxt + delivery
                semigrand_total = total + taxt 
                context = {
                    'total': total,
                    'quantity': quantity,
                    'cart_items': cart_items,
                    'taxt': taxt.quantize(Decimal("0.00")),
                   'semigrand_total': semigrand_total.quantize(Decimal("0.00")),
                    'grand_total': grand_total.quantize(Decimal("0.00")),
                }
                return render(request, 'store/checkout.html', context)
    
                
            else:
                pass
                return render(request, 'store/checkout.html', context)
    
    
    
        except Exception as e:
            
            context = None
            return render(request, 'store/checkout.html',context)       





    
    # try:
    #     cart=Cart.objects.get(cart_id=_cart_id(request))
    #     cart_items=CartItem.objects.filter(cart=cart,is_active=True)
    #     for cart_item in cart_items:
    #         total +=(cart_item.product.precio*cart_item.quantity)
    #         quantity +=cart_item.quantity

    #     taxt = (Decimal("2") * total) / Decimal("100")
    #     grand_total = total + taxt + delivery
    # except ObjectDoesNotExist :
    #     pass
  
    # context={
    #     'total':total,
    #     'quantity':quantity,
    #     'cart_items':cart_items,
    #     'taxt':taxt.quantize(Decimal("0.00")),
    #     'grand_total':grand_total.quantize(Decimal("0.00"))

    # }
    # return render(request, 'store/cart.html',context)

def get_cart_count(request, total=Decimal("0"), quantity=0, cart_items=None, taxt=Decimal("0"), grand_total=Decimal("0"), delivery=Decimal("3.50")):
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
                    context = []
    
    
        except Cart.DoesNotExist:
                cart_count=0
        return JsonResponse({'cart_count': cart_count})
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
                    context = []
    
    
        except Cart.DoesNotExist:
                cart_count=0
        return JsonResponse({'cart_count': cart_count})

def ValidarCarrito(request):
     if request.method=='POST':

      item=request.POST['item']
      cart=_cart_id(request)
      session_data = dict(request.session)
      if session_data:
            try:
              cart=_cart_id(request)
              data ={
               "carritoid":cart,
                "item":item,
                 "usuario":session_data['id']
                 }   
              # Realizar una nueva solicitud a la API para obtener los detalles del producto
              url = f'http://192.168.88.136:3002/ecommer/rs/validarCarrito'

              response = requests.post(url, json=data)  # Usar json=data en lugar de data=data
              data_from_express_api = response.json()
              referer = request.META.get('HTTP_REFERER')


              if response.status_code == 200:
             
                  return JsonResponse({'status': 'success'})
              
              elif response.status_code == 201:
                  return JsonResponse({'status': 'warning'})

                  
              else:
                  return JsonResponse({'status': 'error'})


            except Exception as e:
            
              context = None
              return JsonResponse({'status': 'error', 'message': 'Error interno del servidor'})
            
      else:
            try:
              cart=_cart_id(request)
              data ={
                "carritoid":cart,
                "item":item,
                 }   
              # Realizar una nueva solicitud a la API para obtener los detalles del producto
              url = f'http://192.168.88.136:3002/ecommer/rs/validarCarrito'

              response = requests.post(url, json=data)  # Usar json=data en lugar de data=data

              data_from_express_api = response.json()
              referer = request.META.get('HTTP_REFERER')


              if response.status_code == 200:
             
                  return JsonResponse({'status': 'success'})
              
              elif response.status_code == 201:
                  return JsonResponse({'status': 'warning'})

                  
              else:
                  return JsonResponse({'status': 'error'})


            except Exception as e:
            
              context = None
              return JsonResponse({'status': 'error', 'message': 'Error interno del servidor'})  


