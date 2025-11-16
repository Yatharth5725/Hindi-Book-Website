import { BookCard } from "./BookCard";
import { useFeaturedBooks } from "@/hooks/useBooks";
import { Loader2, AlertCircle } from "lucide-react";

export function FeaturedBooks() {
  const { data, isLoading, error } = useFeaturedBooks();

  if (isLoading) {
    return (
      <section className="py-16 bg-background">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl lg:text-4xl font-bold text-foreground mb-4">
              Featured Books
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Discover our handpicked collection of the finest Hindi literature, 
              poetry, and philosophical works from renowned authors.
            </p>
          </div>
          
          <div className="flex justify-center items-center py-12">
            <Loader2 className="h-8 w-8 animate-spin text-primary" />
            <span className="ml-2 text-muted-foreground">Loading featured books...</span>
          </div>
        </div>
      </section>
    );
  }

  if (error) {
    return (
      <section className="py-16 bg-background">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl lg:text-4xl font-bold text-foreground mb-4">
              Featured Books
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Discover our handpicked collection of the finest Hindi literature, 
              poetry, and philosophical works from renowned authors.
            </p>
          </div>
          
          <div className="flex justify-center items-center py-12">
            <AlertCircle className="h-8 w-8 text-destructive mr-2" />
            <span className="text-destructive">Failed to load books. Please try again later.</span>
          </div>
        </div>
      </section>
    );
  }

  const books = data?.books || [];

  return (
    <section className="py-16 bg-background">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl lg:text-4xl font-bold text-foreground mb-4">
            Featured Books
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Discover our handpicked collection of the finest Hindi literature, 
            poetry, and philosophical works from renowned authors.
          </p>
        </div>
        
        {books.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {books.map((book) => (
              <BookCard key={book.id} book={book} />
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <p className="text-muted-foreground">No books available at the moment.</p>
          </div>
        )}
      </div>
    </section>
  );
}