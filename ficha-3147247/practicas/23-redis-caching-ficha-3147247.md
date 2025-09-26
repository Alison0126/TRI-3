# Práctica 23: Redis Caching Genérico - FICHA 3147247

## ⚡ **REDIS CACHING UNIVERSAL**

> **🛡️ POLÍTICA ANTI-COPIA:** Esta práctica utiliza exclusivamente ejemplos genéricos tipo A/B/C/D para garantizar equidad educativa. Ver: [Política de Equidad](../../../_docs/POLITICA-EQUIDAD-EJEMPLOS.md)

---

## 🎯 **OBJETIVOS DE APRENDIZAJE**

Al finalizar esta práctica serás capaz de:

1. **🔧 Configurar Redis** para caching genérico en FastAPI
2. **📊 Implementar estrategias** de cache universales
3. **⚡ Optimizar consultas** reduciendo carga de base de datos
4. **📈 Medir mejoras** de performance con métricas estándar

---

## 🛠️ **SETUP INICIAL**

### **📦 Dependencias Requeridas**

```bash
# Instalar dependencias
pip install redis aioredis python-dotenv
```

### **🔧 Configuración de Redis**

```python
# app/cache/redis_config.py
import redis.asyncio as aioredis
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class RedisManager:
    def __init__(self):
        self.redis: Optional[aioredis.Redis] = None

    async def connect(self):
        """Conectar a Redis con configuración genérica"""
        self.redis = aioredis.from_url(
            os.getenv("REDIS_URL", "redis://localhost:6379"),
            encoding="utf-8",
            decode_responses=True
        )

    async def disconnect(self):
        """Desconectar de Redis"""
        if self.redis:
            await self.redis.close()

    async def get(self, key: str) -> Optional[str]:
        """Obtener valor del cache"""
        if self.redis:
            return await self.redis.get(key)
        return None

    async def set(self, key: str, value: str, expire: int = 300):
        """Guardar valor en cache con expiración"""
        if self.redis:
            await self.redis.set(key, value, ex=expire)

    async def delete(self, key: str):
        """Eliminar clave del cache"""
        if self.redis:
            await self.redis.delete(key)

    async def clear_pattern(self, pattern: str):
        """Limpiar cache por patrón"""
        if self.redis:
            keys = await self.redis.keys(pattern)
            if keys:
                await self.redis.delete(*keys)

# Instancia global
redis_manager = RedisManager()
```

---

## 🎯 **IMPLEMENTACIÓN POR TIPOS GENÉRICOS**

### **🅰️ TIPO A - Gestión de Datos**

#### **Cache para Registros Principales**

```python
# app/cache/tipo_a_cache.py
import json
from datetime import datetime
from typing import List, Dict, Any
from app.cache.redis_config import redis_manager

class TipoACache:

    @staticmethod
    async def get_registro_principal(registro_id: int) -> Optional[Dict]:
        """Cache para registro principal Tipo A"""
        key = f"tipo_a:registro:{registro_id}"
        cached = await redis_manager.get(key)

        if cached:
            return json.loads(cached)
        return None

    @staticmethod
    async def set_registro_principal(registro_id: int, data: Dict, expire: int = 600):
        """Guardar registro principal en cache"""
        key = f"tipo_a:registro:{registro_id}"
        await redis_manager.set(key, json.dumps(data), expire)

    @staticmethod
    async def get_configuraciones() -> Optional[List[Dict]]:
        """Cache para configuraciones del sistema"""
        key = "tipo_a:configuraciones"
        cached = await redis_manager.get(key)

        if cached:
            return json.loads(cached)
        return None

    @staticmethod
    async def set_configuraciones(configs: List[Dict], expire: int = 1800):
        """Cache configuraciones (30 min)"""
        key = "tipo_a:configuraciones"
        await redis_manager.set(key, json.dumps(configs), expire)

    @staticmethod
    async def invalidate_registro(registro_id: int):
        """Invalidar cache de registro específico"""
        key = f"tipo_a:registro:{registro_id}"
        await redis_manager.delete(key)
```

### **🅱️ TIPO B - Programación Temporal**

#### **Cache para Horarios y Disponibilidad**

```python
# app/cache/tipo_b_cache.py
import json
from datetime import datetime, date
from typing import List, Dict, Any
from app.cache.redis_config import redis_manager

class TipoBCache:

    @staticmethod
    async def get_disponibilidad_fecha(fecha: date) -> Optional[Dict]:
        """Cache para disponibilidad por fecha"""
        key = f"tipo_b:disponibilidad:{fecha.isoformat()}"
        cached = await redis_manager.get(key)

        if cached:
            return json.loads(cached)
        return None

    @staticmethod
    async def set_disponibilidad_fecha(fecha: date, disponibilidad: Dict, expire: int = 300):
        """Cache disponibilidad (5 min - datos dinámicos)"""
        key = f"tipo_b:disponibilidad:{fecha.isoformat()}"
        await redis_manager.set(key, json.dumps(disponibilidad), expire)

    @staticmethod
    async def get_horarios_recurso(recurso_id: int) -> Optional[List[Dict]]:
        """Cache para horarios de recurso"""
        key = f"tipo_b:horarios:recurso:{recurso_id}"
        cached = await redis_manager.get(key)

        if cached:
            return json.loads(cached)
        return None

    @staticmethod
    async def set_horarios_recurso(recurso_id: int, horarios: List[Dict], expire: int = 900):
        """Cache horarios de recurso (15 min)"""
        key = f"tipo_b:horarios:recurso:{recurso_id}"
        await redis_manager.set(key, json.dumps(horarios), expire)

    @staticmethod
    async def invalidate_fecha(fecha: date):
        """Invalidar disponibilidad de fecha específica"""
        key = f"tipo_b:disponibilidad:{fecha.isoformat()}"
        await redis_manager.delete(key)
```

### **🅾️ TIPO C - Servicios de Usuario**

#### **Cache para Perfiles y Servicios**

```python
# app/cache/tipo_c_cache.py
import json
from typing import List, Dict, Any, Optional
from app.cache.redis_config import redis_manager

class TipoCCache:

    @staticmethod
    async def get_perfil_usuario(user_id: int) -> Optional[Dict]:
        """Cache para perfil de usuario"""
        key = f"tipo_c:perfil:{user_id}"
        cached = await redis_manager.get(key)

        if cached:
            return json.loads(cached)
        return None

    @staticmethod
    async def set_perfil_usuario(user_id: int, perfil: Dict, expire: int = 1200):
        """Cache perfil usuario (20 min)"""
        key = f"tipo_c:perfil:{user_id}"
        await redis_manager.set(key, json.dumps(perfil), expire)

    @staticmethod
    async def get_servicios_usuario(user_id: int) -> Optional[List[Dict]]:
        """Cache para servicios asignados al usuario"""
        key = f"tipo_c:servicios:{user_id}"
        cached = await redis_manager.get(key)

        if cached:
            return json.loads(cached)
        return None

    @staticmethod
    async def set_servicios_usuario(user_id: int, servicios: List[Dict], expire: int = 600):
        """Cache servicios usuario (10 min)"""
        key = f"tipo_c:servicios:{user_id}"
        await redis_manager.set(key, json.dumps(servicios), expire)

    @staticmethod
    async def invalidate_usuario(user_id: int):
        """Invalidar cache completo de usuario"""
        pattern = f"tipo_c:*:{user_id}"
        await redis_manager.clear_pattern(pattern)
```

### **🔷 TIPO D - Catálogo de Elementos**

#### **Cache para Inventario y Productos**

```python
# app/cache/tipo_d_cache.py
import json
from typing import List, Dict, Any, Optional
from app.cache.redis_config import redis_manager

class TipoDCache:

    @staticmethod
    async def get_elemento_catalogo(elemento_id: int) -> Optional[Dict]:
        """Cache para elemento del catálogo"""
        key = f"tipo_d:elemento:{elemento_id}"
        cached = await redis_manager.get(key)

        if cached:
            return json.loads(cached)
        return None

    @staticmethod
    async def set_elemento_catalogo(elemento_id: int, elemento: Dict, expire: int = 900):
        """Cache elemento catálogo (15 min)"""
        key = f"tipo_d:elemento:{elemento_id}"
        await redis_manager.set(key, json.dumps(elemento), expire)

    @staticmethod
    async def get_inventario_categoria(categoria: str) -> Optional[List[Dict]]:
        """Cache para inventario por categoría"""
        key = f"tipo_d:inventario:categoria:{categoria}"
        cached = await redis_manager.get(key)

        if cached:
            return json.loads(cached)
        return None

    @staticmethod
    async def set_inventario_categoria(categoria: str, inventario: List[Dict], expire: int = 300):
        """Cache inventario categoría (5 min - datos críticos)"""
        key = f"tipo_d:inventario:categoria:{categoria}"
        await redis_manager.set(key, json.dumps(inventario), expire)

    @staticmethod
    async def invalidate_elemento(elemento_id: int):
        """Invalidar cache de elemento específico"""
        key = f"tipo_d:elemento:{elemento_id}"
        await redis_manager.delete(key)
```

---

## 🔧 **INTEGRACIÓN CON FASTAPI**

### **Middleware de Cache**

```python
# app/middleware/cache_middleware.py
from fastapi import Request, Response
from fastapi.responses import JSONResponse
import json
import hashlib
from app.cache.redis_config import redis_manager

class CacheMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            request = Request(scope, receive)

            # Solo cachear GET requests
            if request.method == "GET":
                cache_key = self._generate_cache_key(request)
                cached_response = await redis_manager.get(cache_key)

                if cached_response:
                    response_data = json.loads(cached_response)
                    response = JSONResponse(content=response_data)
                    await response(scope, receive, send)
                    return

        # Si no hay cache, continuar normalmente
        await self.app(scope, receive, send)

    def _generate_cache_key(self, request: Request) -> str:
        """Generar clave de cache basada en URL y query params"""
        url_with_params = str(request.url)
        return f"response:{hashlib.md5(url_with_params.encode()).hexdigest()}"
```

### **Decorador de Cache**

```python
# app/cache/decorators.py
from functools import wraps
import json
import hashlib
from app.cache.redis_config import redis_manager

def cache_result(expire: int = 300, key_prefix: str = ""):
    """Decorador para cachear resultados de funciones"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generar clave única basada en función y parámetros
            func_name = func.__name__
            args_str = str(args) + str(sorted(kwargs.items()))
            cache_key = f"{key_prefix}:{func_name}:{hashlib.md5(args_str.encode()).hexdigest()}"

            # Intentar obtener del cache
            cached = await redis_manager.get(cache_key)
            if cached:
                return json.loads(cached)

            # Ejecutar función y cachear resultado
            result = await func(*args, **kwargs)
            await redis_manager.set(cache_key, json.dumps(result), expire)

            return result
        return wrapper
    return decorator
```

---

## 📊 **EJEMPLO DE USO EN ENDPOINTS**

### **Endpoints con Cache Implementado**

```python
# app/routes/cached_routes.py
from fastapi import APIRouter, HTTPException
from typing import List, Dict
from app.cache.decorators import cache_result
from app.cache.tipo_a_cache import TipoACache
from app.cache.tipo_b_cache import TipoBCache

router = APIRouter()

@router.get("/tipo-a/registro/{registro_id}")
@cache_result(expire=600, key_prefix="api")
async def get_registro_tipo_a(registro_id: int):
    """Endpoint con cache para Tipo A"""
    # Intentar obtener del cache
    cached_data = await TipoACache.get_registro_principal(registro_id)
    if cached_data:
        return {"data": cached_data, "from_cache": True}

    # Simular consulta a DB (reemplazar con tu lógica)
    data = await simulate_db_query_tipo_a(registro_id)

    # Guardar en cache
    await TipoACache.set_registro_principal(registro_id, data)

    return {"data": data, "from_cache": False}

@router.get("/tipo-b/disponibilidad/{fecha}")
async def get_disponibilidad_tipo_b(fecha: str):
    """Endpoint con cache para Tipo B"""
    from datetime import datetime
    fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()

    # Verificar cache
    cached_data = await TipoBCache.get_disponibilidad_fecha(fecha_obj)
    if cached_data:
        return {"disponibilidad": cached_data, "from_cache": True}

    # Consultar y cachear
    disponibilidad = await simulate_availability_query(fecha_obj)
    await TipoBCache.set_disponibilidad_fecha(fecha_obj, disponibilidad)

    return {"disponibilidad": disponibilidad, "from_cache": False}

# Funciones de simulación (reemplazar con tu lógica de DB)
async def simulate_db_query_tipo_a(registro_id: int):
    return {
        "id": registro_id,
        "nombre": f"Registro {registro_id}",
        "estado": "activo",
        "configuracion": {"param1": "valor1", "param2": "valor2"}
    }

async def simulate_availability_query(fecha):
    return {
        "fecha": fecha.isoformat(),
        "slots_disponibles": 10,
        "slots_ocupados": 5,
        "horarios": ["09:00", "10:00", "11:00"]
    }
```

---

## 📈 **MÉTRICAS Y MONITOREO**

### **Middleware de Métricas de Cache**

```python
# app/middleware/cache_metrics.py
import time
from fastapi import Request
from app.cache.redis_config import redis_manager

class CacheMetrics:
    def __init__(self):
        self.hits = 0
        self.misses = 0
        self.total_requests = 0

    async def log_cache_hit(self, key: str):
        """Registrar hit de cache"""
        self.hits += 1
        self.total_requests += 1
        await redis_manager.set(f"metrics:cache_hits", str(self.hits))

    async def log_cache_miss(self, key: str):
        """Registrar miss de cache"""
        self.misses += 1
        self.total_requests += 1
        await redis_manager.set(f"metrics:cache_misses", str(self.misses))

    async def get_cache_ratio(self) -> float:
        """Obtener ratio de aciertos del cache"""
        if self.total_requests == 0:
            return 0.0
        return self.hits / self.total_requests

# Instancia global
cache_metrics = CacheMetrics()
```

---

## 🧪 **TESTING DE CACHE**

### **Tests de Funcionalidad**

```python
# tests/test_cache.py
import pytest
from app.cache.redis_config import redis_manager
from app.cache.tipo_a_cache import TipoACache

@pytest.fixture
async def setup_redis():
    await redis_manager.connect()
    yield
    await redis_manager.disconnect()

async def test_tipo_a_cache_set_get(setup_redis):
    """Test básico de set/get para Tipo A"""
    test_data = {"id": 1, "nombre": "Test"}

    # Guardar en cache
    await TipoACache.set_registro_principal(1, test_data)

    # Recuperar del cache
    cached_data = await TipoACache.get_registro_principal(1)

    assert cached_data == test_data

async def test_cache_expiration(setup_redis):
    """Test de expiración de cache"""
    import asyncio

    test_data = {"id": 2, "nombre": "Test Expiration"}

    # Guardar con expiración corta (1 segundo)
    await TipoACache.set_registro_principal(2, test_data, expire=1)

    # Verificar que existe
    cached_data = await TipoACache.get_registro_principal(2)
    assert cached_data == test_data

    # Esperar expiración
    await asyncio.sleep(2)

    # Verificar que expiró
    expired_data = await TipoACache.get_registro_principal(2)
    assert expired_data is None
```

---

## 🎯 **ENTREGABLES**

### **📋 Checklist de Implementación**

- [ ] **Redis configurado** y conectado correctamente
- [ ] **Cache implementado** para tu tipo asignado (A/B/C/D)
- [ ] **Middleware de cache** funcionando en endpoints
- [ ] **Decoradores de cache** aplicados a funciones críticas
- [ ] **Invalidación de cache** implementada correctamente
- [ ] **Métricas de cache** registrándose correctamente
- [ ] **Tests de cache** ejecutándose exitosamente

### **📊 Métricas a Medir**

1. **Hit Ratio del Cache:** > 70%
2. **Reducción de consultas DB:** > 50%
3. **Mejora en tiempo de respuesta:** > 30%
4. **Uso de memoria Redis:** Optimizado

---

## 🚀 **SIGUIENTES PASOS**

Una vez completada esta práctica:

1. **📊 Mide las mejoras** obtenidas con métricas
2. **📝 Documenta** la estrategia de cache implementada
3. **🔄 Continúa** con la Práctica 24 (Optimización de DB)

---

**PRÁCTICA 23 - REDIS CACHING COMPLETADA**  
_Técnicas universales aplicables a cualquier API_
