from django.db import models

class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.nombre} ({self.dni})"
