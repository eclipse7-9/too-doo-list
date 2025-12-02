import { useEffect, useState } from 'react'
import './App.css'

// Use VITE_API_BASE when provided by the build; otherwise fall back to the Render URL
const API_BASE = import.meta.env.VITE_API_BASE || 'https://too-doo-list-5.onrender.com'

function App() {
  const [tasks, setTasks] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [newTitle, setNewTitle] = useState('')
  const [editingId, setEditingId] = useState(null)
  const [editingTitle, setEditingTitle] = useState('')

  useEffect(() => {
    fetchTasks()
  }, [])

  async function fetchTasks() {
    setLoading(true)
    setError(null)
    try {
      const res = await fetch(`${API_BASE}/api/tasks`)
      if (!res.ok) throw new Error('Failed to fetch tasks')
      const data = await res.json()
      setTasks(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  async function addTask(e) {
    e.preventDefault()
    const title = newTitle.trim()
    if (!title) return
    try {
      const res = await fetch(`${API_BASE}/api/tasks`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title })
      })
      if (!res.ok) throw new Error('Failed to create')
      const created = await res.json()
      setTasks(prev => [created, ...prev])
      setNewTitle('')
    } catch (err) {
      setError(err.message)
    }
  }

  async function toggleComplete(task) {
    try {
      const res = await fetch(`${API_BASE}/api/tasks/${task.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ completed: !task.completed })
      })
      if (!res.ok) throw new Error('Failed to update')
      const updated = await res.json()
      setTasks(prev => prev.map(t => (t.id === updated.id ? updated : t)))
    } catch (err) {
      setError(err.message)
    }
  }

  function startEdit(task) {
    setEditingId(task.id)
    setEditingTitle(task.title)
  }

  async function saveEdit(e) {
    e.preventDefault()
    const title = editingTitle.trim()
    if (!title) return
    try {
      const res = await fetch(`${API_BASE}/api/tasks/${editingId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title })
      })
      if (!res.ok) throw new Error('Failed to update')
      const updated = await res.json()
      setTasks(prev => prev.map(t => (t.id === updated.id ? updated : t)))
      setEditingId(null)
      setEditingTitle('')
    } catch (err) {
      setError(err.message)
    }
  }

  async function deleteTask(id) {
    if (!confirm('Borrar tarea?')) return
    try {
      const res = await fetch(`${API_BASE}/api/tasks/${id}`, { method: 'DELETE' })
      if (!res.ok) throw new Error('Failed to delete')
      setTasks(prev => prev.filter(t => t.id !== id))
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div className="app-container">
      <h1>To‑Do List</h1>

      <form onSubmit={addTask} className="new-task-form">
        <input
          placeholder="Nueva tarea..."
          value={newTitle}
          onChange={e => setNewTitle(e.target.value)}
        />
        <button type="submit">Agregar</button>
      </form>

      {error && <div className="error">{error}</div>}

      {loading ? (
        <div>Loading...</div>
      ) : (
        <ul className="task-list">
          {tasks.map(task => (
            <li key={task.id} className={`task-item ${task.completed ? 'done' : ''}`}>
              <input
                type="checkbox"
                checked={task.completed}
                onChange={() => toggleComplete(task)}
              />

              {editingId === task.id ? (
                <form onSubmit={saveEdit} className="edit-form">
                  <input value={editingTitle} onChange={e => setEditingTitle(e.target.value)} />
                  <button type="submit">Guardar</button>
                  <button type="button" onClick={() => setEditingId(null)}>Cancelar</button>
                </form>
              ) : (
                <>
                  <span className="title">{task.title}</span>
                  <div className="actions">
                    <button onClick={() => startEdit(task)}>Editar</button>
                    <button onClick={() => deleteTask(task.id)}>Borrar</button>
                  </div>
                </>
              )}
            </li>
          ))}
        </ul>
      )}

      <style>{`
        .app-container { max-width:700px;margin:40px auto;font-family:Inter,system-ui,Arial;padding:0 16px }
        .new-task-form { display:flex; gap:8px; margin-bottom:16px }
        .new-task-form input { flex:1;padding:8px }
        .task-list { list-style:none;padding:0;margin:0 }
        .task-item { display:flex; align-items:center; gap:8px; padding:8px 0; border-bottom:1px solid #eee }
        .task-item.done .title { text-decoration:line-through; color:#666 }
        .title { flex:1 }
        .actions button { margin-left:8px }
        .error { color:crimson; margin-bottom:12px }
        .edit-form { display:flex; gap:8px; flex:1 }
      `}</style>
    </div>
  )
}

export default App
