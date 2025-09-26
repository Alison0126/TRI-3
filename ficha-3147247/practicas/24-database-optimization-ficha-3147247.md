# Práctica 24: Optimización de Base de Datos - FICHA 3147247

## 🗃️ **OPTIMIZACIÓN UNIVERSAL DE BASE DE DATOS**

> **🛡️ POLÍTICA ANTI-COPIA:** Esta práctica utiliza exclusivamente ejemplos genéricos tipo A/B/C/D para garantizar equidad educativa. Ver: [Política de Equidad](../../../_docs/POLITICA-EQUIDAD-EJEMPLOS.md)

---

## 🎯 **OBJETIVOS DE APRENDIZAJE**

Al finalizar esta práctica serás capaz de:

1. **📊 Analizar performance** de consultas con herramientas estándar
2. **🔍 Crear índices** estratégicos para optimización universal
3. **⚡ Optimizar queries** usando técnicas comprobadas
4. **📈 Medir mejoras** con métricas objetivas

---

## 🔧 **ANÁLISIS DE PERFORMANCE**

### **🔍 Herramientas de Diagnóstico**

```python
# app/db/performance_analyzer.py
import time
import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, List, Any
import logging

class DatabasePerformanceAnalyzer:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.query_log = []

    async def analyze_slow_queries(self, threshold_ms: float = 100) -> List[Dict]:
        """Identificar consultas lentas usando threshold universal"""

        # Habilitar log de consultas lentas (PostgreSQL)
        await self.session.execute(text("""
            SET log_min_duration_statement = :threshold
        """), {"threshold": threshold_ms})

        # Para SQLite (desarrollo)
        if "sqlite" in str(self.session.bind.url):
            return await self._analyze_sqlite_queries()

        # Para PostgreSQL (producción)
        return await self._analyze_postgres_queries()

    async def _analyze_postgres_queries(self) -> List[Dict]:
        """Análisis específico para PostgreSQL"""
        result = await self.session.execute(text("""
            SELECT
                query,
                mean_exec_time,
                calls,
                total_exec_time,
                rows
            FROM pg_stat_statements
            WHERE mean_exec_time > 100
            ORDER BY mean_exec_time DESC
            LIMIT 10
        """))

        return [dict(row) for row in result]

    async def _analyze_sqlite_queries(self) -> List[Dict]:
        """Análisis para SQLite (desarrollo)"""
        # Simular análisis para desarrollo
        return [
            {
                "query": "SELECT * FROM entidades WHERE campo LIKE '%valor%'",
                "mean_exec_time": 150.5,
                "suggestion": "Agregar índice en 'campo'"
            }
        ]

    async def measure_query_performance(self, query: str, params: Dict = None) -> Dict:
        """Medir performance de consulta específica"""
        start_time = time.time()

        result = await self.session.execute(text(query), params or {})
        rows = result.fetchall()

        end_time = time.time()
        execution_time = (end_time - start_time) * 1000  # en ms

        return {
            "query": query,
            "execution_time_ms": execution_time,
            "rows_returned": len(rows),
            "params": params
        }
```

---

## 🎯 **ÍNDICES POR TIPOS GENÉRICOS**

### **🅰️ TIPO A - Gestión de Datos**

#### **Modelos Optimizados para Tipo A**

```python
# app/models/tipo_a_optimized.py
from sqlalchemy import Column, Integer, String, DateTime, Text, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class RegistroPrincipal(Base):
    __tablename__ = "registros_principales"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    codigo = Column(String(50), unique=True, index=True)  # Índice único
    categoria = Column(String(100), index=True)  # Búsquedas por categoría
    estado = Column(String(50), index=True)  # Filtros por estado
    fecha_creacion = Column(DateTime, default=func.now(), index=True)  # Ordenamiento temporal
    fecha_actualizacion = Column(DateTime, default=func.now(), onupdate=func.now())
    descripcion = Column(Text)
    metadatos = Column(Text)  # JSON data

    # Índices compuestos para Tipo A
    __table_args__ = (
        # Búsquedas por categoría y estado
        Index('idx_categoria_estado', 'categoria', 'estado'),
        # Búsquedas temporales con estado
        Index('idx_fecha_estado', 'fecha_creacion', 'estado'),
        # Búsquedas por código y categoría
        Index('idx_codigo_categoria', 'codigo', 'categoria'),
        # Índice para paginación eficiente
        Index('idx_id_fecha', 'id', 'fecha_creacion'),
    )

class ConfiguracionSistema(Base):
    __tablename__ = "configuraciones_sistema"

    id = Column(Integer, primary_key=True)
    clave = Column(String(100), unique=True, index=True)
    valor = Column(Text)
    grupo = Column(String(50), index=True)  # Agrupación de configs
    activo = Column(String(10), default="true", index=True)

    __table_args__ = (
        Index('idx_grupo_activo', 'grupo', 'activo'),
    )
```

#### **Consultas Optimizadas Tipo A**

```python
# app/db/queries_tipo_a.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, desc
from sqlalchemy.orm import selectinload
from app.models.tipo_a_optimized import RegistroPrincipal, ConfiguracionSistema
from typing import List, Optional, Dict

class TipoAQueries:

    @staticmethod
    async def get_registros_by_categoria_optimized(
        session: AsyncSession,
        categoria: str,
        estado: str = "activo",
        limit: int = 50,
        offset: int = 0
    ) -> List[RegistroPrincipal]:
        """Consulta optimizada con índice compuesto categoria_estado"""

        query = select(RegistroPrincipal).where(
            and_(
                RegistroPrincipal.categoria == categoria,
                RegistroPrincipal.estado == estado
            )
        ).order_by(desc(RegistroPrincipal.fecha_creacion)).limit(limit).offset(offset)

        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def search_registros_optimized(
        session: AsyncSession,
        search_term: str,
        categoria: Optional[str] = None
    ) -> List[RegistroPrincipal]:
        """Búsqueda optimizada con índices apropiados"""

        query = select(RegistroPrincipal)

        # Usar índice en nombre para búsquedas exactas
        conditions = [RegistroPrincipal.nombre.ilike(f"{search_term}%")]

        if categoria:
            # Usar índice compuesto codigo_categoria
            conditions.append(RegistroPrincipal.categoria == categoria)

        query = query.where(and_(*conditions)).limit(100)

        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_registros_recientes_optimized(
        session: AsyncSession,
        days: int = 7
    ) -> List[RegistroPrincipal]:
        """Consulta temporal optimizada con índice fecha_estado"""
        from datetime import datetime, timedelta

        fecha_limite = datetime.now() - timedelta(days=days)

        query = select(RegistroPrincipal).where(
            and_(
                RegistroPrincipal.fecha_creacion >= fecha_limite,
                RegistroPrincipal.estado == "activo"
            )
        ).order_by(desc(RegistroPrincipal.fecha_creacion))

        result = await session.execute(query)
        return result.scalars().all()
```

### **🅱️ TIPO B - Programación Temporal**

#### **Modelos Optimizados para Tipo B**

```python
# app/models/tipo_b_optimized.py
from sqlalchemy import Column, Integer, String, DateTime, Date, Time, Boolean, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class RecursoTemporal(Base):
    __tablename__ = "recursos_temporales"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False, index=True)
    tipo = Column(String(100), index=True)
    capacidad = Column(Integer)
    estado = Column(String(50), index=True)
    ubicacion = Column(String(255), index=True)

    # Índices para búsquedas de recursos
    __table_args__ = (
        Index('idx_tipo_estado', 'tipo', 'estado'),
        Index('idx_ubicacion_tipo', 'ubicacion', 'tipo'),
    )

class DisponibilidadRecurso(Base):
    __tablename__ = "disponibilidad_recursos"

    id = Column(Integer, primary_key=True)
    recurso_id = Column(Integer, index=True)  # FK
    fecha = Column(Date, index=True)
    hora_inicio = Column(Time, index=True)
    hora_fin = Column(Time, index=True)
    disponible = Column(Boolean, default=True, index=True)
    capacidad_disponible = Column(Integer)

    # Índices críticos para consultas temporales
    __table_args__ = (
        # Búsqueda por recurso y fecha
        Index('idx_recurso_fecha', 'recurso_id', 'fecha'),
        # Búsqueda de disponibilidad por fecha
        Index('idx_fecha_disponible', 'fecha', 'disponible'),
        # Búsqueda por rango de horas
        Index('idx_fecha_hora', 'fecha', 'hora_inicio', 'hora_fin'),
        # Índice compuesto para consultas complejas
        Index('idx_recurso_fecha_disp', 'recurso_id', 'fecha', 'disponible'),
    )

class ReservaTemporal(Base):
    __tablename__ = "reservas_temporales"

    id = Column(Integer, primary_key=True)
    recurso_id = Column(Integer, index=True)
    fecha_reserva = Column(Date, index=True)
    hora_inicio = Column(Time)
    hora_fin = Column(Time)
    estado = Column(String(50), index=True)
    usuario_id = Column(Integer, index=True)
    fecha_creacion = Column(DateTime, default=func.now())

    __table_args__ = (
        Index('idx_recurso_fecha_reserva', 'recurso_id', 'fecha_reserva'),
        Index('idx_usuario_fecha', 'usuario_id', 'fecha_reserva'),
        Index('idx_estado_fecha', 'estado', 'fecha_reserva'),
    )
```

#### **Consultas Optimizadas Tipo B**

```python
# app/db/queries_tipo_b.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, between, func
from datetime import datetime, date, time
from typing import List, Dict
from app.models.tipo_b_optimized import RecursoTemporal, DisponibilidadRecurso, ReservaTemporal

class TipoBQueries:

    @staticmethod
    async def get_disponibilidad_fecha_optimized(
        session: AsyncSession,
        fecha: date,
        tipo_recurso: Optional[str] = None
    ) -> List[Dict]:
        """Consulta optimizada de disponibilidad por fecha"""

        query = select(
            DisponibilidadRecurso.recurso_id,
            DisponibilidadRecurso.hora_inicio,
            DisponibilidadRecurso.hora_fin,
            DisponibilidadRecurso.capacidad_disponible,
            RecursoTemporal.nombre,
            RecursoTemporal.tipo
        ).join(RecursoTemporal).where(
            and_(
                DisponibilidadRecurso.fecha == fecha,
                DisponibilidadRecurso.disponible == True
            )
        )

        if tipo_recurso:
            query = query.where(RecursoTemporal.tipo == tipo_recurso)

        query = query.order_by(DisponibilidadRecurso.hora_inicio)

        result = await session.execute(query)
        return [dict(row) for row in result]

    @staticmethod
    async def check_conflictos_reserva_optimized(
        session: AsyncSession,
        recurso_id: int,
        fecha: date,
        hora_inicio: time,
        hora_fin: time
    ) -> bool:
        """Verificar conflictos usando índices temporales"""

        query = select(func.count(ReservaTemporal.id)).where(
            and_(
                ReservaTemporal.recurso_id == recurso_id,
                ReservaTemporal.fecha_reserva == fecha,
                ReservaTemporal.estado == "confirmada",
                or_(
                    # Solapamiento de horarios
                    and_(
                        ReservaTemporal.hora_inicio <= hora_inicio,
                        ReservaTemporal.hora_fin > hora_inicio
                    ),
                    and_(
                        ReservaTemporal.hora_inicio < hora_fin,
                        ReservaTemporal.hora_fin >= hora_fin
                    ),
                    and_(
                        ReservaTemporal.hora_inicio >= hora_inicio,
                        ReservaTemporal.hora_fin <= hora_fin
                    )
                )
            )
        )

        result = await session.execute(query)
        count = result.scalar()
        return count > 0

    @staticmethod
    async def get_reservas_periodo_optimized(
        session: AsyncSession,
        fecha_inicio: date,
        fecha_fin: date,
        recurso_id: Optional[int] = None
    ) -> List[ReservaTemporal]:
        """Consulta optimizada de reservas por período"""

        query = select(ReservaTemporal).where(
            between(ReservaTemporal.fecha_reserva, fecha_inicio, fecha_fin)
        )

        if recurso_id:
            query = query.where(ReservaTemporal.recurso_id == recurso_id)

        query = query.order_by(
            ReservaTemporal.fecha_reserva,
            ReservaTemporal.hora_inicio
        )

        result = await session.execute(query)
        return result.scalars().all()
```

### **🅾️ TIPO C - Servicios de Usuario**

#### **Modelos Optimizados para Tipo C**

```python
# app/models/tipo_c_optimized.py
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Index, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class PerfilUsuario(Base):
    __tablename__ = "perfiles_usuarios"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, unique=True, index=True)  # FK
    nombre = Column(String(255), index=True)
    email = Column(String(255), unique=True, index=True)
    tipo_usuario = Column(String(50), index=True)
    estado = Column(String(50), index=True)
    fecha_registro = Column(DateTime, default=func.now(), index=True)
    ultimo_acceso = Column(DateTime, index=True)
    preferencias = Column(JSON)  # Configuraciones personalizadas

    __table_args__ = (
        Index('idx_tipo_estado', 'tipo_usuario', 'estado'),
        Index('idx_email_estado', 'email', 'estado'),
        Index('idx_ultimo_acceso', 'ultimo_acceso'),
    )

class ServicioUsuario(Base):
    __tablename__ = "servicios_usuarios"

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, index=True)
    servicio_tipo = Column(String(100), index=True)
    servicio_id = Column(Integer, index=True)
    estado = Column(String(50), index=True)
    fecha_asignacion = Column(DateTime, default=func.now(), index=True)
    fecha_vencimiento = Column(DateTime, index=True)
    parametros = Column(JSON)
    activo = Column(Boolean, default=True, index=True)

    __table_args__ = (
        # Búsqueda por usuario y tipo de servicio
        Index('idx_usuario_tipo', 'usuario_id', 'servicio_tipo'),
        # Servicios activos por usuario
        Index('idx_usuario_activo', 'usuario_id', 'activo'),
        # Servicios por vencer
        Index('idx_vencimiento_activo', 'fecha_vencimiento', 'activo'),
        # Búsqueda por servicio específico
        Index('idx_servicio_tipo_id', 'servicio_tipo', 'servicio_id'),
    )

class ActividadUsuario(Base):
    __tablename__ = "actividades_usuarios"

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, index=True)
    tipo_actividad = Column(String(100), index=True)
    descripcion = Column(Text)
    timestamp = Column(DateTime, default=func.now(), index=True)
    metadata = Column(JSON)

    __table_args__ = (
        Index('idx_usuario_timestamp', 'usuario_id', 'timestamp'),
        Index('idx_tipo_timestamp', 'tipo_actividad', 'timestamp'),
    )
```

### **🔷 TIPO D - Catálogo de Elementos**

#### **Modelos Optimizados para Tipo D**

```python
# app/models/tipo_d_optimized.py
from sqlalchemy import Column, Integer, String, Numeric, DateTime, Text, Index, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class ElementoCatalogo(Base):
    __tablename__ = "elementos_catalogo"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(50), unique=True, index=True)
    nombre = Column(String(255), index=True)
    categoria = Column(String(100), index=True)
    subcategoria = Column(String(100), index=True)
    precio = Column(Numeric(10, 2), index=True)
    estado = Column(String(50), index=True)
    fecha_creacion = Column(DateTime, default=func.now())
    fecha_actualizacion = Column(DateTime, default=func.now(), onupdate=func.now())
    descripcion = Column(Text)
    activo = Column(Boolean, default=True, index=True)

    # Índices para búsquedas de catálogo
    __table_args__ = (
        # Búsqueda por categoría y estado
        Index('idx_categoria_estado', 'categoria', 'estado'),
        # Búsqueda por rango de precios
        Index('idx_precio_categoria', 'precio', 'categoria'),
        # Búsqueda jerárquica
        Index('idx_cat_subcat', 'categoria', 'subcategoria'),
        # Elementos activos por categoría
        Index('idx_categoria_activo', 'categoria', 'activo'),
        # Búsqueda de texto en nombre
        Index('idx_nombre_activo', 'nombre', 'activo'),
    )

class InventarioElemento(Base):
    __tablename__ = "inventario_elementos"

    id = Column(Integer, primary_key=True)
    elemento_id = Column(Integer, index=True)  # FK
    stock_actual = Column(Integer, index=True)
    stock_minimo = Column(Integer)
    stock_maximo = Column(Integer)
    ubicacion = Column(String(100), index=True)
    lote = Column(String(50), index=True)
    fecha_ultima_actualizacion = Column(DateTime, default=func.now(), index=True)

    __table_args__ = (
        # Consultas de stock
        Index('idx_elemento_stock', 'elemento_id', 'stock_actual'),
        # Elementos con stock bajo
        Index('idx_stock_minimo', 'stock_actual', 'stock_minimo'),
        # Búsqueda por ubicación
        Index('idx_ubicacion_elemento', 'ubicacion', 'elemento_id'),
    )

class TransaccionInventario(Base):
    __tablename__ = "transacciones_inventario"

    id = Column(Integer, primary_key=True)
    elemento_id = Column(Integer, index=True)
    tipo_transaccion = Column(String(50), index=True)  # entrada, salida, ajuste
    cantidad = Column(Integer)
    stock_anterior = Column(Integer)
    stock_nuevo = Column(Integer, index=True)
    fecha_transaccion = Column(DateTime, default=func.now(), index=True)
    usuario_id = Column(Integer, index=True)
    referencia = Column(String(100), index=True)

    __table_args__ = (
        Index('idx_elemento_fecha', 'elemento_id', 'fecha_transaccion'),
        Index('idx_tipo_fecha', 'tipo_transaccion', 'fecha_transaccion'),
        Index('idx_usuario_fecha', 'usuario_id', 'fecha_transaccion'),
    )
```

---

## 📊 **HERRAMIENTAS DE MONITOREO**

### **Monitor de Performance de Consultas**

```python
# app/db/query_monitor.py
import time
import asyncio
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine.events import event
from sqlalchemy import text
import logging

class QueryPerformanceMonitor:

    def __init__(self):
        self.slow_queries = []
        self.query_stats = {}
        self.threshold_ms = 100

    @asynccontextmanager
    async def monitor_query(self, query_name: str):
        """Context manager para monitorear performance de consultas"""
        start_time = time.time()
        try:
            yield
        finally:
            execution_time = (time.time() - start_time) * 1000

            if execution_time > self.threshold_ms:
                self.slow_queries.append({
                    "query": query_name,
                    "execution_time_ms": execution_time,
                    "timestamp": time.time()
                })

            # Actualizar estadísticas
            if query_name not in self.query_stats:
                self.query_stats[query_name] = {
                    "count": 0,
                    "total_time": 0,
                    "avg_time": 0,
                    "max_time": 0
                }

            stats = self.query_stats[query_name]
            stats["count"] += 1
            stats["total_time"] += execution_time
            stats["avg_time"] = stats["total_time"] / stats["count"]
            stats["max_time"] = max(stats["max_time"], execution_time)

    async def get_performance_report(self) -> dict:
        """Generar reporte de performance"""
        return {
            "slow_queries": self.slow_queries[-10:],  # Últimas 10
            "query_stats": self.query_stats,
            "recommendations": self._generate_recommendations()
        }

    def _generate_recommendations(self) -> list:
        """Generar recomendaciones de optimización"""
        recommendations = []

        for query, stats in self.query_stats.items():
            if stats["avg_time"] > self.threshold_ms:
                recommendations.append({
                    "query": query,
                    "issue": f"Tiempo promedio alto: {stats['avg_time']:.2f}ms",
                    "suggestion": "Considerar agregar índices o optimizar consulta"
                })

        return recommendations

# Instancia global
query_monitor = QueryPerformanceMonitor()
```

---

## 🧪 **TESTING DE OPTIMIZACIONES**

### **Tests de Performance**

```python
# tests/test_db_performance.py
import pytest
import time
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.queries_tipo_a import TipoAQueries
from app.db.performance_analyzer import DatabasePerformanceAnalyzer

@pytest.fixture
async def performance_analyzer(db_session: AsyncSession):
    return DatabasePerformanceAnalyzer(db_session)

async def test_consulta_optimizada_vs_no_optimizada(db_session: AsyncSession):
    """Comparar performance de consultas optimizadas vs no optimizadas"""

    # Consulta NO optimizada (sin índices)
    start_time = time.time()
    result_no_opt = await db_session.execute(text("""
        SELECT * FROM registros_principales
        WHERE categoria = 'test' AND estado = 'activo'
        ORDER BY fecha_creacion DESC
    """))
    time_no_opt = (time.time() - start_time) * 1000

    # Consulta optimizada (con índices)
    start_time = time.time()
    result_opt = await TipoAQueries.get_registros_by_categoria_optimized(
        db_session, "test", "activo"
    )
    time_opt = (time.time() - start_time) * 1000

    # La consulta optimizada debe ser más rápida
    assert time_opt < time_no_opt
    print(f"Mejora: {((time_no_opt - time_opt) / time_no_opt) * 100:.2f}%")

async def test_indices_efectivos(db_session: AsyncSession, performance_analyzer):
    """Verificar que los índices están siendo utilizados"""

    # Analizar plan de ejecución
    result = await performance_analyzer.measure_query_performance("""
        EXPLAIN (ANALYZE, BUFFERS)
        SELECT * FROM registros_principales
        WHERE categoria = :categoria AND estado = :estado
    """, {"categoria": "test", "estado": "activo"})

    # Verificar que se usa el índice (en producción)
    assert result["execution_time_ms"] < 50  # Debe ser rápido con índice
```

---

## 🎯 **ENTREGABLES**

### **📋 Checklist de Optimización**

- [ ] **Análisis de consultas lentas** completado
- [ ] **Índices estratégicos** creados para tu tipo (A/B/C/D)
- [ ] **Consultas optimizadas** implementadas
- [ ] **Monitoreo de performance** funcionando
- [ ] **Tests de performance** ejecutándose
- [ ] **Reporte de mejoras** documentado

### **📊 Métricas de Éxito**

1. **Reducción tiempo de consulta:** > 50%
2. **Uso eficiente de índices:** Verificado en planes de ejecución
3. **Consultas bajo threshold:** < 100ms para consultas críticas
4. **Throughput mejorado:** Medido en requests/segundo

---

## 🚀 **SIGUIENTES PASOS**

Una vez completada esta práctica:

1. **📊 Documenta** las mejoras obtenidas
2. **🔍 Verifica** el uso correcto de índices
3. **🔄 Continúa** con la Práctica 25 (Middleware)

---

**PRÁCTICA 24 - OPTIMIZACIÓN DB COMPLETADA**  
_Técnicas universales de optimización de base de datos_
