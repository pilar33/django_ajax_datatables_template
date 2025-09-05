from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Paciente

def pacientes_list(request):
    return render(request, 'pacientes/pacientes_list.html')

def pacientes_data(request):
    data = [
        {"id": p.id, "nombre": p.nombre, "dni": p.dni}
        for p in Paciente.objects.all().order_by('id')
    ]
    return JsonResponse({"data": data})

@require_POST
def paciente_crear(request):
    nombre = request.POST.get('nombre', '').strip()
    dni = request.POST.get('dni', '').strip()
    if not nombre or not dni:
        return JsonResponse({"ok": False, "msg": "Campos incompletos."}, status=400)
    if Paciente.objects.filter(dni=dni).exists():
        return JsonResponse({"ok": False, "msg": "El DNI ya existe."}, status=400)
    Paciente.objects.create(nombre=nombre, dni=dni)
    return JsonResponse({"ok": True, "msg": "Paciente creado correctamente."})

@require_POST
def paciente_eliminar(request, pk):
    try:
        p = Paciente.objects.get(pk=pk)
        p.delete()
        return JsonResponse({"ok": True, "msg": "Paciente eliminado."})
    except Paciente.DoesNotExist:
        return JsonResponse({"ok": False, "msg": "Paciente no encontrado."}, status=404)
