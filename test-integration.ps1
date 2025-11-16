# Integration Test Script
Write-Host "🧪 Testing Frontend-Backend Integration..." -ForegroundColor Green
Write-Host ""

# Test Backend
Write-Host "1. Testing Backend API..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get -TimeoutSec 10
    Write-Host "✅ Backend is running!" -ForegroundColor Green
    Write-Host "   Status: $($response.status)" -ForegroundColor Cyan
    Write-Host "   Database: $($response.database)" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Backend is not running!" -ForegroundColor Red
    Write-Host "   Please start backend first: python main.py" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To start backend:" -ForegroundColor Yellow
    Write-Host "cd Backend" -ForegroundColor Gray
    Write-Host ".\backend-env\Scripts\Activate.ps1" -ForegroundColor Gray
    Write-Host "python main.py" -ForegroundColor Gray
    exit 1
}

# Test Books API
Write-Host ""
Write-Host "2. Testing Books API..." -ForegroundColor Yellow
try {
    $books = Invoke-RestMethod -Uri "http://localhost:8000/books?per_page=3" -Method Get -TimeoutSec 10
    Write-Host "✅ Books API is working!" -ForegroundColor Green
    Write-Host "   Found $($books.total) books" -ForegroundColor Cyan
    Write-Host "   Showing $($books.books.Count) books" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Books API failed!" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Yellow
}

# Test Categories API
Write-Host ""
Write-Host "3. Testing Categories API..." -ForegroundColor Yellow
try {
    $categories = Invoke-RestMethod -Uri "http://localhost:8000/categories" -Method Get -TimeoutSec 10
    Write-Host "✅ Categories API is working!" -ForegroundColor Green
    Write-Host "   Found $($categories.Count) categories" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Categories API failed!" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Yellow
}

# Test Frontend
Write-Host ""
Write-Host "4. Testing Frontend..." -ForegroundColor Yellow
try {
    $frontend = Invoke-WebRequest -Uri "http://localhost:8080" -Method Get -TimeoutSec 10
    if ($frontend.StatusCode -eq 200) {
        Write-Host "✅ Frontend is running!" -ForegroundColor Green
        Write-Host "   Status Code: $($frontend.StatusCode)" -ForegroundColor Cyan
    } else {
        Write-Host "❌ Frontend returned status: $($frontend.StatusCode)" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Frontend is not running!" -ForegroundColor Red
    Write-Host "   Please start frontend first: npm run dev" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To start frontend:" -ForegroundColor Yellow
    Write-Host "npm run dev" -ForegroundColor Gray
}

Write-Host ""
Write-Host "🎯 Integration Test Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Open http://localhost:8080 in your browser" -ForegroundColor Cyan
Write-Host "2. Open http://localhost:8000/docs for API documentation" -ForegroundColor Cyan
Write-Host "3. Test the login/register functionality" -ForegroundColor Cyan
Write-Host "4. Try adding books to cart" -ForegroundColor Cyan
Write-Host ""
Write-Host "Happy coding! 🚀" -ForegroundColor Green
