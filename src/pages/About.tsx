import { Header } from "@/components/Header";
import { Footer } from "@/components/Footer";
import { Card, CardContent } from "@/components/ui/card";

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      <main className="container mx-auto px-4 py-12">
        <div className="max-w-4xl mx-auto space-y-8">
          <div className="text-center space-y-4">
            <h1 className="text-4xl lg:text-5xl font-bold text-foreground">
              About Vikas Computers and Printers
            </h1>
            <p className="text-xl text-muted-foreground">
              Preserving Hindi Literature Since 1974
            </p>
          </div>

          <Card>
            <CardContent className="p-8 space-y-6">
              <section>
                <h2 className="text-2xl font-semibold text-foreground mb-4">Our Story</h2>
                <p className="text-muted-foreground leading-relaxed">
                  Founded in 1974, Vikas Computers and Printers has been dedicated to preserving 
                  and promoting Hindi literature for generations. We believe in the power of 
                  books to connect us with India's rich literary heritage and cultural wisdom.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-semibold text-foreground mb-4">Our Mission</h2>
                <p className="text-muted-foreground leading-relaxed">
                  Our mission is to make Hindi literature accessible to everyone. We curate 
                  a diverse collection spanning literature, poetry, philosophy, spiritual texts, 
                  and biographies, ensuring that readers can explore the depth and beauty of 
                  Hindi language and culture.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-semibold text-foreground mb-4">Our Collection</h2>
                <p className="text-muted-foreground leading-relaxed">
                  We offer an extensive collection of Hindi books, from timeless classics to 
                  contemporary works. Our catalog includes works by renowned authors and 
                  award-winning publications, carefully selected to provide readers with 
                  quality literature.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-semibold text-foreground mb-4">Contact Us</h2>
                <div className="space-y-2 text-muted-foreground">
                  <p><strong>Address:</strong> 1/10753, Subhash Park, Naveen Shahdara, Delhi, India</p>
                  <p><strong>Phone:</strong> +91 9810189445</p>
                  <p><strong>Email:</strong> vikascprint@gmail.com</p>
                </div>
              </section>
            </CardContent>
          </Card>
        </div>
      </main>
      <Footer />
    </div>
  );
}

