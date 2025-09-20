from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Optional
\
from . import database, schemas, crud, auth, deps
from . import models
\
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
app = FastAPI(title="Sweet Shop")
\
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
\
@app.on_event("startup")
def startup():
    database.init_db()
    db = database.SessionLocal()
    try:
        \
        try:
            from .auth import get_password_hash, verify_password
            existing_admin = db.query(models.User).filter(models.User.username == "admin").first()
            if not existing_admin:
                admin_user = models.User(
                    username="admin",
                    hashed_password=get_password_hash("admin123"),
                    is_admin=True,
                )
                db.add(admin_user)
                db.commit()
            else:
                \
                if not verify_password("admin123", existing_admin.hashed_password):
                    existing_admin.hashed_password = get_password_hash("admin123")
                    existing_admin.is_admin = True
                    db.add(existing_admin)
                    db.commit()
        except Exception as e:
            print("Admin seed error:", e)
        if not crud.list_sweets(db):                      
            seed_sweets = [
                {
                    "name": "Gulab Jamun", 
                    "category": "Indian Traditional", 
                    "price": 10.0, 
                    "quantity": 50,
                    "description": "Soft, spongy milk-solid dumplings soaked in rose-flavored sugar syrup",
                    "image_url": "https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=300"
                },
                {
                    "name": "Rasgulla", 
                    "category": "Indian Traditional", 
                    "price": 12.0, 
                    "quantity": 40,
                    "description": "Spongy white balls made from cottage cheese in light sugar syrup",
                    "image_url": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=300"
                },
                {
                    "name": "Kaju Katli", 
                    "category": "Premium", 
                    "price": 25.0, 
                    "quantity": 30,
                    "description": "Diamond-shaped cashew fudge, rich and creamy",
                    "image_url": "https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=300"
                },
                {
                    "name": "Barfi", 
                    "category": "Indian Traditional", 
                    "price": 15.0, 
                    "quantity": 25,
                    "description": "Dense milk-based sweet confection, often garnished with nuts",
                    "image_url": "https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=300"
                },
                {
                    "name": "Ladoo", 
                    "category": "Festival Special", 
                    "price": 8.0, 
                    "quantity": 60,
                    "description": "Round sweet balls made from flour, ghee, and sugar",
                    "image_url": "https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=300"
                },
                {
                    "name": "Soan Papdi", 
                    "category": "Festival Special", 
                    "price": 6.0, 
                    "quantity": 100,
                    "description": "Flaky, cube-shaped sweet with a crisp and layered texture",
                    "image_url": "https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=300"
                },
                {
                    "name": "Jalebi", 
                    "category": "Street Sweet", 
                    "price": 9.0, 
                    "quantity": 70,
                    "description": "Crispy, spiral-shaped sweet soaked in sugar syrup",
                    "image_url": "https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=300"
                },
                {
                    "name": "Chocolate Truffle", 
                    "category": "Modern", 
                    "price": 35.0, 
                    "quantity": 20,
                    "description": "Rich chocolate ganache coated in cocoa powder",
                    "image_url": "https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=300"
                },
                {
                    "name": "Sandesh", 
                    "category": "Bengali Special", 
                    "price": 16.0, 
                    "quantity": 35,
                    "description": "Soft, spongy sweet made from fresh cottage cheese",
                    "image_url": "https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=300"
                },
                {
                    "name": "Mysore Pak", 
                    "category": "South Indian", 
                    "price": 22.0, 
                    "quantity": 15,
                    "description": "Rich, ghee-laden sweet with a crumbly texture",
                    "image_url": "https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=300"
                }
            ]
            for sweet_data in seed_sweets:
                try:
                    crud.create_sweet(db, schemas.SweetCreate(**sweet_data))
                except Exception as e:
                    print(f"Error creating sweet {sweet_data['name']}: {e}")
    finally:
        db.close()
@app.post("/api/auth/register", response_model=schemas.Token)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    return auth.register_user(user, db)
@app.post("/api/auth/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login user and get access token"""
    return auth.login_user(form_data, db)
@app.get("/api/auth/me", response_model=schemas.User)
def me(current_user=Depends(deps.get_current_user)):
    """Return current authenticated user's profile"""
    return current_user
@app.post("/api/sweets", response_model=schemas.Sweet)
def create_sweet(
    sweet: schemas.SweetCreate,
    db: Session = Depends(get_db),
    current_user=Depends(deps.get_current_admin),
):
    """Create a new sweet (Admin only)"""
    return crud.create_sweet(db, sweet)
@app.get("/api/sweets", response_model=List[schemas.Sweet])
def list_sweets(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all sweets with pagination"""
    return crud.list_sweets(db, skip=skip, limit=limit)
@app.get("/api/sweets/search", response_model=List[schemas.Sweet])
def search_sweets(
    query: Optional[str] = Query(None, description="Search in name and description"),
    category: Optional[str] = Query(None, description="Filter by category"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price"),
    db: Session = Depends(get_db)
):
    """Advanced search for sweets"""
    return crud.search_sweets(db, query=query, category=category, min_price=min_price, max_price=max_price)
@app.get("/api/sweets/categories", response_model=List[str])
def get_categories(db: Session = Depends(get_db)):
    """Get all available categories"""
    return crud.get_categories(db)
@app.get("/api/sweets/{sweet_id}", response_model=schemas.Sweet)
def get_sweet(
    sweet_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific sweet by ID"""
    return crud.get_sweet_by_id(db, sweet_id)
@app.put("/api/sweets/{sweet_id}", response_model=schemas.Sweet)
def update_sweet(
    sweet_id: int,
    sweet: schemas.SweetUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(deps.get_current_admin),
):
    """Update a sweet (Admin only)"""
    return crud.update_sweet(db, sweet_id, sweet)
@app.delete("/api/sweets/{sweet_id}", response_model=schemas.MessageResponse)
def delete_sweet(
    sweet_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(deps.get_current_admin),
):
    """Delete a sweet (Admin only)"""
    return crud.delete_sweet(db, sweet_id)
@app.post("/api/sweets/{sweet_id}/purchase", response_model=schemas.Sweet)
def purchase_sweet(
    sweet_id: int,
    qty: int = Query(1, ge=1, description="Quantity to purchase"),
    db: Session = Depends(get_db),
    current_user=Depends(deps.get_current_user),
):
    """Purchase a sweet (authenticated users)"""
    return crud.purchase_sweet(db, sweet_id, qty)
@app.post("/api/sweets/{sweet_id}/restock", response_model=schemas.Sweet)
def restock_sweet(
    sweet_id: int,
    qty: int = Query(1, ge=1, description="Quantity to restock"),
    db: Session = Depends(get_db),
    current_user=Depends(deps.get_current_admin),
):
    """Restock a sweet (Admin only)"""
    return crud.restock_sweet(db, sweet_id, qty)
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")
