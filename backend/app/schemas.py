from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
\
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
class User(BaseModel):
    id: int
    username: str
    is_admin: bool = False
    created_at: datetime
    \
    class Config:
        from_attributes = True                                        
class Token(BaseModel):
    access_token: str
    token_type: str
    is_admin: bool = False
class SweetBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    category: str = Field(..., min_length=1, max_length=50)
    price: float = Field(..., gt=0)
    quantity: int = Field(..., ge=0)
    description: Optional[str] = Field(None, max_length=500)
    image_url: Optional[str] = None
class SweetCreate(SweetBase):
    pass
class SweetUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    price: Optional[float] = Field(None, gt=0)
    quantity: Optional[int] = Field(None, ge=0)
    description: Optional[str] = Field(None, max_length=500)
    image_url: Optional[str] = None
class Sweet(SweetBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    \
    class Config:
        from_attributes = True
class MessageResponse(BaseModel):
    message: str
class ErrorResponse(BaseModel):
    detail: str
