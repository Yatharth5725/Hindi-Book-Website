#!/usr/bin/env python3
"""
Book Upload Script for Hindi Book Website
This script helps you upload your books to the database
"""

import requests
from typing import List, Dict

# API Configuration
API_BASE_URL = "http://localhost:8000"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "Admin@123"

class BookUploader:
    def __init__(self):
        self.session = requests.Session()
        self.token = None

    def login_admin(self):
        """Login as admin to get access token"""
        login_data = {
            "username": ADMIN_USERNAME,
            "password": ADMIN_PASSWORD
        }

        try:
            response = self.session.post(f"{API_BASE_URL}/login", json=login_data)
            response.raise_for_status()

            data = response.json()
            self.token = data["access_token"]

            # Set authorization header
            self.session.headers.update({
                "Authorization": f"Bearer {self.token}"
            })

            print("✅ Successfully logged in as admin")
            return True

        except Exception as e:
            print(f"❌ Login failed: {e}")
            return False

    def upload_single_book(self, book_data: Dict):
        """Upload a single book to the database"""
        try:
            response = self.session.post(f"{API_BASE_URL}/books", json=book_data)
            response.raise_for_status()

            book = response.json()
            print(f"✅ Uploaded: {book['title']} by {book['author']}")
            return True

        except Exception as e:
            print(f"❌ Failed to upload {book_data.get('title', 'Unknown')}: {e}")
            return False

    def upload_multiple_books(self, books: List[Dict]):
        """Upload multiple books using bulk endpoint"""
        try:
            bulk_data = {"books": books}
            response = self.session.post(f"{API_BASE_URL}/books/bulk", json=bulk_data)
            response.raise_for_status()

            result = response.json()
            print(f"✅ Bulk upload completed:")
            print(f"   Success: {result['success_count']}")
            print(f"   Failed: {result['failed_count']}")

            if result['errors']:
                print("   Errors:")
                for error in result['errors']:
                    print(f"     - {error}")

            return True

        except Exception as e:
            print(f"❌ Bulk upload failed: {e}")
            return False

    def get_categories(self):
        """Get available categories"""
        try:
            response = self.session.get(f"{API_BASE_URL}/categories")
            response.raise_for_status()

            categories = response.json()
            print("📚 Available categories:")
            for cat in categories:
                print(f"   - {cat['name']} ({cat['count']} books)")

            return [cat['name'] for cat in categories]

        except Exception as e:
            print(f"❌ Failed to get categories: {e}")
            return []

def main():
    print("📚 Hindi Book Uploader")
    print("=" * 50)

    # Initialize uploader
    uploader = BookUploader()

    # Login as admin
    if not uploader.login_admin():
        print("❌ Cannot proceed without admin access")
        return

    # Get available categories
    print("\n📋 Checking available categories...")
    categories = uploader.get_categories()

    # Ask user what to do
    print("\n🎯 What would you like to do?")
    print("1. Upload your own books (manual entry)")
    print("2. Just show categories")

    choice = input("\nEnter your choice (1-2): ").strip()

    if choice == "1":
        print("\n📝 Manual book entry")
        print("Enter book details (press Enter to finish):")

        books = []
        while True:
            print(f"\n--- Book {len(books) + 1} ---")
            title = input("Title: ").strip()
            if not title:
                break

            author = input("Author: ").strip()
            description = input("Description: ").strip()
            category = input(f"Category (available: {', '.join(categories)}): ").strip()
            price = float(input("Price: ") or "0")
            stock = int(input("Stock quantity: ") or "0")
            image = input("Image filename (optional): ").strip()

            book = {
                "title": title,
                "author": author,
                "description": description,
                "category": category,
                "price": price,
                "image_url": image or "placeholder.jpg",
                "stock_quantity": stock
            }

            books.append(book)
            print(f"✅ Added: {title}")

        if books:
            print(f"\n📤 Uploading {len(books)} books...")
            uploader.upload_multiple_books(books)
        else:
            print("❌ No books to upload")

    elif choice == "2":
        print("\n📚 Categories displayed above")

    else:
        print("❌ Invalid choice")

    print("\n🎉 Upload process completed!")
    print("\n💡 Tips:")
    print("- Check your books at: http://localhost:8000/books")
    print("- View admin panel at: http://localhost:8000/docs")
    print("- Test frontend at: http://localhost:8080")

if __name__ == "__main__":
    main()
