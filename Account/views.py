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
from ribasmith.settings import GOOGLE_MAPS_API_KEY
def register(request):
    form=RegistrationForm()
    if request.method == 'POST':
    
        form=RegistrationForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            phone_number=form.cleaned_data['phone_number']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            username=email.split("@")[0]
            user=Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.phone_number=phone_number
            user.save()
            
            current_site=get_current_site(request)
            mail_subject=' Por favor activa tu cuenta en Riba Smith'
            body= render_to_string('accounts/account_verification_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user)
            })

            to_email=email
            send_email=EmailMessage(mail_subject,body,to=[to_email])
            send_email.send()


            #messages.success(request,'Se registrio el usuario exitosamente')

            return redirect('/account/login?command=verification&email='+email)



  
    context={
        'form':form
    }
    return render(request, 'account/register.html',context)

def login(request):
    if request.method== 'POST':
        email=request.POST['email']
        password=request.POST['password']
        cart=_cart_id(request)
        try:
          data ={
           "email":email,
            "password":password,
            "cart":cart

             }   
          # Realizar una nueva solicitud a la API para obtener los detalles del producto
          url = f'http://192.168.88.136:3002/ecommer/rs/login'
  
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
             
          else:
              return JsonResponse({'status': 'error', 'message': 'Error al agregar el producto al carrito'})
  

        except Exception as e:
          print(e)
          context = None
          return JsonResponse({'status': 'error', 'message': 'Error interno del servidor'})
   
    #     user=auth.authenticate(email=email,password=password)
   
    #     if user is not None:
    #         auth.login(request,user)
    #         return redirect('home')
        
    #     else:
    #         messages.error(request, 'Las credenciales son incorrectas')
    #         return redirect('login')


    return render(request, 'accounts/login.html')



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
         return render(request,'accounts/dashboard.html')
    
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
              url = f'http://192.168.88.136:3002/ecommer/rs/obtenerperfil'

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
              url = f'http://192.168.88.136:3002/ecommer/rs/obtenerubicaciones'

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
                        "Detalle" :request.POST['Detalle'],
                        "usuario" :session_data['id'],
                        "Celular" :request.POST['Celular'],
                        "Longitud" :request.POST['longitudInput'],
                        "Latitud" :request.POST['latitudInput'],

                     }   
                  if 'Direccionenvio' in request.POST:
                         data["Activa"] = request.POST['Direccionenvio']
                  else:
                        data["Activa"] = 'No'  # Establece un valor predeterminado si no se seleccionó "Direccionenvio"
                  # Realizar una nueva solicitud a la API para obtener los detalles del producto
                  print(data)
                  url = f'http://192.168.88.136:3002/ecommer/rs/AgregarDireccion'
    
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
                context = {
                          'GOOGLE_MAPS_API_KEY': GOOGLE_MAPS_API_KEY
                          }
                return render(request, 'accounts/AddDireccion.html',context)

      else:
            messages.error(request,'Debe Iniciar Session')
            return redirect('login')


def EliminarDireccion(request,idlista):
      session_data = dict(request.session)
      if session_data:
           
             
                try:
                  data ={
                        "idUbicacion" :idlista,
                        "usuario" :session_data['id'],
                     }   
                  print(data)
                  url = f'http://192.168.88.136:3002/ecommer/rs/EliminarUbicacion'
    
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
            if request.method=='POST':
             
                try:
                  data ={
                        "Detalle" :request.POST['Detalle'],
                        "usuario" :session_data['id'],
                        "Celular" :request.POST['Celular'],
                        "Longitud" :request.POST['longitudInput'],
                        "Latitud" :request.POST['latitudInput'],

                     }   
                  if 'Direccionenvio' in request.POST:
                         data["Activa"] = request.POST['Direccionenvio']
                  else:
                        data["Activa"] = 'No'  # Establece un valor predeterminado si no se seleccionó "Direccionenvio"
                  # Realizar una nueva solicitud a la API para obtener los detalles del producto
               
                  url = f'http://192.168.88.136:3002/ecommer/rs/EditarUbicacion'
    
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
                  url = f'http://192.168.88.136:3002/ecommer/rs/verdirecciones'
    
                  response = requests.post(url, json=data)  # Usar json=data en lugar de data=data
                
                  data_from_express_api = response.json()
                  referer = request.META.get('HTTP_REFERER')
                  data=data_from_express_api['ubcaciones']
                 
                  if response.status_code == 200:
                      context = {
                          'detalle':data[0],
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
                        "Detalle" :request.POST['Detalle'],
                        "usuario" :session_data['id'],
                        "Celular" :request.POST['Celular'],
                        "Longitud" :request.POST['longitudInput'],
                        "Latitud" :request.POST['latitudInput'],
                        "idubicacion":request.POST['idubicacion']

                     }   
                  if 'Direccionenvio' in request.POST:
                         data["Activa"] = request.POST['Direccionenvio']
                  else:
                        data["Activa"] = 'No'  # Establece un valor predeterminado si no se seleccionó "Direccionenvio"
                  # Realizar una nueva solicitud a la API para obtener los detalles del producto
               
                  url = f'http://192.168.88.136:3002/ecommer/rs/EditarUbicacion'
    
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
                  url = f'http://192.168.88.136:3002/ecommer/rs/activarubicacion'
    
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
            messages.error(request,'Debe Iniciar Session')
            return redirect('login')



def ListaCompra(request):
      session_data = dict(request.session)
      if session_data:
            try:
              data ={
                "usuario":session_data['id']
                 }   

              # Realizar una nueva solicitud a la API para obtener los detalles del producto
              url = f'http://192.168.88.136:3002/ecommer/rs/listafavorito'

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
              data ={
                "usuario":session_data['id'],
                "idlista":id
                 }   

              # Realizar una nueva solicitud a la API para obtener los detalles del producto
              url = f'http://192.168.88.136:3002/ecommer/rs/listafavoritoviewproduct'

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
                  url = f'http://192.168.88.136:3002/ecommer/rs/addlistafavorito'
    
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
                  url = f'http://192.168.88.136:3002/ecommer/rs/agregarproductolista'
    
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
                  url = f'http://192.168.88.136:3002/ecommer/rs/agregarlistaProduct'
    
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
              url = f'http://192.168.88.136:3002/ecommer/rs/eliminarLista'

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
              url = f'http://192.168.88.136:3002/ecommer/rs/eliminarProductoListado'

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




