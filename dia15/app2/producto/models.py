from django.db import models

class Producto(models.Model):
    IVA_OPCIONES = [
        ('EXENTO', 'Exento'),
        ('5', '5%'),
        ('10', '10%'),
    ]
    UNID_OPCIONES = [('UNID', 'Unidades'), ('kg', 'kilogramos') ]
    codigo_barra   = models.CharField(max_length=20, unique=True)
    descripcion    = models.CharField(max_length=200)

    precio_costo   = models.IntegerField(default=0)
    precio_venta   = models.IntegerField(default=0)
    iva            = models.CharField(max_length=10, choices=IVA_OPCIONES)

    stock          = models.IntegerField(default=0)
    unidad_medida  = models.CharField(max_length=10, choices=UNID_OPCIONES)

    def __str__(self):
        return str(self.descripcion)