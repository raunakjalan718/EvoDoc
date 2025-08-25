import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../services/auth';

const Header = () => {
  const { currentUser, logout } = useAuth();
  const navigate = useNavigate();
  
  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="py-4 border-b">
      <div className="container mx-auto px-4 flex justify-between items-center">
        <div className="flex items-center">
          <Link to="/" className="flex items-center">
            <svg className="w-8 h-8" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
            </svg>
            <span className="ml-2 text-xl font-bold">EvoDoc</span>
          </Link>
          
          <nav className="hidden md:flex ml-6 space-x-4">
            <Link to="/" className="hover:text-red-700">Home</Link>
            <Link to="/about" className="hover:text-red-700">About</Link>
            <Link to="/features" className="hover:text-red-700">Features</Link>
            <Link to="/contact" className="hover:text-red-700">Contact</Link>
          </nav>
        </div>
        
        <div className="flex items-center space-x-4">
          {currentUser ? (
            <>
              <span>{currentUser.name}</span>
              <button onClick={handleLogout} className="btn btn-primary">Logout</button>
            </>
          ) : (
            <>
              <Link to="/login" className="hover:text-red-700">Login</Link>
              <Link to="/register" className="btn btn-primary">Register</Link>
            </>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;
