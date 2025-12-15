# DevBoard — Documento de Especificación de Requisitos del Proyecto (SRD)

## 1. Nombre

**DevBoard**

## 2. Propósito

Desarrollar una aplicación web para equipos de desarrollo de software que permita gestionar **proyectos** y, dentro de cada proyecto, **tareas**, organizadas mediante un flujo tipo Kanban.

## 3. Alcance

### 3.1 Incluye (MVP)

* Gestión de proyectos.
* Gestión de tareas asociadas obligatoriamente a un proyecto.
* Estados para proyectos y tareas.
* Visualización de tareas por proyecto.
* Interacción mediante una API REST.
* Persistencia de la información.

### 3.2 Fuera de alcance

* Autenticación y control de accesos.
* Gestión avanzada de usuarios.
* Notificaciones automáticas.
* Dependencias entre tareas.

## 4. Actores

* **Miembro del equipo**: gestiona proyectos y tareas.
* **Consumidor de API**: integra el sistema con otras herramientas.

## 5. Requisitos funcionales

### Proyectos

**RF-P01. Crear proyecto**
El sistema permite crear un proyecto.

**RF-P02. Consultar proyectos**
El sistema permite listar proyectos y consultar un proyecto concreto.

**RF-P03. Editar proyecto**
El sistema permite modificar la información de un proyecto.

**RF-P04. Eliminar proyecto**
El sistema permite eliminar un proyecto.

**RF-P05. Cambiar estado del proyecto**
El sistema permite asignar y modificar el estado de un proyecto.

---

### Tareas

**RF-T01. Crear tarea**
El sistema permite crear una tarea asociada a un proyecto existente.

**RF-T02. Consultar tareas**
El sistema permite listar y consultar tareas asociadas a un proyecto.

**RF-T03. Editar tarea**
El sistema permite modificar una tarea.

**RF-T04. Eliminar tarea**
El sistema permite eliminar una tarea.

**RF-T05. Cambiar estado de tarea**
El sistema permite cambiar el estado de una tarea dentro del flujo definido.

---

### Reglas de negocio

**RB-01. Asociación obligatoria**
Toda tarea debe pertenecer a un único proyecto.

**RB-02. Estados de proyecto**
Un proyecto puede encontrarse en uno de los siguientes estados:

* **ACTIVE**
* **ON_HOLD**
* **ARCHIVED**

**RB-03. Estados de tarea**
Una tarea puede encontrarse en uno de los siguientes estados:

* **BACKLOG**
* **IN_PROGRESS**
* **DONE**

**RB-04. Restricciones por estado**
El comportamiento permitido sobre las tareas depende del estado del proyecto al que pertenecen.

*(Las restricciones concretas y su aplicación técnica se definen en el documento de Arquitectura.)*

---

## 6. Requisitos no funcionales

**RNF-01. Desacoplamiento**
El sistema debe permitir una separación clara entre frontend y backend.

**RNF-02. Consistencia funcional**
Las operaciones deben respetar las reglas de negocio definidas.

**RNF-03. Evolutividad**
La solución debe permitir la incorporación futura de nuevas funcionalidades sin cambios disruptivos.

**RNF-04. Documentación**
Las funcionalidades expuestas deben estar documentadas mediante una especificación formal.

---

## 7. Modelo conceptual (alto nivel)

### Proyecto

* Identificador
* Información descriptiva
* Estado

### Tarea

* Identificador
* Proyecto asociado
* Información descriptiva
* Estado

Relación:

* Un **Proyecto** puede tener **múltiples Tareas**.
* Una **Tarea** pertenece a **un único Proyecto**.

---

## 8. Criterios de aceptación (MVP)

* Es posible crear y gestionar proyectos.
* No se pueden crear tareas sin proyecto.
* Las tareas se visualizan por proyecto.
* Los estados de proyectos y tareas se respetan.
* El sistema mantiene la coherencia de las reglas definidas.

---

## 9. Restricciones del desarrollo

* El código se genera mediante interacción con asistentes de programación basados en IA.
* El proceso y las decisiones deben documentarse.

---

### Estado actual

✔ Documento de **Especificación** cerrado
✔ Sin decisiones técnicas embebidas
✔ Apto para evaluación académica

---

## Aclaraciones para implementación (rápido)

Estas aclaraciones eliminan ambigüedades para la fase de implementación (MVP):

- **Transiciones de estado (Tasks):** BACKLOG -> IN_PROGRESS -> DONE. Se permite volver de DONE -> IN_PROGRESS (revert) si hay una razón justificada; documentar el caso en la PR.
- **Transiciones de estado (Projects):** ACTIVE ↔ ON_HOLD, y ACTIVE|ON_HOLD -> ARCHIVED. `ARCHIVED` es terminal y no permite cambios en proyecto ni en tareas.
- **Eliminación de Projects:** por defecto usar **soft delete** (`deleted_at`) para `projects` y `tasks` en el MVP. Si se opta por hard-delete, debe documentarse y dejarse claro que `DELETE` sobre un proyecto con tareas debe responder `409 CONFLICT` a menos que `?hard=true` se solicite y se apruebe explícitamente.

Estas decisiones deben estar sincronizadas con `docs/backend-architecture-spec.md` y `docs/oas.yml`.

