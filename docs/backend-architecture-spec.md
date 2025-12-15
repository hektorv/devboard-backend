# DevBoard — Documento de Arquitectura de Backend (v1.3)

## 1. Objetivo

Definir una arquitectura **API-first** para el backend de DevBoard (gestión de proyectos y tareas) con:

* Backend en Python (**Flask**) con **TDD** desde el inicio.
* Contrato único mediante **OpenAPI** (fuente de verdad).
* Buenas prácticas: configuración por `.env`, **sin números mágicos**, separación estricta de responsabilidades, observabilidad y testabilidad.
* Backend diseñado para operar como **repositorio independiente** del frontend (sin mezclar tooling, carpetas ni dependencias).
* **Usuarios como recurso de dominio** para asignación consistente (`assignee_user_id`) **sin autenticación en MVP**, dejando preparada la evolución a autenticación futura. 

---

## 2. Alcance del backend (MVP)

Incluye:

* CRUD de **Projects**.
* CRUD de **Tasks** (siempre vinculadas a Project).
* CRUD de **Users** (sin login).
* Asignación de tareas mediante **`assignee_user_id`** (nullable).
* Reglas por estado del Project (ACTIVE/ON_HOLD/ARCHIVED).
* Persistencia MySQL.
* Tests automatizados con cobertura **≥ 95%** (deseable 100%).

No incluye (MVP):

* Login, tokens, sesiones.
* Roles (ADMIN/USER) y autorización.
* Permisos por propietario (scoping por usuario).
* Auditoría de cambios.

---

## 3. Principios arquitectónicos

### 3.1 API-first (contrato por delante)

* OpenAPI define rutas, payloads, enums, errores, filtros.
* Backend implementa exactamente OpenAPI.
* Cambios de contrato deben hacerse primero en OpenAPI y luego en backend.

### 3.2 Separación de capas (backend)

* **Routers (HTTP/REST)**: endpoints, parseo, validación superficial, serialización, mapeo de errores a HTTP.
* **Services (domain/business)**: reglas del dominio y validaciones de negocio (incluye consistencia Project↔Task, restricciones por estado, etc.).
* **Repositories (data access)**: operaciones de persistencia y consultas (ORM).
* **Models (ORM)**: entidades SQLAlchemy y relaciones.
* **Schemas/DTOs**: objetos de entrada/salida internos para evitar filtrar ORM en la API.
* **Config**: configuración por entorno y validación en arranque.
* **Utils (cross-cutting)**: decoradores, helpers; nunca lógica de negocio.

### 3.3 Backend repository independence (anti-confusión IA)

* Prohibido incluir Vue/Vite/HTML/UI.
* Prohibido incluir “clientes API” para frontend.
* El backend solo entrega API JSON y documentación técnica (README + referencia OpenAPI).

### 3.4 Código en inglés

* Código, comentarios y docstrings: **inglés**.

---

## 4. Arquitectura lógica (componentes)

### 4.1 Routers

* `HealthRouter`: endpoint de salud.
* `ProjectRouter`: CRUD Projects + cambio de estado.
* `TaskRouter`: CRUD Tasks scoped por project + cambio de estado.
* `UserRouter`: CRUD Users.

Responsabilidad: HTTP, no negocio.

### 4.2 Services

* `ProjectService`: reglas de Project (incl. status).
* `TaskService`: reglas de Task + restricciones por estado del Project + validación de asignación a User.
* `UserService`: reglas de User (unicidad email si aplica, activación/desactivación, etc.).

Responsabilidad: negocio y consistencia.

### 4.3 Repositories

* `ProjectRepository`, `TaskRepository`, `UserRepository` para acceso a datos.

### 4.4 Cross-cutting (decorators)

* Decoradores para:

  * logging/timing
  * boundary de excepciones (log y rethrow)
* Regla: los decoradores **no deben ocultar** errores de dominio; el mapeo a HTTP se define en routers/handlers.

---

## 5. Estructura del repositorio (scaffolding)

```
devboard-backend/
  app/
    __init__.py
    config.py
    constants.py
    errors.py
    logging_conf.py

    utils/
      __init__.py
      decorators.py

    db/
      __init__.py
      session.py

    models/
      __init__.py
      project.py
      task.py
      user.py

    repositories/
      __init__.py
      project_repository.py
      task_repository.py
      user_repository.py

    services/
      __init__.py
      project_service.py
      task_service.py
      user_service.py

    routers/
      __init__.py
      health_router.py
      project_router.py
      task_router.py
      user_router.py

    schemas/
      __init__.py
      project_schemas.py
      task_schemas.py
      user_schemas.py
      error_schemas.py

    tests/
      unit/
        test_project_service.py
        test_task_service.py
        test_user_service.py
      integration/
        test_health_api.py
        test_project_api.py
        test_task_api.py
        test_user_api.py
      conftest.py

  requirements.txt
  run.py
  .env.example
  README.md
```

Ubicación transversal:

* `app/constants.py`: enums/constantes (evitar números mágicos).
* `app/errors.py`: excepciones de dominio.
* `app/utils/decorators.py`: concerns transversales.

---

## 6. Arquitectura de datos (MySQL)

### 6.1 Entidades

**Project**

* `id` (PK)
* `name` (required)
* `description` (nullable)
* `status` (enum: ACTIVE, ON_HOLD, ARCHIVED)
* `created_at`

**User** *(sin autenticación en MVP)*

* `id` (PK)
* `display_name` (required)
* `email` (recommended; si se incluye: unique)
* `is_active` (bool, default true)
* `created_at`

**Task**

* `id` (PK)
* `project_id` (FK → projects.id, required)
* `title` (required)
* `description` (nullable)
* `status` (enum: BACKLOG, IN_PROGRESS, DONE)
* `priority` (enum: LOW, MEDIUM, HIGH)
* `assignee_user_id` (FK → users.id, nullable)
* `created_at`
* `finished_at`
* `deleted_at` (nullable; solo si se adopta soft delete)

### 6.2 Relaciones

* Project 1 → N Tasks
* User 1 → N Tasks (asignación opcional)

### 6.3 Integridad y performance

* NOT NULL: `tasks.project_id`, `tasks.title`.
* Índices recomendados:

  * `tasks(project_id, status)`
  * `tasks(project_id, priority)`
  * `tasks(project_id, assignee_user_id)`
  * `users(email)` si se usa como identificador.

---

## 7. Reglas de negocio (Services)

### 7.1 Reglas Project ↔ Task

* Toda Task debe pertenecer a un Project existente.
* Scoping de endpoints de Task por projectId para evitar ambigüedad.

### 7.2 Restricciones por ProjectStatus

* `ACTIVE`: permite operaciones mutantes sobre tareas.
* `ON_HOLD`: tareas en solo lectura.
* `ARCHIVED`: tareas en solo lectura.

### 7.3 Reglas de asignación a User

* `assignee_user_id` es **opcional** (tarea puede estar sin asignar).
* Si `assignee_user_id` se proporciona:

  * el usuario debe existir
  * política recomendada: debe estar activo (`is_active=true`)
* Si un user se desactiva:

  * las tareas existentes pueden permanecer asignadas
  * se bloquean nuevas asignaciones a ese user

### 7.4 Borrado de Projects con Tasks

Recomendado (MVP):

* Impedir borrar Project si tiene Tasks → HTTP 409.

### 7.5 Enums y constantes (no magic numbers)

* Enums centralizados: `ProjectStatus`, `TaskStatus`, `TaskPriority`.
* Constantes transversales (p. ej. límites) en `constants.py`.

---

## 8. Diseño de API (alineada con OpenAPI)

### 8.1 Convenciones

* Base path `/api`
* JSON UTF-8
* IDs numéricos
* Errores consistentes con `error_code`, `message`, `details` opcional.

### 8.2 Endpoints (alto nivel)

**Health**

* `GET /api/health`

**Users (sin login)**

* `GET /api/users`
* `POST /api/users`
* `GET /api/users/{userId}`
* `PUT /api/users/{userId}`
* `DELETE /api/users/{userId}` *(recomendado: desactivar / soft delete semántico)*

**Projects**

* `GET /api/projects`
* `POST /api/projects`
* `GET /api/projects/{projectId}`
* `PUT /api/projects/{projectId}`
* `DELETE /api/projects/{projectId}`
* `PATCH /api/projects/{projectId}/status`

**Tasks (scoped por project)**

* `GET /api/projects/{projectId}/tasks` (filtros: status, priority, assignee_user_id, q)
* `POST /api/projects/{projectId}/tasks`
* `GET /api/projects/{projectId}/tasks/{taskId}`
* `PUT /api/projects/{projectId}/tasks/{taskId}`
* `DELETE /api/projects/{projectId}/tasks/{taskId}`
* `PATCH /api/projects/{projectId}/tasks/{taskId}/status`

---

## 9. Manejo de errores

### 9.1 ErrorResponse estándar

* `error_code` (string estable)
* `message` (legible)
* `details` (opcional)
* `trace_id` (opcional)

### 9.2 Excepciones de dominio

* Excepciones de dominio viven en `errors.py`.
* Routers o handlers globales convierten a:

  * 400 (validation)
  * 404 (not found)
  * 409 (conflict/business rule)
  * 500 (internal)

---

## 10. Configuración y entorno (`.env`)

* `.env.example` versionado, `.env` ignorado.
* Variables mínimas:

  * `APP_ENV`, `APP_HOST`, `APP_PORT`
  * `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`
  * `LOG_LEVEL`
* Validación de configuración al arranque.

---

## 11. Observabilidad (logging)

* Logs con: timestamp, level, module.
* Opcional: request_id, service_fn, elapsed_ms.
* Domain errors a INFO/WARN; unexpected a ERROR.
* Decoradores pueden estandarizar logging/timing sin contaminar lógica de negocio.

---

## 12. Estrategia TDD y cobertura

### 12.1 Cobertura

* **Cobertura mínima esperada: ≥ 95%**
* **Deseable: 100%** (especialmente services y routers)

### 12.2 Pirámide

1. Unit tests (services)
2. Integration tests (API + DB)
3. E2E UI fuera de alcance backend

### 12.3 Orden de implementación (propuesto)

**Fase 0**

* Health + config + DB test setup

**Fase 1**

* Users CRUD (para habilitar asignaciones desde el inicio)

**Fase 2**

* Projects CRUD + status

**Fase 3**

* Tasks CRUD + filtros + status + validación de asignación + restricciones por estado de Project

**Fase 4**

* Regla delete project con tasks → 409

### 12.4 DB en tests

* MySQL de test (docker recomendado).
* Aislamiento por test: rollback o limpieza determinista.
* Sin dependencia de orden.

---

## 13. Entregables del backend

* Repo `devboard-backend` con:

  * código + tests
  * `requirements.txt`
  * `.env.example`
  * `README.md` con ejecución local, DB, tests y coverage
* Referencia al contrato OpenAPI (`openapi.yaml`) como fuente de verdad. 

---

## 14. Extracto: planificación para futura versión (vNext)

Para incluir en especificaciones como evolución planificada:

* **Autenticación**: endpoint `/api/auth/login` y esquema de seguridad (Bearer token o sesión).
* **Autorización**: roles `ADMIN` y `USER` con endpoints protegidos (401/403).
* **User identity**: `User.email` pasa a ser obligatorio y único si no lo es ya.
* **Trazabilidad**: auditoría de cambios (opcional).
* **Permisos avanzados**: scoping por usuario/proyecto si se requiere.

> Motivación: estas capacidades se excluyen del MVP para mantener complejidad y tiempos controlados, conservando un modelo de datos preparado (`assignee_user_id`) para integración futura.

---

