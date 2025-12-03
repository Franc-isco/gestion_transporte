from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login


from .models import Terminal, Ruta, Bus, Conductor, ViajeProgramado
from .serializers import (
    TerminalSerializer,
    RutaSerializer,
    BusSerializer,
    ConductorSerializer,
    ViajeProgramadoSerializer,
)
from .filters import ViajeProgramadoFilter


@login_required
def home(request):
    return render(request, "index.html")

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Opcional: iniciar sesión automáticamente
            auth_login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

class TerminalViewSet(viewsets.ModelViewSet):
    queryset = Terminal.objects.all()
    serializer_class = TerminalSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["nombre", "ciudad"]
    ordering_fields = ["nombre", "ciudad"]


class RutaViewSet(viewsets.ModelViewSet):
    queryset = Ruta.objects.all()
    serializer_class = RutaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["terminal_origen", "terminal_destino", "activo"]
    search_fields = ["codigo", "terminal_origen__nombre", "terminal_destino__nombre"]
    ordering_fields = ["codigo", "distancia_km", "duracion_estimada_min"]


class BusViewSet(viewsets.ModelViewSet):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["activo"]
    search_fields = ["patente", "marca", "modelo"]
    ordering_fields = ["patente", "capacidad_asientos", "anio_fabricacion"]


class ConductorViewSet(viewsets.ModelViewSet):
    queryset = Conductor.objects.all()
    serializer_class = ConductorSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["activo", "licencia_tipo"]
    search_fields = ["rut", "nombre", "apellido"]
    ordering_fields = ["nombre", "apellido", "rut"]


class ViajeProgramadoViewSet(viewsets.ModelViewSet):
    queryset = ViajeProgramado.objects.all()
    serializer_class = ViajeProgramadoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ViajeProgramadoFilter
    search_fields = [
        "ruta__codigo",
        "bus__patente",
        "conductor__nombre",
        "conductor__apellido",
    ]
    ordering_fields = [
        "fecha_hora_salida",
        "fecha_hora_llegada_estimada",
        "duracion_estimada_min",
    ]
