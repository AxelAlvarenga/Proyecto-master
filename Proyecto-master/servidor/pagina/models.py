
from django.db import models

# Create your models here.


class Usuarios(models.Model):
    cod_usuario=models.AutoField(primary_key=True)
    nombre_usuario = models.CharField(max_length = 50)
    password_usuario = models.CharField(max_length = 50)
    nombre_completo_usuario = models.CharField(max_length = 200)
    tipo_usuario=models.IntegerField()

class cliente(models.Model):
    codigo_cliente=models.IntegerField(primary_key=True)
    nombre_cliente= models.CharField(max_length = 50)
    telefono_cliente= models.IntegerField()
    direccion_cliente=models.CharField(max_length=50)

class cliente_audi(models.Model):
    codigo_cliente=models.IntegerField()
    nombre_cliente= models.CharField(max_length = 50)
    telefono_cliente= models.IntegerField()
    direccion_cliente=models.CharField(max_length=50)
    cod_usuario=models.IntegerField()
    nombre_usuario = models.CharField(max_length = 50)

class categoria(models.Model):
    codigo_categoria=models.AutoField(primary_key=True)
    nombre_categoria=models.CharField(max_length = 50) 

class metodo_pago(models.Model):
    codigo_metodo_pago=models.AutoField(primary_key=True)
    nombre_metodo_pago=models.CharField(max_length = 50) 



class proveedor(models.Model):
    codigo_proveedor=models.AutoField(primary_key=True)
    nombre_proveedor= models.CharField(max_length = 50)
    ruc_proveedor= models.CharField(max_length = 50)
    Telefono_proveedor= models.IntegerField()
    direccion_proveedor=models.CharField(max_length= 50)

class proveedor_audi(models.Model):
    codigo_proveedor=models.IntegerField()
    nombre_proveedor= models.CharField(max_length = 50)
    ruc_proveedor= models.CharField(max_length = 50)
    Telefono_proveedor= models.IntegerField()
    direccion_proveedor=models.CharField(max_length= 50)
    cod_usuario=models.IntegerField()
    nombre_usuario = models.CharField(max_length = 50)

class producto(models.Model):
    codigo_productos=models.IntegerField(primary_key=True)
    nombre_productos= models.CharField(max_length = 50)
    preciocompra_productos= models.IntegerField()
    precioventa_productos= models.IntegerField()
    categoria_productos= models.IntegerField()
    cantidad_productos=models.IntegerField()
    nombre_proveedor = models.ForeignKey(proveedor ,on_delete=models.CASCADE,null=True)

class producto_audi(models.Model):
    codigo_productos=models.IntegerField()
    nombre_productos= models.CharField(max_length = 50)
    preciocompra_productos= models.IntegerField()
    precioventa_productos= models.IntegerField()
    categoria_productos= models.IntegerField()
    cantidad_productos=models.IntegerField()
    nombre_proveedor = models.ForeignKey(proveedor ,on_delete=models.CASCADE,null=True)
    cod_usuario=models.IntegerField()
    nombre_usuario = models.CharField(max_length = 50)

class caja(models.Model):
    codigo_caja=models.AutoField(primary_key=True)
    fecha_caja=models.DateField()
    hora_caja=models.TimeField()
    motivo_caja=models.CharField(max_length = 50, null=True)
    entrada_caja=models.CharField(max_length = 50, null=True)
    salida_caja=models.CharField(max_length = 50, null=True)
    tipo_mov=models.IntegerField(null=True)
    nombre_usuario = models.ForeignKey(Usuarios ,on_delete=models.CASCADE,null=True)
    total_caja=models.CharField(max_length = 50, null=True)

class venta(models.Model):
    codigo_venta=models.AutoField(primary_key=True)
    codigo_cliente_venta = models.IntegerField()
    fecha_venta =models.DateField()
    metodo_de_pago = models.ForeignKey(metodo_pago, on_delete=models.CASCADE)
    total_venta =models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    subtotal_venta=models.DecimalField(default=0.00, max_digits=9, decimal_places=2,null=True)
    iva=models.DecimalField(default=0.00, max_digits=9, decimal_places=2, null=True)
    
class detalle_venta(models.Model):
    venta_detalle=models.AutoField(primary_key=True)
    producto_detalle=models.ForeignKey(producto, on_delete=models.CASCADE)
    precio_detalle=models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cantidad_detalle=models.IntegerField()
    subtotal=models.DecimalField(default=0.00, max_digits=9, decimal_places=2)