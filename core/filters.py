import django_filters
from .models import ViajeProgramado


class ViajeProgramadoFilter(django_filters.FilterSet):
    # ?origen=ID_TERMINAL
    origen = django_filters.NumberFilter(
        field_name="ruta__terminal_origen__id",
        lookup_expr="exact",
    )
    # ?destino=ID_TERMINAL
    destino = django_filters.NumberFilter(
        field_name="ruta__terminal_destino__id",
        lookup_expr="exact",
    )
    # ?fecha=YYYY-MM-DD  (filtra por fecha de salida)
    fecha = django_filters.DateFilter(
        field_name="fecha_hora_salida",
        lookup_expr="date",
    )

    class Meta:
        model = ViajeProgramado
        fields = ["origen", "destino", "fecha"]
