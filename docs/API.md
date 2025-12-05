# API - To‑Do List

Endpoints principales (base: `VITE_API_BASE` o la URL pública `https://too-doo-list-5.onrender.com`):

- GET `/api/tasks`
  - Descripción: Devuelve todas las tareas.
  - Respuesta 200 (ejemplo):
    ```json
    [
      { "id": 1, "title": "Comprar leche", "completed": false, "created_at": "2023-01-01T12:00:00", "updated_at": null }
    ]
    ```

- POST `/api/tasks`
  - Descripción: Crea una nueva tarea.
  - Body (JSON):
    ```json
    { "title": "Ir al banco" }
    ```
  - Curl ejemplo:
    ```bash
    curl -X POST https://too-doo-list-5.onrender.com/api/tasks \
      -H "Content-Type: application/json" \
      -d '{"title":"Ir al banco"}'
    ```

- PUT `/api/tasks/{id}`
  - Descripción: Actualiza campos de una tarea existente.
  - Path param: `id` (integer)
  - Body (JSON) ejemplo:
    ```json
    { "title": "Comprar pan", "completed": true }
    ```
  - Curl ejemplo:
    ```bash
    curl -X PUT https://too-doo-list-5.onrender.com/api/tasks/1 \
      -H "Content-Type: application/json" \
      -d '{"title":"Comprar pan","completed":true}'
    ```

- DELETE `/api/tasks/{id}`
  - Descripción: Elimina una tarea por su `id`.
  - Curl ejemplo:
    ```bash
    curl -X DELETE https://too-doo-list-5.onrender.com/api/tasks/1
    ```

Notas:
- El campo `completed` se expone como booleano en JSON (`true`/`false`). En la base de datos puede almacenarse como `TINYINT(1)` (0/1).
- Si la API devuelve errores 4xx/5xx, revisa `backend` logs y las variables de entorno de conexión a la DB.
