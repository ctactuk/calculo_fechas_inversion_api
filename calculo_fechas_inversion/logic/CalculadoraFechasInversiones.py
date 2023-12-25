from datetime import datetime, timedelta


class CalculadoraFechas:
    def __init__(self, fecha_inicio, plazo, hora_fin, festivos=[]):
        self.fecha_inicio = fecha_inicio
        self.fecha_final = None
        self.plazo = plazo
        self.hora_fin = hora_fin
        self.festivos = set(festivos)
        self.plazo_real = 1

    def es_fin_de_semana_o_festivo(self, fecha):
        return fecha.weekday() >= 5 or fecha.strftime("%Y-%m-%d") in self.festivos

    def ajustar_fecha_inicio(self):
        while self.es_fin_de_semana_o_festivo(self.fecha_inicio):
            self.fecha_inicio += timedelta(days=1)
            self.plazo_real += 1

    def ajustar_fecha_fin(self):
        fecha_fin = self.fecha_inicio
        for _ in range(self.plazo - 1):
            fecha_fin += timedelta(days=1)
            while self.es_fin_de_semana_o_festivo(fecha_fin):
                fecha_fin += timedelta(days=1)
                self.plazo_real += 1
            self.plazo_real += 1
        self.fecha_final = fecha_fin

    def ajustar_fecha_por_horario(self):
        hora_actual = datetime.now().strftime("%H")
        if self.fecha_inicio.date() == datetime.now().date() and hora_actual >= self.hora_fin:
            self.fecha_inicio += timedelta(days=1)
            self.plazo_real += 1

    def calcular_fechas(self):
        self.ajustar_fecha_por_horario()
        self.ajustar_fecha_inicio()
        self.ajustar_fecha_fin()

        return {
            'fechaInicio': self.fecha_inicio,
            'fechaFin': self.fecha_final,
            'plazoReal': self.plazo_real,
            'plazo': self.plazo
        }
