## DevBoard — Backlog MVP con criterios de aceptación (v1.1)

Formato: **Given / When / Then**.
Transiciones de tarea permitidas: `BACKLOG → IN_PROGRESS → DONE` y `DONE → IN_PROGRESS` (reopen). No existe vuelta a `BACKLOG`.

---

### EP-00 Infraestructura y contrato

**US-00.1 Health check**

* Given el backend está ejecutándose
* When consumo `GET /api/health`
* Then recibo `200` con un JSON que indica estado OK

**US-00.2 Configuración por entorno**

* Given existe `.env.example`
* When configuro `.env` y arranco el backend
* Then la app inicia sin credenciales hardcodeadas y falla explícitamente si faltan variables requeridas

**US-00.3 Contrato OpenAPI**

* Given la especificación OpenAPI
* When se implementa el backend
* Then el contrato se cumple exactamente
* Given cambios en la API
* When se actualiza el sistema
* Then se actualiza OpenAPI de forma consistente

---

### EP-01 Users (sin autenticación)

**US-01.1 Crear usuario**

* Given un payload válido de usuario
* When hago `POST /api/users`
* Then recibo `201` con el usuario creado

**US-01.2 Listar y consultar usuario**

* Given existen usuarios
* When hago `GET /api/users`
* Then recibo `200` con lista y paginación
* When hago `GET /api/users/{user_id}`
* Then recibo `200` o `404` si no existe

**US-01.3 Editar usuario**

* Given un usuario existente
* When hago `PUT /api/users/{user_id}` con campos válidos
* Then recibo `200` con los datos actualizados

**US-01.4 Desactivar usuario**

* Given un usuario existente
* When hago `DELETE /api/users/{user_id}`
* Then recibo `204` y el usuario queda desactivado (no usable para nuevas asignaciones)

---

### EP-02 Projects

**US-02.1 Crear proyecto**

* Given un payload válido
* When hago `POST /api/projects`
* Then recibo `201` y el proyecto queda en estado inicial definido por el sistema

**US-02.2 Listar y consultar proyectos**

* Given existen proyectos
* When hago `GET /api/projects`
* Then recibo `200` con lista y paginación
* When hago `GET /api/projects/{project_id}`
* Then recibo `200` o `404`

**US-02.3 Editar proyecto**

* Given un proyecto existente
* When hago `PUT /api/projects/{project_id}`
* Then recibo `200` con el proyecto actualizado

**US-02.4 Cambiar estado de proyecto**

* Given un proyecto existente
* When hago `PATCH /api/projects/{project_id}/status`
* Then recibo `200` con el nuevo estado
* And si el estado cambia a `ARCHIVED`, se registra `finished_at`
* And si el estado cambia a `ARCHIVED`, se registra `finished_at` (timestamp)

Notes:

- Projects use **soft-delete** by default. `DELETE /api/projects/{project_id}` sets `deleted_at` and returns `204` on success. If the project has tasks, returns `409` (policy: block deletion). To hard-delete a project, a separate admin workflow must be defined.
- Pagination: list endpoints use `page` (1-based) and `per_page` query parameters. Defaults: `page=1`, `per_page=20`, `per_page_max=100`.

**US-02.5 Eliminar proyecto**

* Given un proyecto existente
* When hago `DELETE /api/projects/{project_id}`
* Then recibo `204`
* And si el proyecto tiene tareas y la política es “bloquear”, recibo `409`

---

### EP-03 Tasks (scoped por project)

**US-03.1 Crear tarea en un proyecto**

* Given un proyecto existente
* When hago `POST /api/projects/{project_id}/tasks` con payload válido
* Then recibo `201` con la tarea creada
* And si el proyecto no existe recibo `404`

**US-03.2 Listar y consultar tareas de un proyecto**

* Given un proyecto existente con tareas
* When hago `GET /api/projects/{project_id}/tasks`
* Then recibo `200` con lista y paginación
* When hago `GET /api/projects/{project_id}/tasks/{task_id}`
* Then recibo `200` o `404`

**US-03.3 Editar tarea**

* Given una tarea existente en un proyecto
* When hago `PUT /api/projects/{project_id}/tasks/{task_id}`
* Then recibo `200` con la tarea actualizada

**US-03.4 Eliminar tarea**

* Given una tarea existente
* When hago `DELETE /api/projects/{project_id}/tasks/{task_id}`
* Then recibo `204`

**US-03.5 Cambiar estado de tarea**

* Given una tarea existente
* When hago `PATCH /api/projects/{project_id}/tasks/{task_id}/status`
* Then recibo `200` con el nuevo estado
* And si cambia a `DONE`, se registra `finished_at`
* And si cambia de `DONE` a `IN_PROGRESS`, se limpia `finished_at`

**US-03.6 Asignar tarea a usuario**

* Given una tarea existente
* When asigno `assignee_user_id` válido
* Then la tarea queda asignada al usuario

**US-03.7 Filtros y búsqueda**

* Given tareas en un proyecto
* When hago `GET /api/projects/{project_id}/tasks` con filtros (`status`, `priority`, `assignee_user_id`, `q`)
* Then recibo `200` con solo las tareas que cumplen

---

### EP-04 Reglas de negocio (bloqueos y validaciones)

**US-04.1 Restricciones por estado del proyecto**

* Given un proyecto `ON_HOLD` o `ARCHIVED`
* When intento crear/editar/eliminar/cambiar estado de una tarea del proyecto
* Then recibo error de negocio y no se realizan cambios

**US-04.2 Validación de asignación**

* Given una tarea
* When intento asignar un `assignee_user_id` inexistente
* Then recibo error y no se guarda
* When intento asignar a un usuario desactivado
* Then recibo error de negocio y no se guarda

**US-04.3 Restricción de edición del proyecto archivado**

* Given un proyecto `ARCHIVED`
* When intento editar sus datos
* Then recibo error de negocio y no se realizan cambios
* Given un proyecto `ARCHIVED`
* When consulto el proyecto o sus tareas
* Then la operación es permitida (solo lectura)

---

## Definición de “Done” del MVP

* OpenAPI definida y consistente con la implementación.
* Backend implementa EP-00..EP-04.
* Suite de tests pasa y cobertura **≥95%** (deseable 100%).
* README con pasos de ejecución y tests.

