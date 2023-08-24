from administracion.models import Receta
from django.contrib import admin
from django.contrib import messages

@admin.action(description="Actualizar Recetas")
def Actualizar(modeladmin, request, queryset):
    for receta in queryset:  # Itera solo sobre las recetas seleccionadas

        costo_receta = 0

        for ingrediente in receta.ingredientereceta_set.all():
            ingrediente.costo_unitario = ingrediente.producto.COSTO_UNITARIO
            costo_receta += ingrediente.costo_unitario * ingrediente.cantidad
            ingrediente.save()      

        receta.COSTO_RECETA = 0
        receta.COSTO_FINAL = 0
        receta.COSTO_RECETA = costo_receta + 1
        receta.COSTO_FINAL = costo_receta + 1

        receta.save()
            
    messages.success(request, "Recetas seleccionadas actualizadas con éxito.")
