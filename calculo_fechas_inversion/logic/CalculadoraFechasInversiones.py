from datetime import datetime
import pandas as pd


class CalculadoraFechas:
    def __init__(self, fecha_creacion, plazo, fechas_festivas):
        self.fecha_creacion = fecha_creacion
        self.plazo = plazo
        self.fechas_festivas = fechas_festivas
        self.plazo_real = 1
        self.hora_actual = int(datetime.now().strftime("%H"))

    def calcular_fechas(self, hora_fin):
        fecha_inicio = pd.to_datetime(self.fecha_creacion)

        if (datetime.now().strftime("%Y-%m-%d") == self.fecha_creacion):
            dia_adicional_por_horario = self.ajustar_dia_por_horario(
                hora_fin)
            self.plazo_real += dia_adicional_por_horario
            fecha_inicio += pd.DateOffset(days=dia_adicional_por_horario)

        dias_adicionales_fecha_inicio = self.calcular_fecha_inicio(
            fecha_inicio)
        self.plazo_real += dias_adicionales_fecha_inicio
        fecha_inicio += pd.DateOffset(days=dias_adicionales_fecha_inicio)

        dias_adicionales_fecha_fin = self.calcular_fecha_fin(
            fecha_inicio, self.plazo)
        self.plazo_real += dias_adicionales_fecha_fin

        fecha_final = fecha_inicio + \
            pd.DateOffset(days=dias_adicionales_fecha_fin)

        return {
            'producto': 0,
            'plazo': self.plazo,
            'fechaInicio': fecha_inicio,
            'fechaFin': fecha_final,
            'plazoReal': self.plazo_real
        }

    def _es_fecha_festiva(self, fecha):
        return fecha in self.fechas_festivas

    def calcular_fecha_inicio(self, fecha):
        dias_a_adicionar = 0

        while fecha.weekday() in [5, 6] or self._es_fecha_festiva(fecha.strftime("%Y-%m-%d")):
            dias_a_adicionar += 1
            fecha += pd.DateOffset(days=1)

        return dias_a_adicionar

    def calcular_fecha_fin(self, fecha, plazo):
        conteo_dias_1 = 1
        dias_a_adicionar = 0
        while (conteo_dias_1 < plazo):
            if not (fecha.weekday() in [5, 6] or self._es_fecha_festiva(fecha.strftime("%Y-%m-%d"))):
                conteo_dias_1 += 1
            fecha += pd.DateOffset(days=1)
            dias_a_adicionar += 1
        return dias_a_adicionar

    def ajustar_dia_por_horario(self, hora_fin):
        dias_a_adicionar = 0
        if self.hora_actual >= hora_fin:
            dias_a_adicionar += 1
            return dias_a_adicionar
        return dias_a_adicionar
