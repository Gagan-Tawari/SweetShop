from sqlalchemy.orm import Session
from sqlalchemy import or_
from . import models, schemas
from fastapi import HTTPException, status
from typing import List, Optional
\
\
\
\
\
def create_user(db: Session, user: schemas.UserCreate, hashed_password: str, is_admin: bool = False):
    """Create a new user"""
    db_user = models.User(
        username=user.username, 
        hashed_password=hashed_password,
        is_admin=is_admin
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
def get_user_by_username(db: Session, username: str):
    """Get user by username"""
    return db.query(models.User).filter(models.User.username == username).first()
def get_user_by_id(db: Session, user_id: int):
    """Get user by ID"""
    return db.query(models.User).filter(models.User.id == user_id).first()
def create_sweet(db: Session, sweet: schemas.SweetCreate):
    """Create a new sweet"""
    \
    existing = db.query(models.Sweet).filter(models.Sweet.name == sweet.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Sweet with name '{sweet.name}' already exists"
        )
    db_sweet = models.Sweet(
        name=sweet.name,
        category=sweet.category,
        price=sweet.price,
        quantity=sweet.quantity,
        description=sweet.description,
        image_url=sweet.image_url
    )
    db.add(db_sweet)
    db.commit()
    db.refresh(db_sweet)
    return db_sweet
def get_sweet_by_id(db: Session, sweet_id: int):
    """Get sweet by ID"""
    sweet = db.query(models.Sweet).filter(models.Sweet.id == sweet_id).first()
    if not sweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Sweet not found"
        )
    return sweet
def list_sweets(db: Session, skip: int = 0, limit: int = 100):
    """List all sweets with pagination"""
    return db.query(models.Sweet).offset(skip).limit(limit).all()
def search_sweets(db: Session, query: str = None, category: str = None, min_price: float = None, max_price: float = None):
    """Advanced search for sweets"""
    db_query = db.query(models.Sweet)
    \
    if query:
        db_query = db_query.filter(
            or_(
                models.Sweet.name.ilike(f"%{query}%"),
                models.Sweet.description.ilike(f"%{query}%")
            )
        )
    if category:
        db_query = db_query.filter(models.Sweet.category.ilike(f"%{category}%"))
    if min_price is not None:
        db_query = db_query.filter(models.Sweet.price >= min_price)
    if max_price is not None:
        db_query = db_query.filter(models.Sweet.price <= max_price)
    return db_query.all()
def update_sweet(db: Session, sweet_id: int, sweet_update: schemas.SweetUpdate):
    """Update a sweet"""
    db_sweet = get_sweet_by_id(db, sweet_id)
    \
    update_data = sweet_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_sweet, field, value)
    db.commit()
    db.refresh(db_sweet)
    return db_sweet
def delete_sweet(db: Session, sweet_id: int):
    """Delete a sweet"""
    db_sweet = get_sweet_by_id(db, sweet_id)
    db.delete(db_sweet)
    db.commit()
    return {"message": "Sweet deleted successfully"}
def purchase_sweet(db: Session, sweet_id: int, qty: int = 1):
    """Purchase a sweet (decrease quantity)"""
    if qty <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Quantity must be greater than 0"
        )
    db_sweet = get_sweet_by_id(db, sweet_id)
    \
    if db_sweet.quantity < qty:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Not enough stock. Available: {db_sweet.quantity}, Requested: {qty}"
        )
    db_sweet.quantity -= qty
    db.commit()
    db.refresh(db_sweet)
    return db_sweet
def restock_sweet(db: Session, sweet_id: int, qty: int = 1):
    """Restock a sweet (increase quantity)"""
    if qty <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Quantity must be greater than 0"
        )
    db_sweet = get_sweet_by_id(db, sweet_id)
    db_sweet.quantity += qty
    db.commit()
    db.refresh(db_sweet)
    return db_sweet
def get_categories(db: Session):
    """Get all unique categories"""
    categories = db.query(models.Sweet.category).distinct().all()
    return [cat[0] for cat in categories if cat[0]]
