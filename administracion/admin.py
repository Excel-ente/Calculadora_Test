from django import forms
from django.db import models
from django.contrib import admin
from .models import *
from .Funciones import Actualizar,Entregar,Aceptar
from import_export.admin import ImportExportModelAdmin
import pytz
from .AceptacionPresupuesto import generar_reporte
from .Reporte import generar_presupuesto


admin.site.site_header = "Calcul"
admin.site.site_title = "GALAXY 2.0"

class IngredienteRecetaInline(admin.TabularInline):
    model = ingredientereceta
    autocomplete_fields = ('producto',)
    extra = 1
    fields = ('producto', 'cantidad')

class gastosAdicionalesInline(admin.TabularInline):
    model = adicionalreceta
    extra = 1
    fields = ('adicional', 'precio',)

@admin.register(Categoria)
class CategoriaAdmin(ImportExportModelAdmin):
    list_display = ('id','DESCRIPCION',)

#@admin.register(PedidosEntregados)
##class PedidosEntregadosAdmin(ImportExportModelAdmin):
#    list_display = ('Pedido','CLIENTE','FECHA_ENTREGA','PRECIO_VENTA',)
 #   exclude=('COSTO_RECETA','MANO_DE_OBRA','ARTICULO',)
#    actions=[generar_reporte,]

#    def Pedido(self,obj):
#        return f"# {obj.CODIGO}"

#    def PRECIO_VENTA(self, obj):
#        return "💲{:,.2f}".format(obj.PRECIO)
    
#@admin.register(Cliente)
#class ClienteAdmin(ImportExportModelAdmin):
#    list_display = ('NOMBRE_Y_APELLIDO','DIRECCION','EMAIL','TELEFONO',)
#    search_fields = ('NOMBRE_Y_APELLIDO',)

@admin.register(Configuracion)
class ConfiguracionAdmin(ImportExportModelAdmin):
    list_display = ('NOMBRE_EMPRESA','DIRECCION','TELEFONO','EMAIL','LOGO',)

@admin.register(Proveedor)
class ProveedorAdmin(ImportExportModelAdmin):
    list_display = ('EMPRESA', 'NOMBRE','DIRECCION', 'EMAIL','TELEFONO',)
    ordering = ('NOMBRE',)
    search_fields = ('EMPRESA','NOMBRE',)
    list_filter = ('EMPRESA',)
    
#@admin.register(gastosFijos)
#class gastosFijosAdmin(ImportExportModelAdmin):
#    list_display = ('DETALLE', 'IMPORTE',)
#    ordering = ('DETALLE',)
#    search_fields = ('DETALLE',)


#    def IMPORTE(self, obj):
#        return "💲{:,.2f}".format(obj.TOTAL)

@admin.register(gastosAdicionales)
class gastosAdicionalesAdmin(ImportExportModelAdmin):
    list_display = ('PRODUCTO',)
    ordering = ('PRODUCTO',)
    search_fields = ('PRODUCTO',)

@admin.register(Insumo)
class InventarioAdmin(ImportExportModelAdmin):
    list_display = ('CATEGORIA','Producto','PROVEEDOR', 'COSTO_POR_UNIDAD','COSTO_TOTAL')
    ordering = ('PRODUCTO',)
    list_filter=('PROVEEDOR','CATEGORIA')
    exclude=('COSTO_UNITARIO','STOCK','UNIDAD_MEDIDA_USO','PRECIO_VENTA_UNITARIO','PRECIO_VENTA')
    search_fields = ('CATEGORIA__DESCRIPCION', 'PRODUCTO', 'PROVEEDOR__EMPRESA',)

    list_per_page = 25
    list_display_links = ('Producto',)


    def COSTO_TOTAL(self, obj):
        return "💲{:,.2f}".format(obj.PRECIO_COMPRA)
    
    def PRECIO_VENTA(self, obj):
        return "💲{:,.2f}".format(obj.PRECIO_VENTA_UNITARIO)
    
    def COSTO_POR_UNIDAD(self, obj):

        costo_unitario = obj.COSTO_UNITARIO
        unidad_medida = obj.UNIDAD_MEDIDA_USO
        costo_formateado = f'💲{costo_unitario:,.2f}'

        cadena = f'{costo_formateado} x {unidad_medida}'

        return cadena
        
    def Producto(self, obj):

        cadena = f'{obj.PRODUCTO} (x{obj.CANTIDAD} {obj.UNIDAD_MEDIDA_COMPRA})'
        
        return cadena

@admin.register(Receta)
class RecetaAdmin(admin.ModelAdmin):
    inlines = [
        gastosAdicionalesInline,
        IngredienteRecetaInline,
    ]

    list_display = ('NOMBRE','Costo_total','Rentabilidad','Precio_de_venta',)

    ordering = ('NOMBRE',)
    exclude = ('ADICIONALES','GASTOS_ADICIONALES','ARTICULOS','STOCK', 'INGREDIENTES', 'ULTIMA_ACTUALIZACION', 'PRECIO_VENTA', 'COSTO_FINAL',)
    list_per_page = 25
    search_fields=('NOMBRE',)
    list_display_links = ('NOMBRE',)
    actions = [Actualizar, generar_presupuesto]

    def Rentabilidad(self, obj):
        formateo = "% {:,.0f}".format(obj.RENTABILIDAD)
        return formateo

    def Gastos_adicionales(self, obj):  
        formateo = "💲{:,.0f}".format(obj.GASTOS_ADICIONALES)
        return formateo

    def Precio_de_venta(self, obj):
        formateo = "💲{:,.0f}".format(obj.PRECIO_VENTA)
        return formateo
    
    def Costo_total(self, obj):
        formateo = "💲{:,.0f}".format(obj.COSTO_FINAL)
        return formateo

    def Ultima_Actualizacion(self, obj): 
        hora_buenos_aires = pytz.timezone('America/Argentina/Buenos_aires')
        fecha_hora = obj.ULTIMA_ACTUALIZACION.astimezone(hora_buenos_aires)
        formateo = fecha_hora.strftime("%H:%M %d/%m/%Y")

        formateo = "📆 " +formateo
        return formateo
    


#@admin.register(Pedido)
#class PedidoAdmin(admin.ModelAdmin):
#    list_display = ('ESTADO','CLIENTE','VALIDO_HASTA','Precio_de_venta',)
#    exclude=('ESTADO','PRECIO_VENTA','COSTO_FINAL','ARTICULOS',)

#    def Precio_de_venta(self, obj):
#        formateo = "💲{:,.0f}".format(obj.PRECIO_VENTA)
#        return formateo
        
