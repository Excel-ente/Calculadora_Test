# ---------------- PANTUFLA 2.0 ------------------
# Sistema desarrollado por Kevin Turkienich 2023
# Contacto: kevin_turkienich@outlook.com
# Garacias por adquirir este producto!
# ----------------------------------------------

# ---------------- IMPORTACIONES DE MODULOS ----------------->
from django.db import models
from django.core.exceptions import ValidationError

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
    estado=models.BooleanField(verbose_name="ACTIVO",default=False)
    NOMBRE_EMPRESA= models.CharField(max_length=120,null=True,blank=True)
    DIRECCION=models.CharField(max_length=255,null=True,blank=True)
    TELEFONO =models.CharField(max_length=255,null=True,blank=True)          
    EMAIL=models.CharField(max_length=255,null=True,blank=True)
    LOGO= models.ImageField(upload_to='logos/',null=True,blank=True)
    USER = models.CharField(max_length=120,null=True,blank=True)
    
    class Meta:
        verbose_name = 'Mis Datos'
        verbose_name_plural = 'Mis Datos'

# ------------------------------------------------------------------
# ------------------------------------------------------------------
class Categoria(models.Model):
    DESCRIPCION= models.CharField(max_length=120,null=False,blank=False)
    USER = models.CharField(max_length=120,null=True,blank=True)
            
    def __str__(self):
        return self.DESCRIPCION
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural ='Categorias' 
# ------------------------------------------------------------------
# ------------------------------------------------------------------
class Proveedor(models.Model):
    EMPRESA=models.CharField(max_length=120,null=False,blank=False) 
    NOMBRE=models.CharField(max_length=120,null=False,blank=False) 
    DIRECCION=models.CharField(max_length=120,null=True,blank=True)
    EMAIL=models.EmailField(null=True,blank=True)
    TELEFONO=models.CharField(max_length=120,null=False,blank=False)
    USER = models.CharField(max_length=120,null=True,blank=True)

    def __str__(self):
        return self.EMPRESA
    
    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural ='Proveedores' 
# ------------------------------------------------------------------
# ------------------------------------------------------------------
class Insumo(models.Model):
    CATEGORIA = models.ForeignKey(Categoria,on_delete=models.CASCADE,blank=True,null=True)
    PRODUCTO = models.CharField(max_length=120, null=False, blank=False)
    PROVEEDOR=models.ForeignKey(Proveedor,on_delete=models.CASCADE,blank=True,null=True)
    DETALLE = models.TextField(null=True, blank=True)
    STOCK = models.IntegerField(default=0,null=True,blank=True)
    CANTIDAD = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=False, null=False)
    UNIDAD_MEDIDA_COMPRA = models.CharField(max_length=10, choices=UnidadDeMedida, default="Unidades", null=False, blank=False)
    PRECIO_COMPRA = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=False, null=False)
    UNIDAD_MEDIDA_USO = models.CharField(max_length=10, choices=UnidadDeMedidaSalida, default="Unidades", null=False, blank=False)
    COSTO_UNITARIO = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=False, null=False)
    PRECIO_VENTA_UNITARIO = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=False, null=False)
    USER = models.CharField(max_length=120,null=True,blank=True)

    class Meta:
        verbose_name = 'Insumo'
        verbose_name_plural ='Insumos' 

    def __str__(self):
        return f'{self.PRODUCTO} | ${self.COSTO_UNITARIO} x {self.UNIDAD_MEDIDA_USO}'

    def calculate_cost(self):
        if self.PRECIO_COMPRA > 0:
            conversions = {
                "Unidades": 1,
                "Kilogramos": 1000,
                "Litros": 1000,
                "Libras": 16,
                "Onzas": 1,
            }
            conversion_factor = conversions.get(self.UNIDAD_MEDIDA_COMPRA, 1)
            self.COSTO_UNITARIO = self.PRECIO_COMPRA / self.CANTIDAD / conversion_factor

    def convert_units(self):
        conversions = {
            "Kilogramos": "Gramos",
            "Litros": "Mililitros",
            "Libras": "Libras",
            "Onzas": "Onzas",
        }
        self.UNIDAD_MEDIDA_USO = conversions.get(self.UNIDAD_MEDIDA_COMPRA, self.UNIDAD_MEDIDA_USO)

    def save(self, *args, **kwargs):
        self.calculate_cost()
        self.convert_units()
        super(Insumo, self).save(*args, **kwargs)
# ------------------------------------------------------------------
# ------------------------------------------------------------------
class gastosAdicionales(models.Model):
    PRODUCTO  = models.CharField(max_length=255,blank=False,null=False)
    USER = models.CharField(max_length=120,null=True,blank=True)

    def __str__(self):
        return self.PRODUCTO
# ------------------------------------------------------------------
# ------------------------------------------------------------------  
class Receta(models.Model):
    CODIGO=models.AutoField(primary_key=True)
    NOMBRE=models.CharField(verbose_name='PRODUCTO',max_length=120,null=False,blank=False) 
    PORCIONES=models.DecimalField(max_digits=6,decimal_places=2,default=1,blank=False,null=False)
    DETALLE=models.TextField(null=True,blank=True) 
    RENTABILIDAD = models.DecimalField(max_digits=12,decimal_places=2,default=0,blank=True,null=True)
    RENTABILIDAD_POR_PORCION = models.DecimalField(max_digits=12,decimal_places=2,default=0,blank=True,null=True)
    PRECIO_VENTA = models.DecimalField(max_digits=22,decimal_places=2,default=1,blank=False,null=False)
    PRECIO_VENTA_PORCION = models.DecimalField(max_digits=22,decimal_places=2,default=1,blank=False,null=False)
    ADICIONALES = models.ManyToManyField(gastosAdicionales, blank=True)
    INGREDIENTES = models.ManyToManyField(Insumo)
    COSTO_FINAL = models.DecimalField(max_digits=22,decimal_places=2,default=0,blank=True,null=True)

    ARTICULOS = models.TextField(blank=True,null=True)
    GASTOS_ADICIONALES = models.DecimalField(verbose_name="TOTAL ADICIONALES",max_digits=22,decimal_places=2,default=0,blank=True,null=True)
    
    USER = models.CharField(max_length=120,null=True,blank=True)

    def __str__(self):
        return f'{self.NOMBRE} - $ {self.PRECIO_VENTA}'
    
    def clean(self):
        if self.RENTABILIDAD < 0:
            raise ValidationError("La rentabilidad debe ser mayor o igual a 0 %")
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
        costo_final_porcion = (float(total_gastos_adicionales) + float(costo_receta)) / float(self.PORCIONES)

        self.COSTO_FINAL = costo_final

        if self.RENTABILIDAD > 0 and self.RENTABILIDAD <1000000:
            rentabilidad = float(self.RENTABILIDAD)
            self.PRECIO_VENTA = (costo_final) + ((costo_final) * (rentabilidad / 100))
        else:
            self.PRECIO_VENTA = (costo_final)
        

        if self.RENTABILIDAD_POR_PORCION > 0 and self.RENTABILIDAD_POR_PORCION <1000000:
            rentabilidad = float(self.RENTABILIDAD_POR_PORCION)
            self.PRECIO_VENTA_PORCION = (costo_final_porcion) + ((costo_final_porcion) * (rentabilidad / 100))

        else:
            self.PRECIO_VENTA_PORCION = (costo_final_porcion)
        

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
        
