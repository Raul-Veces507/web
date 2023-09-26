from django.contrib import admin
from .models import Product,Banner
from django.utils.html import format_html
import pandas as pd
from django.http import HttpResponse
from io import BytesIO
import openpyxl
# Register your models here.


class adminProduct(admin.ModelAdmin):
    list_display=('nombre','item','sku','inventario','bodega','Marca')
    search_fields=['nombre','item','sku','bodega','Marca']

class adminBanner(admin.ModelAdmin):
       def thumbnail(self,object):
        return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.images.url))
       thumbnail.short_description="imagen de perfil"
       list_display=('thumbnail','nombre','fechainicial','fechaFinal','created_date')




admin.site.register(Banner,adminBanner)

# Define la función de importación desde Excel
def importar_desde_excel(modeladmin, request, queryset):
    # Verifica si se ha seleccionado al menos un registro
    if not queryset:
        modeladmin.message_user(request, "Debes seleccionar al menos un registro para importar desde Excel.", level="warning")
        return

    # Creamos un DataFrame de pandas vacío para recopilar los datos
    df = pd.DataFrame()

    # Itera sobre los registros seleccionados y agrega los campos relevantes al DataFrame
    for producto in queryset:
        data = {
            'nombre': producto.nombre,
            'item': producto.item,
            'sku': producto.sku,
            'precio': producto.precio,
            'Impuesto': producto.Impuesto,
            'Size': producto.Size,
            'img': producto.img,
            'inventario': producto.inventario,
            'bodega': producto.bodega,
            'Marca': producto.Marca,
            'Detalle': producto.Detalle,
            # Agrega más campos según sea necesario
        }
        df = df.append(data, ignore_index=True)

    # Convierte el DataFrame a un archivo Excel
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')
    df.to_excel(writer, index=False, sheet_name='Productos')
    writer.save()
    output.seek(0)

    # Devuelve el archivo Excel como una respuesta HTTP
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=productos.xlsx'
    response.write(output.getvalue())

    return response

# Agrega una descripción a la acción de importación
importar_desde_excel.short_description = "Importar registros seleccionados a Excel"

# Define la clase del administrador de Product con la acción personalizada
class AdminProduct(admin.ModelAdmin):
    list_display=('nombre','item','sku','inventario','bodega','Marca')
    search_fields=['nombre','item','sku','bodega','Marca']
    actions = [importar_desde_excel]  # Agrega la acción de importación
    change_list_template = "admin/change_list_with_upload_button.html"  # Utiliza una plantilla personalizada para agregar el botón de carga

# Registra el modelo Product con el administrador personalizado
admin.site.register(Product, AdminProduct)
