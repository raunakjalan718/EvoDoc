import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className="fixed w-full top-0 bg-white z-50">
      <div className="container mx-auto px-6 py-4 flex justify-between items-center">
        <Link to="/" className="flex items-center">
          <svg className="w-8 h-8 text-primary-600 mr-2" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
          </svg>
          <span className="text-2xl font-bold text-primary-600">EvoDoc</span>
        </Link>
        
        <div className="flex items-center space-x-6">
          <Link 
            to="/login" 
            className="text-lg font-medium text-gray-700 hover:text-primary-600 transition-colors"
          >
            Login
          </Link>
          <Link 
            to="/register" 
            className="text-lg font-medium text-white bg-primary-600 px-6 py-2 rounded-md hover:bg-primary-700 transition-colors"
          >
            Register
          </Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
