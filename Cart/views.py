from django.shortcuts import get_object_or_404, redirect, render
from Cart.models import Cart, CartItem
from store.models import Product
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal
from django.contrib import messages
from django.http import JsonResponse
import requests
# Create your views here.

def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart

def add_cart(request,product_id):

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

        if response.status_code == 200:
             referer = request.META.get('HTTP_REFERER')
             messages.success(request,' Producto Agregado')
             return redirect(referer)

        #    return JsonResponse({'status': 'success', 'message': 'Producto agregado al carrito correctamente'})
            
        else:
            return JsonResponse({'status': 'error', 'message': 'Error al agregar el producto al carrito'})


    except Exception as e:
        print(e)
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




def cart(request, total=Decimal("0"), quantity=0, cart_items=None, taxt=Decimal("0"), grand_total=Decimal("0"), delivery=Decimal("3.50")):
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
                'taxt': taxt.quantize(Decimal("0.00")),
                'grand_total': grand_total.quantize(Decimal("0.00"))
            }
            return render(request, 'store/cart.html', context)

            
        else:
            pass
            return render(request, 'store/cart.html', context)


    except Exception as e:
        print(e)
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


def remove_cart(request, product_id):
    try:
        cart=_cart_id(request)
        data ={
         "cart":cart,
         "product":product_id
           }        
        # Realizar una nueva solicitud a la API para obtener los detalles del producto
        url = f'http://192.168.88.136:3002/ecommer/rs/restarcarrito'

        response = requests.post(url, json=data)  # Usar json=data en lugar de data=data


        if response.status_code == 200:

           return redirect('cart')

            
        else:
            pass
            return redirect('cart')


    except Exception as e:
        print(e)
        context = None
        return redirect('cart')


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


    try:
        cart=_cart_id(request)
        data ={
         "cart":cart,
         "product":product_id
           }        
        # Realizar una nueva solicitud a la API para obtener los detalles del producto
        url = f'http://192.168.88.136:3002/ecommer/rs/eliminarproductcarrito'

        response = requests.post(url, json=data)  # Usar json=data en lugar de data=data


        if response.status_code == 200:

            return redirect('cart')


            
        else:
            pass
            return redirect('cart')



    except Exception as e:
        print(e)
        context = None
        return redirect('cart')

def checkout(request, total=Decimal("0"), quantity=0, cart_items=None, taxt=Decimal("0"), grand_total=Decimal("0"), delivery=Decimal("3.50")):
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
                'taxt': taxt.quantize(Decimal("0.00")),
                'grand_total': grand_total.quantize(Decimal("0.00"))
            }
            return render(request, 'store/checkout.html', context)

            
        else:
            pass
            return render(request, 'store/checkout.html', context)



    except Exception as e:
        print(e)
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

