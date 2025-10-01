# ospina-globalspeak

Proyecto de ejemplo para el dominio asignado a OSPINA ARIZA (Tipo B - Programación Temporal).

Incluye una clase `SchedulingManager` para gestionar estudiantes y programación de clases con detección de conflictos.

Instrucciones rápidas:

- Crear y activar el entorno virtual (opcional).
- Instalar dependencias: `pip install -r requirements.txt`.
- Ejecutar pruebas: `pytest -q`.

Ejemplo rápido (usar desde la carpeta `ospina-globalspeak`):

```python
from scheduling import SchedulingManager, ClassEvent
from datetime import datetime, timedelta

mgr = SchedulingManager()
mgr.add_student("s1", "Ana Ospina")
start = datetime.now()
end = start + timedelta(hours=1)
ev = ClassEvent(id="c1", student_id="s1", start=start, end=end, title="Inglés 101")
mgr.schedule_class(ev)
print(mgr.list_events("s1"))
```

Requisitos:

- Python 3.8+
- pytest (solo para tests)
