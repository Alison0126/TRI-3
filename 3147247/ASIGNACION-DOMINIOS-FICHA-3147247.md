# 🚀 FICHA 3147247 - ASIGNACIÓN DE DOMINIOS SEMANA 6

## 👥 **ASIGNACIÓN DE DOMINIOS ÚNICOS POR ESTUDIANTE**

| Apellido            | Dominio               | Entidad Principal | Prefijo Test | Módulo Test     |
| ------------------- | --------------------- | ----------------- | ------------ | --------------- |
| BONILLA DIAZ        | **Clínica Dental**    | paciente          | `dental_`    | `test_dental`   |
| OSPINA ARIZA        | **Centro Estético**   | tratamiento       | `estetica_`  | `test_estetica` |
| CORTES BAQUERO      | **Laboratorio**       | muestra           | `lab_`       | `test_lab`      |
| RODRIGUEZ CRISTO    | **Autolavado**        | servicio          | `wash_`      | `test_wash`     |
| MARTINEZ TRILLOS    | **Fotografía**        | sesion            | `photo_`     | `test_photo`    |
| BAQUERO VILLARRAGA  | **Eventos**           | evento            | `event_`     | `test_event`    |
| MORALES LOPEZ       | **Mascotas Grooming** | cita              | `groom_`     | `test_groom`    |
| VELANDIA ROJAS      | **Catering**          | menu              | `catering_`  | `test_catering` |
| MONROY MALAVER      | **Spa**               | reserva           | `spa_`       | `test_spa`      |
| AMAYA PATIÑO        | **Academia Música**   | clase             | `music_`     | `test_music`    |
| MUÑOZ ZABALA        | **Rent a Car**        | alquiler          | `rental_`    | `test_rental`   |
| GODOY GOMEZ         | **Funeraria**         | servicio          | `funeral_`   | `test_funeral`  |
| SIERRA ROJAS        | **Courier**           | envio             | `courier_`   | `test_courier`  |
| TANGARIFE MARTINEZ  | **Seguridad**         | guardia           | `security_`  | `test_security` |
| ROMERO NIÑO         | **Jardinería**        | proyecto          | `garden_`    | `test_garden`   |
| BELTRAN RODRIGUEZ   | **Plomería**          | reparacion        | `plumber_`   | `test_plumber`  |
| FONSECA GOMEZ       | **Electricidad**      | instalacion       | `electric_`  | `test_electric` |
| MUÑOZ CONTRERAS     | **Lavandería**        | pedido            | `laundry_`   | `test_laundry`  |
| BETANCOURT BUITRAGO | **Mudanzas**          | traslado          | `moving_`    | `test_moving`   |
| PEREZ VARGAS        | **Diseño Gráfico**    | proyecto          | `design_`    | `test_design`   |
| LEON GUZMAN         | **Carpintería**       | mueble            | `wood_`      | `test_wood`     |
| TRIVIÑO LOPEZ       | **Academia Baile**    | inscripcion       | `dance_`     | `test_dance`    |
| AVELLA FONSECA      | **Psicología**        | consulta          | `psych_`     | `test_psych`    |
| MACIAS ARIAS        | **Nutrición**         | plan              | `nutri_`     | `test_nutri`    |
| MANRIQUE TORRES     | **Cerrajería**        | trabajo           | `keys_`      | `test_keys`     |
| TRAVIEZO MIJARES    | **Academia Idiomas**  | curso             | `lang_`      | `test_lang`     |
| GARCIA GUEVARA      | **Limpieza**          | contrato          | `clean_`     | `test_clean`    |
| MEDRANO RODRIGUEZ   | **Reparación PC**     | diagnostico       | `tech_`      | `test_tech`     |

---

## 📋 **INSTRUCCIONES ESPECÍFICAS PARA SEMANA 6 - TESTING**

### **🚨 REGLAS OBLIGATORIAS**

1. **❌ PROHIBIDO COPIAR Y PEGAR** tests de compañeros
2. **✅ CADA ESTUDIANTE** debe usar SU dominio específico
3. **📝 TODOS LOS TESTS** deben reflejar su negocio
4. **🔍 REVISIÓN INDIVIDUAL** de cobertura y tests por dominio

### **📝 Estructura de Testing Personalizada**

Cada estudiante debe crear tests específicos para su dominio:

```python
# tests/test_{tu_modulo}.py
# Ejemplo framework genérico - PERSONALIZAR COMPLETAMENTE

import pytest
from fastapi import status
from app.models.tu_entidad import TuEntidad

class TestTuDominio:
    """Tests específicos para TU dominio asignado"""

    def test_create_tu_entidad_success(self, client):
        """Test crear TU entidad principal - éxito"""
        data = {
            "campo_1": "valor específico de tu negocio",
            "campo_2": "otro valor relevante",
            # Campos específicos de TU dominio
        }
        response = client.post("/tu_entidades/", json=data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_get_tu_entidad_by_id(self, client):
        """Test obtener TU entidad por ID"""
        # Lógica específica para tu dominio
        pass

    def test_tu_logica_de_negocio_especifica(self, client):
        """Test específico para reglas de TU negocio"""
        # Implementar según tu dominio asignado
        pass
```

### **🎯 Ejemplos de Tests por Tipo de Negocio**

#### **Para negocios de servicios (ej: Spa, Catering, etc.):**

- Test de creación de reservas/citas
- Test de validación de horarios
- Test de cancelación de servicios
- Test de disponibilidad

#### **Para negocios de productos (ej: Rent a Car, etc.):**

- Test de inventario
- Test de disponibilidad de productos
- Test de reservas con fechas
- Test de devoluciones

#### **Para academias/educación (ej: Música, Baile, etc.):**

- Test de inscripciones
- Test de programación de clases
- Test de seguimiento de progreso
- Test de certificaciones

---

## 🚨 **VERIFICACIONES OBLIGATORIAS**

### **Cada test debe incluir:**

1. **✅ Casos de éxito** específicos de tu dominio
2. **❌ Casos de error** relevantes para tu negocio
3. **🔍 Validaciones** de lógica de negocio específica
4. **📊 Cobertura** mínima del 80% en tu módulo

### **El instructor verificará:**

- Que NO hay tests idénticos entre estudiantes
- Que los tests reflejan la lógica específica del dominio
- Que se usan los prefijos y nombres correctos
- Que la cobertura cubre casos relevantes del negocio

---

## 💡 **METODOLOGÍA PERSONALIZADA**

1. **🔍 Identifica** tu dominio en la tabla
2. **📝 Piensa** en los casos de uso específicos de tu negocio
3. **🧪 Crea tests** que validen TU lógica de negocio
4. **📊 Mide cobertura** enfocada en TU módulo
5. **🔧 Refactoriza** considerando las necesidades de TU dominio

**⚠️ IMPORTANTE:** Los tests deben ser tan específicos que no puedan funcionar para otros dominios sin modificación completa.

---

## 🎉 **ENTREGABLES FICHA 3147247**

Al final de la Semana 6, cada estudiante debe tener:

- ✅ Suite de tests específica para SU dominio
- ✅ Cobertura >80% en SU módulo principal
- ✅ Tests de integración para SU API
- ✅ Documentación de SUS casos de prueba
- ✅ Estructura de proyecto profesional para SU negocio
