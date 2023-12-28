from django.contrib import admin
from .models import Producto, HorarioProducto


class HorarioProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'horaInicio', 'horaFin')


admin.site.register(Producto)
admin.site.register(HorarioProducto, HorarioProductoAdmin)
