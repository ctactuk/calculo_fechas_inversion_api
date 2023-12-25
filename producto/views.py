from rest_framework.decorators import api_view, schema, permission_classes
from rest_framework import response, status, permissions
from diasfestivos.models import DiasFestivos
from .models import Producto
from producto.api import ProductoSerializer, ProductoResponseSerializer
from calculo_fechas_inversion.logic.CalculadoraFechasInversiones import CalculadoraFechas
import pandas as pd
from datetime import datetime


@api_view(['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])
@permission_classes((permissions.IsAuthenticated,))
@schema(None)
def productos(request):
    productos = Producto.objects.all()
    productos_serializer = ProductoSerializer(productos, many=True)
    return response.Response(status=status.HTTP_200_OK, data=productos_serializer.data)


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
@schema(None)
def calcular_fechas_inversion(request):
    fecha_creacion = request.data['fechaCreacion']
    plazo = request.data['plazo']
    id_producto = request.data['producto']

    try:
        producto = Producto.objects.get(pk=id_producto)
    except Producto.DoesNotExist:
        return response.Response(status=status.HTTP_404_NOT_FOUND, message='Producto no encontrado')

    dias_festivos = [pd.to_datetime(dia.fecha).strftime(
        "%Y-%m-%d") for dia in __dias_festivos()]

    hora_fin = producto.horario.horaFin.strftime("%H:%M")

    calculo_fechas = CalculadoraFechas(datetime.strptime(
        fecha_creacion, "%Y-%m-%d"), plazo, hora_fin, dias_festivos)

    calculo = calculo_fechas.calcular_fechas()
    calculo['producto'] = producto.id

    producto_serializer = ProductoResponseSerializer(calculo)

    return response.Response(status=status.HTTP_200_OK, data=producto_serializer.data)


def __dias_festivos():
    dias_festivos = DiasFestivos.objects.filter()
    return dias_festivos.all()
