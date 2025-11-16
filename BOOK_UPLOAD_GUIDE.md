# 📚 Book Upload Guide - Hindi Book Website

## 🎯 How to Upload Your Books to the Database

### **Method 1: Using the Admin Panel (Recommended)**

#### Step 1: Start the Backend Server
```powershell
# Open PowerShell
cd "C:\Users\ANUBHAV SHARMA\OneDrive\Desktop\Hindi Book Website\hindi book website\Backend"
.\backend-env\Scripts\Activate.ps1
python main.py
```

#### Step 2: Start the Admin Panel
```powershell
# Open another PowerShell window
cd "C:\Users\ANUBHAV SHARMA\OneDrive\Desktop\Hindi Book Website\hindi book website\Backend"
.\backend-env\Scripts\Activate.ps1
python admin_panel.py
```

#### Step 3: Access Admin Panel
1. Open browser: `http://localhost:8001`
2. You'll see the admin dashboard
3. Click "Seed Database" to add sample books first
4. Click "Add New Book" to add your own books

### **Method 2: Using the Upload Script**

#### Step 1: Start Backend Server
```powershell
cd "C:\Users\ANUBHAV SHARMA\OneDrive\Desktop\Hindi Book Website\hindi book website\Backend"
.\backend-env\Scripts\Activate.ps1
python main.py
```

#### Step 2: Run Upload Script
```powershell
# In another PowerShell window
cd "C:\Users\ANUBHAV SHARMA\OneDrive\Desktop\Hindi Book Website\hindi book website\Backend"
.\backend-env\Scripts\Activate.ps1
python upload_books.py
```

### **Method 3: Using API Documentation**

1. Start backend: `python main.py`
2. Open: `http://localhost:8000/docs`
3. Find the `/seed` endpoint
4. Click "Try it out" → "Execute"
5. This adds sample Hindi books

## 🔧 Admin Panel Features

### **Dashboard** (`http://localhost:8001`)
- View total books, available books, users
- See recent books added
- Quick navigation to all features

### **Manage Books** (`http://localhost:8001/books`)
- View all books in the database
- See book details, prices, stock
- Check availability status

### **Add New Book** (`http://localhost:8001/add-book`)
- Easy form to add books
- All required fields
- Category selection
- Image upload support

### **Seed Database** (`http://localhost:8001/seed`)
- Add sample Hindi books
- Quick way to populate database
- Includes popular Hindi literature

## 📖 Book Information Required

### **Required Fields:**
- **Title**: Book title (Hindi or English)
- **Author**: Author's full name
- **Description**: Brief book summary
- **Category**: Choose from available categories
- **Price**: Price in Indian Rupees
- **Stock Quantity**: Number of copies available

### **Optional Fields:**
- **Image URL**: Book cover image filename

### **Available Categories:**
- धर्म (Religion)
- कविता (Poetry)
- साहित्य (Literature)
- दर्शन (Philosophy)
- इतिहास (History)
- आधुनिक साहित्य (Modern Literature)

## 🖼️ Adding Book Images

### **Step 1: Prepare Images**
1. Resize images to 300x400 pixels (recommended)
2. Use JPG or PNG format
3. Name files descriptively (e.g., `ramayana.jpg`)

### **Step 2: Upload Images**
1. Place images in: `Backend/static/images/books/`
2. Create the folder if it doesn't exist
3. Use the filename in the "Image URL" field

### **Step 3: Test Images**
1. Check if images load at: `http://localhost:8000/static/images/books/filename.jpg`
2. Update image URLs in the database if needed

## 🚀 Quick Start Process

### **For First Time Setup:**
1. Start backend: `python main.py`
2. Start admin panel: `python admin_panel.py`
3. Open: `http://localhost:8001`
4. Click "Seed Database" to add sample books
5. Click "Add New Book" to add your books
6. Start frontend: `npm run dev`
7. View website: `http://localhost:8080`

### **For Adding More Books:**
1. Make sure backend is running
2. Open admin panel: `http://localhost:8001`
3. Click "Add New Book"
4. Fill in book details
5. Submit the form
6. Check "Manage Books" to verify

## 🔍 Checking Your Books

### **In Admin Panel:**
- Dashboard: `http://localhost:8001`
- All Books: `http://localhost:8001/books`

### **In API:**
- All Books: `http://localhost:8000/books`
- API Docs: `http://localhost:8000/docs`

### **In Frontend:**
- Website: `http://localhost:8080`
- Books should appear in the featured section

## 🐛 Troubleshooting

### **Admin Panel Not Loading:**
- Check if backend is running on port 8000
- Check if admin panel is running on port 8001
- Try refreshing the page

### **Books Not Appearing:**
- Check if books were added successfully
- Verify database connection
- Check browser console for errors

### **Images Not Showing:**
- Verify image files are in correct folder
- Check image URLs in database
- Ensure images are accessible via URL

### **Form Submission Errors:**
- Check all required fields are filled
- Verify price is a valid number
- Check stock quantity is a valid number

## 💡 Pro Tips

1. **Start with Sample Books**: Use the seed function first
2. **Use Consistent Naming**: Follow a pattern for image files
3. **Check Categories**: Use existing categories for consistency
4. **Test Everything**: Verify books appear on the website
5. **Backup Database**: Keep a backup of your database file

## 📊 Database Location

Your database file is located at:
```
Backend/hindi_books.db
```

This SQLite file contains all your books and user data.

## 🎉 Success Checklist

- [ ] Backend server running on port 8000
- [ ] Admin panel running on port 8001
- [ ] Can access admin dashboard
- [ ] Successfully added books
- [ ] Books appear on frontend website
- [ ] Images load correctly
- [ ] All book details are correct

## 🚀 Next Steps

After uploading your books:
1. Test the frontend website
2. Try the search functionality
3. Test the shopping cart
4. Add more books as needed
5. Customize categories if required

Your Hindi Book Website is now ready with your book collection! 📚✨
