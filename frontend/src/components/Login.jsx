import React, { useState } from "react"

const API = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000"

export default function Login({ onLogin }) {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState(null)

  async function submit(e) {
    e.preventDefault()
    setError(null)
    try {
      const res = await fetch(`${API}/api/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({ username, password }),
      })
      if (!res.ok) throw new Error(await res.text())
      const data = await res.json()
      onLogin(data.access_token, data.is_admin)
    } catch (err) {
      setError("Invalid login")
    }
  }

  return (
    <div className="form-card" style={{ width: 300 }}>
      <h4>Login</h4>
      <form onSubmit={submit}>
        <div className="form-row">
          <input value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Username" />
        </div>
        <div className="form-row">
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" />
        </div>
        <button className="btn" type="submit">Login</button>
      </form>
      {error && <div className="notice">{error}</div>}
    </div>
  )
}
