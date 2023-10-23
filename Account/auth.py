
from django.shortcuts import redirect
import requests
from ribasmith.settings import URL_APIS
def verificar_autenticacion(request):
    # Verifica si el token de autenticación está presente en la sesión del usuario
    token = request.session.get('token')
 
    if token is None:
        # Si el token no está presente, redirige al usuario a la página de inicio de sesión
        return redirect('login')  # Reemplaza 'login' con la URL de tu página de inicio de sesión

    # Realiza una solicitud a la API de Node.js para verificar la validez del token
    # api_url = f'http://192.168.88.136:3005/ecommer/rs/ruta-protegida'  # Reemplaza con la URL de tu API de autenticación
    endpoint = 'ruta-protegida'
    api_url = f'{URL_APIS}{endpoint}'
    headers = {'x-token': f'{token}'}

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        # Si la API responde con éxito (código 200), el token es válido
        return None
    else:
        # Si la API responde con un código de error (por ejemplo, 401 No Autorizado),
        # el token no es válido, por lo que puedes redirigir al usuario a la página de inicio de sesión
        return redirect('login')  # Reemplaza 'login' con la URL de tu página de inicio de sesión
