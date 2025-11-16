import { Header } from "@/components/Header";
import { Footer } from "@/components/Footer";
import { useParams, Link } from "react-router-dom";
import { useBook } from "@/hooks/useBooks";
import { useAddToCart } from "@/hooks/useCart";
import { useAuth } from "@/contexts/AuthContext";
import { Loader2, AlertCircle, ArrowLeft, ShoppingCart } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { toast } from "@/hooks/use-toast";
import { useState } from "react";

export default function BookDetailPage() {
  const { id } = useParams<{ id: string }>();
  const bookId = id ? parseInt(id) : 0;
  const { data: book, isLoading, error } = useBook(bookId);
  const { isAuthenticated } = useAuth();
  const addToCartMutation = useAddToCart();
  const [isAdding, setIsAdding] = useState(false);

  const getImageUrl = (imageUrl: string) => {
    if (!imageUrl) return "/placeholder.svg";
    if (imageUrl.startsWith("http")) return imageUrl;
    return `http://localhost:8000/static/images/books/${imageUrl}`;
  };

  const handleAddToCart = async () => {
    if (!isAuthenticated) {
      toast({
        title: "Login Required",
        description: "Please log in to add items to your cart.",
        variant: "destructive",
      });
      return;
    }

    if (!book || book.stock_quantity <= 0) {
      toast({
        title: "Out of Stock",
        description: "This book is currently out of stock.",
        variant: "destructive",
      });
      return;
    }

    try {
      setIsAdding(true);
      await addToCartMutation.mutateAsync({ bookId: book.id, quantity: 1 });
      toast({
        title: "Added to Cart",
        description: `${book.title} has been added to your cart.`,
      });
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to add item to cart. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsAdding(false);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-background">
        <Header />
        <main className="container mx-auto px-4 py-12">
          <div className="flex justify-center items-center py-12">
            <Loader2 className="h-8 w-8 animate-spin text-primary" />
            <span className="ml-2 text-muted-foreground">Loading book details...</span>
          </div>
        </main>
        <Footer />
      </div>
    );
  }

  if (error || !book) {
    return (
      <div className="min-h-screen bg-background">
        <Header />
        <main className="container mx-auto px-4 py-12">
          <div className="flex justify-center items-center py-12">
            <AlertCircle className="h-8 w-8 text-destructive mr-2" />
            <span className="text-destructive">Book not found or failed to load.</span>
          </div>
          <Link to="/books">
            <Button variant="outline" className="mt-4">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to Books
            </Button>
          </Link>
        </main>
        <Footer />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <Header />
      <main className="container mx-auto px-4 py-12">
        <Link to="/books">
          <Button variant="ghost" className="mb-6">
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Books
          </Button>
        </Link>

        <div className="grid lg:grid-cols-2 gap-8">
          <div>
            <img
              src={getImageUrl(book.image_url)}
              alt={book.title}
              className="w-full rounded-lg shadow-lg"
              onError={(e) => {
                (e.target as HTMLImageElement).src = "/placeholder.svg";
              }}
            />
          </div>

          <div className="space-y-6">
            <div>
              <span className="text-sm font-medium text-muted-foreground bg-secondary/50 px-3 py-1 rounded-full">
                {book.category}
              </span>
              <h1 className="text-3xl lg:text-4xl font-bold text-foreground mt-4 mb-2">
                {book.title}
              </h1>
              <p className="text-xl text-muted-foreground">by {book.author}</p>
            </div>

            <Card>
              <CardContent className="p-6 space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-2xl font-bold text-primary">
                    ₹{book.price}
                  </span>
                  {book.stock_quantity > 0 ? (
                    <span className="text-sm text-muted-foreground">
                      {book.stock_quantity} in stock
                    </span>
                  ) : (
                    <span className="text-sm text-destructive">
                      Out of stock
                    </span>
                  )}
                </div>

                <Button
                  className="w-full"
                  size="lg"
                  onClick={handleAddToCart}
                  disabled={isAdding || book.stock_quantity <= 0}
                >
                  {isAdding ? (
                    <Loader2 className="h-4 w-4 animate-spin mr-2" />
                  ) : (
                    <ShoppingCart className="h-4 w-4 mr-2" />
                  )}
                  Add to Cart
                </Button>
              </CardContent>
            </Card>

            <div>
              <h2 className="text-xl font-semibold text-foreground mb-3">Description</h2>
              <p className="text-muted-foreground leading-relaxed">
                {book.description || "No description available."}
              </p>
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
}

