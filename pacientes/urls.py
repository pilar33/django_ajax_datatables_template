from django.urls import path
from . import views

urlpatterns = [
    path('', views.pacientes_list, name='pacientes_list'),
    path('pacientes/data/', views.pacientes_data, name='pacientes_data'),
    path('pacientes/crear/', views.paciente_crear, name='paciente_crear'),
    path('pacientes/eliminar/<int:pk>/', views.paciente_eliminar, name='paciente_eliminar'),
]
