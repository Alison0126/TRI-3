# Práctica 25: Middleware Rate Limiting - FICHA 3147247

## 🛠️ **MIDDLEWARE PERSONALIZADO Y RATE LIMITING**

> **🛡️ POLÍTICA ANTI-COPIA:** Esta práctica utiliza exclusivamente ejemplos genéricos tipo A/B/C/D para garantizar equidad educativa. Ver: [Política de Equidad](../../../_docs/POLITICA-EQUIDAD-EJEMPLOS.md)

---

## 🎯 **OBJETIVOS DE APRENDIZAJE**

Al finalizar esta práctica serás capaz de:

1. **🔒 Implementar rate limiting** usando técnicas estándar de la industria
2. **📝 Crear middleware de logging** genérico para monitoreo
3. **⚡ Optimizar performance** mediante control de tráfico inteligente
4. **📊 Monitorear uso** con métricas en tiempo real

---

## 🔧 **RATE LIMITING UNIVERSAL**

### **📦 Dependencias Base**

```bash
# Instalar dependencias para rate limiting
pip install slowapi redis python-dotenv limits
```

### **🔒 Rate Limiter Genérico**

```python
# app/middleware/rate_limiter.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi import Request, Response
from fastapi.responses import JSONResponse
import redis.asyncio as aioredis
import time
from typing import Dict, Optional
import json

class UniversalRateLimiter:
    """Rate limiter universal aplicable a cualquier tipo de API"""

    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_url = redis_url
        self.redis_client: Optional[aioredis.Redis] = None

        # Límites genéricos por tipo de operación
        self.rate_limits = {
            "default": "100/minute",
            "read_operations": "200/minute",
            "write_operations": "50/minute",
            "heavy_operations": "10/minute",
            "auth_operations": "20/minute"
        }

    async def setup(self):
        """Inicializar conexión Redis"""
        self.redis_client = aioredis.from_url(
            self.redis_url,
            encoding="utf-8",
            decode_responses=True
        )

    async def check_rate_limit(
        self,
        identifier: str,
        operation_type: str = "default",
        window_seconds: int = 60
    ) -> Dict[str, any]:
        """Verificar límite de tasa genérico"""

        if not self.redis_client:
            await self.setup()

        current_time = int(time.time())
        window_start = current_time - window_seconds

        # Clave única para el límite
        key = f"rate_limit:{operation_type}:{identifier}:{current_time // window_seconds}"

        # Contador actual
        current_count = await self.redis_client.get(key)
        current_count = int(current_count) if current_count else 0

        # Obtener límite para el tipo de operación
        limit = self._parse_limit(self.rate_limits.get(operation_type, "100/minute"))

        if current_count >= limit:
            return {
                "allowed": False,
                "current_count": current_count,
                "limit": limit,
                "reset_time": (current_time // window_seconds + 1) * window_seconds,
                "retry_after": window_seconds - (current_time % window_seconds)
            }

        # Incrementar contador
        pipe = self.redis_client.pipeline()
        pipe.incr(key)
        pipe.expire(key, window_seconds)
        await pipe.execute()

        return {
            "allowed": True,
            "current_count": current_count + 1,
            "limit": limit,
            "remaining": limit - current_count - 1,
            "reset_time": (current_time // window_seconds + 1) * window_seconds
        }

    def _parse_limit(self, limit_str: str) -> int:
        """Parsear string de límite (ej: '100/minute')"""
        parts = limit_str.split('/')
        return int(parts[0])

# Instancia global
rate_limiter = UniversalRateLimiter()
```

---

## 🎯 **IMPLEMENTACIÓN POR TIPOS GENÉRICOS**

### **🅰️ TIPO A - Gestión de Datos**

#### **Rate Limiting para Operaciones de Datos**

```python
# app/middleware/tipo_a_rate_limiter.py
from fastapi import Request, HTTPException
from app.middleware.rate_limiter import rate_limiter
from typing import Callable

class TipoAMiddleware:
    """Middleware específico para operaciones de gestión de datos"""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            request = Request(scope, receive)

            # Identificar tipo de operación
            operation_type = self._get_operation_type(request)
            identifier = self._get_client_identifier(request)

            # Verificar rate limit
            result = await rate_limiter.check_rate_limit(identifier, operation_type)

            if not result["allowed"]:
                response = self._create_rate_limit_response(result)
                await response(scope, receive, send)
                return

            # Agregar headers informativos
            def add_rate_limit_headers(message):
                if message["type"] == "http.response.start":
                    headers = list(message.get("headers", []))
                    headers.extend([
                        (b"X-RateLimit-Limit", str(result["limit"]).encode()),
                        (b"X-RateLimit-Remaining", str(result.get("remaining", 0)).encode()),
                        (b"X-RateLimit-Reset", str(result["reset_time"]).encode()),
                    ])
                    message["headers"] = headers
                return message

            # Modificar send para incluir headers
            async def send_with_headers(message):
                await send(add_rate_limit_headers(message))

        await self.app(scope, receive, send_with_headers)

    def _get_operation_type(self, request: Request) -> str:
        """Determinar tipo de operación basado en endpoint y método"""
        method = request.method
        path = request.url.path

        # Operaciones de lectura intensiva
        if method == "GET" and "/search" in path:
            return "heavy_operations"
        elif method == "GET" and "/bulk" in path:
            return "heavy_operations"

        # Operaciones de escritura
        elif method in ["POST", "PUT", "PATCH", "DELETE"]:
            return "write_operations"

        # Operaciones de lectura estándar
        elif method == "GET":
            return "read_operations"

        return "default"

    def _get_client_identifier(self, request: Request) -> str:
        """Obtener identificador único del cliente"""
        # Priorizar usuario autenticado
        user_id = getattr(request.state, "user_id", None)
        if user_id:
            return f"user:{user_id}"

        # Fallback a IP
        return f"ip:{request.client.host}"

    def _create_rate_limit_response(self, result: dict):
        """Crear respuesta de rate limit excedido"""
        from fastapi.responses import JSONResponse

        return JSONResponse(
            status_code=429,
            content={
                "error": "Rate limit exceeded",
                "message": f"Too many requests. Limit: {result['limit']} per minute",
                "retry_after": result["retry_after"]
            },
            headers={
                "Retry-After": str(result["retry_after"]),
                "X-RateLimit-Limit": str(result["limit"]),
                "X-RateLimit-Reset": str(result["reset_time"])
            }
        )
```

### **🅱️ TIPO B - Programación Temporal**

#### **Rate Limiting para Operaciones Temporales**

```python
# app/middleware/tipo_b_rate_limiter.py
from fastapi import Request
from app.middleware.rate_limiter import rate_limiter
from datetime import datetime, time

class TipoBMiddleware:
    """Middleware para operaciones de programación temporal"""

    def __init__(self, app):
        self.app = app
        # Límites específicos para operaciones temporales
        self.temporal_limits = {
            "reservation_check": "30/minute",  # Verificación de disponibilidad
            "reservation_create": "10/minute", # Creación de reservas
            "schedule_query": "100/minute",    # Consultas de horarios
            "availability_check": "50/minute"  # Verificación de disponibilidad
        }

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            request = Request(scope, receive)

            operation_type = self._classify_temporal_operation(request)
            identifier = self._get_identifier_with_temporal_context(request)

            # Aplicar límites específicos para operaciones temporales
            result = await rate_limiter.check_rate_limit(
                identifier,
                operation_type,
                window_seconds=self._get_window_for_operation(operation_type)
            )

            if not result["allowed"]:
                response = self._create_temporal_rate_limit_response(result, operation_type)
                await response(scope, receive, send)
                return

        await self.app(scope, receive, send)

    def _classify_temporal_operation(self, request: Request) -> str:
        """Clasificar operación temporal"""
        path = request.url.path.lower()
        method = request.method

        if "disponibilidad" in path or "availability" in path:
            return "availability_check"
        elif "reserva" in path and method == "POST":
            return "reservation_create"
        elif "reserva" in path and method == "GET":
            return "reservation_check"
        elif "horario" in path or "schedule" in path:
            return "schedule_query"

        return "default"

    def _get_identifier_with_temporal_context(self, request: Request) -> str:
        """Identificador con contexto temporal"""
        base_id = f"user:{getattr(request.state, 'user_id', request.client.host)}"

        # Agregar contexto temporal para operaciones críticas
        current_hour = datetime.now().hour
        if current_hour >= 8 and current_hour <= 18:  # Horas pico
            return f"{base_id}:peak"
        else:
            return f"{base_id}:off_peak"

    def _get_window_for_operation(self, operation_type: str) -> int:
        """Ventana de tiempo específica por operación"""
        windows = {
            "reservation_create": 300,  # 5 minutos para creación
            "availability_check": 60,   # 1 minuto para disponibilidad
            "schedule_query": 60,       # 1 minuto para horarios
            "reservation_check": 120    # 2 minutos para verificación
        }
        return windows.get(operation_type, 60)
```

### **🅾️ TIPO C - Servicios de Usuario**

#### **Rate Limiting para Servicios de Usuario**

```python
# app/middleware/tipo_c_rate_limiter.py
from fastapi import Request
from app.middleware.rate_limiter import rate_limiter

class TipoCMiddleware:
    """Middleware para servicios de usuario"""

    def __init__(self, app):
        self.app = app
        # Límites basados en tipo de usuario y servicio
        self.user_limits = {
            "premium": {
                "service_access": "500/minute",
                "profile_updates": "100/minute",
                "data_export": "20/minute"
            },
            "standard": {
                "service_access": "200/minute",
                "profile_updates": "50/minute",
                "data_export": "5/minute"
            },
            "basic": {
                "service_access": "100/minute",
                "profile_updates": "20/minute",
                "data_export": "2/minute"
            }
        }

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            request = Request(scope, receive)

            user_tier = self._get_user_tier(request)
            operation_type = self._classify_service_operation(request)
            identifier = self._get_user_identifier(request)

            # Obtener límite específico para el tier del usuario
            limit_key = f"{user_tier}_{operation_type}"

            result = await rate_limiter.check_rate_limit(identifier, limit_key)

            if not result["allowed"]:
                response = self._create_service_rate_limit_response(result, user_tier)
                await response(scope, receive, send)
                return

        await self.app(scope, receive, send)

    def _get_user_tier(self, request: Request) -> str:
        """Obtener tier del usuario desde contexto"""
        # En implementación real, obtener desde JWT o sesión
        user_tier = getattr(request.state, "user_tier", "standard")
        return user_tier if user_tier in self.user_limits else "basic"

    def _classify_service_operation(self, request: Request) -> str:
        """Clasificar operación de servicio"""
        path = request.url.path.lower()
        method = request.method

        if "/profile" in path and method in ["PUT", "PATCH"]:
            return "profile_updates"
        elif "/export" in path or "/download" in path:
            return "data_export"
        elif "/service" in path:
            return "service_access"

        return "service_access"  # Default
```

### **🔷 TIPO D - Catálogo de Elementos**

#### **Rate Limiting para Catálogo**

```python
# app/middleware/tipo_d_rate_limiter.py
from fastapi import Request
from app.middleware.rate_limiter import rate_limiter

class TipoDMiddleware:
    """Middleware para operaciones de catálogo"""

    def __init__(self, app):
        self.app = app
        # Límites para operaciones de inventario en tiempo real
        self.catalog_limits = {
            "search_intensive": "150/minute",    # Búsquedas complejas
            "inventory_check": "300/minute",     # Verificación de stock
            "price_query": "200/minute",         # Consultas de precios
            "catalog_browse": "500/minute",      # Navegación general
            "inventory_update": "30/minute"      # Actualizaciones de inventario
        }

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            request = Request(scope, receive)

            operation_type = self._classify_catalog_operation(request)
            identifier = self._get_catalog_identifier(request)

            # Aplicar límites específicos de catálogo
            result = await rate_limiter.check_rate_limit(identifier, operation_type)

            if not result["allowed"]:
                response = self._create_catalog_rate_limit_response(result)
                await response(scope, receive, send)
                return

        await self.app(scope, receive, send)

    def _classify_catalog_operation(self, request: Request) -> str:
        """Clasificar operación de catálogo"""
        path = request.url.path.lower()
        method = request.method
        query_params = request.query_params

        # Búsquedas intensivas (con filtros múltiples)
        if "/search" in path and len(query_params) > 3:
            return "search_intensive"

        # Verificación de inventario
        elif "/stock" in path or "/inventory" in path:
            if method == "GET":
                return "inventory_check"
            else:
                return "inventory_update"

        # Consultas de precios
        elif "/price" in path or "/pricing" in path:
            return "price_query"

        # Navegación general de catálogo
        elif "/catalog" in path or "/products" in path:
            return "catalog_browse"

        return "catalog_browse"  # Default para operaciones de catálogo

    def _get_catalog_identifier(self, request: Request) -> str:
        """Identificador específico para operaciones de catálogo"""
        # Combinar usuario + tipo de operación para límites más granulares
        user_id = getattr(request.state, "user_id", request.client.host)
        operation = self._classify_catalog_operation(request)
        return f"catalog:{user_id}:{operation}"
```

---

## 📝 **MIDDLEWARE DE LOGGING UNIVERSAL**

### **Logger de Performance**

```python
# app/middleware/performance_logger.py
import time
import json
import logging
from fastapi import Request, Response
from typing import Dict, Any
import uuid

class PerformanceLoggingMiddleware:
    """Middleware de logging universal para performance"""

    def __init__(self, app):
        self.app = app
        self.logger = logging.getLogger("api_performance")

        # Configurar logger
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            request = Request(scope, receive)
            request_id = str(uuid.uuid4())[:8]
            start_time = time.time()

            # Log inicio de request
            await self._log_request_start(request, request_id)

            # Capturar response
            response_body = []
            response_status = None

            async def capture_response(message):
                nonlocal response_status
                if message["type"] == "http.response.start":
                    response_status = message["status"]
                elif message["type"] == "http.response.body":
                    response_body.append(message.get("body", b""))
                await send(message)

            await self.app(scope, receive, capture_response)

            # Log fin de request
            end_time = time.time()
            await self._log_request_end(
                request, request_id, start_time, end_time,
                response_status, response_body
            )
        else:
            await self.app(scope, receive, send)

    async def _log_request_start(self, request: Request, request_id: str):
        """Log inicio de request"""
        log_data = {
            "request_id": request_id,
            "event": "request_start",
            "method": request.method,
            "url": str(request.url),
            "user_agent": request.headers.get("user-agent"),
            "client_ip": request.client.host,
            "timestamp": time.time()
        }

        self.logger.info(f"REQUEST_START: {json.dumps(log_data)}")

    async def _log_request_end(
        self,
        request: Request,
        request_id: str,
        start_time: float,
        end_time: float,
        status_code: int,
        response_body: list
    ):
        """Log fin de request con métricas"""
        duration = (end_time - start_time) * 1000  # en ms
        response_size = sum(len(chunk) for chunk in response_body)

        log_data = {
            "request_id": request_id,
            "event": "request_end",
            "method": request.method,
            "url": str(request.url),
            "status_code": status_code,
            "duration_ms": round(duration, 2),
            "response_size_bytes": response_size,
            "timestamp": end_time
        }

        # Clasificar por performance
        if duration > 1000:  # > 1 segundo
            self.logger.warning(f"SLOW_REQUEST: {json.dumps(log_data)}")
        elif status_code >= 400:
            self.logger.error(f"ERROR_REQUEST: {json.dumps(log_data)}")
        else:
            self.logger.info(f"REQUEST_END: {json.dumps(log_data)}")
```

---

## 🧪 **TESTING DE MIDDLEWARE**

### **Tests de Rate Limiting**

```python
# tests/test_rate_limiting.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.middleware.rate_limiter import rate_limiter

@pytest.fixture
def client():
    return TestClient(app)

def test_rate_limit_basic(client):
    """Test básico de rate limiting"""
    # Hacer múltiples requests
    responses = []
    for i in range(5):
        response = client.get("/api/test-endpoint")
        responses.append(response)

    # Verificar headers de rate limit
    last_response = responses[-1]
    assert "X-RateLimit-Limit" in last_response.headers
    assert "X-RateLimit-Remaining" in last_response.headers

def test_rate_limit_exceeded(client):
    """Test de límite de rate excedido"""
    # Simular muchos requests rápidos
    for i in range(200):  # Exceder límite típico
        response = client.get("/api/test-endpoint")
        if response.status_code == 429:
            # Verificar respuesta de rate limit
            assert "Rate limit exceeded" in response.json()["error"]
            assert "Retry-After" in response.headers
            break
    else:
        pytest.fail("Rate limit not triggered")

async def test_rate_limiter_different_operations():
    """Test de diferentes tipos de operaciones"""
    # Test operación de lectura
    result_read = await rate_limiter.check_rate_limit(
        "test_user", "read_operations"
    )
    assert result_read["allowed"] == True

    # Test operación pesada
    result_heavy = await rate_limiter.check_rate_limit(
        "test_user", "heavy_operations"
    )
    assert result_heavy["allowed"] == True
    assert result_heavy["limit"] < result_read["limit"]  # Límite más bajo
```

---

## 🎯 **ENTREGABLES**

### **📋 Checklist de Implementación**

- [ ] **Rate limiter universal** configurado y funcionando
- [ ] **Middleware específico** para tu tipo (A/B/C/D) implementado
- [ ] **Logging de performance** registrando métricas
- [ ] **Headers informativos** agregados a responses
- [ ] **Tests de rate limiting** ejecutándose correctamente
- [ ] **Manejo de errores** implementado apropiadamente

### **📊 Métricas a Monitorear**

1. **Requests por minuto** por endpoint
2. **Rate limit hits** y patrones
3. **Performance de requests** (tiempo de respuesta)
4. **Distribución de tráfico** por tipos de operación

---

## 🚀 **SIGUIENTES PASOS**

Una vez completada esta práctica:

1. **📊 Analiza** los logs de performance generados
2. **🔧 Ajusta** los límites según patrones de uso
3. **🔄 Continúa** con la Práctica 26 (Monitoreo)

---

**PRÁCTICA 25 - MIDDLEWARE COMPLETADO**  
_Rate limiting y logging universales implementados_
