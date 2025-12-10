# Arquitectura (diagrama y descripción)

Este documento presenta una vista sencilla (C4 Nivel 1/2) de la arquitectura del proyecto.

## Diagrama (sencillo)

Usuario --> Frontend (Vite / React) --> Backend (FastAPI o Node) --> Base de datos (MySQL / Railway)

Representación ASCII:

```
 [Usuario]
     |
     v
 [Frontend - React (Vite)]  --XHR/HTTP-->  [Backend - FastAPI (Render)]
                                             |
                                             v
                                   [MySQL - Railway / RDS]
```

En producción los proveedores típicos usados por el equipo son: Frontend en Vercel (o GitHub Pages), Backend en Render y DB en Railway.

## Componentes y responsabilidades

- Frontend (`src/`): interfaz de usuario y lógica de presentación.
  - Pantallas principales: listado de tareas, creación/edición de tarea, filtros/estado.
  - Responsabilidad: consumir la API REST, mostrar/validar formularios, navegación.

- Backend (FastAPI, `backend/`): API REST que expone CRUD de tareas.
  - Capas:
    - Rutas / endpoints (`backend/main.py` o similar).
    - Schemas / validación (`backend/schemas.py`).
    - Modelos / ORM (`backend/models.py`) — SQLAlchemy.
    - Database / sesiones (`backend/database.py`).
    - Scripts auxiliares: `init_db.py` para inicializar la BD.

- Alternativa Node (`server/`): implementación paralela del backend en Node.js/Express y SQL (schema.sql).

- Base de datos (MySQL): persistencia de tareas. Esquema principal en `server/schema.sql`.

## Modelo de datos (resumen)

- Tabla `tasks` (MySQL / SQLAlchemy model `Task`):
  - `id` INT AUTO_INCREMENT — PK
  - `title` VARCHAR(255) NOT NULL
  - `completed` TINYINT(1) / BOOLEAN DEFAULT 0
  - `created_at` TIMESTAMP / DATETIME (DEFAULT now)
  - `updated_at` TIMESTAMP / DATETIME (ON UPDATE now)

El modelo en `backend/models.py` (SQLAlchemy) corresponde con `server/schema.sql`.

## Comunicaciones y seguridad

- Comunicación entre Frontend y Backend por HTTP/HTTPS (CORS habilitado en backend para orígenes permitidos).
- En producción asegurar HTTPS y variables de entorno para credenciales (no guardar secrets en el repo).

## Despliegue (sugerencia rápida)

- Frontend: build de Vite → desplegar en Vercel / GitHub Pages.
- Backend: configurar Render con `pip install -r backend/requirements.txt` y `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`.
- DB: Railway o proveedor MySQL. Proveer `DB_*` o `DATABASE_URL` en las variables de Render.

## Artefacto Draw.io / Diagrama editable

Si quieres, puedo exportar un diagrama en formato Draw.io (XML) y añadirlo a `docs/` como `arquitectura.drawio`, o generar un PDF. Dime si prefieres Draw.io o SVG/PDF.
