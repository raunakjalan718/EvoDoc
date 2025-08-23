import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

const Navbar = () => {
  const { currentUser, logout, isAuthenticated, isPatient, isDoctor } = useAuth();
  const navigate = useNavigate();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="bg-white shadow-md border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex-shrink-0 flex items-center">
              <svg className="h-8 w-8 text-primary-600" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2L2 7L12 12L22 7L12 2Z" fill="currentColor" />
                <path d="M2 17L12 22L22 17" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                <path d="M2 12L12 17L22 12" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
              <span className="ml-2 text-xl font-bold text-primary-600">EvoDoc</span>
            </Link>
            
            {isAuthenticated && (
              <div className="hidden md:ml-10 md:flex md:items-baseline md:space-x-4">
                <Link to="/dashboard" className="px-3 py-2 rounded-md text-sm font-medium text-gray-800 hover:text-primary-600 hover:bg-gray-50">
                  Dashboard
                </Link>
                
                {isPatient && (
                  <>
                    <Link to="/treatments" className="px-3 py-2 rounded-md text-sm font-medium text-gray-800 hover:text-primary-600 hover:bg-gray-50">
                      My Treatments
                    </Link>
                    <Link to="/reviews" className="px-3 py-2 rounded-md text-sm font-medium text-gray-800 hover:text-primary-600 hover:bg-gray-50">
                      My Reviews
                    </Link>
                  </>
                )}
                
                {isDoctor && (
                  <>
                    <Link to="/patients" className="px-3 py-2 rounded-md text-sm font-medium text-gray-800 hover:text-primary-600 hover:bg-gray-50">
                      Patients
                    </Link>
                    <Link to="/prescribe" className="px-3 py-2 rounded-md text-sm font-medium text-gray-800 hover:text-primary-600 hover:bg-gray-50">
                      Prescribe
                    </Link>
                  </>
                )}
              </div>
            )}
          </div>
          
          <div className="hidden md:flex items-center">
            {isAuthenticated ? (
              <div className="flex items-center">
                <div className="mr-4 relative">
                  <div className="flex items-center">
                    {currentUser?.profile_image ? (
                      <img src={currentUser.profile_image} alt="Profile" className="h-8 w-8 rounded-full" />
                    ) : (
                      <div className="h-8 w-8 rounded-full bg-primary-100 text-primary-600 flex items-center justify-center">
                        <span className="text-sm font-medium">
                          {currentUser?.first_name?.charAt(0) || currentUser?.username?.charAt(0) || 'U'}
                        </span>
                      </div>
                    )}
                    <span className="ml-2 text-sm font-medium text-gray-700">
                      {currentUser?.first_name || currentUser?.username}
                    </span>
                  </div>
                </div>
                <button
                  onClick={handleLogout}
                  className="ml-2 px-3 py-2 rounded-md text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                >
                  Logout
                </button>
              </div>
            ) : (
              <div className="flex items-center space-x-4">
                <Link to="/login" className="px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-primary-600 hover:bg-gray-50">
                  Login
                </Link>
                <Link to="/register" className="px-3 py-2 rounded-md text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
                  Register
                </Link>
              </div>
            )}
          </div>
          
          {/* Mobile menu button */}
          <div className="flex items-center md:hidden">
            <button
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="inline-flex items-center justify-center p-2 rounded-md text-gray-700 hover:text-primary-600 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500"
            >
              <span className="sr-only">{isMobileMenuOpen ? 'Close menu' : 'Open menu'}</span>
              {isMobileMenuOpen ? (
                <svg className="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              ) : (
                <svg className="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              )}
            </button>
          </div>
        </div>
      </div>
      
      {/* Mobile menu */}
      {isMobileMenuOpen && (
        <div className="md:hidden">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
            {isAuthenticated && (
              <>
                <Link 
                  to="/dashboard" 
                  className="block px-3 py-2 rounded-md text-base font-medium text-gray-800 hover:text-primary-600 hover:bg-gray-50"
                  onClick={() => setIsMobileMenuOpen(false)}
                >
                  Dashboard
                </Link>
                
                {isPatient && (
                  <>
                    <Link 
                      to="/treatments" 
                      className="block px-3 py-2 rounded-md text-base font-medium text-gray-800 hover:text-primary-600 hover:bg-gray-50"
                      onClick={() => setIsMobileMenuOpen(false)}
                    >
                      My Treatments
                    </Link>
                    <Link 
                      to="/reviews" 
                      className="block px-3 py-2 rounded-md text-base font-medium text-gray-800 hover:text-primary-600 hover:bg-gray-50"
                      onClick={() => setIsMobileMenuOpen(false)}
                    >
                      My Reviews
                    </Link>
                  </>
                )}
                
                {isDoctor && (
                  <>
                    <Link 
                      to="/patients" 
                      className="block px-3 py-2 rounded-md text-base font-medium text-gray-800 hover:text-primary-600 hover:bg-gray-50"
                      onClick={() => setIsMobileMenuOpen(false)}
                    >
                      Patients
                    </Link>
                    <Link 
                      to="/prescribe" 
                      className="block px-3 py-2 rounded-md text-base font-medium text-gray-800 hover:text-primary-600 hover:bg-gray-50"
                      onClick={() => setIsMobileMenuOpen(false)}
                    >
                      Prescribe
                    </Link>
                  </>
                )}
              </>
            )}
            
            {!isAuthenticated && (
              <>
                <Link 
                  to="/login" 
                  className="block px-3 py-2 rounded-md text-base font-medium text-gray-800 hover:text-primary-600 hover:bg-gray-50"
                  onClick={() => setIsMobileMenuOpen(false)}
                >
                  Login
                </Link>
                <Link 
                  to="/register" 
                  className="block px-3 py-2 rounded-md text-base font-medium text-gray-800 hover:text-primary-600 hover:bg-gray-50"
                  onClick={() => setIsMobileMenuOpen(false)}
                >
                  Register
                </Link>
              </>
            )}
          </div>
          
          {isAuthenticated && (
            <div className="pt-4 pb-3 border-t border-gray-200">
              <div className="flex items-center px-5">
                <div className="flex-shrink-0">
                  {currentUser?.profile_image ? (
                    <img src={currentUser.profile_image} alt="Profile" className="h-10 w-10 rounded-full" />
                  ) : (
                    <div className="h-10 w-10 rounded-full bg-primary-100 text-primary-600 flex items-center justify-center">
                      <span className="text-sm font-medium">
                        {currentUser?.first_name?.charAt(0) || currentUser?.username?.charAt(0) || 'U'}
                      </span>
                    </div>
                  )}
                </div>
                <div className="ml-3">
                  <div className="text-base font-medium text-gray-800">{currentUser?.first_name} {currentUser?.last_name}</div>
                  <div className="text-sm font-medium text-gray-500">{currentUser?.email}</div>
                </div>
              </div>
              <div className="mt-3 px-2 space-y-1">
                <button
                  onClick={() => {
                    handleLogout();
                    setIsMobileMenuOpen(false);
                  }}
                  className="block w-full text-left px-3 py-2 rounded-md text-base font-medium text-gray-800 hover:text-primary-600 hover:bg-gray-50"
                >
                  Logout
                </button>
              </div>
            </div>
          )}
        </div>
      )}
    </nav>
  );
};

export default Navbar;
