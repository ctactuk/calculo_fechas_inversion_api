from datetime import datetime
import pandas as pd
from typing import List
from producto.models import Producto


class CalculadoraFechas:
    def __init__(self, fecha_creacion, plazo: int, fechas_festivas: List, en_reinversion: bool, producto: Producto):
        self.fecha_creacion = fecha_creacion
        self.plazo = plazo
        self.fechas_festivas = fechas_festivas
        self.plazo_real = 1
        self.fecha_final = None
        self.fecha_inicio = None
        self.en_reinversion = en_reinversion
        self.producto = producto

    def calcular_fechas(self):
        self.ajustar_plazo_real_por_horario()
        self.calcular_fecha_inicio()
        self.calcular_fecha_fin()
        self.plazo_real = (self.fecha_final - self.fecha_inicio).days + 1
        return {
            'producto': self.producto.id,
            'plazo': self.plazo,
            'fechaInicio': self.fecha_inicio,
            'fechaFin': self.fecha_final,
            'plazoReal': self.plazo_real
        }

    def calcular_fecha_inicio(self) -> None:
        while self.es_dia_no_laboral(self.fecha_inicio):
            self.fecha_inicio += pd.DateOffset(days=1)

    def calcular_fecha_fin(self) -> None:
        self.fecha_final = self.fecha_inicio + \
            pd.DateOffset(days=1) + pd.DateOffset(days=self.plazo)

        while self.es_dia_no_laboral(self.fecha_final):
            self.fecha_final += pd.DateOffset(days=1)

    def _es_fecha_festiva(self, fecha) -> None:
        return fecha in self.fechas_festivas

    def es_dia_no_laboral(self, fecha) -> None:
        return fecha.weekday() >= 5 or self._es_fecha_festiva(fecha.strftime("%Y-%m-%d"))

    def ajustar_plazo_real_por_horario(self) -> None:
        self.fecha_inicio = self.fecha_creacion

        hora_cierra_producto = self.producto.horario.horaFin

        hora_creacion = self.fecha_creacion.time()

        if self.en_reinversion:
            if hora_creacion <= hora_cierra_producto:
                self.fecha_inicio += pd.DateOffset(
                    days=self.producto.reinversion_hora_operativa_menor_igual)
            if hora_creacion > hora_cierra_producto:
                self.fecha_inicio += pd.DateOffset(
                    days=self.producto.reinversion_hora_operativa_mayor)
        else:

            if hora_creacion <= hora_cierra_producto:
                self.fecha_inicio += pd.DateOffset(
                    days=self.producto.inversion_hora_operativa_menor_igual)
            if hora_creacion > hora_cierra_producto:
                self.fecha_inicio += pd.DateOffset(
                    days=self.producto.inversion_hora_operativa_mayor)
