import { Link } from "react-router-dom";
import { Mail, Phone, MapPin, Facebook, Twitter, Instagram } from "lucide-react";

export function Footer() {
  return (
    <footer className="bg-foreground text-background py-12">
      <div className="container mx-auto px-4">
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          <div className="space-y-4">
            <h3 className="text-xl font-bold bg-gradient-hero bg-clip-text text-transparent">
              Vikas Computers and Printers
            </h3>
            <p className="text-background/80">
              Preserving and promoting Hindi literature for generations. 
              Your trusted partner in discovering the best of Hindi books.
            </p>
            <div className="flex space-x-4">
              <Facebook className="h-5 w-5 text-background/60 hover:text-background cursor-pointer transition-colors" />
              <Twitter className="h-5 w-5 text-background/60 hover:text-background cursor-pointer transition-colors" />
              <Instagram className="h-5 w-5 text-background/60 hover:text-background cursor-pointer transition-colors" />
            </div>
          </div>
          
          <div>
            <h4 className="font-semibold mb-4 text-background">Quick Links</h4>
            <ul className="space-y-2">
              <li><Link to="/books" className="text-background/80 hover:text-background transition-colors">All Books</Link></li>
              <li><Link to="/books?sort_by=created_at&sort_order=desc" className="text-background/80 hover:text-background transition-colors">New Releases</Link></li>
              <li><Link to="/about" className="text-background/80 hover:text-background transition-colors">About Us</Link></li>
            </ul>
          </div>
          
          <div>
            <h4 className="font-semibold mb-4 text-background">Categories</h4>
            <ul className="space-y-2">
              <li><Link to="/books?category=साहित्य" className="text-background/80 hover:text-background transition-colors">Literature</Link></li>
              <li><Link to="/books?category=कविता" className="text-background/80 hover:text-background transition-colors">Poetry</Link></li>
              <li><Link to="/books?category=दर्शन" className="text-background/80 hover:text-background transition-colors">Philosophy</Link></li>
              <li><Link to="/books?category=धर्म" className="text-background/80 hover:text-background transition-colors">Spiritual</Link></li>
            </ul>
          </div>
          
          <div>
            <h4 className="font-semibold mb-4 text-background">Contact Info</h4>
            <div className="space-y-3">
              <div className="flex items-center space-x-3">
                <MapPin className="h-5 w-5 text-background/60" />
                <span className="text-background/80">1/10753, Subhash Park, Naveen Shahdara, Delhi, India</span>
              </div>
              <div className="flex items-center space-x-3">
                <Phone className="h-5 w-5 text-background/60" />
                <span className="text-background/80">+91 9810189445</span>
              </div>
              <div className="flex items-center space-x-3">
                <Mail className="h-5 w-5 text-background/60" />
                <span className="text-background/80">vikascprint@gmail.com</span>
              </div>
            </div>
          </div>
        </div>
        
        <div className="border-t border-background/20 mt-8 pt-8 text-center">
          <p className="text-background/60">
            © 1974 Vikas Computers and Printers. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
}
