# Frontend-Backend Integration Steps

## 🚀 Quick Start Integration

### Step 1: Start Backend Server
```powershell
# Open PowerShell as Administrator
cd "C:\Users\ANUBHAV SHARMA\OneDrive\Desktop\Hindi Book Website\hindi book website\Backend"
.\backend-env\Scripts\Activate.ps1
python main.py
```

**Expected Output:**
```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Step 2: Start Frontend Server
```powershell
# Open new PowerShell window
cd "C:\Users\ANUBHAV SHARMA\OneDrive\Desktop\Hindi Book Website\hindi book website"
npm run dev
```

**Expected Output:**
```
  VITE v5.4.19  ready in 1234 ms

  ➜  Local:   http://localhost:8080/
  ➜  Network: use --host to expose
```

### Step 3: Test Integration

#### 3.1 Test Backend API
1. Open browser: `http://localhost:8000/docs`
2. Test these endpoints:
   - `GET /health` - Health check
   - `GET /books` - Get books
   - `GET /categories` - Get categories

#### 3.2 Test Frontend
1. Open browser: `http://localhost:8080`
2. Check these features:
   - ✅ Page loads without errors
   - ✅ Featured books section shows data
   - ✅ Book cards display properly
   - ✅ Login/Register dialog works

#### 3.3 Test Full Integration
1. Click user icon in header
2. Register a new account
3. Login with the account
4. Try adding books to cart
5. Check browser console for errors

## 🔧 Integration Features Already Implemented

### ✅ Backend Features
- REST API with FastAPI
- JWT Authentication
- SQLite Database
- Book CRUD operations
- User management
- Shopping cart functionality
- CORS enabled for frontend

### ✅ Frontend Features
- React + TypeScript
- API service layer
- Authentication context
- React Query for state management
- Real-time data fetching
- Error handling
- Loading states

### ✅ Integration Points
- API calls from frontend to backend
- JWT token management
- Real-time data synchronization
- Error handling across layers
- Responsive UI updates

## 🧪 Testing Your Integration

### Test 1: Basic Data Flow
1. Open `http://localhost:8080`
2. Check if books are loading
3. Open browser DevTools (F12)
4. Check Network tab for API calls
5. Verify no CORS errors

### Test 2: Authentication Flow
1. Click user icon in header
2. Try to register: username, email, password
3. Try to login with same credentials
4. Check if user state updates
5. Try adding book to cart

### Test 3: Cart Functionality
1. Login to your account
2. Click "Add to Cart" on any book
3. Check if cart updates
4. Verify success/error messages
5. Check browser console for errors

## 🐛 Common Issues & Solutions

### Issue 1: Backend Not Starting
**Error:** `ModuleNotFoundError` or port conflicts
**Solution:**
```powershell
# Activate virtual environment first
.\backend-env\Scripts\Activate.ps1
# Install missing dependencies
pip install -r requirements.txt
# Change port if needed (edit main.py line 947)
```

### Issue 2: Frontend Not Loading Data
**Error:** "Failed to fetch" or CORS errors
**Solution:**
1. Check if backend is running on port 8000
2. Verify API URL in `src/lib/api.ts`
3. Check CORS settings in backend

### Issue 3: Authentication Not Working
**Error:** Login/register fails
**Solution:**
1. Check backend logs for errors
2. Verify password requirements
3. Check JWT token handling

### Issue 4: Images Not Showing
**Error:** Broken image links
**Solution:**
1. Check image URL construction
2. Verify static file serving
3. Add placeholder images

## 📊 Integration Status

### ✅ Completed
- [x] Backend API server
- [x] Frontend React app
- [x] API service layer
- [x] Authentication system
- [x] Database integration
- [x] CORS configuration
- [x] Error handling
- [x] Loading states

### 🔄 In Progress
- [ ] Cart persistence
- [ ] Search functionality
- [ ] Admin panel
- [ ] Order management

### 📋 Next Steps
1. Test all features
2. Add missing functionality
3. Improve error handling
4. Add more features
5. Deploy to production

## 🎯 Success Criteria

Your integration is successful when:
- ✅ Frontend loads real data from backend
- ✅ Authentication works end-to-end
- ✅ Cart functionality works
- ✅ No console errors
- ✅ Responsive design works
- ✅ Error handling works properly

## 🚀 Next Development Steps

1. **Add Search Functionality**
   - Implement search input
   - Connect to search API
   - Display search results

2. **Create Book Detail Page**
   - Add new route `/book/:id`
   - Fetch book details
   - Display book information

3. **Build Cart Page**
   - Create cart component
   - Show cart items
   - Add quantity controls

4. **Add Admin Panel**
   - Create admin routes
   - Add book management
   - Add user management

5. **Improve UX**
   - Add more loading states
   - Improve error messages
   - Add animations

## 📞 Troubleshooting

If you encounter issues:
1. Check browser console for errors
2. Check backend logs
3. Verify both servers are running
4. Check network connectivity
5. Restart both servers if needed

## 🎉 Congratulations!

Your frontend and backend are now integrated! You have a fully functional full-stack application with:
- Real-time data fetching
- User authentication
- Shopping cart functionality
- Error handling
- Responsive design

Start exploring the code and adding new features!
