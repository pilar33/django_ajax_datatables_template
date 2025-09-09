# tuapp/services/alumnos.py
from django.db import connection, transaction
from Alumnos.models import Alumno

@transaction.atomic
def crear_alumno_con_auditoria(*, nombre: str, dni: str, fecha_nac, actor_id: int | None) -> Alumno:
    with connection.cursor() as c:
        c.execute("CALL sp_alumno_insert(%s, %s, %s, %s)", [nombre, dni, fecha_nac, actor_id])
        new_id = c.fetchone()[0]  # viene del SELECT v_new_id AS id
        while c.nextset():  # limpia resultsets restantes por seguridad
            pass
    return Alumno.objects.get(pk=new_id)
