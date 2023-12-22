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

    plazo_real = 1
    fecha_actual = datetime.now()

    hora_actual = int(fecha_actual.strftime("%H"))
    fecha_inicio = pd.to_datetime(fecha_creacion)

    dias_festivos = __dias_festivos(
        fecha_inicio, fecha_inicio + pd.DateOffset(days=plazo))

    dias_festivos = [pd.to_datetime(dia.fecha).strftime(
        "%Y-%m-%d") for dia in dias_festivos]

    hora_fin = int(producto.horario.horaFin.strftime("%H"))

    calculo_fechas = CalculadoraFechas(
        fecha_inicio, hora_actual, plazo, dias_festivos)

    if (datetime.now().strftime("%Y-%m-%d") == fecha_creacion):
        dia_adicional_por_horario = calculo_fechas.ajustar_dia_por_horario(
            hora_fin)
        plazo_real += dia_adicional_por_horario
        fecha_inicio += pd.DateOffset(days=dia_adicional_por_horario)

    dias_adicionales_fecha_inicio = calculo_fechas.calcular_fecha_inicio(
        fecha_inicio)
    plazo_real += dias_adicionales_fecha_inicio
    fecha_inicio += pd.DateOffset(days=dias_adicionales_fecha_inicio)

    dias_adicionales_fecha_fin = calculo_fechas.calcular_fecha_fin(
        fecha_inicio, plazo)
    plazo_real += dias_adicionales_fecha_fin

    fecha_final = fecha_inicio + pd.DateOffset(days=dias_adicionales_fecha_fin)

    response_product = {
        'producto': id_producto,
        'plazo': plazo,
        'fechaInicio': fecha_inicio,
        'fechaFin': fecha_final,
        'plazoReal': plazo_real
    }

    producto_serializer = ProductoResponseSerializer(response_product)

    return response.Response(status=status.HTTP_200_OK, data=producto_serializer.data)


def __dias_festivos(fecha_inicio, fecha_fin):
    dias_festivos = DiasFestivos.objects.filter(
        fecha__range=[fecha_inicio, fecha_fin])
    return dias_festivos.all()
