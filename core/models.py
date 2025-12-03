from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


class Terminal(models.Model):
    nombre = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.ciudad})"


class Ruta(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    terminal_origen = models.ForeignKey(
        "Terminal",
        related_name="rutas_origen",
        on_delete=models.PROTECT,
    )
    terminal_destino = models.ForeignKey(
        "Terminal",
        related_name="rutas_destino",
        on_delete=models.PROTECT,
    )
    distancia_km = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0.1)],
    )
    duracion_estimada_min = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    activo = models.BooleanField(default=True)

    def clean(self):
        # Validación lógica: origen y destino no pueden ser iguales
        if self.terminal_origen_id == self.terminal_destino_id:
            raise ValidationError("El terminal de origen y destino no pueden ser el mismo.")

    def __str__(self):
        return f"{self.codigo} - {self.terminal_origen} -> {self.terminal_destino}"


class Bus(models.Model):
    patente = models.CharField(max_length=10, unique=True)
    marca = models.CharField(max_length=50, blank=True)
    modelo = models.CharField(max_length=50, blank=True)
    capacidad_asientos = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    anio_fabricacion = models.PositiveIntegerField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.patente} ({self.marca} {self.modelo})"


class Conductor(models.Model):
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    licencia_tipo = models.CharField(max_length=5)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.rut}"


class ViajeProgramado(models.Model):
    ESTADO_CHOICES = [
        ("PROGRAMADO", "Programado"),
        ("EN_CURSO", "En curso"),
        ("COMPLETADO", "Completado"),
        ("CANCELADO", "Cancelado"),
    ]

    ruta = models.ForeignKey(
        Ruta,
        on_delete=models.PROTECT,
        related_name="viajes",
    )
    bus = models.ForeignKey(
        Bus,
        on_delete=models.PROTECT,
        related_name="viajes",
    )
    conductor = models.ForeignKey(
        Conductor,
        on_delete=models.PROTECT,
        related_name="viajes",
    )

    fecha_hora_salida = models.DateTimeField()
    fecha_hora_llegada_estimada = models.DateTimeField()

    duracion_estimada_min = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default="PROGRAMADO",
    )

    observaciones = models.TextField(blank=True)

    def clean(self):
        # Validación: la llegada debe ser después de la salida
        if (
            self.fecha_hora_salida
            and self.fecha_hora_llegada_estimada
            and self.fecha_hora_llegada_estimada <= self.fecha_hora_salida
        ):
            raise ValidationError(
                "La fecha/hora de llegada estimada debe ser posterior a la salida."
            )

        # Podríamos validar también que duracion_estimada_min
        # sea coherente con la diferencia entre salida y llegada,
        # pero eso lo podemos dejar como validación extra en el serializer.

    def __str__(self):
        return f"Viaje {self.id} - {self.ruta} - {self.fecha_hora_salida}"
