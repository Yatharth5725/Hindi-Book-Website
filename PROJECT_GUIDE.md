# Hindi Book Website - Complete Integration Guide

## 🎯 Project Overview

This is a full-stack Hindi book e-commerce website with:
- **Frontend**: React + TypeScript + Vite + Tailwind CSS + Shadcn/ui
- **Backend**: FastAPI + SQLAlchemy + SQLite + JWT Authentication
- **Features**: Book catalog, user authentication, shopping cart, admin panel

## 📁 Project Structure

```
hindi book website/
├── Backend/                    # FastAPI Backend
│   ├── main.py                # Main API server
│   ├── models.py              # Database models
│   ├── schemas.py             # Pydantic schemas
│   ├── auth.py                # Authentication & JWT
│   ├── database.py            # Database configuration
│   ├── requirements.txt       # Python dependencies
│   ├── hindi_books.db         # SQLite database
│   └── .env.example           # Environment variables template
├── src/                       # React Frontend
│   ├── components/            # Reusable UI components
│   │   ├── ui/               # Shadcn/ui components
│   │   ├── BookCard.tsx      # Book display component
│   │   ├── Header.tsx        # Navigation header
│   │   └── ...
│   ├── pages/                # Page components
│   ├── hooks/                # Custom React hooks
│   └── lib/                  # Utility functions
├── package.json              # Frontend dependencies
├── vite.config.ts            # Vite configuration
└── tailwind.config.ts        # Tailwind CSS configuration
```

## 🚀 Getting Started

### 1. Backend Setup

```bash
# Navigate to backend directory
cd "C:\Users\ANUBHAV SHARMA\OneDrive\Desktop\Hindi Book Website\hindi book website\Backend"

# Activate virtual environment
.\backend-env\Scripts\Activate.ps1

# Install dependencies (if not already installed)
pip install -r requirements.txt

# Create .env file for production
copy .env.example .env
# Edit .env with your secure values

# Run the backend server
python main.py
```

**Backend will run on:** `http://localhost:8000`
**API Documentation:** `http://localhost:8000/docs`

### 2. Frontend Setup

```bash
# Navigate to project root
cd "C:\Users\ANUBHAV SHARMA\OneDrive\Desktop\Hindi Book Website\hindi book website"

# Install dependencies
npm install

# Run the frontend development server
npm run dev
```

**Frontend will run on:** `http://localhost:8080`

## 🔗 API Integration Points

### Key Backend Endpoints

| Endpoint | Method | Purpose | Authentication |
|----------|--------|---------|----------------|
| `/books` | GET | Get paginated books | No |
| `/books/{id}` | GET | Get single book | No |
| `/books` | POST | Create book | Admin |
| `/categories` | GET | Get book categories | No |
| `/register` | POST | User registration | No |
| `/login` | POST | User login | No |
| `/cart` | GET | Get user cart | User |
| `/cart` | POST | Add to cart | User |
| `/users/me` | GET | Get user profile | User |

### Frontend Integration Strategy

1. **API Service Layer** - Create centralized API calls
2. **State Management** - Use React Query for server state
3. **Authentication Context** - Manage user login state
4. **Component Updates** - Connect UI to real data

## 🛠️ Development Workflow

### Phase 1: Basic Integration
1. Set up API service functions
2. Connect BookCard to real data
3. Implement basic book listing
4. Add loading states

### Phase 2: Authentication
1. Create login/register forms
2. Implement JWT token management
3. Add protected routes
4. Update header with user info

### Phase 3: Shopping Cart
1. Implement cart state management
2. Connect "Add to Cart" functionality
3. Create cart page/component
4. Add cart persistence

### Phase 4: Advanced Features
1. Search functionality
2. Category filtering
3. Admin panel
4. Order management

## 📚 Learning Resources

### FastAPI (Backend)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [JWT Authentication](https://fastapi.tiangolo.com/tutorial/security/)

### React (Frontend)
- [React Documentation](https://react.dev/)
- [React Query](https://tanstack.com/query/latest)
- [Shadcn/ui Components](https://ui.shadcn.com/)

### Integration
- [REST API Best Practices](https://restfulapi.net/)
- [CORS Configuration](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)

## 🔧 Next Steps

1. **Start with API Integration** - Create service functions
2. **Test Backend** - Use Postman or API docs
3. **Update Components** - Connect to real data
4. **Add Authentication** - Implement login flow
5. **Build Features** - Cart, search, admin panel

## 🐛 Common Issues & Solutions

### Backend Issues
- **Port conflicts**: Change ports in main.py or vite.config.ts
- **Database errors**: Check SQLite file permissions
- **CORS errors**: Verify CORS middleware configuration

### Frontend Issues
- **Build errors**: Check TypeScript types
- **API calls failing**: Verify backend is running
- **Styling issues**: Check Tailwind CSS classes

## 📞 Support

- Check the API documentation at `/docs`
- Review error logs in browser console
- Test API endpoints with Postman
- Check backend logs for detailed errors
