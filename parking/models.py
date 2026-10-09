
# Create your models here.
from django.db import models


class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100, blank=True)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno}"


class Acreditacion(models.Model):
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name="acreditacion"
    )
    tipo = models.CharField(max_length=100)
    documento = models.CharField(max_length=255)
    fecha_validacion = models.DateField(null=True, blank=True)
    estado = models.BooleanField(default=False)

    def __str__(self):
        return f"Acreditación de {self.usuario}"


class Vehiculo(models.Model):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="vehiculos"
    )
    placa = models.CharField(max_length=20, unique=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    color = models.CharField(max_length=30)

    def __str__(self):
        return self.placa


class Estacionamiento(models.Model):
    numero = models.CharField(max_length=20, unique=True)
    ubicacion = models.CharField(max_length=100)
    accesible = models.BooleanField(default=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"Espacio {self.numero}"


class Boleto(models.Model):
    vehiculo = models.ForeignKey(
        Vehiculo,
        on_delete=models.CASCADE,
        related_name="boletos"
    )
    numero_boleto = models.CharField(max_length=50, unique=True)
    fecha_entrada = models.DateTimeField(auto_now_add=True)
    fecha_salida = models.DateTimeField(null=True, blank=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cargo_adicional = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    pagado = models.BooleanField(default=False)

    def __str__(self):
        return self.numero_boleto


class RegistroUso(models.Model):
    boleto = models.ForeignKey(
        Boleto,
        on_delete=models.CASCADE,
        related_name="registros_uso"
    )
    estacionamiento = models.ForeignKey(
        Estacionamiento,
        on_delete=models.CASCADE,
        related_name="registros_uso"
    )
    fecha_entrada = models.DateTimeField(auto_now_add=True)
    fecha_salida = models.DateTimeField(null=True, blank=True)
    autorizado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.boleto} - {self.estacionamiento}"


class CapturaPlaca(models.Model):
    registro_uso = models.ForeignKey(
        RegistroUso,
        on_delete=models.CASCADE,
        related_name="capturas_placa"
    )
    placa_detectada = models.CharField(max_length=20)
    fecha_captura = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(
        upload_to="capturas_placas/",
        blank=True,
        null=True
    )
    confianza = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.placa_detectada


class Pago(models.Model):
    boleto = models.OneToOneField(
        Boleto,
        on_delete=models.CASCADE,
        related_name="pago"
    )
    fecha_pago = models.DateTimeField(auto_now_add=True)
    monto_pagado = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    metodo_pago = models.CharField(max_length=50)

    def __str__(self):
        return f"Pago {self.boleto}"