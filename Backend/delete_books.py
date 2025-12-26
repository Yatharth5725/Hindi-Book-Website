#!/usr/bin/env python3
"""
Safe utility to delete book entries from the database
"""

from typing import List
import requests

# API Configuration
API_BASE_URL = "http://localhost:8000"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "Admin@123"


class BookDeleter:
    def __init__(self):
        self.session = requests.Session()
        self.token = None

    def login_admin(self) -> bool:
        """ Login as admin to get access token."""
        login_data = {
            "USERNAME": ADMIN_USERNAME,
            "password": ADMIN_PASSWORD
        }

        try:
            response = self.session.post(f"{API_BASE_URL}/login", json=login_data)
            response.raise_for_status()

            data = response.json()
            self.token = data["access_token"]

            # set Authorization header
            self.session.headers.update({
                "Authorization": f"Bearer {self.token}"
            })

            print("✅ Successfully logged in as admin")
            return True
        
        except Exception as e:
            print(f"❌ Login failed: {e}")
            return False
    

    def get_all_books(self):
        """Get all books from the database"""

        try:
            response = self.session.get(f"{API_BASE_URL}/books")
            response.raise_for_status()

            books = response.json()
            return books

        except Exception as e:
            print(f"❌ Failed to get books: {e}")
            return []

    def search_books(self, query: str):
        """Search books by title or author"""

        try:
            response = self.session.get(f"{API_BASE_URL}/books/search", params={"q": query})
            response.raise_for_status()

            books = response.json()
            return books

        except Exception as e:
            print(f"❌ Failed to search books: {e}")
            return []


    def delete_single_book(self, book_id: int):
        """Delete a single book """
        try:
            response = self.session.delete(f"{API_BASE_URL}/books/{book_id}")
            response.raise_for_status()

            print(f"✅ Successfully deleted book with ID: {book_id}")
            return True

        except Exception as e:
            print(f"❌ Failed to delete book {book_id}: {e}")
            return False

    def deleting_multiple_books(self, book_ids: List[int]):
        """Deleting multiple books by their IDs"""
        success_count = 0
        failed_count = 0

        for book_id in book_ids:
            if self.delete_single_book(book_id):
                success_count += 1
            else:
                failed_count += 1

        print(f"\n📊 Deletion summary:")
        print(f"   Success: {success_count}")
        print(f"   Failed: {failed_count}")

        return success_count, failed_count


    def display_books(self, books:List):
        """Display books in formatted way"""
        if not books:
            print("📭 No books found")
            return

        print(f"\n📚 Found {len(books)} books:")
        print("="*80)
        for book in books:
            print(f"ID: {book.get('ID' , "N/A")}")
            print(f"Title: {book.get('title', 'N/A')}")
            print(f"Author: {book.get('author', 'N/A')}")
            print(f"Category: {book.get('category', 'N/A')}")
            print(f"Price: ₹{book.get('price', 0)}")
            print(f"Stock: {book.get('stock_quantity', 0)}")
            print("-" * 80)


    def delete_books_by_category(self, category: str):
        """Delete all books in a category"""
        try:
            books = self.get_all_books()
            books_in_category = [b for b in books if b['category'].lower() == category.lower()]

            if not books_in_category:
                print(f"❌ No books in category: {category}")
                return False

            print(f"\n🗑️  Found {len(books_in_category)} books in category '{category}':")
            for book in books_in_category:
                print(f"   - {book['title']} by {book['author']}")

            confirm = input(f"\n⚠️  Delete all {len(books_in_category)} books? (yes/no): ").strip().lower()
            
            if confirm != 'yes':
                print("❌ Deletion cancelled")
                return False

            success_count = 0
            for book in books_in_category:
                if self.delete_single_book(book['id']):
                    success_count += 1

            print(f"\n✅ Deleted {success_count} out of {len(books_in_category)} books")
            return True

        except Exception as e:
            print(f"❌ Failed to delete books by category: {e}")
            return False

    def delete_books_by_title(self, title_keyword: str):
        """Delete books matching title keyword"""
        try:
            # Use search API for efficiency
            books = self.search_books(title_keyword)
            
            if not books:
                print(f"❌ No books found matching: {title_keyword}")
                return False

            print(f"\n🗑️ Found {len(books)} books matching '{title_keyword}':")
            for book in books:
                print(f"   - ID {book['id']}: {book['title']} by {book['author']}")

            confirm = input(f"\n⚠️  Delete all {len(books)} books? (yes/no): ").strip().lower()
            
            if confirm != 'yes':
                print("❌ Deletion cancelled")
                return False

            success_count = 0
            for book in books:
                if self.delete_single_book(book['id']):
                    success_count += 1

            print(f"\n✅ Deleted {success_count} out of {len(books)} books")
            return True

        except Exception as e:
            print(f"❌ Failed to delete books by title: {e}")
            return False

    def delete_all_books(self):
        """Delete all books (use with caution!)"""
        try:
            books = self.get_all_books()
            
            if not books:
                print("📚 No books to delete")
                return False

            print(f"\n⚠️  WARNING: You are about to delete ALL {len(books)} books!")
            print("This action cannot be undone!")
            
            confirm1 = input("\nType 'DELETE ALL' to confirm: ").strip()
            
            if confirm1 != 'DELETE ALL':
                print("❌ Deletion cancelled")
                return False

            confirm2 = input("Are you absolutely sure? (yes/no): ").strip().lower()
            
            if confirm2 != 'yes':
                print("❌ Deletion cancelled")
                return False

            success_count = 0
            for book in books:
                if self.delete_single_book(book['id']):
                    success_count += 1

            print(f"\n✅ Deleted {success_count} out of {len(books)} books")
            return True

        except Exception as e:
            print(f"❌ Failed to delete all books: {e}")
            return False

    def get_categories(self):
        """Get available categories"""
        try:
            response = self.session.get(f"{API_BASE_URL}/categories")
            response.raise_for_status()
            categories = response.json()
            return categories
        except Exception as e:
            print(f"❌ Failed to get categories: {e}")
            return []

def main():
    print("🗑️  Hindi Book Deleter")
    print("=" * 50)

    # Initialize deleter
    deleter = BookDeleter()

    # Login as admin
    if not deleter.login_admin():
        print("❌ Cannot proceed without admin access")
        return

    while True:
        # Show menu
        print("\n🎯 What would you like to do?")
        print("1. View all books")
        print("2. Delete book by ID")
        print("3. Delete books by category")
        print("4. Delete books by title keyword")
        print("5. Delete ALL books (⚠️  DANGER!)")
        print("6. View categories")
        print("7. Exit")

        choice = input("\nEnter your choice (1-7): ").strip()

        if choice == "1":
            print("\n📚 Fetching all books...")
            books = deleter.get_all_books()
            deleter.display_books(books)

        elif choice == "2":
            book_id = input("\nEnter book ID to delete: ").strip()
            try:
                book_id = int(book_id)
                deleter.delete_single_book(book_id)
            except ValueError:
                print("❌ Invalid book ID")

        elif choice == "3":
            categories = deleter.get_categories()
            if categories:
                print("\n📋 Available categories:")
                for cat in categories:
                    print(f"   - {cat}")
            
            category = input("\nEnter category name: ").strip()
            deleter.delete_books_by_category(category)

        elif choice == "4":
            title_keyword = input("\nEnter title keyword: ").strip()
            deleter.delete_books_by_title(title_keyword)

        elif choice == "5":
            deleter.delete_all_books()

        elif choice == "6":
            categories = deleter.get_categories()
            if categories:
                print("\n📋 Available categories:")
                for cat in categories:
                    print(f"   - {cat}")
            else:
                print("❌ No categories found")

        elif choice == "7":
            print("\n👋 Goodbye!")
            break

        else:
            print("❌ Invalid choice")

    print("\n💡 Tips:")
    print("- Check remaining books at: http://localhost:8000/books")
    print("- View admin panel at: http://localhost:8000/docs")

if __name__ == "__main__":
    main()