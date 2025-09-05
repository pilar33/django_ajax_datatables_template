# app/urls.py
from django.urls import path
from . import views

# app/urls.py
urlpatterns = [
    path('alumnos/', views.alumnos_list, name='alumnos_list'),   # muestra la plantilla
    path('alumnos/data/', views.alumnos_data, name='alumnos_data'),  # devuelve {"data": ...}
    path('alumnos/guardar/', views.alumno_crear_actualizar, name='alumno_guardar'),
    path('alumnos/eliminar/<int:pk>/', views.alumno_borrado_logico, name='alumno_borrar'),
]

