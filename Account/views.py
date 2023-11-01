import json
from django.shortcuts import render,redirect

from Cart.views import _cart_id
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
import requests
from django.http import JsonResponse
from django.contrib.auth import logout
# Create your views here.
from datetime import datetime
from ribasmith.settings import GOOGLE_MAPS_API_KEY,URL_APIS





def  wishlistProduct(request):
   if request.method =='POST':
   
    session_data=dict(request.session)
    data = json.loads(request.body)
    selectedProducts = data['selectedProducts']
    
   if session_data:
    try:       
        endpoint = 'insertarProductosCarrito'
        url = f'{URL_APIS}{endpoint}'
        cart=_cart_id(request)
        data ={
            "arrayProduct":selectedProducts,
            "cart":cart,
            "usuario":session_data['id']
             
           }
     
        # Realizar una nueva solicitud a la API para obtener los detalles del producto
        # url = f'http://192.168.88.136:3002/ecommer/rs/seccionesid/1'
        response = requests.post(url,json=data)
        referer = request.META.get('HTTP_REFERER')
        if response.status_code == 200:
           
           return JsonResponse({'status': 'success'})
           
        else:
            return redirect(referer)

    except Exception as e:
        print(e)
        context = None

   return render('store/cart.html',request) 
  







def register(request):

    if request.method == 'POST':
    

            first_name=request.POST['first_name']
            last_name=request.POST['last_name']
            email=request.POST['email']
            phone_number=request.POST['phone_number']
            password=request.POST['password']
            Sexo=request.POST['Sexo']
            FechaN=request.POST['FechaN']

            data={
                "Nombre": first_name,
                "Apellido": last_name,
                "Email": email,
                "password": password,
                "Celular": phone_number,
                "Fecha_nacimiento": FechaN,
                "Sexo": Sexo
            }
            endpoint = 'createUser'
            url = f'{URL_APIS}{endpoint}'

            response = requests.post(url, json=data)
            if response.status_code == 200:
                messages.success(request,'Usuario Creado Con Exito')
                return redirect('login')
                
            elif response.status_code==300:
                messages.error(request,'Error Usuario Ya Se Ecuentra Registrado ')
                return render(request, 'accounts/register.html')
            
            else:
                messages.error(request,'Error Usuario No Registrado ')
                return render(request, 'accounts/register.html')
                
                



    return render(request, 'accounts/register.html')

def login(request):
       
        if request.method== 'POST':
            email=request.POST['email']
            password=request.POST['password']
            session_data = dict(request.session)
            cart=_cart_id(request)

            if "valor_seleccionado" in session_data:
                bodega = session_data['valor_seleccionado']
            else:
                 bodega=114100500
            try:
              data ={
               "email":email,
                "password":password,
                "cart":cart,
                "bodega":bodega

                 }   
              # Realizar una nueva solicitud a la API para obtener los detalles del producto
              endpoint = 'login'
              url = f'{URL_APIS}{endpoint}'
            #   url = f'http://192.168.88.136:3002/ecommer/rs/login'
    
              response = requests.post(url, json=data)  # Usar json=data en lugar de data=data
    
              data_from_express_api = response.json()
              referer = request.META.get('HTTP_REFERER')
    
              if response.status_code == 200:
                 token=data_from_express_api['token']
                 nombre=data_from_express_api['nombre']
                 id=data_from_express_api['id']
                 request.session['token'] = token
                 request.session['Usuario'] = nombre
                 request.session['id'] = id
                 request.session.save()
                 return redirect('home') 

              elif response.status_code == 301:
                messages.error(request,'Usuario No Se Encuentra Activo')
                return redirect('login')
              
              elif response.status_code == 201:
                messages.error(request,'Credenciales Incorrectas')
                return redirect('login')
    

            except Exception as e:
                messages.error(request,'Credenciales Incorrectas')
                return redirect('login')

        return render(request, 'accounts/login.html')

def guardar_valor_en_sesion(request):
    if request.method == 'POST':
        selected_value = request.POST['selected_value']  # Asegúrate de que 'selected_value' sea el nombre correcto del campo HTML.
        selected_text = request.POST['selected_text']  # También obtén el texto de la opción seleccionada si lo necesitas.

        if 'Usuario' in request.session:
            request.session['valor_seleccionado'] = selected_value
            request.session['nombre_tienda'] = selected_text  # Si necesitas guardar el nombre de la tienda.
            request.session.save()
   
        else:
             
            request.session['token'] = ''
            request.session['Usuario'] = ''
            request.session['id'] = ''
            request.session['valor_seleccionado'] = selected_value
            request.session['nombre_tienda'] = selected_text  # Si necesitas guardar el nombre de la tienda.
            request.session.save()
     
             

    
    return redirect('home')  # Redirige a la vista que necesites después de guardar los valores.

def logout(request):
    # logout(request)
    # auth.logout(request)
    # messages.success(request, 'Has salido de sesion')
    if 'token' in request.session:
  
        del request.session['token']
        request.session.modified = True

    if 'Usuario' in request.session:
        
        del request.session['Usuario']
        request.session.modified = True

    if 'id' in request.session:
        
        del request.session['id']
        request.session.modified = True
    if 'valor_seleccionado' in request.session:
        
        del request.session['valor_seleccionado']
        request.session.modified = True

    if 'nombre_tienda' in request.session:
        
        del request.session['nombre_tienda']
        request.session.modified = True

    # Otras acciones que desees realizar después de cerrar la sesión
    return redirect('home')  # Redirige a la página de inicio o a donde desees
    # return redirect('login')


def activate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError,Account.DoesNotExist):
        user=None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request, 'Felicidades tu cuenta esta activa!')
        return redirect('login')
    
    else:
        messages.error(request,' La activacion es invalida')
        return redirect('register')


def dashboard(request):
    session_data = dict(request.session)
    if session_data:
         try:
              data ={
                "usuario":session_data['id']
                 }   

              # Realizar una nueva solicitud a la API para obtener los detalles del producto
              endpoint = 'obtenerperfil'
              url = f'{URL_APIS}{endpoint}'
            #   url = f'http://192.168.88.136:3002/ecommer/rs/obtenerperfil'

              response = requests.post(url, json=data)  # Usar json=data en lugar de data=data
              data_from_express_api = response.json()

              if response.status_code == 200:
                  info=data_from_express_api['user']
                  info2=data_from_express_api['CarritoDecompra'],
                
                  fecha_obj = datetime.strptime(info['Fecha_nacimiento'], '%Y-%m-%dT%H:%M:%S.%fZ')

                  context={
                      'detalle':info,
                      'carrito':info2[0],
                    
                      'Fecha_nacimiento': fecha_obj.strftime('%m/%d/%Y')
                  }
                  return render(request,'accounts/dashboard.html',context)
                  # return redirect('home')
         
          
              else:
                   context={
                      'detalle':[]
                  }
                   return render(request,'accounts/perfil.html',context)
            
         except Exception as e:
              print(e)
              context = None
              return redirect('login')
      
    else:
        return redirect('login')

def perfil(request):
    session_data = dict(request.session)
    if session_data:
         try:
              data ={
                "usuario":session_data['id']
                 }   

              # Realizar una nueva solicitud a la API para obtener los detalles del producto
              endpoint = 'obtenerperfil'
              url = f'{URL_APIS}{endpoint}'
            #   url = f'http://192.168.88.136:3002/ecommer/rs/obtenerperfil'

              response = requests.post(url, json=data)  # Usar json=data en lugar de data=data
              data_from_express_api = response.json()

              if response.status_code == 200:
                  info=data_from_express_api['user']
                  fecha_obj = datetime.strptime(info['Fecha_nacimiento'], '%Y-%m-%dT%H:%M:%S.%fZ')

                  context={
                      'detalle':info,
                      'Fecha_nacimiento': fecha_obj.strftime('%m/%d/%Y')
                  }
                  return render(request,'accounts/perfil.html',context)
                  # return redirect('home')
         
          
              else:
                   context={
                      'detalle':[]
                  }
                   return render(request,'accounts/perfil.html',context)
            
         except Exception as e:
              print(e)
              context = None
              return redirect('login')
      
    
    else:
        return redirect('login')


def EditarPerfil(request):
      session_data = dict(request.session)
      if session_data:
            if request.method == 'POST':
                try:
                  data ={
                    "nombre":request.POST['nombre'],
                    "apellido":request.POST['apellido'],
                    "fechad":request.POST['fechad'],
                    "Sexo":request.POST['Sexo'],
                    "eresmas":request.POST['eresmas'],
                    "empresa":request.POST['empresa'],
                    "Ruc":request.POST['Ruc'],
                    "Dv":request.POST['Dv'],
                    "usuario":session_data['id']
                     }   
                  
                  # Realizar una nueva solicitud a la API para obtener los detalles del producto
                  endpoint = 'EditarPerfil'
                  url = f'{URL_APIS}{endpoint}'
                #   url = f'http://192.168.88.136:3002/ecommer/rs/EditarPerfil'
    
                  response = requests.post(url, json=data)  # Usar json=data en lugar de data=data
                  data_from_express_api = response.json()
                  referer = request.META.get('HTTP_REFERER')
            
                  if(referer == 'http://127.0.0.1:8000/account/dashboard/'):
                      if response.status_code == 200:
                        
                            return JsonResponse({'status': 'success', 'message': 'Perfil Editado'})
                      elif response.status_code == 201:
                            return JsonResponse({'status': 'error', 'message': 'No Se Pudo Editar El Perfil'})
                           

                      elif response.status_code == 301:
                             return JsonResponse({'status': 'error', 'message': 'Usuario No Encontrado'})
                      
                      else:
                      
                          return JsonResponse({'status': 'error', 'message': 'No Se Pudo Editar El Perfil'})
                          
                  
                  else:
                      if response.status_code == 200:
                            messages.success(request,'Perfil Editado')
                            return redirect(referer)
                          # return redirect('home')
                      elif response.status_code == 201:
                            messages.error(request,'No Se Pudo Editar El Perfil')
                            return redirect(referer)

                      else:
                          messages.error(request,'No Se Pudo Editar El Perfil')
                          return redirect(referer)

                except Exception as e:
                  print(e)
                  context = None
                  referer = request.META.get('HTTP_REFERER')
                  messages.error(request,'No Se Pudo Editar El Perfil')
                  return redirect(referer)
            else:
                   referer = request.META.get('HTTP_REFERER')
                   return redirect(referer)
      else:
            referer = request.META.get('HTTP_REFERER')
            messages.error(request,'Debe Iniciar Session')
            return redirect(referer)
      
def ordenes(request):
    session_data = dict(request.session)
    if session_data:
         return render(request,'accounts/Ordenes.html')
    
    else:
        return redirect('login')

def direccion(request):
    session_data = dict(request.session)
    if session_data:
         try:
              data ={
                "usuario":session_data['id']
                 }   

              # Realizar una nueva solicitud a la API para obtener los detalles del producto
              endpoint = 'obtenerubicaciones'
              url = f'{URL_APIS}{endpoint}'
            #   url = f'http://192.168.88.136:3002/ecommer/rs/obtenerubicaciones'

              response = requests.post(url, json=data)  # Usar json=data en lugar de data=data
              data_from_express_api = response.json()

              if response.status_code == 200:
                  info=data_from_express_api['ubcaciones']
                  Total=data_from_express_api['totalUbicaciones']
                  context={
                      'detalle':info,
                      'Total':Total
                  }
                 
                  return render(request,'accounts/manage-direction.html',context)
                  # return redirect('home')
         
          
              else:
                   context={
                      'detalle':[]
                  }
                
                   return render(request,'accounts/manage-direction.html',context)
            
         except Exception as e:
              print(e)
              context = None
              return redirect('login')
      
    
    else:
        return redirect('login')
 

def Agregardireccion(request):
      session_data = dict(request.session)
      if session_data:
            if request.method=='POST':
             
                try:
                  data ={
                 
                        "usuario" :session_data['id'],
                        "Provincia":request.POST['provincia'],
                        "Distrito":request.POST['distrito'],
                        "Corregimiento":request.POST['corregimiento'],
                        "Detalle" :request.POST['Detalle'],
                        "Recibidor":request.POST['recibidor'],
                        "Celular" :request.POST['Celular'],
                        "Longitud" :request.POST['longitudInput'],
                        "Latitud" :request.POST['latitudInput'],

                     }   
                  if 'Direccionenvio' in request.POST:
                         data["Activa"] = request.POST['Direccionenvio']
                  else:
                        data["Activa"] = 'No'  # Establece un valor predeterminado si no se seleccionó "Direccionenvio"
                  # Realizar una nueva solicitud a la API para obtener los detalles del producto
                  endpoint = 'AgregarDireccion'
                  url = f'{URL_APIS}{endpoint}'
                #   url = f'http://192.168.88.136:3002/ecommer/rs/AgregarDireccion'
    
                  response = requests.post(url, json=data)  # Usar json=data en lugar de data=data
                  data_from_express_api = response.json()
                  referer = request.META.get('HTTP_REFERER')
    
                  if response.status_code == 200:
                        messages.success(request,'Direccion Agregada')
                        return redirect('direccion')
                      # return redirect('home')
                  elif response.status_code == 201:
                        messages.error(request,data_from_express_api['message'])
                        return redirect('direccion')
                
                  else:
                      messages.error(request,' No Se Pudo Registar La Ubicacion')
                      return redirect(referer)

                except Exception as e:
                  print(e)
                  context = None
                  referer = request.META.get('HTTP_REFERER')
                  return redirect(referer)
            else:
 
                
                try:
                  data ={
                        "usuario" :session_data['id'],

                     } 
                  endpoint = 'obtenerProvincia'
                  url = f'{URL_APIS}{endpoint}'
                  #   url = f'http://192.168.88.136:3002/ecommer/rs/AgregarDireccion'
    
                  response = requests.post(url, json=data)  # Usar json=data en lugar de data=data
          
                  data_from_express_api = response.json()
                  referer = request.META.get('HTTP_REFERER')
    
                  if response.status_code == 200:
                     context = {
                          'Provincia':data_from_express_api['provincia'],
                          'GOOGLE_MAPS_API_KEY': GOOGLE_MAPS_API_KEY
                          }
                     return render(request, 'accounts/AddDireccion.html',context)
                      # return redirect('home')
                  elif response.status_code == 201:
                        messages.error(request,data_from_express_api['message'])
                        return redirect('direccion')
                
                  else:
                        messages.error(request,data_from_express_api['message'])
                        return redirect('direccion')
                except Exception as e:
                  print(e)
                  context = None
                  referer = request.META.get('HTTP_REFERER')
                  return redirect(referer)
                



      else:
            messages.error(request,'Debe Iniciar Session')
            return redirect('login')


def obtenerdistrito(request):
    session_data = dict(request.session)
    if session_data:
         try:
            if request.method=='POST':
              data ={
                
                "usuario":session_data['id'],
                "idProvincia" :request.POST['idProvincia']
                 }   

              # Realizar una nueva solicitud a la API para obtener los detalles del producto
              endpoint = 'obtenerdistrito'
              url = f'{URL_APIS}{endpoint}'
            #   url = f'http://192.168.88.136:3002/ecommer/rs/obtenerubicaciones'

              response = requests.post(url, json=data)  # Usar json=data en lugar de data=data
              data_from_express_api = response.json()

              if response.status_code == 200:
               return JsonResponse({'status': 'encontrado', 'data':data_from_express_api['distrito'] })
              else:
               return JsonResponse({'status': 'Noencontrado', 'data':[] })
            
         except Exception as e:
              print(e)
              context = None
              return redirect('login')
      
    
    else:
        return redirect('login')
 
     
def obtenercorregimiento(request):
    session_data = dict(request.session)
    if session_data:
         try:
            if request.method=='POST':
              data ={
                
                "usuario":session_data['id'],
                "idProvincia" :request.POST['idProvincia'],
                "idDistrito":request.POST['idDistrito']
                 }   

              # Realizar una nueva solicitud a la API para obtener los detalles del producto
              endpoint = 'obtenerCorregimitento'
              url = f'{URL_APIS}{endpoint}'
            #   url = f'http://192.168.88.136:3002/ecommer/rs/obtenerubicaciones'

              response = requests.post(url, json=data)  # Usar json=data en lugar de data=data
              data_from_express_api = response.json()
            

              if response.status_code == 200:
               return JsonResponse({'status': 'encontrado', 'data':data_from_express_api['corregimiento'] })
              else:
               return JsonResponse({'status': 'Noencontrado', 'data':[] })
            
         except Exception as e:
              print(e)
              context = None
              return redirect('login')
      
    
    else:
        return redirect('login')
 

def EliminarDireccion(request,idlista):
      session_data = dict(request.session)
      if session_data:
           
             
                try:
                  data ={
                        "idUbicacion" :idlista,
                        "usuario" :session_data['id'],
                     }   
                  endpoint = 'EliminarUbicacion'
                  url = f'{URL_APIS}{endpoint}'
                #   url = f'http://192.168.88.136:3002/ecommer/rs/EliminarUbicacion'
    
                  response = requests.post(url, json=data)  # Usar json=data en lugar de data=data
                  data_from_express_api = response.json()
                  referer = request.META.get('HTTP_REFERER')
                  if response.status_code == 200:
                
                     return JsonResponse({'status': 'success', 'message': 'Producto Eliminado del carrito'})
     
                  if response.status_code == 201:
                     
                     return JsonResponse({'status': 'error', 'message': data_from_express_api['message']})

                
                  else:
                      return JsonResponse({'status': 'error', 'message': ' No Se Pudo Registar La Ubicacion'})

                except Exception as e:
                  print(e)
                  context = None
                  referer = request.META.get('HTTP_REFERER')
                  return redirect(referer)

      else:
            messages.error(request,'Debe Iniciar Session')
            return redirect('login')


def EditarDireccion(request,id):
      session_data = dict(request.session)
      if session_data:
            if request.method == 'POST':
             
                try:
                  data ={
                        "usuario" :session_data['id'],
                        "Provincia":request.POST['provincia'],
                        "Distrito":request.POST['distrito'],
                        "Corregimiento":request.POST['corregimiento'],
                        "Detalle" :request.POST['Detalle'],
                        "Recibidor":request.POST['recibidor'],
                        "Celular" :request.POST['Celular'],
                        "Longitud" :request.POST['longitudInput'],
                        "Latitud" :request.POST['latitudInput'],
                        "idUbicacion" :id

                     }   
                  if 'Direccionenvio' in request.POST:
                         data["Activa"] = request.POST['Direccionenvio']
                  else:
                        data["Activa"] = 'No'  # Establece un valor predeterminado si no se seleccionó "Direccionenvio"
                  # Realizar una nueva solicitud a la API para obtener los detalles del producto
                  endpoint = 'EditarUbicacion'
                  url = f'{URL_APIS}{endpoint}'
                #   url = f'http://192.168.88.136:3002/ecommer/rs/EditarUbicacion'
    
                  response = requests.post(url, json=data)  # Usar json=data en lugar de data=data
    
                  data_from_express_api = response.json()
                  referer = request.META.get('HTTP_REFERER')
    
                  if response.status_code == 200:
                        messages.success(request,'Direccion Agregada')
                        return redirect('direccion')
                      # return redirect('home')
                  elif response.status_code == 201:
                        messages.error(request,data_from_express_api['message'])
                        return redirect('direccion')
                
                  else:
                      messages.error(request,' No Se Pudo Registar La Ubicacion')
                      return redirect(referer)

                except Exception as e:
                  print(e)
                  context = None
                  referer = request.META.get('HTTP_REFERER')
                  return redirect(referer)
            else:
                try:
                  data ={
                      "usuario" :session_data['id'],
                        "idUbicacion" :id
                     }   
                  endpoint = 'verdirecciones'
                  url = f'{URL_APIS}{endpoint}'
                #   url = f'http://192.168.88.136:3002/ecommer/rs/verdirecciones'
    
                  response = requests.post(url, json=data)  # Usar json=data en lugar de data=data
                
                  data_from_express_api = response.json()
                  referer = request.META.get('HTTP_REFERER')
                  data=data_from_express_api['ubcaciones']
  
                  if response.status_code == 200:
                      context = {
                          'detalle':data[0],
                          'direcciones':data_from_express_api['provincia'],
                          'GOOGLE_MAPS_API_KEY': GOOGLE_MAPS_API_KEY
                          }
                      return render(request, 'accounts/EditDireccion.html',context)

                  else:
                      messages.error(request,'Direccion No Encontrada')
                      return redirect('direccion')

                except Exception as e:
                  print(e)
                  context = None
                  messages.error(request,'Direccion No Encontrada')
                  return redirect('direccion')
               

      else:
            messages.error(request,'Debe Iniciar Session')
            return redirect('login')
      
def EditarUbicacion(request):
      session_data = dict(request.session)
      if session_data:
            if request.method=='POST':
             
                try:
          
                  data ={
                        "usuario" :session_data['id'],
                        "Provincia":request.POST['provincia'],
                        "Distrito":request.POST['distrito'],
                        "Corregimiento":request.POST['corregimiento'],
                        "Detalle" :request.POST['Detalle'],
                        "Recibidor":request.POST['recibidor'],
                        "Celular" :request.POST['Celular'],
                        "Longitud" :request.POST['longitudInput'],
                        "Latitud" :request.POST['latitudInput'],
                        "idubicacion" :request.POST['id']
                     }   
            
                  if 'Direccionenvio' in request.POST:
                         data["Activa"] = request.POST['Direccionenvio']
                  else:
                        data["Activa"] = 'No'  # Establece un valor predeterminado si no se seleccionó "Direccionenvio"
                  # Realizar una nueva solicitud a la API para obtener los detalles del producto
                  endpoint = 'EditarUbicacion'
                  url = f'{URL_APIS}{endpoint}'
                #   url = f'http://192.168.88.136:3002/ecommer/rs/EditarUbicacion'
    
                  response = requests.post(url, json=data)  # Usar json=data en lugar de data=data
     
             
                  data_from_express_api = response.json()
                  referer = request.META.get('HTTP_REFERER')
    
                  if response.status_code == 200:
                        messages.success(request,'Direccion Editada Con Exito')
                        return redirect('direccion')
                      # return redirect('home')
                  elif response.status_code == 201:
                        messages.error(request,data_from_express_api['message'])
                        return redirect('direccion')
                
                  else:
                      messages.error(request,' No Se Pudo Registar La Ubicacion')
                      return redirect(referer)

                except Exception as e:
                  print(e)
                  context = None
                  referer = request.META.get('HTTP_REFERER')
                  return redirect(referer)
            else:
                referer = request.META.get('HTTP_REFERER')
                return redirect(referer)
               
               

      else:
            messages.error(request,'Debe Iniciar Session')
            return redirect('login')    

def ActivarDireccion(request,idlista):
      session_data = dict(request.session)
      if session_data:
           
             
                try:
                  data ={
                        "idUbicacion" :idlista,
                        "usuario" :session_data['id'],


                     }   
                  endpoint = 'activarubicacion'
                  url = f'{URL_APIS}{endpoint}'
                #   url = f'http://192.168.88.136:3002/ecommer/rs/activarubicacion'
    
                  response = requests.post(url, json=data)  # Usar json=data en lugar de data=data
                  data_from_express_api = response.json()
                  referer = request.META.get('HTTP_REFERER')
    
                  if response.status_code == 200:
                        messages.success(request,'Direccion De Envio Activada')
                        return redirect('direccion')
                      # return redirect('home')
                  elif response.status_code == 201:
                        messages.error(request,data_from_express_api['message'])
                        return redirect('direccion')
                
                  else:
                      messages.error(request,' No Se Pudo Cambiar La Ubicacion')
                      return redirect(referer)

                except Exception as e:
                  print(e)
                  context = None
                  referer = request.META.get('HTTP_REFERER')
                  return redirect(referer)

      else:

            return redirect('login')



def ListaCompra(request):
      session_data = dict(request.session)
      if session_data:
            try:
              data ={
                "usuario":session_data['id']
                 }   

              # Realizar una nueva solicitud a la API para obtener los detalles del producto
              endpoint = 'listafavorito'
              url = f'{URL_APIS}{endpoint}'
            #   url = f'http://192.168.88.136:3002/ecommer/rs/listafavorito'

              response = requests.get(url, json=data)  # Usar json=data en lugar de data=data
              data_from_express_api = response.json()

              if response.status_code == 200:
                  existingCart=data_from_express_api['existingCart']
                  context={
                      'lista':existingCart
                  }
                  return render(request, 'accounts/wishlist.html',context) 
                  # return redirect('home')
         
          
              else:
                   context={
                      'lista':[]
                  }
                   return render(request, 'accounts/wishlist.html',context) 
            
            except Exception as e:
              print(e)
              context = None
              return redirect('login')
      else:
    
           return redirect('login')
      
def Listaproductos(request,id):
      session_data = dict(request.session)
      if session_data:
            try:
              if "valor_seleccionado" in session_data:
                bodega = session_data['valor_seleccionado']
              else:
                bodega=114100500
              data ={
                "usuario":session_data['id'],
                "idlista":id,
                "bodega":bodega
                 }   

              # Realizar una nueva solicitud a la API para obtener los detalles del producto
              endpoint = 'listafavoritoviewproduct'
              url = f'{URL_APIS}{endpoint}'
            #   url = f'http://192.168.88.136:3002/ecommer/rs/listafavoritoviewproduct'

              response = requests.get(url, json=data)  # Usar json=data en lugar de data=data
              data_from_express_api = response.json()
           
              if response.status_code == 200:
                  existingCart=data_from_express_api['carrito']
              
                  context={
                      'Productos':existingCart,
                      'idlista':id
                  }
                  return render(request, 'accounts/wishlistProduct.html',context) 
                  # return redirect('home')
         
          
              elif response.status_code == 201:
                  
                  context={
                      'Productos':[],
                      'idlista':id
                  }
           
                  return render(request, 'accounts/wishlistProduct.html',context) 
              
              else:
          
                  return redirect('dashboard') 
                  
            
            except Exception as e:
              print(e)
              context = None
              return redirect('dashboard') 
      else:
    
           return redirect('login')
      
def NuevaLista(request):
      session_data = dict(request.session)
      if session_data:
            if request.method=='POST':
                try:
                  data ={
                    "Detalle":request.POST['detalle'],
                    "usuario":session_data['id'],
                     }   
                  # Realizar una nueva solicitud a la API para obtener los detalles del producto
                  endpoint = 'addlistafavorito'
                  url = f'{URL_APIS}{endpoint}'
                #   url = f'http://192.168.88.136:3002/ecommer/rs/addlistafavorito'
    
                  response = requests.post(url, json=data)  # Usar json=data en lugar de data=data
                  data_from_express_api = response.json()
                  referer = request.META.get('HTTP_REFERER')
    
                  if response.status_code == 200:
                        messages.success(request,'Lista Creada')
                        return redirect(referer)
                      # return redirect('home')
                  elif response.status_code == 201:
                        messages.error(request,'No Se Pudo Crear La Lista')
                        return redirect(referer)
                
                  else:
                      messages.error(request,' No Se Pudo Crear La Lista')
                      return redirect(referer)

                except Exception as e:
                  print(e)
                  context = None
                
                  return redirect(referer)
            else:
                   referer = request.META.get('HTTP_REFERER')
                   return redirect(referer)
      else:
            messages.error(request,'Debe Iniciar Session')
            return redirect('login')
      

def AgregaraLista(request):
      session_data = dict(request.session)
      if session_data:
            if request.method=='POST':
                try:
                  data ={
                    "idlista":request.POST['idlista'],
                    "item":request.POST['item']
                     }   
                  # Realizar una nueva solicitud a la API para obtener los detalles del producto
                  endpoint = 'agregarproductolista'
                  url = f'{URL_APIS}{endpoint}'
                #   url = f'http://192.168.88.136:3002/ecommer/rs/agregarproductolista'
    
                  response = requests.post(url, json=data)  # Usar json=data en lugar de data=data
                  data_from_express_api = response.json()
                  referer = request.META.get('HTTP_REFERER')
    
                  if response.status_code == 200:
                        messages.success(request,' Producto Agregado Al Listado')
                        return redirect(referer)
                      # return redirect('home')
                  elif response.status_code == 201:
                        messages.error(request,' Producto Ya Se Encuentra En El Listado')
                        return redirect(referer)
                
                  else:
                      messages.error(request,' No se pudo Agregar Al Listado')
                      return redirect(referer)

                except Exception as e:
                  print(e)
                  context = None
                  messages.error(request,' No se pudo Agregar Al Listado')
                  return redirect(referer)
            else:
                   referer = request.META.get('HTTP_REFERER')
                   return redirect(referer)
      else:
            referer = request.META.get('HTTP_REFERER')
            messages.error(request,'Debe Iniciar Session')
            return redirect(referer)
      

def AgregaraListaNueva(request):
      session_data = dict(request.session)
      if session_data:
            if request.method=='POST':
                try:
                  data ={
                    "usuario":session_data['id'],
                    "Detalle":request.POST['detalle'],
                    "item":request.POST['item']
                     }   
                  # Realizar una nueva solicitud a la API para obtener los detalles del producto
                  endpoint = 'agregarlistaProduct'
                  url = f'{URL_APIS}{endpoint}'
                #   url = f'http://192.168.88.136:3002/ecommer/rs/agregarlistaProduct'
    
                  response = requests.post(url, json=data)  # Usar json=data en lugar de data=data
                  data_from_express_api = response.json()
                  referer = request.META.get('HTTP_REFERER')
    
                  if response.status_code == 200:
                        messages.success(request,' Producto Agregado Al Listado')
                        return redirect(referer)
                      # return redirect('home')
                  elif response.status_code == 201:
                        messages.error(request,' Producto Ya Se Encuentra En El Listado')
                        return redirect(referer)
                
                  else:
                      messages.error(request,' No se pudo Agregar Al Listado')
                      return redirect(referer)

                except Exception as e:
                  print(e)
                  context = None
                  messages.error(request,' No se pudo Agregar Al Listado')
                  return redirect(referer)
            else:
                   referer = request.META.get('HTTP_REFERER')
                   return redirect(referer)
      else:
            referer = request.META.get('HTTP_REFERER')
            messages.error(request,'Debe Iniciar Session')
            return redirect(referer)
      

def eliminarLista(request,idlista):
      session_data = dict(request.session)
      if session_data:
            try:
              data ={
                "usuario":session_data['id'],
                "idlista":idlista,
                 }   

              # Realizar una nueva solicitud a la API para obtener los detalles del producto
              endpoint = 'eliminarLista'
              url = f'{URL_APIS}{endpoint}'
            #   url = f'http://192.168.88.136:3002/ecommer/rs/eliminarLista'

              response = requests.post(url, json=data)  # Usar json=data en lugar de data=data
              data_from_express_api = response.json()
              referer = request.META.get('HTTP_REFERER')
              if response.status_code == 200:
        
                 messages.success(request,'Lista Eliminada')
                 return redirect(referer)
         
          
              elif response.status_code == 201:
            
                 messages.success(request,data_from_express_api['message'] )
                 return redirect(referer)
              
              else:
          
                  return redirect('dashboard') 
                  
            
            except Exception as e:
              print(e)
              context = None
              return redirect('dashboard') 
      else:
    
           return redirect('login')

def eliminarProductoListado(request,idlista,item):
      session_data = dict(request.session)
      if session_data:
            try:
              data ={
                "usuario":session_data['id'],
                "idlista":idlista,
                "item":item
                 }   

              # Realizar una nueva solicitud a la API para obtener los detalles del producto
              endpoint = 'eliminarProductoListado'
              url = f'{URL_APIS}{endpoint}'
            #   url = f'http://192.168.88.136:3002/ecommer/rs/eliminarProductoListado'

              response = requests.post(url, json=data)  # Usar json=data en lugar de data=data
              data_from_express_api = response.json()
              referer = request.META.get('HTTP_REFERER')
              if response.status_code == 200:
        
                 messages.success(request,' Producto Eliminado Del Listado')
                 return redirect(referer)
         
          
              elif response.status_code == 201:
            
                 messages.success(request,data_from_express_api['message'] )
                 return redirect(referer)
              
              else:
          
                  return redirect('dashboard') 
                  
            
            except Exception as e:
              print(e)
              context = None
              return redirect('dashboard') 
      else:
    
           return redirect('login')



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
             endpoint = 'carrito'
             url = f'{URL_APIS}{endpoint}'
            #  url = f'http://192.168.88.136:3002/ecommer/rs/carrito'
     
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
              endpoint = 'carrito'
              url = f'{URL_APIS}{endpoint}'
            #   url = f'http://192.168.88.136:3002/ecommer/rs/carrito'
      
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




