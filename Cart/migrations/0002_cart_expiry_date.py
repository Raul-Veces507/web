# Generated by Django 4.2.4 on 2023-10-09 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='expiry_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
