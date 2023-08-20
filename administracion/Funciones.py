from administracion.models import Receta
from django.contrib import admin
from django.contrib import messages
from .models import PedidosEntregados,gastosFijos
from django.db import models

'''
@admin.action(description="Actualizar Presupuestos")
def Actualizar(modeladmin, request, queryset):

    for receta in Receta.objects.all().filter(ESTADO="Pendiente"):
        
        if receta.ESTADO=="Pendiente":
            costo_receta = 0

            for ingrediente in receta.ingredientereceta_set.all():
                costo_receta += ingrediente.cantidad * ingrediente.costo_unitario

            receta.COSTO_RECETA = costo_receta 
            receta.COSTO_FINAL = costo_receta
            receta.save()
'''
'''
@admin.action(description="Actualizar Presupuestos")
def Actualizar(modeladmin, request, queryset):
    for receta in queryset:
        if receta.ESTADO == "Pendiente":
            costo_receta = 0

            for ingrediente in receta.ingredientereceta_set.all():
                costo_receta += ingrediente.cantidad * ingrediente.costo_unitario

            receta.COSTO_FINAL = costo_receta
            receta.save()
        else:
            messages.warning(request, f"No se puede actualizar el costo de la receta con código {receta.CODIGO} porque el estado no es pendiente.")

'''
@admin.action(description="Actualizar Recetas")
def Actualizar(modeladmin, request, queryset):

    for receta in Receta.objects.all():

        costo_receta = 0

        for ingrediente in receta.ingredientereceta_set.all():

            ingrediente.costo_unitario = ingrediente.producto.COSTO_UNITARIO
            costo_receta += ingrediente.costo_unitario * ingrediente.cantidad
            ingrediente.save()      

        receta.COSTO_RECETA=0
        receta.COSTO_FINAL=0
        receta.COSTO_RECETA = costo_receta + 1
        receta.COSTO_FINAL = costo_receta + 1

        receta.save()
            
    messages.success(request, "Recetas actualizadas con éxito.")






@admin.action(description="Aceptar Presupuesto")
def Aceptar(modeladmin, request, queryset):
    for receta in queryset:
        if receta.ESTADO == "Pendiente":
            receta.ESTADO = "Aceptado"
            receta.save()
        else:
            messages.warning(request, f"No se puede aceptar el pedido de la receta con código {receta.CODIGO} porque el estado no es pendiente.")

@admin.action(description="Entregar Pedido")
def Entregar(modeladmin, request, queryset):
    for receta in queryset:
        if receta.ESTADO == "Aceptado":
            receta.ESTADO = "Entregado"
            
            # Obtener una lista de los insumos de la receta
            insumos_receta = [(ingrediente.producto.PRODUCTO, ingrediente.cantidad) for ingrediente in receta.ingredientereceta_set.all()]  
            
            gastos_fijos = gastosFijos.objects.aggregate(models.Sum('TOTAL'))['TOTAL__sum'] or 0
            mano_de_obra = 0 #(receta.DIAS_DE_TRABAJO) * (gastos_fijos / 25)

            receta_entregada = PedidosEntregados(
                CODIGO=receta.CODIGO,
                CLIENTE=receta.CLIENTE,
                FECHA_ENTREGA=receta.FECHA_ENTREGA,
                ARTICULO=", ".join([f"{producto} ({cantidad})" for producto, cantidad in insumos_receta]),  # Convertir la lista en una cadena separada por comas
                DETALLE=receta.DETALLE,
                #DIAS_DE_TRABAJO=receta.DIAS_DE_TRABAJO,
                COSTO_RECETA=receta.COSTO_FINAL,
                GASTOS_ADICIONALES=receta.GASTOS_ADICIONALES,
                #MANO_DE_OBRA=receta.DIAS_DE_TRABAJO * mano_de_obra,
                PRECIO=receta.PRECIO_VENTA,
                INGREDIENTES=", ".join([f"{producto} ({cantidad})" for producto, cantidad in insumos_receta]), # Convertir la lista en una cadena separada por comas
            )
            receta_entregada.save()
            
            receta.save()
        else:
            messages.warning(request, f"No se puede entregar el pedido de la receta con código {receta.CODIGO} porque el estado no es aceptado.")
