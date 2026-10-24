from django.contrib import admin

from .models import Estacionamiento, Sensor


@admin.register(Estacionamiento)
class EstacionamientoAdmin(admin.ModelAdmin):
    list_display = ("numero_cajon", "estado")
    list_filter = ("estado",)
    search_fields = ("numero_cajon",)


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = (
        "id_sensor",
        "estacionamiento",
        "tipo_sensor",
        "estado",
        "estado_ocupacion",
    )
    list_filter = ("tipo_sensor", "estado", "estado_ocupacion")
    search_fields = ("tipo_sensor", "estacionamiento__numero_cajon")
