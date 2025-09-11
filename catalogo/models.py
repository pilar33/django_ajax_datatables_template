from django.db import models

# Create your models here.
class Libro(models.Model):
    titulo = models.CharField(max_length=150)
    autor = models.CharField(max_length=120)
    anio = models.PositiveIntegerField()
    isbn = models.CharField(max_length=20, unique=True)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} - {self.autor}"

