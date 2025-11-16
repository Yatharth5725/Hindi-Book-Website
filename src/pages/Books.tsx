import { Header } from "@/components/Header";
import { Footer } from "@/components/Footer";
import { BookCard } from "@/components/BookCard";
import { useBooks } from "@/hooks/useBooks";
import { useSearchParams } from "react-router-dom";
import { Loader2, AlertCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useState, useEffect } from "react";

export default function BooksPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [currentPage, setCurrentPage] = useState(1);
  
  const page = parseInt(searchParams.get("page") || "1");
  const category = searchParams.get("category") || undefined;
  const search = searchParams.get("search") || undefined;
  const sortBy = searchParams.get("sort_by") || "created_at";
  const sortOrder = searchParams.get("sort_order") || "desc";

  const { data, isLoading, error } = useBooks({
    page,
    per_page: 12,
    category,
    search,
    sort_by: sortBy,
    sort_order: sortOrder,
  });

  useEffect(() => {
    setCurrentPage(page);
  }, [page]);

  const handlePageChange = (newPage: number) => {
    const params = new URLSearchParams(searchParams);
    params.set("page", newPage.toString());
    setSearchParams(params);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const handleSortChange = (value: string) => {
    const [field, order] = value.split("-");
    const params = new URLSearchParams(searchParams);
    params.set("sort_by", field);
    params.set("sort_order", order);
    setSearchParams(params);
  };

  return (
    <div className="min-h-screen bg-background">
      <Header />
      <main className="container mx-auto px-4 py-8">
        <div className="mb-8 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <h1 className="text-3xl lg:text-4xl font-bold text-foreground mb-2">
              {search ? `Search Results for "${search}"` : category ? `${category} Books` : "All Books"}
            </h1>
            {data && (
              <p className="text-muted-foreground">
                Showing {data.books.length} of {data.total} books
              </p>
            )}
          </div>
          
          <Select
            value={`${sortBy}-${sortOrder}`}
            onValueChange={handleSortChange}
          >
            <SelectTrigger className="w-[200px]">
              <SelectValue placeholder="Sort by" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="created_at-desc">Newest First</SelectItem>
              <SelectItem value="created_at-asc">Oldest First</SelectItem>
              <SelectItem value="title-asc">Title A-Z</SelectItem>
              <SelectItem value="title-desc">Title Z-A</SelectItem>
              <SelectItem value="price-asc">Price Low to High</SelectItem>
              <SelectItem value="price-desc">Price High to Low</SelectItem>
            </SelectContent>
          </Select>
        </div>

        {isLoading && (
          <div className="flex justify-center items-center py-12">
            <Loader2 className="h-8 w-8 animate-spin text-primary" />
            <span className="ml-2 text-muted-foreground">Loading books...</span>
          </div>
        )}

        {error && (
          <div className="flex justify-center items-center py-12">
            <AlertCircle className="h-8 w-8 text-destructive mr-2" />
            <span className="text-destructive">Failed to load books. Please try again later.</span>
          </div>
        )}

        {data && !isLoading && !error && (
          <>
            {data.books.length > 0 ? (
              <>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 mb-8">
                  {data.books.map((book) => (
                    <BookCard key={book.id} book={book} />
                  ))}
                </div>
                
                {data.pages > 1 && (
                  <div className="flex justify-center items-center gap-2">
                    <Button
                      variant="outline"
                      onClick={() => handlePageChange(currentPage - 1)}
                      disabled={currentPage === 1}
                    >
                      Previous
                    </Button>
                    <span className="text-muted-foreground">
                      Page {currentPage} of {data.pages}
                    </span>
                    <Button
                      variant="outline"
                      onClick={() => handlePageChange(currentPage + 1)}
                      disabled={currentPage === data.pages}
                    >
                      Next
                    </Button>
                  </div>
                )}
              </>
            ) : (
              <div className="text-center py-12">
                <p className="text-muted-foreground text-lg">No books found.</p>
              </div>
            )}
          </>
        )}
      </main>
      <Footer />
    </div>
  );
}

