from django.contrib import admin
from .models import Product,Banner,ProductViewBanner,ProductViewPrincipal
from django.utils.html import format_html
import pandas as pd
# Register your models here.


class adminProduct(admin.ModelAdmin):
    list_display=('nombre','item','sku','inventario','bodega','Marca','events_id','categoria_id','subcategoria_id')
    search_fields=['nombre','item','sku','bodega','Marca']

class adminBanner(admin.ModelAdmin):
       def thumbnail(self,object):
        return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.images.url))
       thumbnail.short_description="imagen de perfil"
       list_display=('thumbnail','nombre','fechainicial','fechaFinal','created_date')

class adminProductViewBanner(admin.ModelAdmin):
       def thumbnail(self,object):
        return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.images.url))
       thumbnail.short_description="imagen de perfil"
       list_display=('thumbnail','Banner','product')

class adminProductViewPrincipal(admin.ModelAdmin):

       list_display=('product','status','created_at','update_at')


class ProductAdmin1(admin.ModelAdmin):
    actions = ['cargar_desde_excel']

    from .models import Product  # Asegúrate de importar el modelo Product correctamente en esta parte de tu archivo admin.py

class ProductAdmin1(admin.ModelAdmin):
    actions = ['cargar_desde_excel']

    def cargar_desde_excel(self, request, queryset):
        for producto in queryset:
            archivo_excel = producto.archivo_excel  # Asume que tienes un campo FileField llamado 'archivo_excel'
            df = pd.read_excel(archivo_excel.path)
            for index, row in df.iterrows():
                nuevo_producto = Product(
                    id=row['id'],
                    nombre=row['nombre'],
                    item=row['item'],
                    sku=row['sku'],
                    precio=row['precio'],
                    impuesto=row['impuesto'],
                    Size=row['size'],
                    Marca=row['marca'],
                    Detalle=row['detalle'],
                    events_id=row['Evento'],
                    categoria_id=row['Categoria'],
                    subcategoria_id=row['subacategoria'],
                    CodigoPeso=row['codigoPesp'],
                    FactorConversion=row['FactorConversion']
                )
                nuevo_producto.save()

    cargar_desde_excel.short_description = "Cargar desde Excel"




admin.site.register(Banner,adminBanner)

admin.site.register(Product,ProductAdmin1)

admin.site.register(ProductViewBanner)

admin.site.register(ProductViewPrincipal)
