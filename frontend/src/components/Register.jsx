import React, { useState } from "react"

const API = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000"

export default function Register({ onLogin }) {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState(null)

  async function submit(e) {
    e.preventDefault()
    setError(null)
    try {
      const res = await fetch(`${API}/api/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      })
      if (!res.ok) {
        let msg = "Registration failed"
        try { const j = await res.json(); if (j && j.detail) msg = j.detail } catch(_) { msg = await res.text() }
        throw new Error(msg)
      }
      const data = await res.json()
      onLogin(data.access_token, data.is_admin)
    } catch (err) {
      setError(err.message || "Registration failed")
    }
  }

  return (
    <div className="form-card" style={{ width: 300 }}>
      <h4>Register</h4>
      <form onSubmit={submit}>
        <div className="form-row">
          <input value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Username" />
        </div>
        <div className="form-row">
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" />
        </div>
        <button className="btn" type="submit">Register</button>
      </form>
      {error && <div className="notice">{error}</div>}
    </div>
  )
}
