from django.urls import path
from pagina import views
urlpatterns = [path('', views.login ,name='login'), 
path('index.html', views.inicio ,name='inicio'),
path('salir', views.salir ,name='salir'),
path('editproducto/<int:producto_actual>',views.editproducto, name='editproducto'),
path('editclientes/<int:cliente_actual>', views.editclientes ,name='editclientes'),
path('reportes_cliente', views.reportescliente ,name='reportes_cliente'),
path('borrarproducto/<int:producto_actual>', views.borrarproducto , name='borrarproducto'),
path('borrarcliente/<int:cliente_actual>', views.borrarcliente , name='borrarcliente'),
path('borrarproveedor/<int:proveedor_actual>', views.borrarproveedor , name='borrarproveedor'),
path('borrarcategoria/<int:categoria_actual>', views.borrarcategoria , name='borrarcategoria'),
path('cargar_proveedor/<int:proveedor_actual>', views.editproveedor , name='cargar_proveedor'),
path('modusuarios/<int:usuario_actual>',views.modusuarios, name='modusuarios'),
path('borusuario/<int:usuario_actual>',views.borusuario, name='borusuario'),
path('cargar_compra', views.cargar_compra ,name='cargar_compra'),
path('movimiento_caja', views.cerrar_caja ,name='movimiento_caja'),
path('abrir_caja/<int:caja_actual>', views.abrir_caja ,name='abrir_caja'),
path('cerrar_caja/<int:caja_actual>', views.cerrar_caja ,name='cerrar_caja'),
path('cargar_categoria/<int:categoria_actual>', views.editcategoria ,name='cargar_categoria'),
path('retirar_caja/<int:caja_actual>', views.retirar_caja ,name='retirar_caja'),
path('punto_venta', views.punto_venta ,name='punto_venta')

]
