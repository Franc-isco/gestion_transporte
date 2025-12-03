from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    TerminalViewSet,
    RutaViewSet,
    BusViewSet,
    ConductorViewSet,
    ViajeProgramadoViewSet,
)

router = DefaultRouter()
router.register(r"terminales", TerminalViewSet, basename="terminal")
router.register(r"rutas", RutaViewSet, basename="ruta")
router.register(r"buses", BusViewSet, basename="bus")
router.register(r"conductores", ConductorViewSet, basename="conductor")
router.register(r"viajes", ViajeProgramadoViewSet, basename="viajeprogramado")

urlpatterns = [
    path("", include(router.urls)),
]
