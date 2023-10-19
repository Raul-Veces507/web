from django.db import models

from category.models import categorias

# Create your models here.
class Grupo(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(categorias, on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.nombre
    
    def categrorianame(self):
        print(self)
        return self.categoria.nombre
    