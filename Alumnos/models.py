from django.db import models

# Create your models here.

class Alumno(models.Model):
    nombre = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True)
    fecha_nac = models.DateField(null=True, blank=True)
    iEstado = models.BooleanField(default=True)  

    def __str__(self):
        return f"{self.nombre} ({self.dni})"

    class Meta:
        verbose_name = 'Alumno'
        verbose_name_plural = 'Alumnos'

# iEstado controla el borrado lógico: sólo se mostrarán los alumnos con iEstado=True