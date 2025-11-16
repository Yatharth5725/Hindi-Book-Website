import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { CheckCircle, Heart, Globe, Users } from "lucide-react";

const features = [
  {
    icon: CheckCircle,
    title: "Quality Publications",
    description: "Every book is carefully edited and beautifully designed"
  },
  {
    icon: Heart,
    title: "Cultural Heritage",
    description: "Preserving and promoting Hindi literary traditions"
  },
  {
    icon: Globe,
    title: "Global Reach",
    description: "Delivering Hindi literature worldwide"
  },
  {
    icon: Users,
    title: "Author Support",
    description: "Supporting both established and emerging Hindi authors"
  }
];

export function About() {
  return (
    <section className="py-16 bg-background">
      <div className="container mx-auto px-4">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          <div className="space-y-8">
            <div className="space-y-4">
              <h2 className="text-3xl lg:text-4xl font-bold text-foreground">
                About Hindi Pustaka Prakashan
              </h2>
              <p className="text-lg text-muted-foreground leading-relaxed">
                For over three decades, Hindi Pustaka Prakashan has been at the forefront 
                of Hindi literature publishing. We are committed to bringing you the finest 
                works in Hindi language, spanning classical literature, contemporary fiction, 
                poetry, philosophy, and spiritual texts.
              </p>
              <p className="text-lg text-muted-foreground leading-relaxed">
                Our mission is to preserve India's rich literary heritage while fostering 
                new voices in Hindi literature. We work closely with renowned authors and 
                emerging writers to publish books that inspire, educate, and entertain.
              </p>
            </div>
            
            <Button size="lg" className="bg-primary hover:bg-primary/90">
              Learn More About Us
            </Button>
          </div>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
            {features.map((feature) => {
              const IconComponent = feature.icon;
              return (
                <Card key={feature.title} className="bg-gradient-card border-border/50">
                  <CardContent className="p-6 text-center">
                    <div className="mb-4 inline-flex items-center justify-center w-12 h-12 rounded-full bg-primary/10">
                      <IconComponent className="h-6 w-6 text-primary" />
                    </div>
                    <h3 className="font-semibold text-foreground mb-2">
                      {feature.title}
                    </h3>
                    <p className="text-muted-foreground text-sm">
                      {feature.description}
                    </p>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </div>
      </div>
    </section>
  );
}