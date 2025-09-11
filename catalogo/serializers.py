from rest_framework import serializers
from .models import Libro

# Serializador: convierte el modelo Libro en JSON y valida datos recibidos
class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro  # modelo a serializar
        fields = ['id', 'titulo', 'autor', 'anio', 'isbn', 'creado']  # campos expuestos en la API
        read_only_fields = ['id', 'creado']  # estos campos no se pueden modificar por API

    # Validación personalizada para el campo año
    def validate_anio(self, value):
        if value < 1400 or value > 2100:
            raise serializers.ValidationError('Año fuera de rango razonable.')
        return value
