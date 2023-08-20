# ---------------- GALAXY 2.0 ------------------
# Sistema desarrollado por Kevin Turkienich 2023
# Contacto: kevin_turkienich@outlook.com
# Garacias por adquirir este producto!
# ----------------------------------------------

# ---------------- IMPORTACIONES DE MODULOS ----------------->
import datetime
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.core.exceptions import ValidationError

# ---------------- CALCULO DE FECHA DE PRESUPUESTO ----------------->
from datetime import date, timedelta

# Obtener la fecha en 7 dias
fecha_actual = date.today()
fecha_sabado = fecha_actual + timedelta(days=7)
# ------------------------------------------------------------------

# ---------------------- TABLAS DE DATOS --------------------------------------->
UnidadDeMedida = [
    ("Unidades","Unidades"),
    ("Kilogramos","Kilogramos"),
    ("Litros","Litros"),
    ("Onzas","Onzas"),
    ("Libras","Libras"),
]

Estado = [
    ("Pendiente","Pendiente"),
    ("Aceptado","Aceptado"),
    ("Entregado","Entregado"),
]

UnidadDeMedidaSalida = [
    ("Unidades","Unidades"),
    ("Gramos","Gramos"),
    ("Mililitros","Mililitros"),
    ("Onzas","Onzas"),
    ("Libras","Libras"),
]
# ------------------------------------------------------------------

# ---------------- MODELADO DE BASES DE DATOS --------------------------------->

class Configuracion(models.Model):
    estado=models.BooleanField(default=False)
    NOMBRE_EMPRESA= models.CharField(max_length=120,null=True,blank=True)
    DIRECCION=models.CharField(max_length=255,null=True,blank=True)
    TELEFONO =models.CharField(max_length=255,null=True,blank=True)          
    EMAIL=models.CharField(max_length=255,null=True,blank=True)
    LOGO= models.ImageField(upload_to='logos/',null=True,blank=True)

# ------------------------------------------------------------------
class Categoria(models.Model):
    DESCRIPCION= models.CharField(max_length=120,null=False,blank=False)
            
    def __str__(self):
        return self.DESCRIPCION
# ------------------------------------------------------------------
# ------------------------------------------------------------------
class Cliente(models.Model):
    NUMERO_CLIENTE= models.AutoField(primary_key=True)
    NOMBRE_Y_APELLIDO=models.CharField(max_length=120,null=False,blank=False)
    DIRECCION=models.CharField(max_length=255,null=False,blank=False)
    EMAIL=models.CharField(max_length=120,null=True,blank=True)
    TELEFONO =models.CharField(max_length=15,null=False,blank=False)
                   
    def __str__(self):
        return self.NOMBRE_Y_APELLIDO
# ------------------------------------------------------------------
# ------------------------------------------------------------------
class Proveedor(models.Model):
    EMPRESA=models.CharField(max_length=120,null=False,blank=False) 
    NOMBRE=models.CharField(max_length=120,null=False,blank=False) 
    DIRECCION=models.CharField(max_length=120,null=True,blank=True)
    EMAIL=models.EmailField(null=True,blank=True)
    TELEFONO=models.CharField(max_length=120,null=False,blank=False)

    def __str__(self):
        return self.EMPRESA
    
    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural ='Proveedores' 
# ------------------------------------------------------------------
# ------------------------------------------------------------------
class Insumo(models.Model):
    #CODIGO = models.CharField(max_length=120,unique=True, null=False, blank=False)
    CATEGORIA = models.ForeignKey(Categoria,on_delete=models.CASCADE,blank=True,null=True)
    PRODUCTO = models.CharField(max_length=120, null=False, blank=False,unique=True)
    PROVEEDOR=models.ForeignKey(Proveedor,on_delete=models.CASCADE,blank=True,null=True)
    DETALLE = models.TextField(null=True, blank=True)
    STOCK = models.IntegerField(default=0,null=True,blank=True)
    CANTIDAD = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=False, null=False)
    UNIDAD_MEDIDA_COMPRA = models.CharField(max_length=10, choices=UnidadDeMedida, default="Unidades", null=False, blank=False)
    PRECIO_COMPRA = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=False, null=False)
    UNIDAD_MEDIDA_USO = models.CharField(max_length=10, choices=UnidadDeMedidaSalida, default="Unidades", null=False, blank=False)
    COSTO_UNITARIO = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=False, null=False)
    PRECIO_VENTA_UNITARIO = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=False, null=False)

    class Meta:
        verbose_name = 'Material'
        verbose_name_plural ='Materiales' 

    def __str__(self):
        return f'{self.PRODUCTO} | ${self.COSTO_UNITARIO} x {self.UNIDAD_MEDIDA_USO}'


    def save(self, *args, **kwargs):

        if self.PRECIO_COMPRA > 0:
            if str(self.UNIDAD_MEDIDA_COMPRA) == str(self.UNIDAD_MEDIDA_USO):
                self.COSTO_UNITARIO = self.PRECIO_COMPRA / self.CANTIDAD
            elif str(self.UNIDAD_MEDIDA_COMPRA) == "Kilogramos" or str(self.UNIDAD_MEDIDA_COMPRA) == "Litros":
                self.COSTO_UNITARIO = self.PRECIO_COMPRA / self.CANTIDAD / 1000
            elif str(self.UNIDAD_MEDIDA_COMPRA) == "Libras":
                self.COSTO_UNITARIO = self.PRECIO_COMPRA / self.CANTIDAD / 16

        if self.UNIDAD_MEDIDA_COMPRA == "Unidades":
            self.UNIDAD_MEDIDA_USO = "Unidades"

        if self.UNIDAD_MEDIDA_COMPRA == "Kilogramos":
            self.UNIDAD_MEDIDA_USO = "Gramos"

        if self.UNIDAD_MEDIDA_COMPRA == "Litros":
            self.UNIDAD_MEDIDA_USO = "Mililitros"

        if self.UNIDAD_MEDIDA_COMPRA == "Libras":
            self.UNIDAD_MEDIDA_USO = "Libras"

        if self.UNIDAD_MEDIDA_COMPRA == "Onzas":
            self.UNIDAD_MEDIDA_USO = "Onzas"


        super(Insumo, self).save(*args, **kwargs)
# ------------------------------------------------------------------
# ------------------------------------------------------------------
class gastosAdicionales(models.Model):
    PRODUCTO  = models.CharField(max_length=255,blank=False,null=False,unique=True)

    def __str__(self):
        return self.PRODUCTO
# ------------------------------------------------------------------
# ------------------------------------------------------------------  
class Receta(models.Model):
    
    CODIGO=models.AutoField(primary_key=True)
    NOMBRE=models.CharField(verbose_name='PRODUCTO',max_length=120,null=False,blank=False) 
    DETALLE=models.TextField(null=True,blank=True) 
    RENTABILIDAD = models.DecimalField(max_digits=12,decimal_places=2,default=0,blank=True,null=True)
    PRECIO_VENTA = models.DecimalField(max_digits=22,decimal_places=2,default=1,blank=False,null=False)
    ADICIONALES = models.ManyToManyField(gastosAdicionales, blank=True)
    INGREDIENTES = models.ManyToManyField(Insumo)
    COSTO_FINAL = models.DecimalField(max_digits=22,decimal_places=2,default=0,blank=True,null=True)

    ARTICULOS = models.TextField(blank=True,null=True)
    GASTOS_ADICIONALES = models.DecimalField(verbose_name="TOTAL ADICIONALES",max_digits=22,decimal_places=2,default=0,blank=True,null=True)


    def __str__(self):
        return f'{self.NOMBRE} - $ {self.PRECIO_VENTA}'
    
    def clean(self):
        if self.RENTABILIDAD >= 0 and self.RENTABILIDAD < 10000:
            pass
        else:
            raise ValidationError("La rentabilidad debe ser mayor que 0 %")
        super().clean()

    class Meta:
        verbose_name = 'Receta'
        verbose_name_plural ='Recetas' 

    def save(self, *args, **kwargs):

        if not self.pk:
            super(Receta,self).save(*args, **kwargs)

        costo_receta = 0
        total_gastos_adicionales = 0
        self.COSTO_FINAL = 0

        #Capturar el costo de los insumos
        for ingrediente in self.ingredientereceta_set.all():
            costo_receta += ingrediente.cantidad * ingrediente.costo_unitario

        #Capturar el costo de los gastos adicionales
        for gasto in self.adicionalreceta_set.all():
            total_gastos_adicionales += gasto.precio

        self.GASTOS_ADICIONALES = float(total_gastos_adicionales)

        costo_final = float(total_gastos_adicionales) + float(costo_receta)

        self.COSTO_FINAL = costo_final

        if self.RENTABILIDAD > 0 and self.RENTABILIDAD <1000000:
            rentabilidad = float(self.RENTABILIDAD)
            self.PRECIO_VENTA = (costo_final) + ((costo_final) * (rentabilidad / 100))
        else:
            rentabilidad = float(0)
            self.PRECIO_VENTA = (costo_final)
        

        # Generar el texto de los artículos en el formato deseado
        insumos_receta = self.ingredientereceta_set.all()
        articulos = []
        for ingrediente in insumos_receta:
            nombre_producto = ingrediente.producto.PRODUCTO.split(' | $')[0]
            cantidad = ingrediente.cantidad
            u_medida = ingrediente.medida_uso
            precio_unitario = ingrediente.costo_unitario
            precio_total = cantidad * precio_unitario
            articulo = "{} | {} {} | $ {:.2f} | $ {:.2f}".format(nombre_producto, cantidad,u_medida, precio_unitario, precio_total)
            articulos.append(articulo)

        self.ARTICULOS = "\n\n".join(articulos)
        super().save(*args, **kwargs)
# ------------------------------------------------------------------
# ------------------------------------------------------------------ 
class ingredientereceta(models.Model):

    producto  = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=20, decimal_places=2, default=1, blank=False, null=False)
    costo_unitario = models.DecimalField(max_digits=20, decimal_places=2,blank=True,null=True)
    medida_uso = models.CharField(max_length=255,blank=True,null=True)
    subtotal = models.DecimalField(max_digits=20,decimal_places=2,default=0,blank=False,null=False)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural ='Productos incluidos en la receta' 

    def __str__(self):
        return f'{self.receta.NOMBRE} ({self.producto.UNIDAD_MEDIDA_USO})'
    
    def clean(self):
        if self.cantidad <= 0:
            raise ValidationError("Por favor ingrese una cantidad superior a 0.")
        super().clean()

    def save(self, *args, **kwargs):

        self.costo_unitario = self.producto.COSTO_UNITARIO
        self.medida_uso = self.producto.UNIDAD_MEDIDA_USO
        self.subtotal = self.costo_unitario * self.cantidad

        super().save(*args, **kwargs)
# ------------------------------------------------------------------
# ------------------------------------------------------------------ 
class adicionalreceta(models.Model):
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    adicional  = models.ForeignKey(gastosAdicionales, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=20, decimal_places=2,blank=False,null=False)

    def save(self, *args, **kwargs):


        super().save(*args, **kwargs)
        
# ------------------------------------------------------------------
# ------------------------------------------------------------------ 
class gastosFijos(models.Model):
    DETALLE  = models.CharField(max_length=255,blank=False,null=False)
    TOTAL = models.DecimalField(max_digits=20, decimal_places=2,blank=False,null=False)
    
    def clean(self):
        if self.TOTAL and self.TOTAL < 0:
            raise ValidationError("Por favor ingrese un monto superior a 0.")
        super().clean()


    def save(self, *args, **kwargs):

        if not self.pk:
            super().save(*args, **kwargs)

        super().save(*args, **kwargs)


    class Meta:
        verbose_name = 'Gasto mensual'
        verbose_name_plural ='Gastos mensuales' 
# ------------------------------------------------------------------
# ------------------------------------------------------------------ 
class PedidosEntregados(models.Model):
    CODIGO = models.CharField(max_length=10)
    CLIENTE = models.ForeignKey(Cliente, on_delete=models.CASCADE,blank=True,null=True)
    FECHA_ENTREGA = models.DateField(null=True, blank=True,default=datetime.date.today)
    ARTICULO=models.TextField() 
    DETALLE=models.CharField(max_length=120,null=True,blank=True) 
    #DIAS_DE_TRABAJO=models.DecimalField(max_digits=4,decimal_places=2,default=1,blank=False,null=False)
    COSTO_RECETA = models.DecimalField(verbose_name="Costo articulos",max_digits=22,decimal_places=2,default=0,blank=True,null=True)
    #MANO_DE_OBRA = models.DecimalField(max_digits=22,decimal_places=2,default=1,blank=False,null=False)
    PRECIO = models.DecimalField(max_digits=22,decimal_places=2,default=1,blank=False,null=False)
    INGREDIENTES = models.TextField(blank=True,null=True)
    GASTOS_ADICIONALES = models.DecimalField(verbose_name="TOTAL ADICIONALES",max_digits=22,decimal_places=2,default=0,blank=True,null=True)
# ------------------------------------------------------------------ 
# ------------------------------------------------------------------
class Pedido(models.Model):
    CODIGO=models.AutoField(primary_key=True)
    ESTADO= models.CharField(choices=Estado,max_length=20,default="Pendiente",blank=True,null=True)
    CLIENTE = models.ForeignKey(Cliente, on_delete=models.CASCADE,blank=True,null=True)
    FECHA_ENTREGA = models.DateField(null=True, blank=True)
    PRECIO_VENTA = models.DecimalField(max_digits=22,decimal_places=2,default=1,blank=True,null=True)
    ARTICULOS_INCLUIDOS = models.ManyToManyField(Receta)
    COSTO_FINAL = models.DecimalField(max_digits=22,decimal_places=2,default=0,blank=True,null=True)
    VALIDO_HASTA = models.DateField(blank=True, null=True, default=fecha_sabado)
    ULTIMA_ACTUALIZACION = models.DateTimeField(blank=True,null=True,auto_now=True)
    ARTICULOS = models.TextField(blank=True,null=True)
    GASTOS_ADICIONALES = models.DecimalField(verbose_name="TOTAL ADICIONALES",max_digits=22,decimal_places=2,default=0,blank=True,null=True)

    def __str__(self):
        return f'{self.CLIENTE} - $ {self.PRECIO_VENTA} - Entrega: {self.FECHA_ENTREGA}'
    
    def clean(self):
        if self.pk:
            if self.ESTADO == "Entregado" or self.ESTADO == "Aceptado":
                raise ValidationError("No se puede modificar un pedido Aceptado/Entregado")
        super().clean()

    class Meta:
        verbose_name = 'Presupuesto'
        verbose_name_plural ='Presupuestos' 

    def save(self, *args, **kwargs):

        if not self.pk:
            super(Pedido,self).save(*args, **kwargs)
        super().save(*args, **kwargs)
# ------------------------------------------------------------------
# ------------------------------------------------------------------ 
class productopedido(models.Model):

    producto  = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=20, decimal_places=2, default=1, blank=False, null=False)
    costo_unitario = models.DecimalField(max_digits=20, decimal_places=2,blank=True,null=True)
    medida_uso = models.CharField(max_length=255,blank=True,null=True)
    subtotal = models.DecimalField(max_digits=20,decimal_places=2,default=0,blank=False,null=False)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural ='Productos incluidos en la receta' 

    def __str__(self):
        return f'{self.receta.NOMBRE} ({self.producto.UNIDAD_MEDIDA_USO})'
    
    def clean(self):
        if self.cantidad <= 0:
            raise ValidationError("Por favor ingrese una cantidad superior a 0.")
        super().clean()

    def save(self, *args, **kwargs):

        self.costo_unitario = self.producto.COSTO_UNITARIO
        self.medida_uso = self.producto.UNIDAD_MEDIDA_USO
        self.subtotal = self.costo_unitario * self.cantidad

        super().save(*args, **kwargs)
# ------------------------------------------------------------------
# ------------------------------------------------------------------