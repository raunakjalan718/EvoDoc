import React from 'react';
import { Link } from 'react-router-dom';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="container footer-content">
        <div className="footer-links">
          <Link to="/about" className="footer-link">About</Link>
          <Link to="/features" className="footer-link">Features</Link>
          <Link to="/contact" className="footer-link">Contact</Link>
          <Link to="/privacy" className="footer-link">Privacy Policy</Link>
          <Link to="/terms" className="footer-link">Terms of Service</Link>
        </div>
        
        <div className="footer-copyright">
          &copy; {new Date().getFullYear()} EvoDoc. All rights reserved.
        </div>
      </div>
    </footer>
  );
};

export default Footer;
