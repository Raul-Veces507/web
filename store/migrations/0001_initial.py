# Generated by Django 4.2.4 on 2023-09-26 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('images', models.ImageField(upload_to='photos/banner')),
                ('fechainicial', models.DateTimeField()),
                ('fechaFinal', models.DateTimeField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('item', models.CharField(max_length=255)),
                ('sku', models.CharField(max_length=25)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=16)),
                ('Impuesto', models.IntegerField()),
                ('Size', models.CharField(max_length=50)),
                ('inventario', models.IntegerField()),
                ('bodega', models.IntegerField()),
                ('Marca', models.CharField(max_length=50)),
                ('Detalle', models.CharField(max_length=200)),
                ('CodigoPeso', models.IntegerField()),
                ('FactorConversion', models.DecimalField(decimal_places=2, max_digits=4)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
