import React from "react"

export default function CartModal({ sweet, qty, setQty, onClose, onConfirm }) {
  if (!sweet) return null
  const inc = () => setQty((n) => Math.min(n + 1, 99))
  const dec = () => setQty((n) => Math.max(1, n - 1))
  const total = (Number(sweet.price) * qty).toFixed(2)

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-card" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div className="modal-title">Shopping Cart</div>
          <button className="modal-close" onClick={onClose}>×</button>
        </div>
        <div className="modal-body">
          <div className="cart-row">
            <div className="cart-name">{sweet.name}</div>
            <div className="cart-price">₹{Number(sweet.price).toFixed(2)} each</div>
            <div className="qty-ctrl">
              <button onClick={dec} className="qty-btn">−</button>
              <input value={qty} onChange={(e)=>{
                let v = parseInt(e.target.value||'1',10); if (Number.isNaN(v)) v=1; v=Math.max(1,Math.min(99,v)); setQty(v)
              }} />
              <button onClick={inc} className="qty-btn">+</button>
            </div>
            <div className="cart-line">₹{total}</div>
          </div>
        </div>
        <div className="modal-footer">
          <div className="total">Total: ₹{total}</div>
          <button className="btn" onClick={onConfirm}>Purchase</button>
        </div>
      </div>
    </div>
  )
}
