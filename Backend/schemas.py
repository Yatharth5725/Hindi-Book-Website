from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class BookCreate(BaseModel):
    title: str
    author: str
    description: str
    category: str
    price: float
    image_url: str
    stock_quantity: Optional[int] = 0

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    stock_quantity: Optional[int] = None
    is_available: Optional[bool] = None

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    description: str
    category: str
    price: float
    image_url: str
    stock_quantity: int
    is_available: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str

class CartItemResponse(BaseModel):
    id: int
    book: BookResponse
    quantity: int
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class CartAdd(BaseModel):
    book_id: int
    quantity: Optional[int] = 1

class CartUpdate(BaseModel):
    quantity: int

class PaginatedBooks(BaseModel):
    books: List[BookResponse]
    total: int
    page: int
    per_page: int
    pages: int

class CartSummary(BaseModel):
    items: List[CartItemResponse]
    total_items: int
    total_price: float

class BulkBookCreate(BaseModel):
    books: List[BookCreate]

class BulkOperationResponse(BaseModel):
    success_count: int
    failed_count: int
    errors: List[str]
    