
from django.db import models
from django.urls import reverse

from category.models import categorias

class Product(models.Model):
    # Definir los campos que corresponden a la estructura de la tabla
    id = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=255)
    item = models.CharField(max_length=255)
    sku = models.CharField(max_length=25)
    precio = models.CharField(max_length=255)
    Impuesto = models.IntegerField()
    Size = models.CharField(max_length=50)
    img = models.CharField(max_length=255)
    inventario = models.IntegerField()
    bodega = models.IntegerField()
    Marca = models.CharField(max_length=50)
    Detalle = models.CharField(max_length=200)
    events_id = models.BigIntegerField(null=True, blank=True)
    categoria_id = models.BigIntegerField(null=True, blank=True)
    subcategoria_id = models.IntegerField(null=True, blank=True)
    Botones = models.IntegerField()
    updated_at = models.DateTimeField(null=True, blank=True)
    CodigoPeso = models.IntegerField()
    FactorConversion = models.DecimalField(max_digits=4, decimal_places=2)

    # Establecer managed = False para que Django no cree la tabla
    class Meta:
        managed = False
        db_table = 'products'  # Especifica el nombre de la tabla existente en la base de datos
    def __str__(self):
        return self.nombre
    
    def categrorianame(self):
        cat=categorias.objects.filter(id=self.categoria_id).values_list('name', flat=True).first()
        print(cat)
      
        return cat
    
    def get_url_marca(self):
        return reverse('products_by_category_marca',args=[self.categoria_id,self.Marca])
    

    def viewproduct(self):
           return reverse('product_detail',args=[self.categoria_id,self.item])
    
   
    



class Banner(models.Model):
    
    nombre=models.CharField(max_length=50)
    images=models.ImageField(upload_to='photos/banner')
    fechainicial=models.DateTimeField()
    fechaFinal=models.DateTimeField()
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.nombre


class ProductViewPrincipal(models.Model):
    Status=(
        ('Activo','Activo'),
        ('Desactivdado','Desactivdado'),

       )
     
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    status=models.CharField(max_length=50,choices=Status,default='Activo')
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.product.nombre


class ProductViewBanner(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    Banner=models.ForeignKey(Banner, on_delete=models.CASCADE,blank=True,null=True)
    def __str__(self):
        return self.product.nombre
    def __str__(self):
        return self.Banner.nombre

