# Generated by Django 4.0.2 on 2022-02-20 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagina', '0005_venta_cantidad_detalle'),
    ]

    operations = [
        migrations.AddField(
            model_name='venta',
            name='codigo_producto',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='venta',
            name='nombre_producto_venta',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
