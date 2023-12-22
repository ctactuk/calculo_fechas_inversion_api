import pandas as pd


class CalculadoraFechas:
    def __init__(self, fecha_creacion, hora_actual, plazo, fechas_festivas):
        self.fecha_creacion = fecha_creacion
        self.plazo = plazo
        self.fechas_festivas = fechas_festivas
        self.hora_actual = hora_actual

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
