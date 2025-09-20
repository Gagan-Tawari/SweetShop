import React, { useEffect, useState } from "react"
import AuthPage from "./components/AuthPage"
import SweetsList from "./components/SweetsList"

const API = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000"

export default function App() {
  const [token, setToken] = useState(localStorage.getItem("token"))
  const [isAdmin, setIsAdmin] = useState(localStorage.getItem("isAdmin") === "true")
  const [loading, setLoading] = useState(false)

  function handleLogin(token, isAdminFlag) {
    setToken(token)
    setIsAdmin(isAdminFlag)
    localStorage.setItem("token", token)
    localStorage.setItem("isAdmin", isAdminFlag)
  }

  function handleLogout() {
    setToken(null)
    setIsAdmin(false)
    localStorage.removeItem("token")
    localStorage.removeItem("isAdmin")
  }

  
  useEffect(() => {
    async function checkMe() {
      if (!token) return
      try {
        setLoading(true)
        const r = await fetch(`${API}/api/auth/me`, {
          headers: { Authorization: `Bearer ${token}` },
        })
        if (r.ok) {
          const me = await r.json()
          if (typeof me.is_admin === "boolean") {
            setIsAdmin(me.is_admin)
            localStorage.setItem("isAdmin", me.is_admin)
          }
        } else if (r.status === 401) {
          handleLogout()
        }
      } catch (_) {
        
      } finally {
        setLoading(false)
      }
    }
    checkMe()
  }, [token])

  return (
    <div>
      {token && (
        <div className="header" style={{position:'relative', padding:'18px 16px'}}>
          <div style={{position:'absolute', right:16, top:14}}>
            {isAdmin && <span style={{marginRight:10, fontWeight:600, color:'#b91c1c'}}>Admin</span>}
            <button className="btn ghost" onClick={handleLogout}>Logout</button>
          </div>
          <div style={{display:'flex', justifyContent:'center'}}>
            <div className="logo" style={{display:'inline-flex', alignItems:'center', gap:10, background:'#ffffffcc', padding:'8px 12px', borderRadius:12, boxShadow:'0 6px 18px rgba(0,0,0,0.06)'}}>
              <img src="/logo.svg" alt="Sweet Shop" width={26} height={26} style={{borderRadius:6}} />
              <span>Sweet Shop</span>
              {loading && <span style={{fontSize:12, color:'#666'}}>checking…</span>}
            </div>
          </div>
        </div>
      )}

      {!token ? (
        <AuthPage onLogin={handleLogin} />
      ) : (
        <SweetsList token={token} isAdmin={isAdmin} />
      )}

      <footer className="site-footer" style={{padding:'28px 12px', color:'#333'}}>
        <div className="container">
          <div style={{display:'grid', gridTemplateColumns:'1.2fr 1fr 1fr', gap:16}}>
            <div style={{display:'flex', alignItems:'center', gap:10}}>
              <img src="/logo.svg" alt="Sweet Shop" width={28} height={28} style={{borderRadius:6}} />
              <div>
                <div style={{fontWeight:800}}>Sweet Shop</div>
                <div style={{fontSize:13, color:'#777'}}>Authentic Indian sweets, made fresh daily.</div>
              </div>
            </div>
            <div>
              <div style={{fontWeight:700, marginBottom:8}}>Contact</div>
              <div style={{fontSize:14}}>Email: sweetshop@example.com</div>
              <div style={{fontSize:14}}>Phone: +91 98765 43210</div>
              <div style={{fontSize:14}}>Address: 12, MG Road, Jaipur, Rajasthan</div>
            </div>
            <div>
              <div style={{fontWeight:700, marginBottom:8}}>Hours</div>
              <div style={{fontSize:14}}>Mon–Sat: 10:00 AM – 9:00 PM</div>
              <div style={{fontSize:14}}>Sun: 11:00 AM – 7:00 PM</div>
              <div style={{fontSize:13, color:'#777', marginTop:10}}>© {new Date().getFullYear()} Sweet Shop</div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
