// React Query hooks for book data fetching
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api, Book, PaginatedBooks, Category } from '@/lib/api';

// Types
interface BookQueryParams {
  page?: number;
  per_page?: number;
  category?: string;
  search?: string;
  min_price?: number;
  max_price?: number;
  sort_by?: string;
  sort_order?: string;
}

// Query keys
export const bookKeys = {
  all: ['books'] as const,
  lists: () => [...bookKeys.all, 'list'] as const,
  list: (params?: BookQueryParams) => [...bookKeys.lists(), params] as const,
  details: () => [...bookKeys.all, 'detail'] as const,
  detail: (id: number) => [...bookKeys.details(), id] as const,
  categories: () => [...bookKeys.all, 'categories'] as const,
  search: (query: string) => [...bookKeys.all, 'search', query] as const,
};

// Get books with pagination and filters
export function useBooks(params?: {
  page?: number;
  per_page?: number;
  category?: string;
  search?: string;
  min_price?: number;
  max_price?: number;
  sort_by?: string;
  sort_order?: string;
}) {
  return useQuery({
    queryKey: bookKeys.list(params),
    queryFn: () => api.getBooks(params),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

// Get single book
export function useBook(id: number) {
  return useQuery({
    queryKey: bookKeys.detail(id),
    queryFn: () => api.getBook(id),
    enabled: !!id,
  });
}

// Get categories
export function useCategories() {
  return useQuery({
    queryKey: bookKeys.categories(),
    queryFn: () => api.getCategories(),
    staleTime: 10 * 60 * 1000, // 10 minutes
  });
}

// Search books
export function useSearchBooks(query: string, limit: number = 10) {
  return useQuery({
    queryKey: bookKeys.search(query),
    queryFn: () => api.searchBooks(query, limit),
    enabled: query.length >= 2,
    staleTime: 2 * 60 * 1000, // 2 minutes
  });
}

// Featured books (first page with limited items)
export function useFeaturedBooks() {
  return useQuery({
    queryKey: bookKeys.list({ page: 1, per_page: 8 }),
    queryFn: () => api.getBooks({ page: 1, per_page: 8 }),
    staleTime: 10 * 60 * 1000, // 10 minutes
  });
}

// Books by category
export function useBooksByCategory(category: string, page: number = 1, perPage: number = 12) {
  return useQuery({
    queryKey: bookKeys.list({ category, page, per_page: perPage }),
    queryFn: () => api.getBooks({ category, page, per_page: perPage }),
    enabled: !!category,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}
