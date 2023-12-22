from rest_framework import serializers, response, status, views
from producto.models import Producto
import datetime as dt


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'


class ProductoResponseSerializer(serializers.Serializer):
    producto = serializers.IntegerField()
    plazo = serializers.IntegerField()
    fechaInicio = serializers.DateTimeField()
    fechaFin = serializers.DateTimeField()
    plazoReal = serializers.IntegerField()
