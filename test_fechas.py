import pandas as pd
from datetime import datetime, timedelta

fechaCreacion = '2023-12-23'
plazo = 10
hora_inicio = 8
hora_fin = 17

fecha_inicio = pd.to_datetime(fechaCreacion)

fechas_festivas = [
    '2023-12-24',
    '2023-12-25',
    '2023-12-31',
    '2024-01-01',
]
plazo_real = 1
conteo_dias = 1

fecha_actual = datetime.now()

hora_actual = int(fecha_actual.strftime("%H"))


def es_fecha_festiva(fecha):
    return fecha in fechas_festivas


def calcular_fecha_inicio(fecha):
    dias_a_adicionar = 0

    while fecha.weekday() in [5, 6] or es_fecha_festiva(fecha.strftime("%Y-%m-%d")):
        dias_a_adicionar += 1
        fecha += pd.DateOffset(days=1)

    return dias_a_adicionar


def calcular_fecha_fin(fecha, plazo):
    conteo_dias_1 = 1
    dias_a_adicionar = 0
    while (conteo_dias_1 < plazo):
        if not (fecha.weekday() in [5, 6] or es_fecha_festiva(fecha.strftime("%Y-%m-%d"))):
            conteo_dias_1 += 1
        fecha += pd.DateOffset(days=1)
        dias_a_adicionar += 1
    return dias_a_adicionar


def ajustar_dia_por_horario(hora_inicio, hora_fin, fecha):
    dias_a_adicionar = 0
    if hora_actual >= hora_fin:
        dias_a_adicionar += 1
        return dias_a_adicionar
    return dias_a_adicionar


dias_adicional_por_horario = ajustar_dia_por_horario(hora_inicio, hora_fin, fecha_inicio)
plazo_real += dias_adicional_por_horario
fecha_inicio += pd.DateOffset(days=dias_adicional_por_horario)

dias_adicionales_fecha_inicio = calcular_fecha_inicio(fecha_inicio)
plazo_real += dias_adicionales_fecha_inicio
fecha_inicio += pd.DateOffset(days=dias_adicionales_fecha_inicio)

dias_adicionales_fecha_fin = calcular_fecha_fin(fecha_inicio, plazo)
plazo_real += dias_adicionales_fecha_fin

fecha_final = fecha_inicio + pd.DateOffset(days=dias_adicionales_fecha_fin)

print("Fecha inicio: ", fecha_inicio)
print("Fecha fin: ", fecha_final)
print("Plazo real: ", plazo_real)
print("Plazo: ", plazo)
