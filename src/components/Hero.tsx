import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";
import heroImage from "@/assets/imgg.jpg";

export function Hero() {
  return (
    <section className="relative bg-gradient-hero overflow-hidden">
      <div className="container mx-auto px-4 py-20 lg:py-32">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          <div className="space-y-8">
            <div className="space-y-4">
              <h1 className="text-4xl lg:text-6xl font-bold text-primary-foreground leading-tight">
                Discover the
                <span className="block text-accent-foreground">
                  Wisdom of Hindi Literature
                </span>
              </h1>
              <p className="text-xl text-primary-foreground/90 leading-relaxed">
                Explore our extensive collection of Hindi books spanning literature, 
                philosophy, poetry, and spiritual texts. Connect with India's rich 
                literary heritage through our carefully curated publications.
              </p>
            </div>
            
            <div className="flex flex-col sm:flex-row gap-4">
              <Link to="/books">
                <Button size="lg" variant="secondary" className="text-lg px-8 hover:bg-primary-foreground/10">
                  Browse Collection
                </Button>
              </Link>
              <Link to="/books?sort_by=created_at&sort_order=desc">
                <Button size="lg" variant="secondary" className="text-lg px-8 hover:bg-primary-foreground/10">
                  New Releases
                </Button>
              </Link>
            </div>
          </div>
          
          <div className="relative">
            <div className="absolute inset-0 bg-gradient-to-r from-primary/20 to-accent/20 rounded-2xl blur-3xl"></div>
            <img 
              src={heroImage} 
              alt="Collection of Hindi Books"
              className="relative z-10 w-full rounded-2xl shadow-elegant"
            />
          </div>
        </div>
      </div>
    </section>
  );
}
