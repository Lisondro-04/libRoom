# Uso básico de drf-spectacular

Es una herramienta que genera automáticamente documentación OpenAPI 3.0, permite obtener una vista interactiva (como Swagger UI o Redoc) para explorar los endpoints.

## docstring

Cadena de texto que se coloca justo debajo de la definición de una clase, función o método para explicar qué hace. En DRF y drf-spectacular, estas descripciones se usan para generar la documentación en la api.

## Ejemplo en ViewSet

from rest_framework.viewsets import ModelViewSet
from myapp.models import Personaje
from myapp.serializers import PersonajeSerializer

class PersonajeViewSet(ModelViewSet):
    """
    API para gestionar personajes.
    
    Permite crear, obtener, actualizar y eliminar personajes
    dentro de una obra literaria.
    """
    queryset = Personaje.objects.all()
    serializer_class = PersonajeSerializer'

## Ejemplo en Serializer

from rest_framework import serializers
from myapp.models import Personaje

class PersonajeSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Personaje.
    
    Contiene información como nombre, descripción y rol en la historia.
    """

    class Meta:
        model = Personaje
        fields = '__all__'




