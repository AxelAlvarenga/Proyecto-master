import json
from django.db import models
from django.http import JsonResponse, request,HttpResponse
from django.shortcuts import render, redirect
from pagina.models import *
from django.views.generic import ListView
from datetime import date




def login(request):
    if request.method == "GET":
        if request.session.get("cod_usuario"):
            return redirect("reportes_cliente")
        else: 
            return render(request, 'login.html')
    if request.method == "POST":
        nusuario = request.POST.get("usuario")
        pusuario = request.POST.get("contra")
        usuario_actual=Usuarios.objects.filter(nombre_usuario=nusuario).exists()
        if usuario_actual:
            datos_usuario=Usuarios.objects.filter(nombre_usuario=nusuario).first()

            if getattr(datos_usuario,"password_usuario")==pusuario:
                request.session["cod_usuario"]=getattr(datos_usuario, "cod_usuario")
                request.session["nombredelusuario"]=getattr(datos_usuario, "nombre_usuario")
                request.session["nombre_completo_usuario"]=getattr(datos_usuario, "nombre_completo_usuario")
                request.session["tipo_usuario"]=getattr(datos_usuario, "tipo_usuario")
                return redirect("reportes_cliente")
            else:
                return render(request, 'login.html', {"mensaje_error":"Contraseña ingresada es incorrecta."})
        else:
            return render(request, 'login.html', {"mensaje_error":"Usuario ingresado no existe."})

def validar(request, pageSuccess , parameters={}):
    if request.session.get("cod_usuario"):
        if (request.session.get("tipo_usuario") == 2) and ((pageSuccess == 'cargar_cliente.html')) and ((pageSuccess == 'cargar_compra.html')) :
            return render(request, "reportes_cliente.html", {"nombre_completo": request.session.get("nombredelusuario"),"tipo_usuario": request.session.get("tipo_usuario"), "mensaje": "Este usuario no cuenta con los privilegios suficientes"})
        else: 
            return render(request, pageSuccess, {"nombre_completo": request.session.get("nombredelusuario"),"tipo_usuario": request.session.get("tipo_usuario"), "parameters": parameters})
    else:
        return render(request, 'login.html') 

          
def inicio(request):
    if request.session.get("cod_usuario"):
        return render(request,"index.html",{"nombre_completo": request.session.get("nombredelusuario"),"tipo_usuario": request.session.get("tipo_usuario")})
    else:
        return redirect('login')


def salir(request):

    request.session.flush()
    return redirect("./")



class listaproductos(ListView):
    model=producto
    template_name='pagina/cargar_compra'

    def get_queryset(self):
        return self.model.objects.filter(cod_usuario=True)

    def get(self , request, *args, **Kwargs):
        if request.is_ajax():
            lista_productos=[]

            for producto in self.get_queryset():
                data_producto = {}
                data_producto['id']=producto.codigo_producto
                data_producto['nombre']=producto.nombre_productos
                data_producto['precio']=producto.precioventa_productos
                data_producto['categoria']=producto.categoria_productos
                data_producto['cantidad']=producto.cantidad_productos
                lista_productos.append(data_producto)
            data=json.dumps(lista_productos)
             
            return HttpResponse(data, 'aplication/json')
        else:
            return render (request, self.template_name)

def cargar_compra(request):

    if request.session.get("cod_usuario"):
        listaproveedor=proveedor.objects.all()
        listacategoria = categoria.objects.all()
        listatabla=producto.objects.all()
        return validar(request, "cargar_compra.html", {"nombre_completo":request.session.get("nombredelusuario"),"listatabla":listatabla, "listacategoria":listacategoria, "listaproveedor":listaproveedor})
    else:
            return redirect('login')





def editproducto(request, producto_actual=0):
    listacategoria = categoria.objects.all()
    listaproveedor=proveedor.objects.all()
    if request.session.get("cod_usuario"):
        if request.method=="GET":
            product_actual=producto.objects.filter(codigo_productos=producto_actual).exists()
            if product_actual:
                datos_producto=producto.objects.filter(codigo_productos=producto_actual).first()
                return validar(request, 'editproducto.html',
                {"datos_act":datos_producto, "producto_actual":producto_actual, "titulo":"Editar Usuario", "listacategoria":listacategoria, "listaproveedor":listaproveedor})
            else:
                return validar(request, "editproducto.html",
                {"nombre_completo":request.session.get("nombredelusuario"), "producto_actual":producto_actual, "titulo":"Cargar Usuario", "listacategoria":listacategoria ,"listaproveedor":listaproveedor})

        if request.method=="POST":
            if producto_actual==0:
                producto_nuevo=producto(codigo_productos=request.POST.get('codigo_productos'),
                preciocompra_productos=request.POST.get('preciocompra_productos'),
                precioventa_productos=request.POST.get('precioventa_productos'),
                cantidad_productos=request.POST.get('cantidad_productos'),
                categoria_productos=request.POST.get('categoria_productos'),
                nombre_productos=request.POST.get("nombre_productos"),
                nombre_proveedor_id=request.POST.get("proveedor"))
                
                producto_nuevo.save()
            else:
                datos_usuario=producto.objects.filter(codigo_productos=producto_actual).first()
                producto_nuevo=producto_audi(nombre_productos = datos_usuario.nombre_productos,
                preciocompra_productos=datos_usuario.preciocompra_productos,
                precioventa_productos=datos_usuario.precioventa_productos,
                cantidad_productos=datos_usuario.cantidad_productos,
                codigo_productos=datos_usuario.codigo_productos,
                categoria_productos=datos_usuario.categoria_productos,
                nombre_proveedor_id=datos_usuario.nombre_proveedor_id,
                cod_usuario=request.session.get("cod_usuario"),
                nombre_usuario=request.session.get("nombredelusuario"))

                producto_nuevo.save()
                producto_actual=producto.objects.get(codigo_productos=producto_actual)
                producto_actual.nombre_productos=request.POST.get("nombre_productos")
                producto_actual.codigo_productos=request.POST.get("codigo_productos")
                producto_actual.preciocompra_productos=request.POST.get("preciocompra_productos")
                producto_actual.cantidad_productos=request.POST.get("cantidad_productos")
                producto_actual.precioventa_productos=request.POST.get("precioventa_productos")
                producto_actual.categoria_productos=request.POST.get("categoria_productos")
                producto_actual.nombre_proveedor_id=request.POST.get("proveedor")
                producto_actual.save()

            return redirect("../cargar_compra")
    else:
         return redirect('login')

def editclientes(request, cliente_actual=0):
    listaclientes=cliente.objects.all()
    if request.session.get("cod_usuario"):
        if request.method=="GET":
            clie_actual=cliente.objects.filter(codigo_cliente=cliente_actual).exists()
            if clie_actual:
                datos_cliente=cliente.objects.filter(codigo_cliente=cliente_actual).first()
                return validar(request, 'cargar_cliente.html', {"nombre_completo": request.session.get("nombredelusuario"),"tipo_usuario": request.session.get("tipo_usuario"),"datos_act":datos_cliente, "cliente_actual":cliente_actual, "titulo":"Editar Usuario" , "listaclientes":listaclientes})
            else:
                return validar(request, "cargar_cliente.html", {"nombre_completo": request.session.get("nombredelusuario"),"tipo_usuario": request.session.get("tipo_usuario"), "cliente_actual":cliente_actual, "titulo":"Cargar Usuario" , "listaclientes":listaclientes})

        if request.method=="POST":
            if cliente_actual==0:
                cliente_nuevo=cliente(codigo_cliente=request.POST.get('codigo_cliente'),
                nombre_cliente=request.POST.get('nombre_cliente'),
                telefono_cliente=request.POST.get('telefonos_cliente'),
                direccion_cliente=request.POST.get("direccion_cliente"))

                cliente_nuevo.save()
            else:
                datos_usuario=cliente.objects.filter(codigo_cliente=cliente_actual).first()
                cliente_nueva=cliente_audi(nombre_cliente = datos_usuario.nombre_cliente,
                codigo_cliente=datos_usuario.codigo_cliente,
                direccion_cliente=datos_usuario.direccion_cliente,
                cod_usuario=request.session.get("cod_usuario"),
                nombre_usuario=request.session.get("nombredelusuario"),
                telefono_cliente=datos_usuario.telefono_cliente)
                cliente_nueva.save()

                cliente_actual=cliente.objects.get(codigo_cliente=cliente_actual)
                cliente_actual.nombre_cliente=request.POST.get("nombre_cliente")
                cliente_actual.codigo_cliente=request.POST.get("codigo_cliente")
                cliente_actual.direccion_cliente=request.POST.get("direccion_cliente")
                cliente_actual.telefono_cliente=request.POST.get("telefonos_cliente")

                cliente_actual.save()

            
        return redirect("../editclientes/0")
    else:
        return redirect('login')

def reportescliente(request):
    if request.session.get("cod_usuario"):
        listatabla=venta.objects.all()
        listacliente=cliente.objects.all()
        listametodo=metodo_pago.objects.all()
        return validar(request, "reportes_cliente.html", {"nombre_completo":request.session.get("nombredelusuario"),"listatabla":listatabla,"listacliente":listacliente,"listametodo":listametodo})
    else:
         return redirect('login')    


def modusuarios(request, usuario_actual=0):
    if request.session.get("cod_usuario"):
        listatabla=Usuarios.objects.all()
        if request.method=="GET":
            usu_actual=Usuarios.objects.filter(cod_usuario = usuario_actual).exists()
            if usu_actual:
                datos_usuario=Usuarios.objects.filter(cod_usuario=usuario_actual).first()
                return render(request, 'verusuario.html',
                {"datos_act":datos_usuario, "usuario_actual":usuario_actual, "titulo":"Editar Usuario", "listatabla":listatabla})
            else:
                return render(request, "verusuario.html", {"nombre_completo":request.session.get("nombredelusuario"), "usuario_actual":usuario_actual, "titulo":"Modificar Usuario" ,"listatabla":listatabla})

        if request.method=="POST":
            if usuario_actual==0:
                usuario_nuevo=Usuarios(cod_usuario=request.POST.get('cod_usuario'),
                nombre_completo_usuario=request.POST.get('nombre_completo_usuario'),
                nombre_usuario=request.POST.get('nombre_usuario'),
                tipo_usuario=request.POST.get('tipo_usuario'),
                password_usuario=request.POST.get('password_usuario'))

                usuario_nuevo.save()
            else:
                usuario_actual=Usuarios.objects.get(cod_usuario=usuario_actual)
                usuario_actual.nombre_completo_usuario=request.POST.get("nombre_completo_usuario")
                usuario_actual.nombre_usuario=request.POST.get("nombre_usuario")
                usuario_actual.password_usuario=request.POST.get("password_usuario")
                usuario_actual.tipo_usuario=request.POST.get("tipo_usuario")
                usuario_actual.save() 

            return redirect ("../modusuarios/0")
        else:
            return redirect('login')    

def borusuario (request, usuario_actual):
    Usuarios.objects.filter(cod_usuario = usuario_actual).delete()
    return redirect ("../modusuarios/0")
      
def editproveedor(request, proveedor_actual=0):
    listaproveedor=proveedor.objects.all()
    if request.session.get("cod_usuario"):
        if request.method=="GET":
            prov_actual=proveedor.objects.filter(codigo_proveedor=proveedor_actual).exists()
            if prov_actual:
                datos_proveedor=proveedor.objects.filter(codigo_proveedor=proveedor_actual).first()
                return render(request, 'cargar_proveedor.html',
                {"datos_act":datos_proveedor, "proveedor_actual":proveedor_actual, "titulo":"Editar Usuario","listaproveedor":listaproveedor})
            else:
                return render(request, "cargar_proveedor.html", {"nombre_completo":request.session.get("nombredelusuario"), "proveedor_actual":proveedor_actual, "titulo":"Cargar Usuario","listaproveedor":listaproveedor})

        if request.method=="POST":
            if proveedor_actual==0:
                proveedor_nuevo=proveedor(codigo_proveedor=request.POST.get('codigo_proveedor'),
                nombre_proveedor=request.POST.get('nombre_proveedor'),
                ruc_proveedor=request.POST.get('ruc_proveedor'),
                Telefono_proveedor=request.POST.get('Telefono_proveedor'),
                direccion_proveedor=request.POST.get("direccion_proveedor"))
                
                proveedor_nuevo.save()

            else:
                datos_usuario=proveedor.objects.filter(codigo_proveedor=proveedor_actual).first()
                proveedor_nuevo=proveedor_audi(nombre_proveedor = datos_usuario.nombre_proveedor,
                ruc_proveedor=datos_usuario.ruc_proveedor,
                Telefono_proveedor=datos_usuario.Telefono_proveedor,
                codigo_proveedor=datos_usuario.codigo_proveedor,
                direccion_proveedor=datos_usuario.direccion_proveedor,
                cod_usuario=request.session.get("cod_usuario"),
                nombre_usuario=request.session.get("nombredelusuario"))

                proveedor_nuevo.save()

                proveedor_actual=proveedor.objects.get(codigo_proveedor=proveedor_actual)
                proveedor_actual.nombre_proveedor=request.POST.get("nombre_proveedor")
                proveedor_actual.ruc_proveedor=request.POST.get("ruc_proveedor")
                proveedor_actual.Telefono_proveedor=request.POST.get("Telefono_proveedor")
                proveedor_actual.direccion_proveedor=request.POST.get("direccion_proveedor")
                proveedor_actual.save() 

            return redirect("../cargar_proveedor/0")
    else:
            return redirect('login')
def editcategoria(request, categoria_actual=0):
    if request.session.get("cod_usuario"):
        listacategoria=categoria.objects.all()
        if request.method=="GET":
            cat_actual=categoria.objects.filter(codigo_categoria=categoria_actual).exists()
            if cat_actual:
                datos_categoria=categoria.objects.filter(codigo_categoria=categoria_actual).first()
                return render(request, 'cargar_categoria.html',
                {"datos_act":datos_categoria, "categoria_actual":categoria_actual, "titulo":"Editar Usuario","listacategoria":listacategoria})
            else:
                return render(request, "cargar_categoria.html", {"nombre_completo":request.session.get("nombredelusuario"), "categoria_actual":categoria_actual, "titulo":"Cargar Usuario","listacategoria":listacategoria})
    else:
            return redirect('login')
    if request.method=="POST":
        if categoria_actual==0:
            categoria_nuevo=categoria(codigo_categoria=request.POST.get('codigo_categoria'),
            nombre_categoria=request.POST.get('nombre_categoria'))
            categoria_nuevo.save()

        else:
            categoria_actual=categoria.objects.get(codigo_categoria=categoria_actual)
            categoria_actual.nombre_categoria=request.POST.get("nombre_categoria")
            categoria_actual.save() 

        return redirect("../cargar_categoria/0")
    else:
            return redirect('login')

def punto_venta(request):
    if request.session.get("cod_usuario"):
        if request.method == "GET":
            listatabla=producto.objects.all()
            listacliente=cliente.objects.all()
            listametodo=metodo_pago.objects.all()
            return validar(request, "punto_venta.html", {"nombre_completo":request.session.get("nombredelusuario"),"listatabla":listatabla,"listacliente":listacliente,"listametodo":listametodo})

        elif request.method == "POST":
            print(request.POST.get('codigo_cliente'))
            factura_venta_nueva=venta(codigo_cliente_venta_id=request.POST.get('codigo_cliente'),
            fecha_venta = date.today(),
            total=request.POST.get('total_factura_venta'), 
            iva=request.POST.get('iva10_factura_venta'),
            metodo_de_pago_id=request.POST.get('metodo_pago'))
            factura_venta_nueva.save()

        error = 'No hay error!'
        response = JsonResponse({'error':error})
        response.status_code = 201
        return response

    else:
        return redirect("login")
            
def venta_detalle(request):
    if request.method == "POST":
        id_ultima_factura=venta.objects.all().last().codigo_venta

        factura_venta_deta=detalle_venta(venta_id=int(id_ultima_factura), 
        producto_detalle_id=request.POST.get('id_producto_id'),
        cantidad_detalle=request.POST.get('cant_producto'),
        subtotal=request.POST.get('subtotal_factura_venta'))
        factura_venta_deta.save()
    error = 'No hay error!'
    response = JsonResponse({'error':error})
    response.status_code = 201
    return response

def borrarproducto(request,producto_actual ):

    producto.objects.filter(codigo_productos= producto_actual).delete()

    return redirect("../buscar")

def borrarcliente(request,cliente_actual ):

    cliente.objects.filter(codigo_cliente= cliente_actual).delete()

    return redirect("../editclientes/0")


def borrarproveedor(request,proveedor_actual ):


    proveedor.objects.filter(codigo_proveedor= proveedor_actual).delete()

    return redirect("../cargar_proveedor/0")

def retirar_caja(request, caja_actual=0):
    if request.session.get("cod_usuario"):
        listacaja=caja.objects.all()
        listausuario=Usuarios.objects.all()
        if request.method=="GET":
            caj_actual=caja.objects.filter(codigo_caja=caja_actual).exists()
            if caj_actual:
                datos_caja=caja.objects.filter(codigo_caja=caja_actual).first()
                return render(request, 'retirar_caja.html', {"datos_act":datos_caja, "caja_actual":caja_actual, "titulo":"Editar Usuario","listacaja":listacaja,"listausuario":listausuario})
            else:
                return render(request, "retirar_caja.html", {"nombre_completo":request.session.get("nombredelusuario"), "caja_actual":caja_actual, "titulo":"Cargar Usuario","listacaja":listacaja,"listausuario":listausuario})

        if request.method=="POST":
            datos_usuario=Usuarios.objects.filter(nombre_usuario=request.POST.get('nombredelusuario')).first()
            
            if caja_actual==0:
                caja_nuevo=caja(codigo_caja=request.POST.get('codigo_caja'),
                nombre_usuario_id=getattr(datos_usuario, "cod_usuario"),
                tipo_mov=request.POST.get('tipo_mov'),
                motivo_caja=request.POST.get('motivo_caja'),
                fecha_caja=request.POST.get('fecha_caja'),
                hora_caja=request.POST.get('hora_caja'),
                entrada_caja=request.POST.get('entrada_caja'),
                salida_caja=request.POST.get('salida_caja'))
                caja_nuevo.save()

            return redirect("../movimiento_caja")
        else:
            return redirect('login')



def abrir_caja(request, caja_actual=0):
    if request.session.get("cod_usuario"):
        listacaja=caja.objects.all()
        listausuario=Usuarios.objects.all()
        if request.method=="GET":
            caj_actual=caja.objects.filter(codigo_caja=caja_actual).exists()
            if caj_actual:
                datos_caja=caja.objects.filter(codigo_caja=caja_actual).first()
                return render(request, 'abrir_caja.html',
                {"datos_act":datos_caja, "caja_actual":caja_actual, "titulo":"Editar Usuario","listacaja":listacaja,"listausuario":listausuario})
            else:
                return render(request, "abrir_caja.html", {"nombre_completo":request.session.get("nombredelusuario"), "caja_actual":caja_actual, "titulo":"Cargar Usuario","listacaja":listacaja,"listausuario":listausuario})

        if request.method=="POST":
            datos_usuario=Usuarios.objects.filter(nombre_usuario=request.POST.get('nombredelusuario')).first()
            
            if caja_actual==0:
                caja_nuevo=caja(codigo_caja=request.POST.get('codigo_caja'),
                tipo_mov=request.POST.get('tipo_mov'),
                nombre_usuario_id=getattr(datos_usuario, "cod_usuario"),
                motivo_caja=request.POST.get('motivo_caja'),
                fecha_caja=request.POST.get('fecha_caja'),
                hora_caja=request.POST.get('hora_caja'),
                entrada_caja=request.POST.get('entrada_caja'),
                salida_caja=request.POST.get('salida_caja'))
                caja_nuevo.save()

            return redirect("../movimiento_caja")
        else:
            return redirect('login')

def borrarcategoria(request, categoria_actual ):

    categoria.objects.filter(codigo_categoria= categoria_actual).delete()

    return redirect("../cargar_categoria/0")
     

def cerrar_caja(request, caja_actual=0):
    if request.session.get("cod_usuario"):
        listatabla=caja.objects.all()
        listaventa=venta.objects.all()
        listausuario=Usuarios.objects.all()
        if request.method=="GET":
            caj_actual=caja.objects.filter(codigo_caja=caja_actual).exists()
            if caj_actual:
                datos_caja=caja.objects.filter(codigo_caja=caja_actual).first()
                return validar(request, 'caja.html',
                {"datos_act":datos_caja, "caja_actual":caja_actual, "titulo":"Editar Usuario","listatabla":listatabla,"listausuario":listausuario,"listaventa":listaventa})
            else:
                return validar(request, "caja.html", {"nombre_completo":request.session.get("nombredelusuario"), "caja_actual":caja_actual, "titulo":"Cargar Usuario","listatabla":listatabla,"listausuario":listausuario, "listaventa":listaventa})

        if request.method=="POST":
            datos_usuario=Usuarios.objects.filter(nombre_usuario=request.POST.get('nombredelusuario')).first()
            
            if caja_actual==0:
                caja_nuevo=caja(codigo_caja=request.POST.get('codigo_caja'),
                nombre_usuario_id=getattr(datos_usuario, "cod_usuario"),
                tipo_mov=request.POST.get('tipo_mov'),
                motivo_caja=request.POST.get('motivo_caja'),
                fecha_caja=request.POST.get('fecha_caja'),
                hora_caja=request.POST.get('hora_caja'),
                entrada_caja=request.POST.get('entrada_caja'),
                total_caja=request.POST.get('total_caja'),
                salida_caja=request.POST.get('salida_caja'))
                caja_nuevo.save()

            return redirect("../movimiento_caja")   
    else:
            return redirect('login')
