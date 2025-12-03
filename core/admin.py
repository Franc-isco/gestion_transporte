from django.contrib import admin
from .models import Terminal, Ruta, Bus, Conductor, ViajeProgramado


@admin.register(Terminal)
class TerminalAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "ciudad", "activo")
    list_filter = ("ciudad", "activo")
    search_fields = ("nombre", "ciudad")


@admin.register(Ruta)
class RutaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "codigo",
        "terminal_origen",
        "terminal_destino",
        "distancia_km",
        "duracion_estimada_min",
        "activo",
    )
    list_filter = ("terminal_origen", "terminal_destino", "activo")
    search_fields = ("codigo", "terminal_origen__nombre", "terminal_destino__nombre")


@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ("id", "patente", "marca", "modelo", "capacidad_asientos", "activo")
    list_filter = ("activo", "marca")
    search_fields = ("patente", "marca", "modelo")


@admin.register(Conductor)
class ConductorAdmin(admin.ModelAdmin):
    list_display = ("id", "rut", "nombre", "apellido", "telefono", "licencia_tipo", "activo")
    list_filter = ("activo", "licencia_tipo")
    search_fields = ("rut", "nombre", "apellido")


@admin.register(ViajeProgramado)
class ViajeProgramadoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "ruta",
        "bus",
        "conductor",
        "fecha_hora_salida",
        "fecha_hora_llegada_estimada",
        "duracion_estimada_min",
        "estado",
    )
    list_filter = ("estado", "ruta", "bus", "conductor")
    search_fields = (
        "ruta__codigo",
        "bus__patente",
        "conductor__nombre",
        "conductor__apellido",
    )
