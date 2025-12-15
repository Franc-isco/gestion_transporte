from rest_framework import serializers
from .models import Terminal, Ruta, Bus, Conductor, ViajeProgramado
from django.utils import timezone


class TerminalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terminal
        fields = "__all__"


class RutaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ruta
        fields = "__all__"

    def validate(self, attrs):
        origen = attrs.get("terminal_origen") or getattr(self.instance, "terminal_origen", None)
        destino = attrs.get("terminal_destino") or getattr(self.instance, "terminal_destino", None)

        if origen and destino and origen == destino:
            raise serializers.ValidationError(
                {"terminal_destino": "El terminal de destino no puede ser igual al de origen."}
            )

        return attrs


class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = "__all__"


class ConductorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conductor
        fields = "__all__"


class ViajeProgramadoSerializer(serializers.ModelSerializer):
    ruta_codigo = serializers.ReadOnlyField(source="ruta.codigo")
    bus_patente = serializers.ReadOnlyField(source="bus.patente")
    conductor_nombre = serializers.ReadOnlyField(source="conductor.nombre")

    class Meta:
        model = ViajeProgramado
        fields = [
            "id",
            "ruta",
            "ruta_codigo",
            "bus",
            "bus_patente",
            "conductor",
            "conductor_nombre",
            "fecha_hora_salida",
            "fecha_hora_llegada_estimada",
            "duracion_estimada_min",
            "estado",
            "observaciones",
        ]

    def validate(self, attrs):
        """
        Validaciones extra:
        - llegada > salida
        - evitar solapamiento de viajes para un mismo bus o conductor
        """
        instance = self.instance

        ruta = attrs.get("ruta") or getattr(instance, "ruta", None)
        bus = attrs.get("bus") or getattr(instance, "bus", None)
        conductor = attrs.get("conductor") or getattr(instance, "conductor", None)
        salida = attrs.get("fecha_hora_salida") or getattr(instance, "fecha_hora_salida", None)
        llegada = attrs.get("fecha_hora_llegada_estimada") or getattr(
            instance, "fecha_hora_llegada_estimada", None
        )

        # 1) llegada > salida
        if salida and llegada and llegada <= salida:
            raise serializers.ValidationError(
                {"fecha_hora_llegada_estimada": "La llegada debe ser posterior a la salida."}
            )

        # Si faltan datos básicos, no seguimos validando 
        if not (bus and conductor and salida and llegada):
            return attrs

        # Rango de tiempo del viaje actual
        inicio = salida
        fin = llegada

        # 2) evitar solapamiento de viajes para el mismo bus
        qs_bus = ViajeProgramado.objects.filter(bus=bus)
        # Si es update, excluimos el propio registro
        if instance is not None:
            qs_bus = qs_bus.exclude(pk=instance.pk)

        qs_bus = qs_bus.filter(
            fecha_hora_salida__lt=fin,
            fecha_hora_llegada_estimada__gt=inicio,
        )

        if qs_bus.exists():
            raise serializers.ValidationError(
                {"bus": "El bus ya tiene un viaje programado que se solapa en este horario."}
            )

        # 3) evitar solapamiento de viajes para el mismo conductor
        qs_conductor = ViajeProgramado.objects.filter(conductor=conductor)
        if instance is not None:
            qs_conductor = qs_conductor.exclude(pk=instance.pk)

        qs_conductor = qs_conductor.filter(
            fecha_hora_salida__lt=fin,
            fecha_hora_llegada_estimada__gt=inicio,
        )

        if qs_conductor.exists():
            raise serializers.ValidationError(
                {
                    "conductor": "El conductor ya tiene un viaje programado que se solapa en este horario."
                }
            )

        return attrs
