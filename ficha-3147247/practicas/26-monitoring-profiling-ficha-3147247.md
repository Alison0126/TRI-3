# Práctica 26: Monitoring y Profiling - FICHA 3147247

## 📊 **MONITOREO Y PROFILING UNIVERSAL**

> **🛡️ POLÍTICA ANTI-COPIA:** Esta práctica utiliza exclusivamente ejemplos genéricos tipo A/B/C/D para garantizar equidad educativa. Ver: [Política de Equidad](../../../_docs/POLITICA-EQUIDAD-EJEMPLOS.md)

---

## 🎯 **OBJETIVOS DE APRENDIZAJE**

Al finalizar esta práctica serás capaz de:

1. **📈 Implementar métricas** estándar de performance para APIs
2. **📊 Crear dashboards** informativos usando herramientas universales
3. **🔔 Configurar alertas** proactivas para problemas de performance
4. **🔍 Realizar profiling** detallado de aplicaciones FastAPI

---

## 🛠️ **SETUP DE MONITOREO**

### **📦 Dependencias para Monitoring**

```bash
# Instalar herramientas de monitoreo
pip install prometheus-client psutil py-spy memory-profiler
pip install grafana-api influxdb-client
```

### **📊 Sistema de Métricas Universal**

```python
# app/monitoring/metrics_collector.py
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from prometheus_client import CollectorRegistry, CONTENT_TYPE_LATEST
import psutil
import time
from typing import Dict, Any
import asyncio
from fastapi import Request, Response
from fastapi.responses import PlainTextResponse

class UniversalMetricsCollector:
    """Colector de métricas universal para cualquier tipo de API"""

    def __init__(self):
        self.registry = CollectorRegistry()

        # Métricas universales de API
        self.http_requests_total = Counter(
            'http_requests_total',
            'Total HTTP requests',
            ['method', 'endpoint', 'status_code'],
            registry=self.registry
        )

        self.http_request_duration = Histogram(
            'http_request_duration_seconds',
            'HTTP request duration in seconds',
            ['method', 'endpoint'],
            registry=self.registry
        )

        self.active_connections = Gauge(
            'active_connections',
            'Number of active connections',
            registry=self.registry
        )

        # Métricas de sistema
        self.cpu_usage = Gauge(
            'cpu_usage_percent',
            'CPU usage percentage',
            registry=self.registry
        )

        self.memory_usage = Gauge(
            'memory_usage_bytes',
            'Memory usage in bytes',
            registry=self.registry
        )

        self.disk_usage = Gauge(
            'disk_usage_percent',
            'Disk usage percentage',
            registry=self.registry
        )

        # Métricas específicas de aplicación
        self.cache_hits = Counter(
            'cache_hits_total',
            'Total cache hits',
            ['cache_type'],
            registry=self.registry
        )

        self.cache_misses = Counter(
            'cache_misses_total',
            'Total cache misses',
            ['cache_type'],
            registry=self.registry
        )

        self.database_queries = Counter(
            'database_queries_total',
            'Total database queries',
            ['query_type', 'table'],
            registry=self.registry
        )

        self.database_query_duration = Histogram(
            'database_query_duration_seconds',
            'Database query duration in seconds',
            ['query_type'],
            registry=self.registry
        )

        # Iniciar recolección de métricas de sistema
        self._start_system_metrics_collection()

    def _start_system_metrics_collection(self):
        """Iniciar recolección automática de métricas de sistema"""
        async def collect_system_metrics():
            while True:
                try:
                    # CPU
                    cpu_percent = psutil.cpu_percent(interval=1)
                    self.cpu_usage.set(cpu_percent)

                    # Memoria
                    memory = psutil.virtual_memory()
                    self.memory_usage.set(memory.used)

                    # Disco
                    disk = psutil.disk_usage('/')
                    self.disk_usage.set(disk.percent)

                except Exception as e:
                    print(f"Error collecting system metrics: {e}")

                await asyncio.sleep(10)  # Cada 10 segundos

        # Ejecutar en background
        asyncio.create_task(collect_system_metrics())

    def record_http_request(self, method: str, endpoint: str, status_code: int, duration: float):
        """Registrar request HTTP"""
        self.http_requests_total.labels(
            method=method,
            endpoint=endpoint,
            status_code=status_code
        ).inc()

        self.http_request_duration.labels(
            method=method,
            endpoint=endpoint
        ).observe(duration)

    def record_cache_hit(self, cache_type: str):
        """Registrar cache hit"""
        self.cache_hits.labels(cache_type=cache_type).inc()

    def record_cache_miss(self, cache_type: str):
        """Registrar cache miss"""
        self.cache_misses.labels(cache_type=cache_type).inc()

    def record_database_query(self, query_type: str, table: str, duration: float):
        """Registrar consulta de base de datos"""
        self.database_queries.labels(
            query_type=query_type,
            table=table
        ).inc()

        self.database_query_duration.labels(
            query_type=query_type
        ).observe(duration)

    def get_metrics(self) -> str:
        """Obtener métricas en formato Prometheus"""
        return generate_latest(self.registry)

# Instancia global
metrics_collector = UniversalMetricsCollector()
```

---

## 🎯 **MÉTRICAS POR TIPOS GENÉRICOS**

### **🅰️ TIPO A - Gestión de Datos**

#### **Métricas Específicas para Datos**

```python
# app/monitoring/tipo_a_metrics.py
from prometheus_client import Counter, Histogram, Gauge
from app.monitoring.metrics_collector import metrics_collector

class TipoAMetrics:
    """Métricas específicas para gestión de datos"""

    def __init__(self):
        # Métricas de registros
        self.registros_created = Counter(
            'registros_created_total',
            'Total registros creados',
            ['categoria']
        )

        self.registros_updated = Counter(
            'registros_updated_total',
            'Total registros actualizados',
            ['categoria']
        )

        self.registros_search_time = Histogram(
            'registros_search_duration_seconds',
            'Tiempo de búsqueda de registros',
            ['search_type']
        )

        # Métricas de configuración
        self.config_loads = Counter(
            'config_loads_total',
            'Total cargas de configuración'
        )

        self.active_registros = Gauge(
            'active_registros_count',
            'Número de registros activos',
            ['categoria']
        )

    def record_registro_created(self, categoria: str):
        """Registrar creación de registro"""
        self.registros_created.labels(categoria=categoria).inc()
        metrics_collector.record_database_query("INSERT", "registros", 0.1)

    def record_search_operation(self, search_type: str, duration: float):
        """Registrar operación de búsqueda"""
        self.registros_search_time.labels(search_type=search_type).observe(duration)

    def update_active_count(self, categoria: str, count: int):
        """Actualizar contador de registros activos"""
        self.active_registros.labels(categoria=categoria).set(count)

# Instancia para Tipo A
tipo_a_metrics = TipoAMetrics()
```

### **🅱️ TIPO B - Programación Temporal**

#### **Métricas para Operaciones Temporales**

```python
# app/monitoring/tipo_b_metrics.py
from prometheus_client import Counter, Histogram, Gauge
from datetime import datetime

class TipoBMetrics:
    """Métricas específicas para programación temporal"""

    def __init__(self):
        # Métricas de disponibilidad
        self.availability_checks = Counter(
            'availability_checks_total',
            'Total verificaciones de disponibilidad',
            ['resource_type']
        )

        self.reservations_created = Counter(
            'reservations_created_total',
            'Total reservas creadas',
            ['resource_type', 'status']
        )

        self.reservation_conflicts = Counter(
            'reservation_conflicts_total',
            'Total conflictos de reserva',
            ['conflict_type']
        )

        # Métricas de tiempo
        self.schedule_query_time = Histogram(
            'schedule_query_duration_seconds',
            'Tiempo de consulta de horarios',
            ['query_type']
        )

        # Gauge para recursos disponibles
        self.available_resources = Gauge(
            'available_resources_count',
            'Recursos disponibles por tipo',
            ['resource_type', 'time_slot']
        )

        self.peak_usage_hours = Gauge(
            'peak_usage_hours',
            'Horas de mayor uso',
            ['hour']
        )

    def record_availability_check(self, resource_type: str, duration: float):
        """Registrar verificación de disponibilidad"""
        self.availability_checks.labels(resource_type=resource_type).inc()
        self.schedule_query_time.labels(query_type="availability").observe(duration)

    def record_reservation(self, resource_type: str, status: str):
        """Registrar reserva"""
        self.reservations_created.labels(
            resource_type=resource_type,
            status=status
        ).inc()

    def record_conflict(self, conflict_type: str):
        """Registrar conflicto de programación"""
        self.reservation_conflicts.labels(conflict_type=conflict_type).inc()

    def update_availability(self, resource_type: str, time_slot: str, count: int):
        """Actualizar disponibilidad de recursos"""
        self.available_resources.labels(
            resource_type=resource_type,
            time_slot=time_slot
        ).set(count)

tipo_b_metrics = TipoBMetrics()
```

### **🅾️ TIPO C - Servicios de Usuario**

#### **Métricas de Servicios**

```python
# app/monitoring/tipo_c_metrics.py
from prometheus_client import Counter, Histogram, Gauge

class TipoCMetrics:
    """Métricas específicas para servicios de usuario"""

    def __init__(self):
        # Métricas de usuario
        self.user_logins = Counter(
            'user_logins_total',
            'Total logins de usuarios',
            ['user_tier']
        )

        self.service_requests = Counter(
            'service_requests_total',
            'Total solicitudes de servicio',
            ['service_type', 'user_tier']
        )

        self.profile_updates = Counter(
            'profile_updates_total',
            'Total actualizaciones de perfil',
            ['update_type']
        )

        # Métricas de performance de servicios
        self.service_response_time = Histogram(
            'service_response_duration_seconds',
            'Tiempo de respuesta de servicios',
            ['service_type']
        )

        # Métricas de estado
        self.active_users = Gauge(
            'active_users_count',
            'Usuarios activos',
            ['tier']
        )

        self.service_utilization = Gauge(
            'service_utilization_percent',
            'Utilización de servicios',
            ['service_type']
        )

    def record_user_login(self, user_tier: str):
        """Registrar login de usuario"""
        self.user_logins.labels(user_tier=user_tier).inc()

    def record_service_request(self, service_type: str, user_tier: str, duration: float):
        """Registrar solicitud de servicio"""
        self.service_requests.labels(
            service_type=service_type,
            user_tier=user_tier
        ).inc()

        self.service_response_time.labels(
            service_type=service_type
        ).observe(duration)

    def update_active_users(self, tier: str, count: int):
        """Actualizar usuarios activos"""
        self.active_users.labels(tier=tier).set(count)

tipo_c_metrics = TipoCMetrics()
```

### **🔷 TIPO D - Catálogo de Elementos**

#### **Métricas de Catálogo e Inventario**

```python
# app/monitoring/tipo_d_metrics.py
from prometheus_client import Counter, Histogram, Gauge

class TipoDMetrics:
    """Métricas específicas para catálogo de elementos"""

    def __init__(self):
        # Métricas de búsqueda
        self.catalog_searches = Counter(
            'catalog_searches_total',
            'Total búsquedas en catálogo',
            ['search_type', 'category']
        )

        self.search_results = Histogram(
            'search_results_count',
            'Número de resultados por búsqueda',
            ['category']
        )

        # Métricas de inventario
        self.inventory_checks = Counter(
            'inventory_checks_total',
            'Total verificaciones de inventario',
            ['check_type']
        )

        self.stock_updates = Counter(
            'stock_updates_total',
            'Total actualizaciones de stock',
            ['update_type', 'category']
        )

        # Métricas de performance
        self.search_duration = Histogram(
            'catalog_search_duration_seconds',
            'Duración de búsquedas en catálogo',
            ['complexity']
        )

        # Estado del inventario
        self.low_stock_items = Gauge(
            'low_stock_items_count',
            'Elementos con stock bajo',
            ['category']
        )

        self.total_catalog_items = Gauge(
            'total_catalog_items_count',
            'Total elementos en catálogo',
            ['category', 'status']
        )

        self.inventory_value = Gauge(
            'inventory_value_total',
            'Valor total del inventario',
            ['category']
        )

    def record_search(self, search_type: str, category: str, duration: float, results: int):
        """Registrar búsqueda en catálogo"""
        self.catalog_searches.labels(
            search_type=search_type,
            category=category
        ).inc()

        self.search_results.labels(category=category).observe(results)

        complexity = "simple" if results < 50 else "complex"
        self.search_duration.labels(complexity=complexity).observe(duration)

    def record_inventory_check(self, check_type: str):
        """Registrar verificación de inventario"""
        self.inventory_checks.labels(check_type=check_type).inc()

    def record_stock_update(self, update_type: str, category: str):
        """Registrar actualización de stock"""
        self.stock_updates.labels(
            update_type=update_type,
            category=category
        ).inc()

    def update_low_stock_count(self, category: str, count: int):
        """Actualizar contador de elementos con stock bajo"""
        self.low_stock_items.labels(category=category).set(count)

tipo_d_metrics = TipoDMetrics()
```

---

## 📊 **DASHBOARD UNIVERSAL**

### **Dashboard Web Simple**

```python
# app/monitoring/dashboard.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json
import asyncio
from app.monitoring.metrics_collector import metrics_collector

class UniversalDashboard:
    """Dashboard universal para monitoreo"""

    def __init__(self):
        self.templates = Jinja2Templates(directory="app/templates")

    async def get_dashboard_data(self) -> dict:
        """Obtener datos para el dashboard"""

        # Simular datos agregados (en producción usar TimeSeries DB)
        return {
            "system_health": {
                "cpu_usage": 45.2,
                "memory_usage": 67.8,
                "disk_usage": 23.1,
                "active_connections": 142
            },
            "api_performance": {
                "requests_per_minute": 1250,
                "avg_response_time": 89.5,
                "error_rate": 0.8,
                "cache_hit_rate": 78.2
            },
            "database_stats": {
                "queries_per_minute": 890,
                "avg_query_time": 45.3,
                "slow_queries": 3,
                "connections": 28
            },
            "alerts": [
                {
                    "level": "warning",
                    "message": "High CPU usage detected",
                    "timestamp": "2025-09-13T10:30:00Z"
                }
            ]
        }

    async def render_dashboard(self, request: Request) -> HTMLResponse:
        """Renderizar dashboard HTML"""
        data = await self.get_dashboard_data()

        return self.templates.TemplateResponse(
            "dashboard.html",
            {"request": request, "data": data}
        )

dashboard = UniversalDashboard()
```

### **Template de Dashboard**

```html
<!-- app/templates/dashboard.html -->
<!DOCTYPE html>
<html>
  <head>
    <title>API Performance Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
      body {
        font-family: Arial, sans-serif;
        margin: 20px;
      }
      .grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 20px;
      }
      .card {
        border: 1px solid #ddd;
        padding: 20px;
        border-radius: 8px;
      }
      .metric {
        font-size: 2em;
        font-weight: bold;
        color: #333;
      }
      .label {
        color: #666;
        margin-bottom: 5px;
      }
      .alert {
        padding: 10px;
        margin: 5px 0;
        border-radius: 4px;
      }
      .warning {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
      }
      .error {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
      }
    </style>
  </head>
  <body>
    <h1>API Performance Dashboard</h1>

    <div class="grid">
      <!-- Sistema -->
      <div class="card">
        <h3>System Health</h3>
        <div class="label">CPU Usage</div>
        <div class="metric">{{ data.system_health.cpu_usage }}%</div>

        <div class="label">Memory Usage</div>
        <div class="metric">{{ data.system_health.memory_usage }}%</div>

        <div class="label">Active Connections</div>
        <div class="metric">{{ data.system_health.active_connections }}</div>
      </div>

      <!-- API Performance -->
      <div class="card">
        <h3>API Performance</h3>
        <div class="label">Requests/min</div>
        <div class="metric">{{ data.api_performance.requests_per_minute }}</div>

        <div class="label">Avg Response Time</div>
        <div class="metric">{{ data.api_performance.avg_response_time }}ms</div>

        <div class="label">Cache Hit Rate</div>
        <div class="metric">{{ data.api_performance.cache_hit_rate }}%</div>
      </div>

      <!-- Database -->
      <div class="card">
        <h3>Database Stats</h3>
        <div class="label">Queries/min</div>
        <div class="metric">{{ data.database_stats.queries_per_minute }}</div>

        <div class="label">Avg Query Time</div>
        <div class="metric">{{ data.database_stats.avg_query_time }}ms</div>

        <div class="label">Slow Queries</div>
        <div class="metric">{{ data.database_stats.slow_queries }}</div>
      </div>

      <!-- Alertas -->
      <div class="card">
        <h3>Recent Alerts</h3>
        {% for alert in data.alerts %}
        <div class="alert {{ alert.level }}">
          <strong>{{ alert.level.upper() }}:</strong> {{ alert.message }}
          <br /><small>{{ alert.timestamp }}</small>
        </div>
        {% endfor %}
      </div>
    </div>

    <!-- Gráfico de Performance -->
    <div style="margin-top: 30px;">
      <canvas
        id="performanceChart"
        width="400"
        height="200"></canvas>
    </div>

    <script>
      // Gráfico de performance en tiempo real
      const ctx = document.getElementById('performanceChart').getContext('2d');
      const chart = new Chart(ctx, {
          type: 'line',
          data: {
              labels: ['5min ago', '4min ago', '3min ago', '2min ago', '1min ago', 'Now'],
              datasets: [{
                  label: 'Response Time (ms)',
                  data: [95, 89, 87, 92, 85, {{ data.api_performance.avg_response_time }}],
                  borderColor: 'rgb(75, 192, 192)',
                  tension: 0.1
              }]
          },
          options: {
              responsive: true,
              scales: {
                  y: {
                      beginAtZero: true
                  }
              }
          }
      });

      // Auto-refresh cada 30 segundos
      setTimeout(() => {
          location.reload();
      }, 30000);
    </script>
  </body>
</html>
```

---

## 🔔 **SISTEMA DE ALERTAS**

### **Alertas Automatizadas**

```python
# app/monitoring/alerts.py
import asyncio
import smtplib
from email.mime.text import MIMEText
from typing import List, Dict, Any
import json
from datetime import datetime
from app.monitoring.metrics_collector import metrics_collector

class AlertManager:
    """Sistema de alertas universal"""

    def __init__(self):
        self.alert_rules = {
            "high_cpu": {"threshold": 80, "duration": 300},  # 80% por 5 min
            "high_memory": {"threshold": 85, "duration": 300},
            "slow_response": {"threshold": 1000, "duration": 180},  # 1s por 3 min
            "high_error_rate": {"threshold": 5, "duration": 120},  # 5% por 2 min
            "low_cache_hit": {"threshold": 50, "duration": 600}  # <50% por 10 min
        }

        self.active_alerts = {}
        self.alert_history = []

    async def start_monitoring(self):
        """Iniciar monitoreo de alertas"""
        while True:
            try:
                await self._check_all_rules()
                await asyncio.sleep(30)  # Verificar cada 30 segundos
            except Exception as e:
                print(f"Error in alert monitoring: {e}")

    async def _check_all_rules(self):
        """Verificar todas las reglas de alerta"""

        # Obtener métricas actuales (simulado)
        current_metrics = await self._get_current_metrics()

        # Verificar cada regla
        for rule_name, rule_config in self.alert_rules.items():
            await self._check_rule(rule_name, rule_config, current_metrics)

    async def _get_current_metrics(self) -> Dict[str, float]:
        """Obtener métricas actuales (simulado)"""
        import psutil
        import random

        return {
            "cpu_usage": psutil.cpu_percent(),
            "memory_usage": psutil.virtual_memory().percent,
            "avg_response_time": random.uniform(50, 200),  # Simular
            "error_rate": random.uniform(0, 3),  # Simular
            "cache_hit_rate": random.uniform(60, 90)  # Simular
        }

    async def _check_rule(self, rule_name: str, rule_config: Dict, metrics: Dict):
        """Verificar regla específica"""

        threshold = rule_config["threshold"]
        duration = rule_config["duration"]

        # Lógica específica por tipo de alerta
        triggered = False
        current_value = 0

        if rule_name == "high_cpu":
            current_value = metrics["cpu_usage"]
            triggered = current_value > threshold

        elif rule_name == "high_memory":
            current_value = metrics["memory_usage"]
            triggered = current_value > threshold

        elif rule_name == "slow_response":
            current_value = metrics["avg_response_time"]
            triggered = current_value > threshold

        elif rule_name == "high_error_rate":
            current_value = metrics["error_rate"]
            triggered = current_value > threshold

        elif rule_name == "low_cache_hit":
            current_value = metrics["cache_hit_rate"]
            triggered = current_value < threshold

        # Manejar estado de alerta
        if triggered:
            await self._handle_alert_triggered(rule_name, current_value, threshold)
        else:
            await self._handle_alert_resolved(rule_name)

    async def _handle_alert_triggered(self, rule_name: str, current_value: float, threshold: float):
        """Manejar alerta activada"""

        now = datetime.now()

        if rule_name not in self.active_alerts:
            # Nueva alerta
            self.active_alerts[rule_name] = {
                "start_time": now,
                "current_value": current_value,
                "threshold": threshold
            }

            alert = {
                "rule": rule_name,
                "level": self._get_alert_level(rule_name),
                "message": f"{rule_name.replace('_', ' ').title()}: {current_value:.2f} (threshold: {threshold})",
                "timestamp": now.isoformat(),
                "value": current_value,
                "threshold": threshold
            }

            await self._send_alert(alert)
            self.alert_history.append(alert)
        else:
            # Actualizar alerta existente
            self.active_alerts[rule_name]["current_value"] = current_value

    async def _handle_alert_resolved(self, rule_name: str):
        """Manejar alerta resuelta"""

        if rule_name in self.active_alerts:
            resolved_alert = {
                "rule": rule_name,
                "level": "info",
                "message": f"{rule_name.replace('_', ' ').title()} resolved",
                "timestamp": datetime.now().isoformat(),
                "duration": str(datetime.now() - self.active_alerts[rule_name]["start_time"])
            }

            await self._send_alert(resolved_alert)
            self.alert_history.append(resolved_alert)

            del self.active_alerts[rule_name]

    def _get_alert_level(self, rule_name: str) -> str:
        """Obtener nivel de alerta"""
        critical_rules = ["high_cpu", "high_memory"]
        warning_rules = ["slow_response", "high_error_rate"]

        if rule_name in critical_rules:
            return "critical"
        elif rule_name in warning_rules:
            return "warning"
        else:
            return "info"

    async def _send_alert(self, alert: Dict):
        """Enviar alerta (implementar según necesidades)"""

        # Log de alerta
        print(f"ALERT [{alert['level'].upper()}]: {alert['message']}")

        # Aquí implementar envío por email, Slack, webhook, etc.
        # await self._send_email_alert(alert)
        # await self._send_webhook_alert(alert)

    def get_alert_status(self) -> Dict:
        """Obtener estado actual de alertas"""
        return {
            "active_alerts": self.active_alerts,
            "recent_history": self.alert_history[-10:],  # Últimas 10
            "total_active": len(self.active_alerts)
        }

# Instancia global
alert_manager = AlertManager()
```

---

## 🔍 **PROFILING AVANZADO**

### **Profiler de Performance**

```python
# app/monitoring/profiler.py
import cProfile
import pstats
import io
from functools import wraps
import time
import tracemalloc
from typing import Dict, Any, Callable
import asyncio

class PerformanceProfiler:
    """Profiler universal para análisis detallado"""

    def __init__(self):
        self.profiles = {}
        self.memory_snapshots = {}
        tracemalloc.start()

    def profile_function(self, func_name: str = None):
        """Decorador para profiling de funciones"""
        def decorator(func: Callable):
            name = func_name or f"{func.__module__}.{func.__name__}"

            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                # Profiling de CPU
                profiler = cProfile.Profile()

                # Memory snapshot inicial
                snapshot1 = tracemalloc.take_snapshot()
                start_time = time.time()

                profiler.enable()
                try:
                    if asyncio.iscoroutinefunction(func):
                        result = await func(*args, **kwargs)
                    else:
                        result = func(*args, **kwargs)
                finally:
                    profiler.disable()

                end_time = time.time()
                snapshot2 = tracemalloc.take_snapshot()

                # Guardar resultados
                await self._save_profile_results(
                    name, profiler, snapshot1, snapshot2,
                    end_time - start_time
                )

                return result

            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                # Versión síncrona
                name = func_name or f"{func.__module__}.{func.__name__}"
                profiler = cProfile.Profile()

                snapshot1 = tracemalloc.take_snapshot()
                start_time = time.time()

                profiler.enable()
                try:
                    result = func(*args, **kwargs)
                finally:
                    profiler.disable()

                end_time = time.time()
                snapshot2 = tracemalloc.take_snapshot()

                # Guardar resultados (versión síncrona)
                asyncio.create_task(self._save_profile_results(
                    name, profiler, snapshot1, snapshot2,
                    end_time - start_time
                ))

                return result

            if asyncio.iscoroutinefunction(func):
                return async_wrapper
            else:
                return sync_wrapper

        return decorator

    async def _save_profile_results(
        self,
        name: str,
        profiler: cProfile.Profile,
        snapshot1,
        snapshot2,
        duration: float
    ):
        """Guardar resultados del profiling"""

        # Análisis de CPU
        s = io.StringIO()
        ps = pstats.Stats(profiler, stream=s)
        ps.sort_stats('cumulative')
        ps.print_stats(20)  # Top 20 funciones

        # Análisis de memoria
        top_stats = snapshot2.compare_to(snapshot1, 'lineno')
        memory_growth = sum(stat.size_diff for stat in top_stats[:10])

        self.profiles[name] = {
            "duration": duration,
            "cpu_profile": s.getvalue(),
            "memory_growth": memory_growth,
            "timestamp": time.time(),
            "top_memory_stats": [
                {
                    "file": stat.traceback.format()[0] if stat.traceback.format() else "unknown",
                    "size_diff": stat.size_diff,
                    "count_diff": stat.count_diff
                }
                for stat in top_stats[:5]
            ]
        }

    def get_profile_report(self, function_name: str = None) -> Dict[str, Any]:
        """Obtener reporte de profiling"""

        if function_name:
            return self.profiles.get(function_name, {})

        # Reporte general
        total_functions = len(self.profiles)

        if total_functions == 0:
            return {"message": "No profile data available"}

        # Funciones más lentas
        slowest = sorted(
            self.profiles.items(),
            key=lambda x: x[1]["duration"],
            reverse=True
        )[:5]

        # Funciones con mayor uso de memoria
        memory_intensive = sorted(
            self.profiles.items(),
            key=lambda x: x[1]["memory_growth"],
            reverse=True
        )[:5]

        return {
            "total_functions_profiled": total_functions,
            "slowest_functions": [
                {"name": name, "duration": data["duration"]}
                for name, data in slowest
            ],
            "memory_intensive_functions": [
                {"name": name, "memory_growth": data["memory_growth"]}
                for name, data in memory_intensive
            ],
            "detailed_profiles": {
                name: data for name, data in self.profiles.items()
            }
        }

# Instancia global
profiler = PerformanceProfiler()
```

---

## 🧪 **TESTING DE MONITOREO**

### **Tests de Métricas**

```python
# tests/test_monitoring.py
import pytest
from app.monitoring.metrics_collector import metrics_collector
from app.monitoring.alerts import alert_manager

def test_metrics_collection():
    """Test recolección básica de métricas"""

    # Simular request HTTP
    metrics_collector.record_http_request("GET", "/api/test", 200, 0.1)

    # Verificar que se registró
    metrics_output = metrics_collector.get_metrics()
    assert "http_requests_total" in metrics_output
    assert "http_request_duration_seconds" in metrics_output

def test_cache_metrics():
    """Test métricas de cache"""

    # Registrar hit y miss
    metrics_collector.record_cache_hit("redis")
    metrics_collector.record_cache_miss("redis")

    # Verificar métricas
    metrics_output = metrics_collector.get_metrics()
    assert "cache_hits_total" in metrics_output
    assert "cache_misses_total" in metrics_output

async def test_alert_system():
    """Test sistema básico de alertas"""

    # Simular condición de alerta
    test_metrics = {
        "cpu_usage": 90,  # Alto
        "memory_usage": 50,
        "avg_response_time": 100,
        "error_rate": 1,
        "cache_hit_rate": 80
    }

    # Verificar detección de alerta
    # En un test real, verificarías que se genere la alerta apropiada
    assert test_metrics["cpu_usage"] > 80  # Debería generar alerta
```

---

## 🎯 **ENTREGABLES**

### **📋 Checklist de Monitoreo**

- [ ] **Sistema de métricas** implementado y recolectando datos
- [ ] **Dashboard web** funcionando y mostrando métricas
- [ ] **Alertas automáticas** configuradas y probadas
- [ ] **Profiling de funciones** críticas implementado
- [ ] **Métricas específicas** para tu tipo (A/B/C/D) funcionando
- [ ] **Tests de monitoreo** ejecutándose correctamente

### **📊 Métricas Clave a Monitorear**

1. **Performance API:** Tiempo respuesta, throughput, errores
2. **Sistema:** CPU, memoria, disco, conexiones
3. **Base de datos:** Queries/min, tiempo promedio, consultas lentas
4. **Cache:** Hit rate, miss rate, memoria utilizada
5. **Tipo específico:** Métricas relevantes para A/B/C/D

---

## 🚀 **INTEGRACIÓN FINAL**

Una vez completadas todas las prácticas:

1. **📊 Dashboard completo** mostrando todas las métricas
2. **🔔 Alertas configuradas** para todos los componentes
3. **📈 Reporte de performance** documentando mejoras
4. **🎯 API optimizada** con monitoreo integral

---

**PRÁCTICA 26 - MONITORING COMPLETADO**  
_Sistema de monitoreo universal implementado_

**SEMANA 7 - FICHA 3147247 COMPLETADA**  
_Todas las prácticas de optimización finalizadas_
