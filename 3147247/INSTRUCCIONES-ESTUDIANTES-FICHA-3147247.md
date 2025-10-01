# 🚀 INSTRUCCIONES PARA ESTUDIANTES - FICHA 3147247

## 📋 **TU DOMINIO ASIGNADO PARA TESTING - SEMANA 6**

### 🚨 **IMPORTANTE: METODOLOGÍA PERSONALIZADA PARA TESTING**

Cada estudiante de la ficha 3147247 tiene un **dominio de negocio único** para implementar testing. Busca tu apellido en la tabla y usa **SOLO** ese dominio para todos tus tests.

---

## 👥 **TABLA DE ASIGNACIONES FICHA 3147247**

| Apellido                | 🏢 **Tu Dominio** | 📦 **Tu Entidad** | 🔑 **Tu Prefijo** | 🧪 **Tu Módulo Test** |
| ----------------------- | ----------------- | ----------------- | ----------------- | --------------------- |
| **BONILLA DIAZ**        | Clínica Dental    | paciente          | `dental_`         | `test_dental`         |
| **OSPINA ARIZA**        | Centro Estético   | tratamiento       | `estetica_`       | `test_estetica`       |
| **CORTES BAQUERO**      | Laboratorio       | muestra           | `lab_`            | `test_lab`            |
| **RODRIGUEZ CRISTO**    | Autolavado        | servicio          | `wash_`           | `test_wash`           |
| **MARTINEZ TRILLOS**    | Fotografía        | sesion            | `photo_`          | `test_photo`          |
| **BAQUERO VILLARRAGA**  | Eventos           | evento            | `event_`          | `test_event`          |
| **MORALES LOPEZ**       | Mascotas Grooming | cita              | `groom_`          | `test_groom`          |
| **VELANDIA ROJAS**      | Catering          | menu              | `catering_`       | `test_catering`       |
| **MONROY MALAVER**      | Spa               | reserva           | `spa_`            | `test_spa`            |
| **AMAYA PATIÑO**        | Academia Música   | clase             | `music_`          | `test_music`          |
| **MUÑOZ ZABALA**        | Rent a Car        | alquiler          | `rental_`         | `test_rental`         |
| **GODOY GOMEZ**         | Funeraria         | servicio          | `funeral_`        | `test_funeral`        |
| **SIERRA ROJAS**        | Courier           | envio             | `courier_`        | `test_courier`        |
| **TANGARIFE MARTINEZ**  | Seguridad         | guardia           | `security_`       | `test_security`       |
| **ROMERO NIÑO**         | Jardinería        | proyecto          | `garden_`         | `test_garden`         |
| **BELTRAN RODRIGUEZ**   | Plomería          | reparacion        | `plumber_`        | `test_plumber`        |
| **FONSECA GOMEZ**       | Electricidad      | instalacion       | `electric_`       | `test_electric`       |
| **MUÑOZ CONTRERAS**     | Lavandería        | pedido            | `laundry_`        | `test_laundry`        |
| **BETANCOURT BUITRAGO** | Mudanzas          | traslado          | `moving_`         | `test_moving`         |
| **PEREZ VARGAS**        | Diseño Gráfico    | proyecto          | `design_`         | `test_design`         |
| **LEON GUZMAN**         | Carpintería       | mueble            | `wood_`           | `test_wood`           |
| **TRIVIÑO LOPEZ**       | Academia Baile    | inscripcion       | `dance_`          | `test_dance`          |
| **AVELLA FONSECA**      | Psicología        | consulta          | `psych_`          | `test_psych`          |
| **MACIAS ARIAS**        | Nutrición         | plan              | `nutri_`          | `test_nutri`          |
| **MANRIQUE TORRES**     | Cerrajería        | trabajo           | `keys_`           | `test_keys`           |
| **TRAVIEZO MIJARES**    | Academia Idiomas  | curso             | `lang_`           | `test_lang`           |
| **GARCIA GUEVARA**      | Limpieza          | contrato          | `clean_`          | `test_clean`          |
| **MEDRANO RODRIGUEZ**   | Reparación PC     | diagnostico       | `tech_`           | `test_tech`           |

---

## 💡 **FRAMEWORK DE TESTING PERSONALIZADO**

### **⚠️ ESTRUCTURA BASE (personalizar completamente)**

```python
# tests/{tu_modulo_test}.py
import pytest
from fastapi import status
from fastapi.testclient import TestClient

class TestTuDominio:
    \"\"\"Suite de tests para TU dominio específico\"\"\"

    def test_create_tu_entidad_success(self, client):
        \"\"\"Test crear TU entidad principal - caso éxito\"\"\"
        data = {
            "campo_1": "valor específico de tu negocio",
            "campo_2": "valor relevante para tu dominio",
            "campo_3": 123,  # Según la naturaleza de tu negocio
            # Agregar campos específicos de TU entidad
        }
        response = client.post("/tu_entidades/", json=data)
        assert response.status_code == status.HTTP_201_CREATED

        response_data = response.json()
        assert response_data["campo_1"] == data["campo_1"]
        assert "id" in response_data

    def test_create_tu_entidad_invalid_data(self, client):
        \"\"\"Test crear TU entidad - datos inválidos\"\"\"
        data = {
            "campo_1": "",  # Inválido según tu negocio
            "campo_2": "valor_demasiado_largo" * 100
        }
        response = client.post("/tu_entidades/", json=data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_tu_entidad_by_id_success(self, client):
        \"\"\"Test obtener TU entidad por ID - éxito\"\"\"
        # Primero crear la entidad
        create_data = {
            "campo_1": "valor_test",
            # Completar según tu dominio
        }
        create_response = client.post("/tu_entidades/", json=create_data)
        created_id = create_response.json()["id"]

        # Luego obtenerla
        response = client.get(f"/tu_entidades/{created_id}")
        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert response_data["id"] == created_id
        assert response_data["campo_1"] == create_data["campo_1"]

    def test_get_tu_entidad_not_found(self, client):
        \"\"\"Test obtener TU entidad - ID inexistente\"\"\"
        response = client.get("/tu_entidades/99999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_tu_logica_negocio_especifica(self, client):
        \"\"\"Test específico para reglas de TU negocio\"\"\"
        # Implementar según las reglas únicas de tu dominio
        # Ejemplo: validación de horarios, disponibilidad, etc.
        pass

    def test_get_all_tu_entidades(self, client):
        \"\"\"Test listar todas TUS entidades\"\"\"
        # Crear algunas entidades primero
        for i in range(3):
            data = {
                "campo_1": f"test_entity_{i}",
                # Completar según tu dominio
            }
            client.post("/tu_entidades/", json=data)

        # Obtener lista
        response = client.get("/tu_entidades/")
        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert isinstance(response_data, list)
        assert len(response_data) >= 3
```

### **🚨 IMPORTANTE: Personalización Obligatoria**

**NO uses este código directamente. Debes:**

1. **Reemplazar `TuDominio`** con el nombre de TU dominio específico
2. **Reemplazar `tu_entidad`** con TU entidad principal de la tabla
3. **Reemplazar `tu_modulo_test`** con TU módulo específico
4. **Agregar campos específicos** según la naturaleza de TU negocio
5. **Implementar validaciones únicas** de TU dominio
6. **Crear casos de error** relevantes para TU contexto

---

## 🎯 **EJEMPLOS ESPECÍFICOS POR TIPO DE NEGOCIO**

### **🦷 Si eres BONILLA (Clínica Dental):**

```python
class TestClínicaDental:
    def test_create_paciente_success(self, client):
        data = {
            "nombre": "María García",
            "edad": 35,
            "telefono": "3001234567",
            "historial_medico": "Sin alergias conocidas",
            "tipo_tratamiento": "limpieza_dental",
            "fecha_cita": "2024-12-15T10:00:00"
        }
        # Test específico para clínica dental

    def test_validate_edad_paciente(self, client):
        \"\"\"Test validación edad paciente\"\"\"
        data = {"edad": -5}  # Edad inválida
        # Test específico de validación dental
```

### **💄 Si eres OSPINA (Centro Estético):**

```python
class TestCentroEstetico:
    def test_create_tratamiento_success(self, client):
        data = {
            "nombre_tratamiento": "Limpieza facial",
            "duracion_minutos": 60,
            "precio": 80000,
            "tipo_piel": "mixta",
            "productos_utilizados": ["exfoliante", "mascarilla"]
        }
        # Test específico para centro estético

    def test_validate_duracion_tratamiento(self, client):
        \"\"\"Test validación duración tratamiento\"\"\"
        data = {"duracion_minutos": 0}  # Duración inválida
        # Test específico de validación estética
```

### **🧪 Si eres CORTES (Laboratorio):**

```python
class TestLaboratorio:
    def test_create_muestra_success(self, client):
        data = {
            "codigo_muestra": "LAB001",
            "tipo_analisis": "hemograma_completo",
            "fecha_toma": "2024-12-15T08:00:00",
            "paciente_id": "PAC001",
            "urgente": False,
            "observaciones": "Ayuno de 12 horas"
        }
        # Test específico para laboratorio

    def test_validate_codigo_muestra_unico(self, client):
        \"\"\"Test validación código único\"\"\"
        # Test específico de validación laboratorio
```

---

## 🎯 **TU TAREA DE HOY**

### **Paso 1: Identifica tu información específica**

1. **✅ Busca tu apellido** en la tabla superior
2. **✅ Anota tu dominio, entidad, prefijo y módulo**
3. **✅ NO cambies de dominio** durante toda la práctica
4. **✅ Piensa en las características únicas** de tu negocio

### **Paso 2: Adapta el framework a tu dominio**

1. **✅ Crea tu archivo** `tests/{tu_modulo_test}.py`
2. **✅ Reemplaza todos los términos genéricos** por los específicos de tu negocio
3. **✅ Define campos únicos** para tu entidad principal
4. **✅ Implementa validaciones específicas** de tu dominio

### **Paso 3: Implementa casos de prueba únicos**

1. **✅ Tests de creación** con datos válidos de tu negocio
2. **✅ Tests de validación** específicos de tu dominio
3. **✅ Tests de casos de error** relevantes para tu contexto
4. **✅ Tests de lógica de negocio** única de tu dominio

### **Paso 4: Verifica cobertura específica**

1. **✅ Ejecuta pytest** en tu módulo específico
2. **✅ Mide cobertura** enfocada en tu implementación
3. **✅ Asegura >80% cobertura** en tu módulo principal
4. **✅ Documenta casos especiales** de tu negocio

---

## 🔍 **VERIFICACIÓN DEL INSTRUCTOR - FICHA 3147247**

Durante la clase, el instructor verificará que:

### ✅ **Verificaciones técnicas específicas:**

- Tu código usa el prefijo correcto según tu fila en la tabla
- Tus tests están en el módulo correcto (`test_{tu_modulo}`)
- No hay código idéntico entre estudiantes de la ficha
- Los tests reflejan la lógica específica de tu dominio asignado

### ❓ **Preguntas que debes poder responder:**

- ¿Por qué elegiste esos casos de prueba para tu negocio específico?
- ¿Qué validaciones son críticas en tu dominio?
- ¿Cómo manejas los casos de error únicos de tu negocio?
- ¿Qué cobertura es más importante para tu tipo de aplicación?

---

## 🚨 **REGLAS ESPECÍFICAS FICHA 3147247**

### **✅ PERMITIDO:**

- Consultar documentación oficial de pytest
- Preguntar al instructor sobre tu dominio específico
- Colaborar en conceptos generales de testing
- Adaptar ejemplos genéricos a tu contexto

### **❌ PROHIBIDO:**

- Copiar tests de compañeros (diferentes dominios)
- Intercambiar código entre estudiantes
- Usar ejemplos sin personalizar completamente
- Implementar lógica que no corresponde a tu negocio

### **⚖️ CONSECUENCIAS:**

- **Primera vez copiando:** Advertencia y rehacer
- **Segunda vez:** Pérdida automática de 50% de la nota
- **Código idéntico:** Ambos estudiantes pierden puntos

---

## 🎉 **ENTREGABLES FICHA 3147247**

Al final de la Semana 6, debes tener:

- ✅ **Archivo de tests** `test_{tu_modulo}.py` funcionando
- ✅ **Cobertura >80%** en tu módulo principal
- ✅ **Al menos 10 tests diferentes** específicos de tu dominio
- ✅ **Casos de éxito y error** únicos de tu negocio
- ✅ **Documentación** de tus casos de prueba especiales

**¡Tu implementación será única en toda la ficha!** 🚀

---

## 📞 **SOPORTE DURANTE LA CLASE**

- 🙋‍♂️ **Dudas técnicas:** Pregunta al instructor
- 📋 **Verificación de progreso:** Checklist personalizado
- 🔍 **Revisión de implementación:** Feedback específico por dominio
- 💡 **Sugerencias de mejora:** Adaptadas a tu tipo de negocio

**¡Éxito en tu implementación personalizada!** 🎯
