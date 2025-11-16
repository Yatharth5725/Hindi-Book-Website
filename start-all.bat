@echo off
echo 🚀 Starting Hindi Book Website - Complete Setup
echo ================================================
echo.

echo 📚 Starting Backend Server...
start "Backend Server" cmd /k "cd /d \"C:\Users\ANUBHAV SHARMA\OneDrive\Desktop\Hindi Book Website\hindi book website\Backend\" && .\backend-env\Scripts\Activate.ps1 && python main.py"

echo ⏳ Waiting for backend to start...
timeout /t 5 /nobreak > nul

echo 🎛️ Starting Admin Panel...
start "Admin Panel" cmd /k "cd /d \"C:\Users\ANUBHAV SHARMA\OneDrive\Desktop\Hindi Book Website\hindi book website\Backend\" && .\backend-env\Scripts\Activate.ps1 && python admin_panel.py"

echo ⏳ Waiting for admin panel to start...
timeout /t 3 /nobreak > nul

echo 🌐 Starting Frontend Server...
start "Frontend Server" cmd /k "cd /d \"C:\Users\ANUBHAV SHARMA\OneDrive\Desktop\Hindi Book Website\hindi book website\" && npm run dev"

echo ⏳ Waiting for frontend to start...
timeout /t 5 /nobreak > nul

echo.
echo ✅ All servers started successfully!
echo.
echo 📊 Access Points:
echo    Backend API:    http://localhost:8000
echo    API Docs:       http://localhost:8000/docs
echo    Admin Panel:    http://localhost:8001
echo    Frontend:       http://localhost:8080
echo.
echo 📚 Next Steps:
echo    1. Open Admin Panel: http://localhost:8001
echo    2. Click "Seed Database" to add sample books
echo    3. Click "Add New Book" to add your books
echo    4. Open Frontend: http://localhost:8080 to see your books
echo.
echo 🎉 Happy Book Uploading!
echo.
pause
