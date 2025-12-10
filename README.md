# ✅ To‑Do List (React + FastAPI) — Documentación en español

Proyecto simple de lista de tareas con:
- Frontend: React + Vite (deploy en GitHub Pages)
- Backend principal: Python (FastAPI) desplegado en Render
- Base de datos: MySQL en Railway

Esta documentación asume que el repositorio abierto es `c:\Users\Aprendiz\Desktop\too-doo-list-develop`.

---

## 🤖 Tecnologías clave
- Frontend: React (Vite), JavaScript, CSS
- Backend principal: FastAPI + uvicorn (Python 3.8+)
- DB: MySQL (Railway)
- Herramientas: npm, pip, virtualenv, gh-pages (frontend deploy)

---
# ⚜ To‑Do List (React + FastAPI)

Proyecto sencillo de lista de tareas con frontend en React (Vite) y backend en Python (FastAPI). Este repositorio incluye además una alternativa de backend en Node.js (`server/`).

**Estado:** documentación centralizada y ejemplos para ejecución local y despliegue.

**Contenido de esta README:** descripción, stack, requisitos, cómo ejecutar frontend/backend en local, variables de entorno, enlaces de producción y organización del repositorio.

---

## 📃 Descripción

Aplicación To‑Do (CRUD) para gestionar tareas. En producción típico flujo:

Usuario → Frontend (Vercel / GitHub Pages) → Backend (Render) → Base de datos (Railway / MySQL)

---

## 🛠 Stack tecnológico

- Frontend: React + Vite (JS/JSX)
- Backend principal: Python 3.x + FastAPI + Uvicorn
- Alternativa backend: Node.js (Express) en `server/`
- Base de datos: MySQL (esquema en `server/schema.sql`)

---

## 🔰 Requisitos previos

- Node.js (16+) y `npm` para el frontend y el `server/`
- Python 3.8+ y `pip` para el backend FastAPI
- MySQL si quieres correr la base de datos localmente

---

## ⭕ Ejecutar frontend en local

1. Instalar dependencias:

```powershell
cd <repo-root>
npm install
```

2. Fijar la variable de entorno para la API (ejemplo en PowerShell):

```powershell
$env:VITE_API_BASE = "http://localhost:8000"
npm run dev
```

Nota: `npm run dev` usa Vite y por defecto abre `http://localhost:5173`.

---

## ⭕ Ejecutar backend (FastAPI) en local

1. Crear y activar entorno virtual (PowerShell):

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Variables de entorno (ejemplo):

```powershell
$env:DB_HOST = "127.0.0.1"
$env:DB_PORT = "3306"
$env:DB_USER = "root"
$env:DB_PASSWORD = ""
$env:DB_NAME = "todo_db"
```

3. Inicializar esquema y arrancar:

```powershell
python init_db.py
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

El Swagger/OpenAPI estará en `http://localhost:8000/docs`.

---

## Variables de entorno y `.env.example`

Se incluye un ejemplo en `.env.example` en la raíz con las variables mínimas necesarias. Puntos clave:

- Frontend: `VITE_API_BASE` (URL base de la API)
- Backend (FastAPI): `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` — o alternativamente `DATABASE_URL` si se soporta.

---

## Enlaces de producción (ejemplos / placeholders)

- Frontend (producción, Vercel/GitHub Pages): https://<tu-frontend>
- Backend (producción, Render): https://<tu-backend>
- Base de datos (Railway): https://railway.app/project/<tu-proyecto>

Sustituye los placeholders por las URLs reales cuando estén disponibles.

---

## Documentación de arquitectura

Ver `docs/ARQUITECTURA.md` (diagrama C4 sencillo y descripción de componentes).

---

## Documentación de la API

Ver `docs/API.md` para endpoints, métodos HTTP, body esperado, respuestas de ejemplo y códigos de estado.

---

## Organización del repositorio (scaffolding)

- `src/` — Frontend React + Vite
- `public/` — Recursos estáticos del frontend
- `backend/` — FastAPI (app, models, esquemas, scripts de inicialización)
- `server/` — Backend alternativo en Node.js (express) y `schema.sql`
- `docs/` — Documentación (API, ARQUITECTURA, DEPLOY)
- `package.json` — comandos de frontend / root

---

## Endpoints principales (resumen)

Base: `VITE_API_BASE` (dev `http://localhost:8000`)

- GET  `/api/tasks`           — Listar tareas
- POST `/api/tasks`           — Crear tarea (JSON: `{ "title": "texto" }`)
- PUT  `/api/tasks/{id}`      — Actualizar tarea (JSON: `{ "title": "...", "completed": true }`)
- DELETE `/api/tasks/{id}`    — Eliminar tarea

Respuestas de ejemplo y detalles en `docs/API.md`.

---

## Próximos pasos sugeridos

- Rellenar las URLs de producción en este README.
- Añadir `DATABASE_URL` parsing en `backend` para soportar providers modernos.
- Añadir `frontend/.env.example` si el frontend necesita variables adicionales.

Si quieres, puedo commitear estos cambios y abrir un PR con los archivos añadidos.
