# PowerShell script to start all servers
Write-Host "🚀 Starting Hindi Book Website - Complete Setup" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""

# Start Backend Server
Write-Host "📚 Starting Backend Server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'C:\Users\ANUBHAV SHARMA\OneDrive\Desktop\Hindi Book Website\hindi book website\Backend'; .\backend-env\Scripts\Activate.ps1; python main.py"

Start-Sleep -Seconds 5

# Start Admin Panel
Write-Host "🎛️ Starting Admin Panel..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'C:\Users\ANUBHAV SHARMA\OneDrive\Desktop\Hindi Book Website\hindi book website\Backend'; .\backend-env\Scripts\Activate.ps1; python admin_panel.py"

Start-Sleep -Seconds 3

# Start Frontend Server
Write-Host "🌐 Starting Frontend Server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'C:\Users\ANUBHAV SHARMA\OneDrive\Desktop\Hindi Book Website\hindi book website'; npm run dev"

Start-Sleep -Seconds 5

Write-Host ""
Write-Host "✅ All servers started successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Access Points:" -ForegroundColor Cyan
Write-Host "   Backend API:    http://localhost:8000" -ForegroundColor White
Write-Host "   API Docs:       http://localhost:8000/docs" -ForegroundColor White
Write-Host "   Admin Panel:    http://localhost:8001" -ForegroundColor White
Write-Host "   Frontend:       http://localhost:8080" -ForegroundColor White
Write-Host ""
Write-Host "📚 Next Steps:" -ForegroundColor Cyan
Write-Host "   1. Open Admin Panel: http://localhost:8001" -ForegroundColor White
Write-Host "   2. Click 'Seed Database' to add sample books" -ForegroundColor White
Write-Host "   3. Click 'Add New Book' to add your books" -ForegroundColor White
Write-Host "   4. Open Frontend: http://localhost:8080 to see your books" -ForegroundColor White
Write-Host ""
Write-Host "🎉 Your Hindi Book Website is LIVE!" -ForegroundColor Green
Write-Host ""
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
