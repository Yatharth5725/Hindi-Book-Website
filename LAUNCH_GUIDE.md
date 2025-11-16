# 🚀 Launch Guide - Hindi Book Website

## ❌ Common PowerShell Error Fixed

**Problem:** PowerShell doesn't use `&&` like bash
**Solution:** Use `;` instead of `&&`

### ❌ Wrong (causes error):
```powershell
cd "path" && command1 && command2
```

### ✅ Correct:
```powershell
cd "path"; command1; command2
```

## 🎯 How to Launch Your Website

### **Method 1: Use the PowerShell Script (Easiest)**

1. **Open PowerShell as Administrator**
2. **Navigate to your project:**
   ```powershell
   cd "C:\Users\ANUBHAV SHARMA\OneDrive\Desktop\Hindi Book Website\hindi book website"
   ```
3. **Run the launch script:**
   ```powershell
   .\start-all.ps1
   ```

### **Method 2: Manual Launch (Step by Step)**

#### **Step 1: Start Backend Server**
```powershell
# Open PowerShell Terminal 1
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

#### **Step 2: Start Admin Panel**
```powershell
# Open PowerShell Terminal 2
cd "C:\Users\ANUBHAV SHARMA\OneDrive\Desktop\Hindi Book Website\hindi book website\Backend"
.\backend-env\Scripts\Activate.ps1
python admin_panel.py
```

**Expected Output:**
```
🚀 Starting Admin Panel...
📊 Dashboard: http://localhost:8001
🎛️ Starting Admin Panel...
INFO:     Started server process [5678]
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
```

#### **Step 3: Start Frontend Server**
```powershell
# Open PowerShell Terminal 3
cd "C:\Users\ANUBHAV SHARMA\OneDrive\Desktop\Hindi Book Website\hindi book website"
npm run dev
```

**Expected Output:**
```
  VITE v5.4.19  ready in 1234 ms

  ➜  Local:   http://localhost:8080/
  ➜  Network: use --host to expose
```

## 🌐 Access Your Website

Once all servers are running:

- **🌐 Main Website**: `http://localhost:8080`
- **🎛️ Admin Panel**: `http://localhost:8001`
- **📊 API Docs**: `http://localhost:8000/docs`
- **🔧 Backend API**: `http://localhost:8000`

## 📚 Add Your Books

1. **Open Admin Panel**: `http://localhost:8001`
2. **Click "Seed Database"** - Adds sample Hindi books
3. **Click "Add New Book"** - Add your own books
4. **Fill in book details**:
   - Title (in Hindi or English)
   - Author name
   - Description
   - Category (choose from dropdown)
   - Price (in ₹)
   - Stock quantity
   - Image filename (optional)

## 🎉 Your Website is Live!

### **Features Available:**
- ✅ Beautiful Hindi book display
- ✅ User registration and login
- ✅ Shopping cart functionality
- ✅ Admin panel for book management
- ✅ Search and filter books
- ✅ Responsive design
- ✅ Real-time data from database

### **Next Steps:**
1. Add your book collection
2. Customize the design if needed
3. Test all functionality
4. Share with your customers!

## 🐛 Troubleshooting

### **If Backend Won't Start:**
```powershell
# Check if virtual environment is activated
.\backend-env\Scripts\Activate.ps1

# Install missing dependencies
pip install -r requirements.txt

# Try starting again
python main.py
```

### **If Frontend Won't Start:**
```powershell
# Install dependencies
npm install

# Try starting again
npm run dev
```

### **If Ports are Busy:**
- Backend uses port 8000
- Admin panel uses port 8001
- Frontend uses port 8080
- Close other applications using these ports

## 🎯 Success Checklist

- [ ] Backend running on port 8000
- [ ] Admin panel running on port 8001
- [ ] Frontend running on port 8080
- [ ] Can access all URLs
- [ ] Can add books through admin panel
- [ ] Books appear on main website
- [ ] User registration works
- [ ] Shopping cart works

## 🚀 You're Ready to Launch!

Your Hindi Book Website is fully functional and ready for your customers! 🎉📚✨
