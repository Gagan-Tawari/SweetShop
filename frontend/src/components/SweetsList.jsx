import React, { useEffect, useState } from "react"
import SweetForm from "./SweetForm.jsx"
import CartModal from "./CartModal.jsx"
import toast from "react-hot-toast"

const API = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000"

const IMG_MAP = {
  "Gulab Jamun": "https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=600",
  Rasgulla: "https://images.unsplash.com/photo-1668236547887-80e7f8bf777f?w=600",
  "Kaju Katli": "https://images.unsplash.com/photo-1511910849309-0dffb4a6e116?w=600",
  Barfi: "https://images.unsplash.com/photo-1603899122236-14f9b1ba2fde?w=600",
  Jalebi: "https://images.unsplash.com/photo-1631452180519-61ee1a7109a2?w=600",
  Laddu: "https://images.unsplash.com/photo-1604335399105-8f1ca1bde342?w=600",
  "Peda": "https://images.unsplash.com/photo-1615485737666-7b36a2a26c6f?w=600",
  "Soan Papdi": "https://images.unsplash.com/photo-1643378222247-9da3dbf6a9a3?w=600",
}

export default function SweetsList({ token, isAdmin }) {
  const [sweets, setSweets] = useState([])
  const [search, setSearch] = useState("")
  const [loading, setLoading] = useState(false)
  const [categories, setCategories] = useState([])
  const [selectedCategory, setSelectedCategory] = useState("")
  const [minPrice, setMinPrice] = useState("")
  const [maxPrice, setMaxPrice] = useState("")
  const [showCart, setShowCart] = useState(false)
  const [cartSweet, setCartSweet] = useState(null)
  const [qty, setQty] = useState(1)

  async function load() {
    setLoading(true)
    try {
      const r = await fetch(`${API}/api/sweets`)
      if (r.ok) {
        const data = await r.json()
        setSweets(data)
      }
    } catch (e) {
      console.error(e)
    } finally {
      setLoading(false)
    }
  }

  async function loadCategories() {
    try {
      const r = await fetch(`${API}/api/sweets/categories`)
      if (r.ok) setCategories(await r.json())
    } catch (_) {}
  }

  useEffect(() => {
    load()
    loadCategories()
  }, [])

  function openCart(s) {
    if (!token) return alert("Please login first.")
    setCartSweet(s)
    setQty(1)
    setShowCart(true)
  }

  async function confirmPurchase() {
    if (!cartSweet) return
    const r = await fetch(`${API}/api/sweets/${cartSweet.id}/purchase?qty=${qty}`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
    })
    if (r.ok) {
      toast.success(`Purchased ${qty} item${qty>1?'s':''}`)
      setShowCart(false)
      setCartSweet(null)
      load()
    } else {
      const err = await r.text()
      toast.error("Purchase failed: " + err)
    }
  }

  async function doSearch() {
    const q = search.trim()
    try {
      const params = new URLSearchParams()
      if (q) params.set("query", q)
      if (selectedCategory) params.set("category", selectedCategory)
      if (minPrice) params.set("min_price", String(minPrice))
      if (maxPrice) params.set("max_price", String(maxPrice))
      const url = params.toString() ? `${API}/api/sweets/search?${params.toString()}` : `${API}/api/sweets`
      const r = await fetch(url)
      if (r.ok) {
        const data = await r.json()
        setSweets(data)
      }
    } catch (e) {
      console.error(e)
    }
  }

  function imgFor(s) {
    return null
  }

  return (
    <div className="container">
      <div className="filter-bar form-card">
        <input
          placeholder="Search sweets..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          onKeyDown={(e) => { if (e.key === 'Enter') doSearch() }}
        />
        <input className="input-sm" placeholder="Min price" type="number" value={minPrice} onChange={(e)=>setMinPrice(e.target.value)} />
        <input className="input-sm" placeholder="Max price" type="number" value={maxPrice} onChange={(e)=>setMaxPrice(e.target.value)} />
        <button className="btn" onClick={doSearch}>Apply</button>
        <button className="btn ghost" onClick={() => { setSearch(""); setSelectedCategory(""); setMinPrice(""); setMaxPrice(""); load() }}>Reset</button>
      </div>
      {categories.length > 0 && (
        <div className="chip-row" style={{marginBottom:14}}>
          <div className={`chip ${selectedCategory === "" ? "active" : ""}`} onClick={() => { setSelectedCategory(""); doSearch() }}>All</div>
          {categories.map((c) => (
            <div key={c} className={`chip ${selectedCategory === c ? "active" : ""}`} onClick={() => { setSelectedCategory(c); doSearch() }}>{c}</div>
          ))}
        </div>
      )}
      <div className="topbar" style={{marginTop:0}}>
        <h3 style={{margin:0}}>Available Sweets {loading ? "— loading..." : `(${sweets.length})`}</h3>
        {isAdmin && (
          <div style={{ width: 360 }}>
            <SweetForm token={token} onSaved={load} />
          </div>
        )}
      </div>
      <div className="grid">
        {sweets.map((s) => (
          <div className="sweet-card" key={s.id}>
            <div>
              <div className="sweet-ph">{(s.name||'?').slice(0,1)}</div>
              <div className="sweet-title">{s.name}</div>
              <div className="sweet-meta">{s.category || "General"}</div>
              <div className="sweet-price">₹{Number(s.price).toFixed(2)}</div>
              <div className="sweet-qty">Stock: {s.quantity}</div>
              {s.description && (
                <div style={{ marginTop: 8, color:'#555', fontSize: 13 }}>{s.description}</div>
              )}
            </div>
            <div className="sweet-actions">
              <button className="btn" disabled={s.quantity === 0} onClick={() => openCart(s)}>🛒 Purchase</button>
              {isAdmin && (
                <SweetForm token={token} onSaved={() => { toast.success("Updated"); load() }} editSweet={s} />
              )}
            </div>
          </div>
        ))}
      </div>

      {showCart && (
        <CartModal
          sweet={cartSweet}
          qty={qty}
          setQty={setQty}
          onClose={() => setShowCart(false)}
          onConfirm={confirmPurchase}
        />
      )}
    </div>
  )
}
