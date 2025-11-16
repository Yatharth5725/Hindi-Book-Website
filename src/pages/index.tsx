import { Header } from "@/components/Header";
import { Hero } from "@/components/Hero";
import { FeaturedBooks } from "@/components/Featurebooks";
import { Categories } from "@/components/categories";
// Removed import of About as file is missing
import { Footer } from "@/components/Footer";

const Index = () => {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      <main>
        <Hero />
        <FeaturedBooks />
        <Categories />
        {/* Removed About component as file is missing */}
      </main>
      <Footer />
    </div>
  );
};

export default Index;