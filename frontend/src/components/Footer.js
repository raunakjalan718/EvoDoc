import React from 'react';
import { Link } from 'react-router-dom';

const Footer = () => {
  return (
    <footer className="py-6 border-t mt-auto">
      <div className="container mx-auto px-4">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="mb-4 md:mb-0">
            <Link to="/" className="text-lg font-bold">EvoDoc</Link>
          </div>
          
          <div className="flex space-x-4">
            <Link to="/about" className="hover:text-red-700">About</Link>
            <Link to="/features" className="hover:text-red-700">Features</Link>
            <Link to="/contact" className="hover:text-red-700">Contact</Link>
            <Link to="/privacy" className="hover:text-red-700">Privacy Policy</Link>
            <Link to="/terms" className="hover:text-red-700">Terms of Service</Link>
          </div>
        </div>
        
        <div className="mt-4 text-center text-sm text-gray-600">
          © {new Date().getFullYear()} EvoDoc. All rights reserved.
        </div>
      </div>
    </footer>
  );
};

export default Footer;
