import React, { useState } from "react"

const API = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000"

export default function AuthPage({ onLogin }) {
  const [mode, setMode] = useState("login")
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState(null)

  async function submit(e) {
    e.preventDefault()
    setError(null)
    try {
      if (mode === "login") {
        const form = new URLSearchParams()
        form.set("username", username)
        form.set("password", password)
        const res = await fetch(`${API}/api/auth/login`, {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: form.toString(),
        })
        if (!res.ok) {
          let msg = "Invalid login"
          try { const j = await res.json(); if (j && j.detail) msg = j.detail } catch(_) {}
          throw new Error(msg)
        }
        const data = await res.json()
        onLogin(data.access_token, data.is_admin)
      } else {
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
      }
    } catch (err) {
      setError(err.message || "Error")
    }
  }

  return (
    <div className="auth-wrap">
      <div className="auth-nav">
        <div className="brand">
          <img src="/logo.svg" width={22} height={22} alt="logo" />
          <span>Sweet Shop</span>
        </div>
        <div className="nav-actions">
          <button className={`tab ${mode==='login'?'active':''}`} onClick={() => setMode('login')}>Login</button>
          <button className={`tab ${mode==='register'?'active':''}`} onClick={() => setMode('register')}>Register</button>
        </div>
      </div>

      <div className="auth-center">
        <div className="auth-card">
          <div className="auth-title">{mode === 'login' ? 'Welcome Back' : 'Create Account'}</div>
          <form onSubmit={submit}>
            <div className="form-row">
              <input value={username} onChange={(e)=>setUsername(e.target.value)} placeholder="Username" />
            </div>
            <div className="form-row">
              <input type="password" value={password} onChange={(e)=>setPassword(e.target.value)} placeholder="Password" />
            </div>
            <button className="btn" type="submit">{mode === 'login' ? 'Sign In' : 'Sign Up'}</button>
          </form>
          {error && <div className="notice" style={{marginTop:10}}>{error}</div>}
          <div className="small" style={{marginTop:10}}>
            {mode === 'login' ? (
              <>Don't have an account? <a href="#" onClick={(e)=>{e.preventDefault(); setMode('register')}}>Sign up here</a></>
            ) : (
              <>Already have an account? <a href="#" onClick={(e)=>{e.preventDefault(); setMode('login')}}>Sign in here</a></>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
