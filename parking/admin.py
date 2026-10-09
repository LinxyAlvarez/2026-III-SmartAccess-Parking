from django.contrib import admin
from .models import (
    Usuario,
    Acreditacion,
    Vehiculo,
    Estacionamiento,
    Boleto,
    RegistroUso,
    CapturaPlaca,
    Pago,
)

admin.site.register(Usuario)
admin.site.register(Acreditacion)
admin.site.register(Vehiculo)
admin.site.register(Estacionamiento)
admin.site.register(Boleto)
admin.site.register(RegistroUso)
admin.site.register(CapturaPlaca)
admin.site.register(Pago)