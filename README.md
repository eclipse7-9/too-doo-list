# To‑Do List (React) — Front: GitHub Pages · Backend: Render · DB: Railway

Proyecto simple de una aplicación To‑Do hecha con React en el frontend, una API en FastAPI para el backend y una base de datos MySQL en Railway. El frontend se publicó con GitHub Pages, el backend con Render y la base de datos está en Railway.

## Tecnologías
- Frontend: React (Create React App)
- Backend: Python + FastAPI
- Base de datos: MySQL (Railway)
- Despliegue:
  - Frontend: GitHub Pages
  - Backend: Render
  - DB: Railway

## URLs de despliegue (ejemplos)
- Frontend (GitHub Pages): https://github.com/eclipse7-9/too-doo-list
- Backend (Render): https://too-doo-list-5.onrender.com/docs

## Variables de entorno importantes
Frontend (archivo .env en la carpeta frontend):
- https://eclipse7-9.github.io/too-doo-list/

Backend (en Render: Environment Variables):
- PORT= (Render asigna el puerto)
- DATABASE_URL= mysql://root:cJLReaUgXOkoNgNxDqCTTkjfLdtQqgyR@mysql-nk3.railway.internal:3306/railway

## Configuración y despliegue del frontend (GitHub Pages)

1. Instala gh-pages:
   - npm install --save-dev gh-pages
2. Desplegar:
   - npm run deploy

## Configuración y despliegue del backend (Render)
1. Sube tu repo a GitHub.
2. En Render crea un nuevo Web Service y conecta el repo.
3. Configura el build command (por ejemplo `npm install && npm run build`) y start command (`node index.js` o `npm start`).
4. Añade la variable de entorno DATABASE_URL con la cadena proporcionada por Railway.
5. Asegúrate de permitir CORS desde el dominio del frontend (o configurar CORS dinámico).

## Configuración de la base de datos (Railway)
1. Crea un proyecto PostgreSQL en Railway.
2. Crea la tabla `todos`:
3. sql
CREATE TABLE tasks (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  completed TINYINT(1) DEFAULT 0
);

   ```
