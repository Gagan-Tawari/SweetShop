import React, { useState } from "react"

const API = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000"

export default function SweetForm({ token, onSaved, editSweet }) {
  const [name, setName] = useState(editSweet ? editSweet.name : "")
  const [category, setCategory] = useState(editSweet ? editSweet.category : "")
  const [price, setPrice] = useState(editSweet ? editSweet.price : "")
  const [quantity, setQuantity] = useState(editSweet ? editSweet.quantity : "")
  const [description, setDescription] = useState(editSweet ? editSweet.description || "" : "")
  const [imageUrl, setImageUrl] = useState(editSweet ? editSweet.image_url || "" : "")
  const [error, setError] = useState("")

  async function handleSubmit(e) {
    e.preventDefault()
    if (!token) {
      setError("Login required")
      return
    }

    const base = { name, category, price: Number(price), quantity: Number(quantity), description, image_url: imageUrl }
    
    const body = editSweet
      ? Object.fromEntries(Object.entries(base).filter(([_, v]) => v !== "" && v !== null && v !== undefined && !(typeof v === 'number' && Number.isNaN(v))))
      : base
    const url = editSweet ? `${API}/api/sweets/${editSweet.id}` : `${API}/api/sweets`
    const method = editSweet ? "PUT" : "POST"

    try {
      const r = await fetch(url, {
        method,
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(body),
      })
      if (r.ok) {
        setError("")
        if (!editSweet) {
          setName("")
          setCategory("")
          setPrice("")
          setQuantity("")
          setDescription("")
          setImageUrl("")
        }
        onSaved()
      } else {
        setError("Error: " + (await r.text()))
      }
    } catch (e) {
      setError("Error: " + e.message)
    }
  }

  return (
    <form className="sweet-form" onSubmit={handleSubmit}>
      {!editSweet && <h4>Add New Sweet</h4>}
      {editSweet && <h4>Edit: {editSweet.name}</h4>}
      <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Name" />
      <input value={category} onChange={(e) => setCategory(e.target.value)} placeholder="Category" />
      <input
        value={price}
        onChange={(e) => setPrice(e.target.value)}
        placeholder="Price"
        type="number"
      />
      <input
        value={quantity}
        onChange={(e) => setQuantity(e.target.value)}
        placeholder="Quantity"
        type="number"
      />
      <textarea
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        placeholder="Description (optional)"
        rows={3}
      />
      <input
        value={imageUrl}
        onChange={(e) => setImageUrl(e.target.value)}
        placeholder="Image URL (optional)"
      />
      <button className="btn" type="submit">{editSweet ? "Update" : "Add"}</button>
      {error && <div className="error">{error}</div>}
    </form>
  )
}
