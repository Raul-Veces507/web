from django.contrib import admin
from .models import Grupo
# Register your models here.

class adminGrupo(admin.ModelAdmin):
    list_display=('nombre','categoria','created_date','modified_date')
    search_fields=['nombre','categoria']


admin.site.register(Grupo,adminGrupo)