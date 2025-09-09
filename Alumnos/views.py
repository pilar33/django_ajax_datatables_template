# app/views.py
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render
from .models import Alumno


# para la auditoria
from django.db import connection, transaction
from datetime import datetime
from django.views.decorators.http import require_POST
from django.db import DatabaseError
from Alumnos.services.alumnos import crear_alumno_con_auditoria

def alumnos_list(request):
    """Renderiza la plantilla con DataTables."""
    return render(request, 'alumnos/alumnos_list.html')

def alumnos_data(request):
    """Devuelve la lista de alumnos activos en formato JSON para DataTables."""
    data = [
        {
            'id': a.id,
            'nombre': a.nombre,
            'dni': a.dni,
            'fecha_nac': a.fecha_nac.strftime('%Y-%m-%d') if a.fecha_nac else '',
        }
        for a in Alumno.objects.filter(iEstado=True)
    ]
    return JsonResponse({'data': data})


#La vista fue diseñada para mostrar funcionamiento con ajax
# @require_POST
# def alumno_crear_actualizar(request):
#     """
#     Crea un nuevo alumno o actualiza uno existente.
#     Si se recibe un campo 'id', se actualiza ese registro;
#     si no, se crea un nuevo registro.
#     """
#     datos = request.POST
#     alumno_id = datos.get('id')
#     nombre = datos.get('nombre', '').strip()
#     dni = datos.get('dni', '').strip()
#     fecha_nac = datos.get('fecha_nac')

#     # Validaciones básicas
#     if not nombre or not dni:
#         return JsonResponse({'ok': False, 'msg': 'Campos obligatorios'}, status=400)

#     # Actualizar
#     if alumno_id:
#         try:
#             alumno = Alumno.objects.get(pk=alumno_id)
#             alumno.nombre = nombre
#             alumno.dni = dni
#             alumno.fecha_nac = fecha_nac or None
#             alumno.iEstado = True
#             alumno.save()
#             return JsonResponse({'ok': True, 'msg': 'Alumno actualizado'})
#         except Alumno.DoesNotExist:
#             return JsonResponse({'ok': False, 'msg': 'Alumno no encontrado'}, status=404)

#     # Crear (verificar DNI único)
#     if Alumno.objects.filter(dni=dni).exists():
#         return JsonResponse({'ok': False, 'msg': 'El DNI ya existe'}, status=400)

#     Alumno.objects.create(nombre=nombre, dni=dni, fecha_nac=fecha_nac or None)
#     return JsonResponse({'ok': True, 'msg': 'Alumno creado correctamente'})

#agregar alumnos, que incluye auditoria
def _parse_fecha(fecha_str):
    if not fecha_str:
        return None
    try:
        return datetime.strptime(fecha_str, "%Y-%m-%d").date()
    except ValueError:
        return None

@require_POST
def alumno_crear_actualizar(request):
    """
    Crea un nuevo alumno (vía SP con auditoría) o actualiza uno existente (ORM).
    Si se recibe 'id' => UPDATE; si no => INSERT con sp_alumno_insert.
    """
    datos = request.POST
    alumno_id = datos.get('id')
    nombre = (datos.get('nombre') or '').strip()
    dni = (datos.get('dni') or '').strip()
    fecha_nac = _parse_fecha(datos.get('fecha_nac'))

    if not nombre or not dni:
        return JsonResponse({'ok': False, 'msg': 'Campos obligatorios'}, status=400)

    actor_id = request.user.id if request.user.is_authenticated else None

    # Actualizar (podés mantener ORM o crear un sp_alumno_update y llamarlo aquí)
    if alumno_id:
        try:
            alumno = Alumno.objects.get(pk=alumno_id)
            # Validar unicidad de DNI para otro registro
            if Alumno.objects.filter(dni=dni).exclude(pk=alumno_id).exists():
                return JsonResponse({'ok': False, 'msg': 'El DNI ya existe'}, status=400)

            alumno.nombre = nombre
            alumno.dni = dni
            alumno.fecha_nac = fecha_nac
            alumno.iEstado = True
            alumno.save()
            return JsonResponse({'ok': True, 'msg': 'Alumno actualizado', 'id': alumno.id})
        except Alumno.DoesNotExist:
            return JsonResponse({'ok': False, 'msg': 'Alumno no encontrado'}, status=404)

    # Crear con SP (el SP ya valida DNI duplicado y audita)
    try:
        alumno = crear_alumno_con_auditoria(
            nombre=nombre, dni=dni, fecha_nac=fecha_nac, actor_id=actor_id
        )
        return JsonResponse({'ok': True, 'msg': 'Alumno creado correctamente', 'id': alumno.id})
    except DatabaseError as e:
        msg = str(e)
        if 'DNI ya existe' in msg:
            return JsonResponse({'ok': False, 'msg': 'El DNI ya existe'}, status=400)
        return JsonResponse({'ok': False, 'msg': 'Error de base de datos'}, status=500)

@require_POST
def alumno_borrado_logico(request, pk):
    """Marca el registro como inactivo (borrado lógico) cambiando iEstado a False."""
    try:
        alumno = Alumno.objects.get(pk=pk)
        alumno.iEstado = False
        alumno.save()
        return JsonResponse({'ok': True, 'msg': 'Alumno desactivado'})
    except Alumno.DoesNotExist:
        return JsonResponse({'ok': False, 'msg': 'Alumno no encontrado'}, status=404)
