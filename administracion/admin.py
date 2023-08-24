# ---------------- PANTUFLA 2.0 ------------------
# Sistema desarrollado por Kevin Turkienich 2023
# Contacto: kevin_turkienich@outlook.com
# Garacias por adquirir este producto!
# ----------------------------------------------

# ---------------- IMPORTACIONES DE MODULOS ----------------->

from django.contrib import admin
from .models import *
from .Funciones import Actualizar
from import_export.admin import ImportExportModelAdmin
import pytz
from .Reporte import generar_presupuesto

# ---------------- TITULO DEL SITIO ----------------->

admin.site.site_header = "Pantufla"
admin.site.site_title = "Pantufla"

# ---------------- ADMINISTRACION DE MODELOS  ----------------->

class IngredienteRecetaInline(admin.TabularInline):
    model = ingredientereceta
    autocomplete_fields = ('producto',)
    extra = 1
    fields = ('producto', 'cantidad')

class gastosAdicionalesInline(admin.TabularInline):
    model = adicionalreceta
    extra = 1
    fields = ('adicional', 'precio',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "adicional":
            kwargs["queryset"] = gastosAdicionales.objects.filter(USER=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)   
    
class CategoriaAdmin(admin.ModelAdmin):
    list_display=('DESCRIPCION',)
    exclude=('USER',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(USER=request.user.username)  # Filtra por el nombre de usuario activo

    def save_model(self, request, obj, form, change):
        if not obj.USER:
            obj.USER = request.user.username
        super().save_model(request, obj, form, change)

class ConfiguracionAdmin(ImportExportModelAdmin):
    list_display = ('estado','NOMBRE_EMPRESA','DIRECCION','TELEFONO','EMAIL','LOGO',)
    exclude=('USER',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(USER=request.user.username)  # Filtra por el nombre de usuario activo

    def save_model(self, request, obj, form, change):
        if not obj.USER:
            obj.USER = request.user.username
        super().save_model(request, obj, form, change)

class ProveedorAdmin(ImportExportModelAdmin):
    list_display = ('EMPRESA', 'NOMBRE','DIRECCION', 'EMAIL','TELEFONO',)
    ordering = ('NOMBRE',)
    search_fields = ('EMPRESA','NOMBRE',)
    list_filter = ('EMPRESA',)
    exclude=('USER',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(USER=request.user.username)  # Filtra por el nombre de usuario activo

    def save_model(self, request, obj, form, change):
        if not obj.USER:
            obj.USER = request.user.username
        super().save_model(request, obj, form, change)

class gastosAdicionalesAdmin(ImportExportModelAdmin):
    list_display=('PRODUCTO',)
    ordering = ('PRODUCTO',)
    search_fields = ('PRODUCTO',)
    exclude=('USER',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(USER=request.user.username)  # Filtra por el nombre de usuario activo

    def save_model(self, request, obj, form, change):
        if not obj.USER:
            obj.USER = request.user.username
        super().save_model(request, obj, form, change)


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in ["CATEGORIA", "PROVEEDOR"]:
            kwargs["queryset"] = db_field.related_model.objects.filter(USER=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
class InventarioAdmin(ImportExportModelAdmin):
    list_display = ('CATEGORIA','Producto','PROVEEDOR', 'COSTO_POR_UNIDAD','COSTO_TOTAL')
    ordering = ('PRODUCTO',)
    list_filter=('PROVEEDOR','CATEGORIA')
    exclude=('COSTO_UNITARIO','STOCK','UNIDAD_MEDIDA_USO','PRECIO_VENTA_UNITARIO','PRECIO_VENTA','USER')
    search_fields = ('CATEGORIA__DESCRIPCION', 'PRODUCTO', 'PROVEEDOR__EMPRESA',)

    list_per_page = 50
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

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(USER=request.user.username)  # Filtra por el nombre de usuario activo

    def save_model(self, request, obj, form, change):
        if not obj.USER:
            obj.USER = request.user.username
        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in ["CATEGORIA", "PROVEEDOR"]:
            kwargs["queryset"] = db_field.related_model.objects.filter(USER=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class RecetaAdmin(admin.ModelAdmin):

    inlines = [
        gastosAdicionalesInline,
        IngredienteRecetaInline,
    ]

    list_display = ('NOMBRE','Costo_por_porcion','Rentabilidad_porcion','Precio_porcion','Costo_total','Rentabilidad','Precio_de_venta',)
    ordering = ('NOMBRE',)
    exclude = ('ADICIONALES','GASTOS_ADICIONALES','ARTICULOS','STOCK', 'INGREDIENTES', 'ULTIMA_ACTUALIZACION', 'PRECIO_VENTA','PRECIO_VENTA_PORCION', 'COSTO_FINAL','USER')
    list_per_page = 50
    search_fields=('NOMBRE',)
    list_display_links = ('NOMBRE',)
    actions = [Actualizar, generar_presupuesto]

    def Receta(self, obj):  
        return obj.NOMBRE
        
    def Costo_por_porcion(self, obj):  

        calculo = obj.COSTO_FINAL / obj.PORCIONES 

        return "💲{:,.2f}".format(calculo)

    def Rentabilidad(self, obj):
        formateo = "% {:,.2f}".format(obj.RENTABILIDAD)
        return formateo
    
    def Rentabilidad_porcion(self, obj):
        formateo = "% {:,.2f}".format(obj.RENTABILIDAD_POR_PORCION)
        return formateo

    def Gastos_adicionales(self, obj):  
        formateo = "💲{:,.2f}".format(obj.GASTOS_ADICIONALES)
        return formateo

    def Precio_porcion(self, obj):
        calculo = obj.PRECIO_VENTA_PORCION
        return "💲{:,.2f}".format(calculo)
    
    def Precio_de_venta(self, obj):
        formateo = "💲{:,.2f}".format(obj.PRECIO_VENTA)
        return formateo
    
    def Costo_total(self, obj):
        formateo = "💲{:,.2f}".format(obj.COSTO_FINAL)
        return formateo

    def Ultima_Actualizacion(self, obj): 
        hora_buenos_aires = pytz.timezone('America/Argentina/Buenos_aires')
        fecha_hora = obj.ULTIMA_ACTUALIZACION.astimezone(hora_buenos_aires)
        formateo = fecha_hora.strftime("%H:%M %d/%m/%Y")

        formateo = "📆 " +formateo
        return formateo
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(USER=request.user.username)  # Filtra por el nombre de usuario activo

    def save_model(self, request, obj, form, change):
        if not obj.USER:
            obj.USER = request.user.username
        super().save_model(request, obj, form, change)

# ---------------- REGISTRACION DE MODULOS ----------------->

admin.site.register(Receta, RecetaAdmin)
admin.site.register(Proveedor, ProveedorAdmin)
admin.site.register(Configuracion, ConfiguracionAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Insumo, InventarioAdmin)
admin.site.register(gastosAdicionales,gastosAdicionalesAdmin)