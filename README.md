# Django + jQuery AJAX + DataTables (Plantilla mínima)

Proyecto base para listar/crear/eliminar registros con DataTables usando AJAX (JsonResponse en Django).

## Requisitos
- Python 3.10+
- pip, venv
- (Opcional) MySQL + `mysqlclient`

## Instalación rápida
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Migraciones iniciales
python manage.py migrate

# Crear superusuario (para admin)
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver
```

## MySQL (opcional)
- Instalar `mysqlclient` (ya incluido en requirements).
- En `isdm/settings.py` descomentar el bloque de `DATABASES` para MySQL y completar credenciales.

## Rutas
- `/` → lista con DataTables + modal crear
- `/pacientes/data/` → JSON para DataTables
- `/pacientes/crear/` → POST crear
- `/pacientes/eliminar/<id>/` → POST eliminar
# django_ajax_datatables_template_conAuditoria
