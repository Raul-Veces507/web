from django.contrib import admin
from .models import Departamento
# Register your models here.

class adminDepartamento(admin.ModelAdmin):
    list_display=('nombre','created_date','modified_date')
    search_fields=['nombre']


admin.site.register(Departamento,adminDepartamento)

