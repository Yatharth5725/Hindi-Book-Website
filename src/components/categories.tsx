import { Card, CardContent } from "@/components/ui/card";
import { BookOpen, Heart, Lightbulb, Users, Star, Award } from "lucide-react";
import { useCategories } from "@/hooks/useBooks";
import { Loader2, AlertCircle } from "lucide-react";
import { Link } from "react-router-dom";

const iconMap: Record<string, React.ComponentType<{ className?: string }>> = {
  Literature: BookOpen,
  साहित्य: BookOpen,
  Poetry: Heart,
  कविता: Heart,
  Philosophy: Lightbulb,
  दर्शन: Lightbulb,
  Biographies: Users,
  जीवनी: Users,
  Spiritual: Star,
  धर्म: Star,
  "Award Winners": Award,
  इतिहास: Award,
};

export function Categories() {
  const { data: categories, isLoading, error } = useCategories();

  if (isLoading) {
    return (
      <section className="py-16 bg-muted/30">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl lg:text-4xl font-bold text-foreground mb-4">
              Book Categories
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Explore our diverse collection organized by genres and themes 
              to find exactly what you're looking for.
            </p>
          </div>
          <div className="flex justify-center items-center py-12">
            <Loader2 className="h-8 w-8 animate-spin text-primary" />
          </div>
        </div>
      </section>
    );
  }

  if (error) {
    return (
      <section className="py-16 bg-muted/30">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl lg:text-4xl font-bold text-foreground mb-4">
              Book Categories
            </h2>
            <div className="flex justify-center items-center py-12">
              <AlertCircle className="h-8 w-8 text-destructive mr-2" />
              <span className="text-destructive">Failed to load categories.</span>
            </div>
          </div>
        </div>
      </section>
    );
  }

  const categoriesList = categories || [];

  return (
    <section className="py-16 bg-muted/30">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl lg:text-4xl font-bold text-foreground mb-4">
            Book Categories
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Explore our diverse collection organized by genres and themes 
            to find exactly what you're looking for.
          </p>
        </div>
        
        {categoriesList.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {categoriesList.map((category) => {
              const IconComponent = iconMap[category.name] || BookOpen;
              return (
                <Link key={category.name} to={`/category/${encodeURIComponent(category.name)}`}>
                  <Card className="group cursor-pointer transition-all duration-300 hover:shadow-elegant bg-gradient-card border-border/50 hover:border-primary/20">
                    <CardContent className="p-6 text-center">
                      <div className="mb-4 inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary/10 group-hover:bg-primary/20 transition-colors">
                        <IconComponent className="h-8 w-8 text-primary" />
                      </div>
                      <h3 className="text-xl font-semibold text-foreground mb-2">
                        {category.name}
                      </h3>
                      <p className="text-primary font-medium mb-2">
                        {category.count} {category.count === 1 ? "Book" : "Books"}
                      </p>
                    </CardContent>
                  </Card>
                </Link>
              );
            })}
          </div>
        ) : (
          <div className="text-center py-12">
            <p className="text-muted-foreground">No categories available at the moment.</p>
          </div>
        )}
      </div>
    </section>
  );
}
