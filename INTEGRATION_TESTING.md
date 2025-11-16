# Integration Testing Guide

## 🧪 How to Test Your Full-Stack Integration

### Step 1: Start Backend Server

```bash
# Terminal 1 - Backend
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

```bash
# Terminal 2 - Frontend
cd "C:\Users\ANUBHAV SHARMA\OneDrive\Desktop\Hindi Book Website\hindi book website"
npm run dev
```

**Expected Output:**
```
  VITE v5.4.19  ready in 1234 ms

  ➜  Local:   http://localhost:8080/
  ➜  Network: use --host to expose
```

### Step 3: Test Integration Points

#### 3.1 Test Backend API
1. Open `http://localhost:8000/docs` in browser
2. Test these endpoints:
   - `GET /health` - Should return healthy status
   - `GET /books` - Should return paginated books
   - `GET /categories` - Should return book categories

#### 3.2 Test Frontend
1. Open `http://localhost:8080` in browser
2. Check these features:
   - ✅ Page loads without errors
   - ✅ Featured books section shows real data
   - ✅ Book cards display properly
   - ✅ Login/Register dialog works
   - ✅ Add to cart functionality (requires login)

#### 3.3 Test Authentication Flow
1. Click the user icon in header
2. Try to register a new account
3. Try to login with existing account
4. Test "Add to Cart" - should prompt login if not authenticated

### Step 4: Debug Common Issues

#### Backend Issues
- **Port 8000 in use**: Change port in `main.py` line 947
- **Database errors**: Check SQLite file permissions
- **Import errors**: Ensure virtual environment is activated

#### Frontend Issues
- **API calls failing**: Check if backend is running on port 8000
- **CORS errors**: Verify CORS middleware in backend
- **Build errors**: Check TypeScript types and imports

#### Integration Issues
- **Data not loading**: Check browser console for errors
- **Authentication not working**: Verify JWT token handling
- **Images not showing**: Check image URL construction

### Step 5: Verify Full Functionality

#### ✅ Checklist
- [ ] Backend server running on port 8000
- [ ] Frontend server running on port 8080
- [ ] Books loading from API
- [ ] Categories displaying
- [ ] User registration working
- [ ] User login working
- [ ] Add to cart working (when logged in)
- [ ] Error handling working
- [ ] Loading states showing
- [ ] Responsive design working

### Step 6: Next Development Steps

1. **Add More Pages**: Create book detail page, cart page
2. **Enhance Search**: Implement search functionality
3. **Add Admin Panel**: Create admin interface
4. **Improve UX**: Add more loading states, animations
5. **Add Tests**: Write unit and integration tests

## 🐛 Troubleshooting

### Common Error Messages

**"Failed to fetch"**
- Backend not running
- CORS issues
- Wrong API URL

**"Token expired"**
- JWT token expired
- Need to login again

**"Network Error"**
- Backend server down
- Port conflicts
- Firewall blocking

### Debug Commands

```bash
# Check if ports are in use
netstat -an | findstr :8000
netstat -an | findstr :8080

# Check backend logs
cd Backend && python main.py

# Check frontend build
npm run build
```

## 🎯 Success Criteria

Your integration is successful when:
1. Frontend loads real data from backend
2. Authentication works end-to-end
3. Cart functionality works
4. No console errors
5. Responsive design works
6. Error handling works properly

## 📚 Learning Path

1. **Week 1**: Understand the codebase structure
2. **Week 2**: Add new features (search, filters)
3. **Week 3**: Implement admin panel
4. **Week 4**: Add advanced features (orders, payments)
5. **Week 5**: Deploy to production

## 🚀 Production Deployment

When ready for production:
1. Set up proper environment variables
2. Use production database (PostgreSQL)
3. Set up proper CORS origins
4. Add rate limiting
5. Set up monitoring and logging
6. Deploy backend to cloud service
7. Deploy frontend to CDN
