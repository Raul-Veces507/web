from django.urls import reverse
from django.db import models

from Departamento.models import Departamento

# Create your models here.
class categorias(models.Model):
    
    name = models.CharField(max_length=255)
    img = models.CharField(max_length=255)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   


    def __str__(self):
        return self.name
    


    
  