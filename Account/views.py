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
          print(data_from_express_api)
  
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
        print('j')
        del request.session['token']
        request.session.modified = True

    if 'Usuario' in request.session:
        print('j2')
        del request.session['Usuario']
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




