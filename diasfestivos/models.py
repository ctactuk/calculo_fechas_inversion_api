from django.db import models


class DiasFestivos(models.Model):
    fecha = models.DateField()
    descripcion = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Día Festivo"
        verbose_name_plural = "Días Festivos"
        ordering = ['fecha']

    def __str__(self):
        return str(self.fecha) + " - " + self.descripcion
