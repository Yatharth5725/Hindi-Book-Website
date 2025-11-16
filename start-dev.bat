@echo off
echo Starting Hindi Book Website Development Environment...
echo.

echo Starting Backend Server...
start "Backend Server" cmd /k "cd /d "C:\Users\ANUBHAV SHARMA\OneDrive\Desktop\Hindi Book Website\hindi book website\Backend" && .\backend-env\Scripts\Activate.ps1 && python main.py"

echo Waiting for backend to start...
timeout /t 5 /nobreak > nul

echo Starting Frontend Server...
start "Frontend Server" cmd /k "cd /d "C:\Users\ANUBHAV SHARMA\OneDrive\Desktop\Hindi Book Website\hindi book website" && npm run dev"

echo.
echo Development servers starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:8080
echo API Docs: http://localhost:8000/docs
echo.
echo Press any key to exit...
pause > nul
