# Mi API FastAPI - Semana 2

## ¿Qué hace?

API mejorada con validación automática de datos y type hints.

## Nuevos Features (Semana 2)

- ✅ Type hints en todas las funciones
- ✅ Validación automática con Pydantic
- ✅ Endpoint POST para crear datos
- ✅ Parámetros de ruta (ejemplo: /products/{id})
- ✅ Búsqueda con parámetros query

## ¿Cómo ejecutar?

```bash
pip install fastapi pydantic uvicorn
uvicorn main:app --reload
```


**2. Subir a GitHub** (10 min):

```bash
# En tu terminal, en la carpeta de tu proyecto
git add .
git commit -m "Semana 2: API con Pydantic y Type Hints"
git push

**Frases de lo mas relevante**
-Se implementaron endpoints para crear, listar, buscar y obtener productos por ID, mostrando operaciones CRUD básicas.
-Se usó manejo de errores con HTTPException para devolver respuestas adecuadas cuando un producto no existe.
-La API maneja un almacenamiento temporal en memoria usando una lista simple para simular una base de datos.


**2. Subir a GitHub** (10 min):

```bash
# En tu terminal, en la carpeta de tu proyecto
git add .
git commit -m "Semana 2: API con Pydantic y Type Hints"
git push

tu-repositorio/
├── main.py                    # API con Type Hints + Pydantic
├── requirements.txt           # fastapi, pydantic, uvicorn
└── README.md                  # Documentación actualizada