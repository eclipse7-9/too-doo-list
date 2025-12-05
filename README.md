# To‑Do List (React + FastAPI) — Documentación en español

Proyecto simple de lista de tareas con:
- Frontend: React + Vite (deploy en GitHub Pages)
- Backend principal: Python (FastAPI) desplegado en Render
- Base de datos: MySQL en Railway

Esta documentación asume que el repositorio abierto es `c:\Users\Aprendiz\Desktop\too-doo-list-develop`.

---

## Tecnologías clave
- Frontend: React (Vite), JavaScript, CSS
- Backend principal: FastAPI + uvicorn (Python 3.8+)
- DB: MySQL (Railway)
- Herramientas: npm, pip, virtualenv, gh-pages (frontend deploy)

---

## Arquitectura y despliegue
- Frontend: desplegado en GitHub Pages. El frontend consume la API configurada por la variable VITE_API_BASE.
- Backend (API): desplegado en Render. Expone endpoints REST para listar/crear/actualizar/eliminar tareas.
- Base de datos: MySQL alojada en Railway (usada por el backend).

Asegúrate de que:
- Render tenga la variable de entorno `DATABASE_URL` apuntando a la DB de Railway.
- El backend permita CORS desde el dominio de GitHub Pages (o uso de `*` en desarrollo).
- El frontend use `VITE_API_BASE` que apunte a la URL del backend en Render para producción.

---

## Estructura relevante
- frontend: `index.html`, `src/`, `.env` (VITE_API_BASE)
- backend (FastAPI): `backend/main.py`, `backend/database.py`, `backend/schemas.py`, `backend/init_db.py`
- alternativa Node: `server/index.js`, `server/db.js`, `server/schema.sql`
- CI / deploy: `.github/workflows/`, `render.yaml`

---

## Endpoints (resumen)
Rutas principales del backend FastAPI (base: VITE_API_BASE o URL de Render):

- GET  /tasks          — obtener todas las tareas
- POST /tasks          — crear una tarea (body JSON: { "title": "texto" })
- PUT  /tasks/{id}     — actualizar (title/completed)
- DELETE /tasks/{id}   — eliminar tarea

Ejemplo curl:
- Listar:
  curl http://localhost:8000/tasks
- Crear:
  curl -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d '{"title":"Comprar"}'

---

## Variables de entorno importantes
- Frontend:
  - VITE_API_BASE=http://localhost:8000 (desarrollo) o https://<tu-backend-en-render>
- Backend (FastAPI):
  - DATABASE_URL=mysql://USER:PASSWORD@HOST:3306/DATABASE
  - (opcional) PORT, otras variables según `backend/start.sh` o Render
- Server (Node): revisar `server/.env.example`

Cómo exportar en Windows (PowerShell):
- Frontend (temporal): $env:VITE_API_BASE="http://localhost:8000"
- Backend (temporal): $env:DATABASE_URL="mysql://user:pass@host:3306/dbname"

En cmd:
- set VITE_API_BASE=http://localhost:8000

---

## Instalación y ejecución (paso a paso)

1) Clonar
- git clone <repo-url>
- cd too-doo-list-develop

2) Frontend (desarrollo)
- npm install
- Crear `.env` en raíz del frontend o ajustar `.env` existente:
  # To‑Do List (React + FastAPI)

  Proyecto To‑Do List sencillo con frontend en React (Vite) y backend principal en Python (FastAPI). Este repositorio incluye también una alternativa de backend en Node.js.

  URLs públicas del proyecto
  - Backend (OpenAPI / Swagger): https://too-doo-list-5.onrender.com/docs
  - Frontend (GitHub Pages): https://eclipse7-9.github.io/too-doo-list/

  Resumen
  - Frontend: React + Vite, configuración por `VITE_API_BASE`.
  - Backend principal: FastAPI en `backend/` que expone CRUD de tareas.
  - Base de datos: MySQL (esquema en `server/schema.sql`).

  Estructura principal
  - `backend/` — FastAPI (app, DB, esquemas, scripts de inicialización).
  - `server/` — alternativa Node.js (Express) con endpoints equivalentes.
  - `src/` — frontend React + Vite.

  Endpoints principales
  - GET  `/api/tasks`         — listar tareas
  - POST `/api/tasks`         — crear tarea (JSON: `{ "title": "texto" }`)
  - PUT  `/api/tasks/{id}`    — actualizar tarea (JSON: `{ "title": "...", "completed": true }`)
  - DELETE `/api/tasks/{id}`  — eliminar tarea

  Variables de entorno (ejemplos)
  - Backend:
    - `DB_HOST` (ej. `127.0.0.1`)
    - `DB_PORT` (ej. `3306`)
    - `DB_USER`
    - `DB_PASSWORD`
    - `DB_NAME`
    - `FRONTEND_ALLOWED_ORIGINS` (ej. `http://localhost:5173,https://eclipse7-9.github.io`)
    - `PORT` (Render provee `$PORT`)
  - Frontend:
    - `VITE_API_BASE` (ej. `http://localhost:8000` en dev / `https://too-doo-list-5.onrender.com` en prod)

  Comandos de desarrollo (PowerShell)
  Frontend:
  ```powershell
  cd C:\Users\Aprendiz\Desktop\too-doo-list-develop
  npm install
  $env:VITE_API_BASE="http://localhost:8000"
  npm run dev
  ```

  Backend (FastAPI):
  ```powershell
  cd C:\Users\Aprendiz\Desktop\too-doo-list-develop\backend
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  pip install -r requirements.txt
  $env:DB_HOST="127.0.0.1"
  $env:DB_PORT="3306"
  $env:DB_USER="root"
  $env:DB_PASSWORD=""
  $env:DB_NAME="todo_db"
  python init_db.py
  uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
  ```

  Despliegue (resumen)
  - Backend (Render):
    - Build: `pip install -r backend/requirements.txt`
    - Start: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
    - Variables: `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `FRONTEND_ALLOWED_ORIGINS`
    - Ejecutar `python backend/init_db.py` si la DB está vacía.
  - Frontend (GitHub Pages):
    - Antes de build: `VITE_API_BASE` → `https://too-doo-list-5.onrender.com`
    - `npm run build` y `npm run deploy` (usa `gh-pages`).

  Recomendaciones
  - Unificar la conexión a DB: documentar `DB_*` o añadir soporte para `DATABASE_URL` en `backend`.
  - Documentar que la API devuelve boolean en JSON para `completed` (DB guarda 0/1).
  - Verificar que Render ejecute los comandos en el directorio `backend/` cuando se use `start.sh` o `Procfile`.

  Archivos añadidos en el repo:
  - `backend/.env.example`
  - `.env.example` (root)
  - `docs/API.md`
  - `docs/DEPLOY.md`

  Si quieres, puedo commitear estos cambios y abrir un PR, o implementar soporte para `DATABASE_URL` en el backend.
