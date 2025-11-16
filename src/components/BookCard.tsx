import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Book } from "@/lib/api";
import { useAddToCart } from "@/hooks/useCart";
import { useAuth } from "@/contexts/AuthContext";
import { useState } from "react";
import { Link } from "react-router-dom";
import { Loader2, ShoppingCart } from "lucide-react";
import { toast } from "@/hooks/use-toast";

interface BookCardProps {
  book: Book;
}

export function BookCard({ book }: BookCardProps) {
  const { isAuthenticated } = useAuth();
  const addToCartMutation = useAddToCart();
  const [isAdding, setIsAdding] = useState(false);

  const handleAddToCart = async (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    
    if (!isAuthenticated) {
      toast({
        title: "Login Required",
        description: "Please log in to add items to your cart.",
        variant: "destructive",
      });
      return;
    }

    if (book.stock_quantity <= 0) {
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

  // Get image URL - handle both relative and absolute URLs
  const getImageUrl = (imageUrl: string) => {
    if (!imageUrl) return "/placeholder.svg";
    if (imageUrl.startsWith("http")) return imageUrl;
    return `http://localhost:8000/static/images/books/${imageUrl}`;
  };

  return (
    <Card className="group overflow-hidden transition-all duration-300 hover:shadow-book bg-gradient-card border-border/50">
      <Link to={`/books/${book.id}`}>
        <div className="overflow-hidden aspect-[3/4] cursor-pointer">
          <img
            src={getImageUrl(book.image_url)}
            alt={book.title}
            className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
            onError={(e) => {
              (e.target as HTMLImageElement).src = "/placeholder.svg";
            }}
          />
        </div>
      </Link>
      <CardContent className="p-4">
        <div className="space-y-2">
          <span className="text-xs font-medium text-muted-foreground bg-secondary/50 px-2 py-1 rounded-full">
            {book.category}
          </span>
          <Link to={`/books/${book.id}`}>
            <h3 className="font-semibold text-foreground line-clamp-2 leading-tight hover:text-primary transition-colors cursor-pointer">
              {book.title}
            </h3>
          </Link>
          <p className="text-sm text-muted-foreground">
            {book.author}
          </p>
          <div className="flex items-center justify-between pt-2">
            <div className="flex flex-col">
              <span className="font-bold text-primary text-lg">
                ₹{book.price}
              </span>
              {book.stock_quantity > 0 ? (
                <span className="text-xs text-muted-foreground">
                  {book.stock_quantity} in stock
                </span>
              ) : (
                <span className="text-xs text-destructive">
                  Out of stock
                </span>
              )}
            </div>
            <Button 
              size="sm" 
              className="bg-primary hover:bg-primary/90 text-primary-foreground"
              onClick={handleAddToCart}
              disabled={isAdding || book.stock_quantity <= 0}
            >
              {isAdding ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <>
                  <ShoppingCart className="h-4 w-4 mr-1" />
                  Add to Cart
                </>
              )}
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
