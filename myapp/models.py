from django.db import models

class Ingrediente(models.Model):
    nombre = models.CharField(max_length=100)
    cantidad = models.IntegerField(default=100)  # Porcentaje del ingrediente

    def __str__(self):
        return f"{self.nombre} ({self.cantidad}%)"

class HistorialBebidas(models.Model):
    nombre = models.CharField(max_length=200)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.fecha}"
