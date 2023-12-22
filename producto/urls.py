from django.contrib import admin
from django.urls import path
from .views import calcular_fechas_inversion, productos

urlpatterns = [
    path('productos/', productos),
    path('calcularfechas', calcular_fechas_inversion),
]
