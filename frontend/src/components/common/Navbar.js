import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

const Navbar = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const { currentUser, logout } = useAuth();
  const location = useLocation();
  
  // Handle scroll event to change navbar style
  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 10) {
        setScrolled(true);
      } else {
        setScrolled(false);
      }
    };
    
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);
  
  // Get appropriate nav links based on user role
  const getNavLinks = () => {
    if (!currentUser) {
      return [
        { to: '/', label: 'Home' },
        { to: '/about', label: 'About' },
        { to: '/features', label: 'Features' },
        { to: '/contact', label: 'Contact' },
      ];
    }
    
    switch(currentUser.role) {
      case 'patient':
        return [
          { to: '/patient/dashboard', label: 'Dashboard' },
          { to: '/patient/appointments', label: 'Appointments' },
          { to: '/patient/health-records', label: 'Records' },
          { to: '/patient/doctors', label: 'Doctors' },
        ];
      case 'doctor':
        return [
          { to: '/doctor/dashboard', label: 'Dashboard' },
          { to: '/doctor/patients', label: 'Patients' },
          { to: '/doctor/appointments', label: 'Appointments' },
          { to: '/doctor/analytics', label: 'Analytics' },
        ];
      case 'admin':
        return [
          { to: '/admin/dashboard', label: 'Dashboard' },
          { to: '/admin/users', label: 'Users' },
          { to: '/admin/appointments', label: 'Appointments' },
          { to: '/admin/models', label: 'ML Models' },
        ];
      default:
        return [];
    }
  };
  
  const links = getNavLinks();
  
  // Handle logout
  const handleLogout = () => {
    logout();
    // Redirect to home page
    window.location.href = '/';
  };
  
  // Check if link is active
  const isActive = (path) => {
    return location.pathname === path;
  };
  
  return (
    <nav className={`navbar ${scrolled ? 'scrolled' : ''}`}>
      <div className="container navbar-container">
        <Link to="/" className="navbar-logo">
          <svg className="w-8 h-8" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
          </svg>
          <span>EvoDoc</span>
        </Link>
        
        {/* Desktop navigation */}
        <div className="navbar-links">
          {links.map((link, index) => (
            <Link 
              key={index}
              to={link.to}
              className={`navbar-link ${isActive(link.to) ? 'active' : ''}`}
            >
              {link.label}
            </Link>
          ))}
          
          {currentUser ? (
            <div className="flex items-center gap-4">
              <div className="navbar-user">
                <img 
                  src={currentUser.profileImage || "https://via.placeholder.com/32"} 
                  alt={currentUser.name}
                  className="w-8 h-8 rounded-full"
                />
                <span className="ml-2">{currentUser.name}</span>
              </div>
              
              <button onClick={handleLogout} className="btn btn-outline btn-sm">
                Logout
              </button>
            </div>
          ) : (
            <div className="flex items-center gap-4">
              <Link to="/login" className="navbar-link">Login</Link>
              <Link to="/register" className="btn btn-primary btn-sm">Register</Link>
            </div>
          )}
        </div>
        
        {/* Mobile menu button */}
        <div className="navbar-mobile-menu">
          <button 
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="p-2"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              {mobileMenuOpen ? (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        </div>
      </div>
      
      {/* Mobile menu */}
      {mobileMenuOpen && (
        <div className="navbar-mobile-links">
          {links.map((link, index) => (
            <Link 
              key={index}
              to={link.to}
              className={`navbar-link ${isActive(link.to) ? 'active' : ''}`}
              onClick={() => setMobileMenuOpen(false)}
            >
              {link.label}
            </Link>
          ))}
          
          {currentUser ? (
            <>
              <div className="navbar-user">
                <img 
                  src={currentUser.profileImage || "https://via.placeholder.com/32"} 
                  alt={currentUser.name}
                  className="w-8 h-8 rounded-full"
                />
                <span className="ml-2">{currentUser.name}</span>
              </div>
              
              <button onClick={handleLogout} className="btn btn-outline btn-sm">
                Logout
              </button>
            </>
          ) : (
            <>
              <Link 
                to="/login" 
                className="navbar-link" 
                onClick={() => setMobileMenuOpen(false)}
              >
                Login
              </Link>
              <Link 
                to="/register" 
                className="btn btn-primary btn-sm"
                onClick={() => setMobileMenuOpen(false)}
              >
                Register
              </Link>
            </>
          )}
        </div>
      )}
    </nav>
  );
};

export default Navbar;
