# Despliegue - Backend (Render) y Frontend (GitHub Pages)

Este archivo contiene los pasos mínimos para desplegar la API en Render y el frontend en GitHub Pages.

Backend — Render (FastAPI)

1. Crear un servicio web en Render que apunte al repositorio y branch adecuado.
2. En la configuración del servicio:
   - Build command: `pip install -r backend/requirements.txt`
   - Start command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
3. Añadir las variables de entorno en Render (Settings → Environment):
   - `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`
   - `FRONTEND_ALLOWED_ORIGINS` (ej. `https://eclipse7-9.github.io`)
4. Si la base de datos está vacía, ejecutar `python backend/init_db.py` desde la shell de Render o incluirlo como job en `render.yaml`.
5. Verificar que `https://<tu-servicio>.onrender.com/docs` responde y muestra los endpoints.

Frontend — GitHub Pages

1. Preparar `VITE_API_BASE` antes de compilar para producción. Localmente en PowerShell:
```powershell
$env:VITE_API_BASE="https://too-doo-list-5.onrender.com"
npm run build
npm run deploy
```
2. El script `deploy` (si existe) utiliza `gh-pages` para publicar `dist/` en la rama `gh-pages`.
3. Asegúrate de que el dominio publicado (por ejemplo `https://eclipse7-9.github.io/too-doo-list/`) está dentro de `FRONTEND_ALLOWED_ORIGINS` en el backend para evitar errores CORS.

Comprobaciones post-deploy
- Confirmar que `https://too-doo-list-5.onrender.com/docs` carga correctamente.
- Confirmar que el frontend en GitHub Pages carga y realiza peticiones a la API.

Consejos
- Para entornos CI, exporta `VITE_API_BASE` como variable de entorno en la acción de GitHub antes de ejecutar `npm run build`.
- Considera agregar soporte para `DATABASE_URL` en el backend si quieres simplificar la cadena de conexión (muchos hosts PaaS entregan `DATABASE_URL`).
