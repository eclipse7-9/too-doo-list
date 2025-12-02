from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

# Support both running as a package (uvicorn backend.main:app) and as a module
try:
    from backend import schemas
    from backend.database import get_conn
except Exception:
    import schemas
    from database import get_conn

app = FastAPI()

# Configure CORS origins from env var. When using credentials the
# Access-Control-Allow-Origin header must be the exact origin (not "*").
frontends = os.getenv("FRONTEND_ALLOWED_ORIGINS", "https://eclipse7-9.github.io")
origins = [o.strip() for o in frontends.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Handle Private Network Access preflight requests (Chrome PNA).
# When a secure origin (https) tries to call a local/private address,
# the browser sends the header `Access-Control-Request-Private-Network: true`
# on the preflight. The server must reply with
# `Access-Control-Allow-Private-Network: true` to allow the request.
class PrivateNetworkMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        acrpn = request.headers.get("access-control-request-private-network", "").lower()
        # Handle preflight specially
        if request.method == "OPTIONS" and acrpn == "true":
            origin = request.headers.get("origin")
            # Build allow-origin value: echo the origin when present and allowed,
            # otherwise fall back to the first configured origin or '*'.
            allow_origin = None
            if origin:
                if "*" in origins:
                    allow_origin = origin
                elif origin in origins:
                    allow_origin = origin
            if allow_origin is None:
                allow_origin = origins[0] if origins else "*"

            headers = {
                "Access-Control-Allow-Origin": allow_origin,
                "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS",
                "Access-Control-Allow-Headers": request.headers.get(
                    "access-control-request-headers", "*"
                ),
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Allow-Private-Network": "true",
            }
            return Response(status_code=204, headers=headers)

        # For non-preflight, proceed and add headers if needed
        response = await call_next(request)
        if acrpn == "true":
            response.headers["Access-Control-Allow-Private-Network"] = "true"

        # Ensure Access-Control-Allow-Origin is present for browser requests
        origin = request.headers.get("origin")
        if origin:
            if "*" in origins:
                # When credentials are allowed, echo the origin (browsers disallow '*')
                response.headers["Access-Control-Allow-Origin"] = origin
            elif origin in origins:
                response.headers["Access-Control-Allow-Origin"] = origin

        return response


app.add_middleware(PrivateNetworkMiddleware)


@app.get('/api/tasks', response_model=list[schemas.TaskOut])
def list_tasks():
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute('SELECT id, title, completed, created_at, updated_at FROM tasks ORDER BY id DESC')
            rows = cur.fetchall()
            for r in rows:
                r['completed'] = bool(r.get('completed', 0))
            return rows
    finally:
        conn.close()


@app.post('/api/tasks', response_model=schemas.TaskOut, status_code=201)
def create_task(payload: schemas.TaskCreate):
    title = payload.title.strip()
    if not title:
        raise HTTPException(status_code=400, detail='Title required')
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute('INSERT INTO tasks (title) VALUES (%s)', (title,))
            last_id = cur.lastrowid
        conn.commit()
        with conn.cursor() as cur:
            cur.execute('SELECT id, title, completed, created_at, updated_at FROM tasks WHERE id = %s', (last_id,))
            row = cur.fetchone()
            row['completed'] = bool(row.get('completed', 0))
            return row
    finally:
        conn.close()


@app.put('/api/tasks/{task_id}', response_model=schemas.TaskOut)
def update_task(task_id: int, payload: schemas.TaskUpdate):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            # check exists
            cur.execute('SELECT id FROM tasks WHERE id = %s', (task_id,))
            if cur.fetchone() is None:
                raise HTTPException(status_code=404, detail='Not found')
            parts = []
            values = []
            if payload.title is not None:
                parts.append('title = %s')
                values.append(payload.title.strip())
            if payload.completed is not None:
                parts.append('completed = %s')
                values.append(1 if payload.completed else 0)
            if parts:
                sql = 'UPDATE tasks SET ' + ', '.join(parts) + ' WHERE id = %s'
                values.append(task_id)
                cur.execute(sql, tuple(values))
                conn.commit()
            cur.execute('SELECT id, title, completed, created_at, updated_at FROM tasks WHERE id = %s', (task_id,))
            row = cur.fetchone()
            row['completed'] = bool(row.get('completed', 0))
            return row
    finally:
        conn.close()


@app.delete('/api/tasks/{task_id}')
def delete_task(task_id: int):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM tasks WHERE id = %s', (task_id,))
            affected = cur.rowcount
            conn.commit()
            if affected == 0:
                raise HTTPException(status_code=404, detail='Not found')
            return {"success": True}
    finally:
        conn.close()


if __name__ == '__main__':
    import uvicorn
    port = int(os.getenv('PORT', 8000))
    uvicorn.run('backend.main:app', host='0.0.0.0', port=port, reload=True)
