from django.urls import path

from . import views

urlpatterns=[
    path('register/',views.register, name='register'),
    path('wishlistProduct/',views.wishlistProduct,name="wishlistProduct"),
    path('login/',views.login, name='login'),
    path('logout/',views.logout, name='logout'),
    path('guardar_valor_en_sesion/',views.guardar_valor_en_sesion, name='guardar_valor_en_sesion'),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('perfil/',views.perfil, name='perfil'),
    path('EditarPerfil/',views.EditarPerfil, name='EditarPerfil'),
    path('ordenes/<str:idordens>/',views.ordenes, name='ordenes'),
    path('direccion/',views.direccion, name='direccion'),
    path('obtenerdistrito/',views.obtenerdistrito, name='obtenerdistrito'),
    path('obtenercorregimiento/',views.obtenercorregimiento, name='obtenercorregimiento'),
    path('direccion/Agregar',views.Agregardireccion, name='Agregardireccion'),
    path('EliminarDireccion/<str:idlista>/',views.EliminarDireccion, name='EliminarDireccion'),
    path('ActivarDireccion/<str:idlista>/',views.ActivarDireccion, name='ActivarDireccion'),
    path('direccion/Editar/<str:id>',views.EditarDireccion,name='EditarDireccion'),
    path('direccion/EditarUbicacion/',views.EditarUbicacion,name='EditarUbicacion'),
    path('ListaCompra/',views.ListaCompra,name='ListaCompra'),
    path('ListaCompra/<str:id>',views.Listaproductos,name='Listaproductos'),
    path('NuevaLista/>',views.NuevaLista,name='NuevaLista'),
    path('AgregaraLista/',views.AgregaraLista,name='AgregaraLista'),
    path('AgregaraListaNueva/',views.AgregaraListaNueva,name='AgregaraListaNueva'),
    path('eliminarLista/<str:idlista>',views.eliminarLista,name='eliminarLista'),
    path('eliminarProductoListado/<str:idlista>/<str:item>',views.eliminarProductoListado,name='eliminarProductoListado'),
    path('activate/<uidb64>/',views.activate, name='activate'),
    

    
    

]