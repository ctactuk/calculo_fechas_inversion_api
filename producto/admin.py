from django.contrib import admin
from .models import Producto, HorarioProducto


class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'producto', 'plazo', 'fechaCreacion', 'horario')
    fields = ('producto', 'plazo', 'fechaCreacion', 'horario')
    readonly_fields = ('fechaInicio', 'fechaFin',
                       'plazoReal', 'fechaCreacion',)


class HorarioProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'horaInicio', 'horaFin')


admin.site.register(Producto, ProductoAdmin)
admin.site.register(HorarioProducto, HorarioProductoAdmin)
