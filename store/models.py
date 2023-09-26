
from django.db import models
from django.urls import reverse
from Grupo.models import Grupo

from category.models import categorias

class Product(models.Model):

    nombre = models.CharField(max_length=255)
    item = models.CharField(max_length=255)
    sku = models.CharField(max_length=25)
    precio = models.DecimalField(max_digits=16, decimal_places=2)
    Impuesto = models.IntegerField()
    Size = models.CharField(max_length=50)
    inventario = models.IntegerField()
    bodega = models.IntegerField()
    Marca = models.CharField(max_length=50)
    Detalle = models.CharField(max_length=200)
    CodigoPeso = models.IntegerField()
    FactorConversion = models.DecimalField(max_digits=4, decimal_places=2)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now=True)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE,null=True)

  
    def __str__(self):
        return self.nombre
    
    def categrorianame(self):
        cat=categorias.objects.filter(id=self.grupo.categoria_id).values_list('name', flat=True).first()
        return cat
     
    
    def get_url_marca(self):
        return reverse('products_by_category_marca',args=[self.categoria_id,self.Marca])
    

    def viewproduct(self):
           return reverse('product_detail',args=[self.grupo,self.item])
    
   
    



class Banner(models.Model):
    
    nombre=models.CharField(max_length=50)
    images=models.ImageField(upload_to='photos/banner')
    fechainicial=models.DateTimeField()
    fechaFinal=models.DateTimeField()
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.nombre



