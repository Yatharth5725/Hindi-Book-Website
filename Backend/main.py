from fastapi import FastAPI, HTTPException, Depends, status, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
import logging
import math
import os

# Import our organized modules
from database import get_db, engine, create_tables, check_db_connection
from models import Book, User, CartItem, Base
from schemas import (
    BookCreate, BookResponse, BookUpdate, UserCreate, UserResponse, 
    UserLogin, CartItemResponse, Token, CartAdd, CartUpdate,
    PaginatedBooks, CartSummary, BulkBookCreate, BulkOperationResponse
)
from auth import (
    create_access_token, get_current_user, get_current_admin_user,
    hash_password, verify_password
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create database tables
try:
    create_tables()
    logger.info("✅ Database initialized successfully")
except Exception as e:
    logger.error(f"❌ Database initialization error: {str(e)}")

# App initialization
app = FastAPI(
    title="Hindi Books API",
    description="API for Hindi Literature Bookstore with Image Support",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Create static directory if it doesn't exist
try:
    os.makedirs("static/images/books", exist_ok=True)
    logger.info("✅ Static directories ready")
except Exception as e:
    logger.warning(f"⚠️  Static directory warning: {str(e)}")

# Mount static files for images
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except Exception as e:
    logger.warning(f"⚠️  Static files mount warning: {str(e)}")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development - restrict in production
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# ==================== UTILITY FUNCTIONS ====================

def get_image_url(image_filename: Optional[str]) -> Optional[str]:
    """Convert image filename to full URL"""
    if not image_filename:
        return None
    return f"/static/images/books/{image_filename}"

# ==================== HEALTH & ROOT ENDPOINTS ====================

@app.get("/health")
def health_check():
    """Health check endpoint"""
    db_status = check_db_connection()
    return {
        "status": "healthy" if db_status else "unhealthy",
        "database": "connected" if db_status else "disconnected",
        "static_files": os.path.exists("static/images/books"),
        "version": "2.0.0"
    }

@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "message": "Hindi Books API is running!",
        "version": "2.0.0",
        "features": ["Image Support", "Extended Book Collection", "Admin Dashboard"],
        "docs": "/docs",
        "health": "/health",
        "static_files": "/static"
    }

# ==================== BOOK ENDPOINTS ====================

@app.get("/books", response_model=PaginatedBooks)
def get_books(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(12, ge=1, le=50, description="Items per page"),
    category: Optional[str] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(None, description="Search in title or author"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price filter"),
    sort_by: Optional[str] = Query("created_at", description="Sort by: title, author, price, created_at"),
    sort_order: Optional[str] = Query("desc", description="Sort order: asc, desc"),
    db: Session = Depends(get_db)
):
    """Get books with pagination, filtering, and sorting"""
    try:
        # Build query
        query = db.query(Book).filter(Book.is_available == True)
        
        # Apply filters
        if category:
            query = query.filter(Book.category == category)
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                (Book.title.ilike(search_term)) | 
                (Book.author.ilike(search_term)) |
                (Book.description.ilike(search_term))
            )
        if min_price is not None:
            query = query.filter(Book.price >= min_price)
        if max_price is not None:
            query = query.filter(Book.price <= max_price)
        
        # Apply sorting
        if sort_by in ["title", "author", "price", "created_at"]:
            sort_column = getattr(Book, sort_by)
            if sort_order == "desc":
                query = query.order_by(sort_column.desc())
            else:
                query = query.order_by(sort_column.asc())
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        skip = (page - 1) * per_page
        books = query.offset(skip).limit(per_page).all()
        
        # Calculate total pages
        pages = math.ceil(total / per_page) if total > 0 else 1
        
        return PaginatedBooks(
            books=[
                {
                    "id": book.id,
                    "title": book.title,
                    "author": book.author,
                    "description": book.description,
                    "category": book.category,
                    "price": book.price,
                    "image_url": get_image_url(book.image_url),
                    "stock_quantity": book.stock_quantity,
                    "is_available": book.is_available,
                    "created_at": book.created_at
                }
                for book in books
            ],
            total=total,
            page=page,
            per_page=per_page,
            pages=pages
        )
    except Exception as e:
        logger.error(f"Error fetching books: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """Get single book by ID"""
    try:
        book = db.query(Book).filter(Book.id == book_id, Book.is_available == True).first()
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        return {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "description": book.description,
            "category": book.category,
            "price": book.price,
            "image_url": get_image_url(book.image_url),
            "stock_quantity": book.stock_quantity,
            "is_available": book.is_available,
            "created_at": book.created_at
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching book {book_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/books", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(
    book: BookCreate, 
    current_user: dict = Depends(get_current_admin_user), 
    db: Session = Depends(get_db)
):
    """Create new book (Admin only)"""
    try:
        db_book = Book(**book.dict())
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        logger.info(f"Book created: {db_book.title} by admin {current_user['sub']}")
        return db_book
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating book: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not create book")

@app.post("/books/bulk", response_model=BulkOperationResponse)
def create_books_bulk(
    bulk_books: BulkBookCreate,
    current_user: dict = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Create multiple books at once (Admin only)"""
    success_count = 0
    failed_count = 0
    errors = []
    
    try:
        for book_data in bulk_books.books:
            try:
                db_book = Book(**book_data.dict())
                db.add(db_book)
                db.commit()
                db.refresh(db_book)
                success_count += 1
            except Exception as e:
                failed_count += 1
                errors.append(f"Failed to create '{book_data.title}': {str(e)}")
                db.rollback()
        
        logger.info(f"Bulk create: {success_count} success, {failed_count} failed by admin {current_user['sub']}")
        return BulkOperationResponse(
            success_count=success_count,
            failed_count=failed_count,
            errors=errors
        )
    except Exception as e:
        logger.error(f"Error in bulk create: {str(e)}")
        raise HTTPException(status_code=500, detail="Bulk operation failed")

@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int,
    book_update: BookUpdate,
    current_user: dict = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Update book (Admin only)"""
    try:
        db_book = db.query(Book).filter(Book.id == book_id).first()
        if not db_book:
            raise HTTPException(status_code=404, detail="Book not found")
        
        # Update fields
        update_data = book_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_book, field, value)
        
        db.commit()
        db.refresh(db_book)
        logger.info(f"Book updated: {db_book.title} by admin {current_user['sub']}")
        return db_book
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating book {book_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not update book")

@app.delete("/books/{book_id}")
def delete_book(
    book_id: int,
    current_user: dict = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Soft delete book (Admin only)"""
    try:
        db_book = db.query(Book).filter(Book.id == book_id).first()
        if not db_book:
            raise HTTPException(status_code=404, detail="Book not found")
        
        db_book.is_available = False
        db.commit()
        logger.info(f"Book deleted: {db_book.title} by admin {current_user['sub']}")
        return {"message": "Book deleted successfully", "book_id": book_id}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting book {book_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not delete book")

@app.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    """Get all book categories with counts"""
    try:
        categories = db.query(
            Book.category, 
            func.count(Book.id).label('count')
        ).filter(
            Book.is_available == True
        ).group_by(Book.category).all()
        
        return [{"name": cat[0], "count": cat[1]} for cat in categories if cat[0]]
    except Exception as e:
        logger.error(f"Error fetching categories: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not fetch categories")

# ==================== USER ENDPOINTS ====================

@app.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register new user"""
    try:
        # Check if user exists
        existing_user = db.query(User).filter(
            (User.username == user.username) | (User.email == user.email)
        ).first()
        if existing_user:
            if existing_user.username == user.username:
                raise HTTPException(status_code=400, detail="Username already registered")
            else:
                raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create new user
        hashed_password = hash_password(user.password)
        db_user = User(
            username=user.username, 
            email=user.email, 
            hashed_password=hashed_password,
            is_admin=False
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        logger.info(f"New user registered: {db_user.username}")
        return db_user
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error registering user: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not register user")

@app.post("/login", response_model=Token)
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    """User login"""
    try:
        user = db.query(User).filter(User.username == user_login.username).first()
        if not user or not verify_password(user_login.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid username or password",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        access_token = create_access_token(
            data={"sub": user.username, "is_admin": user.is_admin}
        )
        logger.info(f"User logged in: {user.username}")
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        raise HTTPException(status_code=500, detail="Login failed")

@app.get("/users/me", response_model=UserResponse)
def get_current_user_info(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user information"""
    try:
        username = current_user["sub"]
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching user info: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not fetch user information")

# ==================== CART ENDPOINTS ====================

@app.post("/cart", status_code=status.HTTP_201_CREATED)
def add_to_cart(
    cart_item: CartAdd, 
    current_user: dict = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Add item to cart"""
    try:
        username = current_user["sub"]
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check if book exists and is available
        book = db.query(Book).filter(
            Book.id == cart_item.book_id, 
            Book.is_available == True
        ).first()
        if not book:
            raise HTTPException(status_code=404, detail="Book not found or unavailable")
        
        # Check stock
        if book.stock_quantity < cart_item.quantity:
            raise HTTPException(
                status_code=400, 
                detail=f"Only {book.stock_quantity} items available in stock"
            )
        
        # Check if item already in cart
        existing_item = db.query(CartItem).filter(
            CartItem.user_id == user.id, 
            CartItem.book_id == cart_item.book_id
        ).first()
        
        if existing_item:
            new_quantity = existing_item.quantity + cart_item.quantity
            if new_quantity > book.stock_quantity:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Cannot add {cart_item.quantity} more. Only {book.stock_quantity - existing_item.quantity} available"
                )
            existing_item.quantity = new_quantity
        else:
            new_item = CartItem(
                user_id=user.id, 
                book_id=cart_item.book_id, 
                quantity=cart_item.quantity
            )
            db.add(new_item)
        
        db.commit()
        logger.info(f"Added to cart: Book {cart_item.book_id} for user {username}")
        return {"message": "Added to cart successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error adding to cart: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not add to cart")

@app.get("/cart", response_model=CartSummary)
def get_cart(
    current_user: dict = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Get user's cart"""
    try:
        username = current_user["sub"]
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        cart_items = db.query(CartItem).filter(CartItem.user_id == user.id).all()
        
        items = []
        total_price = 0.0
        total_items = 0
        
        for item in cart_items:
            book = db.query(Book).filter(Book.id == item.book_id).first()
            if book and book.is_available:
                cart_item_response = CartItemResponse(
                    id=item.id,
                    book={
                        "id": book.id,
                        "title": book.title,
                        "author": book.author,
                        "description": book.description,
                        "category": book.category,
                        "price": book.price,
                        "image_url": get_image_url(book.image_url),
                        "stock_quantity": book.stock_quantity,
                        "is_available": book.is_available,
                        "created_at": book.created_at
                    },
                    quantity=item.quantity,
                    created_at=item.created_at
                )
                items.append(cart_item_response)
                total_price += book.price * item.quantity
                total_items += item.quantity
        
        return CartSummary(
            items=items,
            total_items=total_items,
            total_price=round(total_price, 2)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching cart: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not fetch cart")

@app.put("/cart/{cart_item_id}")
def update_cart_item(
    cart_item_id: int,
    cart_update: CartUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update cart item quantity"""
    try:
        username = current_user["sub"]
        user = db.query(User).filter(User.username == username).first()
        
        cart_item = db.query(CartItem).filter(
            CartItem.id == cart_item_id,
            CartItem.user_id == user.id
        ).first()
        
        if not cart_item:
            raise HTTPException(status_code=404, detail="Cart item not found")
        
        # Check book availability and stock
        book = db.query(Book).filter(Book.id == cart_item.book_id).first()
        if not book or not book.is_available:
            raise HTTPException(status_code=400, detail="Book no longer available")
        
        if book.stock_quantity < cart_update.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Only {book.stock_quantity} items available in stock"
            )
        
        cart_item.quantity = cart_update.quantity
        db.commit()
        
        logger.info(f"Updated cart item {cart_item_id} for user {username}")
        return {"message": "Cart item updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating cart item: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not update cart item")

@app.delete("/cart/{cart_item_id}")
def remove_from_cart(
    cart_item_id: int, 
    current_user: dict = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Remove item from cart"""
    try:
        username = current_user["sub"]
        user = db.query(User).filter(User.username == username).first()
        
        cart_item = db.query(CartItem).filter(
            CartItem.id == cart_item_id, 
            CartItem.user_id == user.id
        ).first()
        
        if not cart_item:
            raise HTTPException(status_code=404, detail="Cart item not found")
        
        db.delete(cart_item)
        db.commit()
        
        logger.info(f"Removed cart item {cart_item_id} for user {username}")
        return {"message": "Removed from cart successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error removing from cart: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not remove from cart")

@app.delete("/cart")
def clear_cart(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Clear user's entire cart"""
    try:
        username = current_user["sub"]
        user = db.query(User).filter(User.username == username).first()
        
        deleted_count = db.query(CartItem).filter(CartItem.user_id == user.id).delete()
        db.commit()
        
        logger.info(f"Cleared {deleted_count} items from cart for user {username}")
        return {"message": f"Cleared {deleted_count} items from cart"}
    except Exception as e:
        db.rollback()
        logger.error(f"Error clearing cart: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not clear cart")

# ==================== ADMIN ENDPOINTS ====================

@app.post("/admin/users/{username}/make-admin")
def make_admin(
    username: str, 
    current_user: dict = Depends(get_current_admin_user), 
    db: Session = Depends(get_db)
):
    """Make user an admin (Admin only)"""
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if user.is_admin:
            return {"message": f"{username} is already an admin"}
        
        user.is_admin = True
        db.commit()
        
        logger.info(f"User {username} made admin by {current_user['sub']}")
        return {"message": f"{username} is now an admin"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error making user admin: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not update user privileges")

@app.get("/admin/users", response_model=List[UserResponse])
def get_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: dict = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get all users (Admin only)"""
    try:
        users = db.query(User).offset(skip).limit(limit).all()
        return users
    except Exception as e:
        logger.error(f"Error fetching users: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not fetch users")

@app.get("/admin/stats")
def get_admin_stats(
    current_user: dict = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get admin statistics"""
    try:
        total_books = db.query(func.count(Book.id)).filter(Book.is_available == True).scalar()
        total_users = db.query(func.count(User.id)).scalar()
        total_categories = db.query(func.count(func.distinct(Book.category))).filter(Book.is_available == True).scalar()
        
        # Low stock books (less than 10 in stock)
        low_stock_books = db.query(Book).filter(
            Book.is_available == True,
            Book.stock_quantity < 10
        ).limit(10).all()
        
        # Recent activities
        recent_users = db.query(User).order_by(User.created_at.desc()).limit(5).all()
        recent_books = db.query(Book).order_by(Book.created_at.desc()).limit(5).all()
        
        return {
            "total_books": total_books,
            "total_users": total_users,
            "total_categories": total_categories,
            "low_stock_books": [
                {"id": b.id, "title": b.title, "stock": b.stock_quantity} 
                for b in low_stock_books
            ],
            "recent_users": [
                {"username": u.username, "created_at": u.created_at} 
                for u in recent_users
            ],
            "recent_books": [
                {"title": b.title, "author": b.author, "created_at": b.created_at} 
                for b in recent_books
            ]
        }
    except Exception as e:
        logger.error(f"Error fetching admin stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not fetch statistics")

# ==================== SEED & SEARCH ENDPOINTS ====================

@app.post("/seed")
def seed_data(db: Session = Depends(get_db)):
    """Seed initial data"""
    try:
        # Check if data already exists
        existing_books = db.query(Book).first()
        existing_admin = db.query(User).filter(User.username == "admin").first()
        
        if existing_books and existing_admin:
            return {"message": "Data already exists", "status": "skipped"}
        
        # Create default admin user if doesn't exist
        if not existing_admin:
            admin_user = User(
                username="admin",
                email="admin@hindibooks.com",
                hashed_password=hash_password("Admin@123"),
                is_admin=True
            )
            db.add(admin_user)
            logger.info("Default admin user created")
        
        # Add sample books if needed (currently empty - use upload script)
        books = []
        
        if books:
            for book in books:
                db.add(book)
        
        db.commit()
        logger.info("Database seeded successfully")
        return {
            "message": "Seed completed successfully!",
            "books_added": len(books),
            "admin_created": not existing_admin,
            "note": "Use upload_books.py script to add books, or add them via /docs interface"
        }
    except Exception as e:
        db.rollback()
        logger.error(f"Error seeding data: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not seed data")

@app.get("/search")
def search_books(
    q: str = Query(..., min_length=2, description="Search query"),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Quick search endpoint for autocomplete"""
    try:
        search_term = f"%{q}%"
        books = db.query(Book).filter(
            Book.is_available == True,
            (Book.title.ilike(search_term)) | 
            (Book.author.ilike(search_term))
        ).limit(limit).all()
        
        return {
            "query": q,
            "results": [
                {
                    "id": book.id,
                    "title": book.title,
                    "author": book.author,
                    "description": book.description,
                    "category": book.category,
                    "price": book.price,
                    "image_url": get_image_url(book.image_url),
                    "stock_quantity": book.stock_quantity,
                    "is_available": book.is_available,
                    "created_at": book.created_at.isoformat() if book.created_at else None
                }
                for book in books
            ],
            "count": len(books)
        }
    except Exception as e:
        logger.error(f"Error searching books: {str(e)}")
        raise HTTPException(status_code=500, detail="Search failed")

# ==================== ERROR HANDLERS ====================

@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {"error": "Resource not found", "status_code": 404}

@app.exception_handler(422)
async def validation_error_handler(request, exc):
    return {"error": "Validation failed", "details": exc.detail, "status_code": 422}

@app.exception_handler(500)
async def internal_server_error_handler(request, exc):
    logger.error(f"Internal server error: {str(exc)}")
    return {"error": "Internal server error", "status_code": 500}

# ==================== RUN APP ====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)