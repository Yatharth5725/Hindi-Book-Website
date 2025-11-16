#!/usr/bin/env python3
"""
Simple Admin Panel for Hindi Book Website
This provides a web interface to manage books
"""

from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from sqlalchemy.orm import Session
from database import get_db
from models import Book, User
from schemas import BookCreate
from auth import get_current_admin_user
import os

# Create admin app
admin_app = FastAPI(title="Admin Panel", docs_url=None, redoc_url=None)

# Mount static files
admin_app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

@admin_app.get("/", response_class=HTMLResponse)
async def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    """Admin dashboard"""
    try:
        # Get statistics
        total_books = db.query(Book).count()
        available_books = db.query(Book).filter(Book.is_available == True).count()
        total_users = db.query(User).count()
        
        # Get recent books
        recent_books = db.query(Book).order_by(Book.created_at.desc()).limit(5).all()
        
        return templates.TemplateResponse("admin_dashboard.html", {
            "request": request,
            "total_books": total_books,
            "available_books": available_books,
            "total_users": total_users,
            "recent_books": recent_books
        })
    except Exception as e:
        return HTMLResponse(f"<h1>Error loading dashboard: {str(e)}</h1>")

@admin_app.get("/books", response_class=HTMLResponse)
async def admin_books(request: Request, db: Session = Depends(get_db)):
    """Books management page"""
    try:
        books = db.query(Book).order_by(Book.created_at.desc()).all()
        return templates.TemplateResponse("admin_books.html", {
            "request": request,
            "books": books
        })
    except Exception as e:
        return HTMLResponse(f"<h1>Error loading books: {str(e)}</h1>")

@admin_app.get("/add-book", response_class=HTMLResponse)
async def add_book_form(request: Request):
    """Add book form"""
    return templates.TemplateResponse("add_book.html", {
        "request": request,
        "categories": ["धर्म", "कविता", "साहित्य", "दर्शन", "इतिहास", "आधुनिक साहित्य"]
    })

@admin_app.post("/add-book")
async def add_book(
    title: str = Form(...),
    author: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    price: float = Form(...),
    stock_quantity: int = Form(...),
    image_url: str = Form(""),
    db: Session = Depends(get_db)
):
    """Add new book"""
    try:
        book = Book(
            title=title,
            author=author,
            description=description,
            category=category,
            price=price,
            stock_quantity=stock_quantity,
            image_url=image_url or "placeholder.jpg"
        )
        
        db.add(book)
        db.commit()
        db.refresh(book)
        
        return RedirectResponse(url="/books", status_code=303)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding book: {str(e)}")

@admin_app.get("/seed", response_class=HTMLResponse)
async def seed_database(request: Request, db: Session = Depends(get_db)):
    """Seed database with sample data"""
    try:
        # Check if books already exist
        existing_books = db.query(Book).first()
        if existing_books:
            return HTMLResponse("<h1>Database already has books!</h1><p><a href='/'>Go to Dashboard</a></p>")
        
        # Sample books data
        sample_books = [
            Book(title="रामायण", author="महर्षि वाल्मीकि", description="हिंदू धर्म का महाकाव्य", category="धर्म", price=500.0, image_url="ramayana.jpg", stock_quantity=50),
            Book(title="महाभारत", author="महर्षि व्यास", description="विश्व का सबसे बड़ा महाकाव्य", category="धर्म", price=600.0, image_url="mahabharata.jpg", stock_quantity=30),
            Book(title="गोदान", author="मुंशी प्रेमचंद", description="भारतीय किसान जीवन का महान उपन्यास", category="साहित्य", price=400.0, image_url="godan.jpg", stock_quantity=35),
            Book(title="मधुशाला", author="हरिवंश राय बच्चन", description="प्रेम, जीवन और दर्शन की अद्भुत कविता", category="कविता", price=300.0, image_url="madhushala.jpg", stock_quantity=40),
            Book(title="कबीर के दोहे", author="संत कबीर", description="जीवन दर्शन से भरे अमर दोहे", category="कविता", price=200.0, image_url="kabir.jpg", stock_quantity=75),
        ]
        
        for book in sample_books:
            db.add(book)
        
        db.commit()
        
        return HTMLResponse(f"<h1>Database seeded successfully!</h1><p>Added {len(sample_books)} books.</p><p><a href='/'>Go to Dashboard</a></p>")
        
    except Exception as e:
        return HTMLResponse(f"<h1>Error seeding database: {str(e)}</h1>")

if __name__ == "__main__":
    print("🚀 Starting Admin Panel...")
    print("📊 Dashboard: http://localhost:8001")
    print("📚 Books: http://localhost:8001/books")
    print("➕ Add Book: http://localhost:8001/add-book")
    print("🌱 Seed DB: http://localhost:8001/seed")
    
    uvicorn.run(admin_app, host="0.0.0.0", port=8001)
