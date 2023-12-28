from django.db import models

import datetime as dt

HOUR_CHOICES = [(dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(0, 24)]


class HorarioProducto(models.Model):
    name = models.CharField(max_length=100)
    horaInicio = models.TimeField(
        verbose_name="Hora de inicio", choices=HOUR_CHOICES)
    horaFin = models.TimeField(
        verbose_name="Hora de fin", choices=HOUR_CHOICES)

    class Meta:
        verbose_name = "Horario"
        verbose_name_plural = "Horarios"
        ordering = ['horaInicio']

    def __str__(self):
        return self.name + " - " + str(self.horaInicio) + " - " + str(self.horaFin)


class Producto(models.Model):
    producto = models.CharField(max_length=100)
    inversion_hora_operativa_menor_igual = models.IntegerField()
    inversion_hora_operativa_mayor = models.IntegerField()
    reinversion_hora_operativa_menor_igual = models.IntegerField()
    reinversion_hora_operativa_mayor = models.IntegerField()
    horario = models.OneToOneField(
        HorarioProducto, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['producto']

    def __str__(self):
        return self.producto + " - " + str(self.horario) + " - " + str(self.inversion_hora_operativa_menor_igual) + " - " + str(self.inversion_hora_operativa_mayor) + " - " + str(self.reinversion_hora_operativa_menor_igual) + " - " + str(self.reinversion_hora_operativa_mayor)
