from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

from .models import Terminal, Ruta, Bus, Conductor, ViajeProgramado


class RutaModelTest(TestCase):
    def setUp(self):
        self.terminal1 = Terminal.objects.create(nombre="Terminal A", ciudad="Ciudad X")
        self.terminal2 = Terminal.objects.create(nombre="Terminal B", ciudad="Ciudad Y")

    def test_origen_y_destino_no_pueden_ser_iguales(self):
        ruta = Ruta(
            codigo="R-001",
            terminal_origen=self.terminal1,
            terminal_destino=self.terminal1,
            distancia_km=100,
            duracion_estimada_min=60,
        )
        with self.assertRaises(ValidationError):
            ruta.clean()


class ViajeProgramadoModelTest(TestCase):
    def setUp(self):
        t1 = Terminal.objects.create(nombre="Terminal A", ciudad="Ciudad X")
        t2 = Terminal.objects.create(nombre="Terminal B", ciudad="Ciudad Y")

        self.ruta = Ruta.objects.create(
            codigo="R-001",
            terminal_origen=t1,
            terminal_destino=t2,
            distancia_km=100,
            duracion_estimada_min=60,
        )
        self.bus = Bus.objects.create(
            patente="AAA111",
            capacidad_asientos=40,
        )
        self.conductor = Conductor.objects.create(
            rut="11111111-1",
            nombre="Juan",
            apellido="Pérez",
            telefono="123456789",
            licencia_tipo="A1",
        )

    def test_llegada_debe_ser_posterior_a_salida(self):
        salida = timezone.now()
        llegada = salida - timedelta(minutes=30)

        viaje = ViajeProgramado(
            ruta=self.ruta,
            bus=self.bus,
            conductor=self.conductor,
            fecha_hora_salida=salida,
            fecha_hora_llegada_estimada=llegada,
            duracion_estimada_min=60,
        )

        with self.assertRaises(ValidationError):
            viaje.clean()
