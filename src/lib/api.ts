// API Service Layer for Hindi Books Website
// This file contains all API calls to the backend

// Allow overriding the backend URL via env for deployments (Render, Vercel, etc.)
const API_BASE_URL =
  import.meta.env?.VITE_API_BASE_URL?.replace(/\/+$/, '') ||
  'http://localhost:8000';

// Types matching backend schemas
export interface Book {
  id: number;
  title: string;
  author: string;
  description: string;
  category: string;
  price: number;
  image_url: string;
  stock_quantity: number;
  is_available: boolean;
  created_at: string;
}

export interface User {
  id: number;
  username: string;
  email: string;
  is_admin: boolean;
  created_at: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface PaginatedBooks {
  books: Book[];
  total: number;
  page: number;
  per_page: number;
  pages: number;
}

export interface Category {
  name: string;
  count: number;
}

export interface CartItem {
  id: number;
  book: Book;
  quantity: number;
  created_at: string;
}

export interface CartSummary {
  items: CartItem[];
  total_items: number;
  total_price: number;
}

export interface BookQueryParams {
  page?: number;
  per_page?: number;
  category?: string;
  search?: string;
  min_price?: number;
  max_price?: number;
  sort_by?: string;
  sort_order?: string;
}

// API Client with error handling
class ApiClient {
  private baseURL: string;
  private token: string | null = null;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
    // Load token from localStorage on initialization
    this.token = localStorage.getItem('auth_token');
  }

  // Set authentication token
  setToken(token: string | null) {
    this.token = token;
    if (token) {
      localStorage.setItem('auth_token', token);
    } else {
      localStorage.removeItem('auth_token');
    }
  }

  // Get headers with optional authentication
  private getHeaders(includeAuth: boolean = false): HeadersInit {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };

    if (includeAuth && this.token) {
      headers.Authorization = `Bearer ${this.token}`;
    }

    return headers;
  }

  // Generic request method
  private async request<T>(
    endpoint: string,
    options: RequestInit = {},
    includeAuth: boolean = false
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    
    const response = await fetch(url, {
      ...options,
      headers: {
        ...this.getHeaders(includeAuth),
        ...options.headers,
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  // Book endpoints
  async getBooks(params?: {
    page?: number;
    per_page?: number;
    category?: string;
    search?: string;
    min_price?: number;
    max_price?: number;
    sort_by?: string;
    sort_order?: string;
  }): Promise<PaginatedBooks> {
    const searchParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          searchParams.append(key, value.toString());
        }
      });
    }
    
    const queryString = searchParams.toString();
    const endpoint = queryString ? `/books?${queryString}` : '/books';
    
    return this.request<PaginatedBooks>(endpoint);
  }

  async getBook(id: number): Promise<Book> {
    return this.request<Book>(`/books/${id}`);
  }

  async getCategories(): Promise<Category[]> {
    return this.request<Category[]>('/categories');
  }

  async searchBooks(query: string, limit: number = 10): Promise<{ results: Book[]; count: number }> {
    return this.request<{ results: Book[]; count: number }>(`/search?q=${encodeURIComponent(query)}&limit=${limit}`);
  }

  // Authentication endpoints
  async login(credentials: LoginRequest): Promise<LoginResponse> {
    const response = await this.request<LoginResponse>('/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
    
    // Store token for future requests
    this.setToken(response.access_token);
    return response;
  }

  async register(userData: RegisterRequest): Promise<User> {
    return this.request<User>('/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  async getCurrentUser(): Promise<User> {
    return this.request<User>('/users/me', { method: 'GET' }, true);
  }

  // Cart endpoints
  async getCart(): Promise<CartSummary> {
    return this.request<CartSummary>('/cart', { method: 'GET' }, true);
  }

  async addToCart(bookId: number, quantity: number = 1): Promise<{ message: string }> {
    return this.request<{ message: string }>('/cart', {
      method: 'POST',
      body: JSON.stringify({ book_id: bookId, quantity }),
    }, true);
  }

  async updateCartItem(cartItemId: number, quantity: number): Promise<{ message: string }> {
    return this.request<{ message: string }>(`/cart/${cartItemId}`, {
      method: 'PUT',
      body: JSON.stringify({ quantity }),
    }, true);
  }

  async removeFromCart(cartItemId: number): Promise<{ message: string }> {
    return this.request<{ message: string }>(`/cart/${cartItemId}`, {
      method: 'DELETE',
    }, true);
  }

  async clearCart(): Promise<{ message: string }> {
    return this.request<{ message: string }>('/cart', {
      method: 'DELETE',
    }, true);
  }

  // Health check
  async healthCheck(): Promise<{ status: string; database: string; static_files: boolean }> {
    return this.request<{ status: string; database: string; static_files: boolean }>('/health');
  }
}

// Create and export API client instance
export const apiClient = new ApiClient(API_BASE_URL);

// Export individual functions for convenience
export const api = {
  // Books
  getBooks: (params?: BookQueryParams) => apiClient.getBooks(params),
  getBook: (id: number) => apiClient.getBook(id),
  getCategories: () => apiClient.getCategories(),
  searchBooks: (query: string, limit?: number) => apiClient.searchBooks(query, limit),
  
  // Auth
  login: (credentials: LoginRequest) => apiClient.login(credentials),
  register: (userData: RegisterRequest) => apiClient.register(userData),
  getCurrentUser: () => apiClient.getCurrentUser(),
  logout: () => apiClient.setToken(null),
  
  // Cart
  getCart: () => apiClient.getCart(),
  addToCart: (bookId: number, quantity?: number) => apiClient.addToCart(bookId, quantity),
  updateCartItem: (cartItemId: number, quantity: number) => apiClient.updateCartItem(cartItemId, quantity),
  removeFromCart: (cartItemId: number) => apiClient.removeFromCart(cartItemId),
  clearCart: () => apiClient.clearCart(),
  
  // Utility
  healthCheck: () => apiClient.healthCheck(),
};
