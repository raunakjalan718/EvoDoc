import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

const Login = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    role: 'patient' // Default role
  });
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  
  const { login } = useAuth();
  const navigate = useNavigate();
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
    
    // Clear error when field is modified
    if (errors[name]) {
      setErrors({ ...errors, [name]: '' });
    }
  };
  
  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email is invalid';
    }
    
    if (!formData.password) {
      newErrors.password = 'Password is required';
    }
    
    return newErrors;
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate form
    const formErrors = validateForm();
    if (Object.keys(formErrors).length > 0) {
      setErrors(formErrors);
      return;
    }
    
    setIsLoading(true);
    
    try {
      // Attempt to login
      await login(formData.email, formData.password, formData.role);
      
      // Redirect based on role
      switch (formData.role) {
        case 'doctor':
          navigate('/doctor/dashboard');
          break;
        case 'admin':
          navigate('/admin/dashboard');
          break;
        case 'patient':
        default:
          navigate('/patient/dashboard');
          break;
      }
    } catch (error) {
      setErrors({ general: 'Invalid email or password' });
    } finally {
      setIsLoading(false);
    }
  };
  
  return (
    <div className="flex min-h-screen bg-gray-50">
      <div className="container mx-auto flex flex-col md:flex-row items-center justify-center px-4 py-12">
        {/* Left side - Form */}
        <div className="w-full md:w-1/2 max-w-md">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold">Welcome Back</h1>
            <p className="text-gray-600 mt-2">Sign in to your EvoDoc account</p>
          </div>
          
          {errors.general && (
            <div className="alert alert-danger mb-4">
              {errors.general}
            </div>
          )}
          
          <form onSubmit={handleSubmit} className="card p-6">
            {/* User role selection */}
            <div className="form-group mb-6">
              <label className="form-label">I am a:</label>
              <div className="flex gap-4">
                <label className="flex items-center cursor-pointer">
                  <input
                    type="radio"
                    name="role"
                    value="patient"
                    checked={formData.role === 'patient'}
                    onChange={handleChange}
                    className="mr-2"
                  />
                  Patient
                </label>
                
                <label className="flex items-center cursor-pointer">
                  <input
                    type="radio"
                    name="role"
                    value="doctor"
                    checked={formData.role === 'doctor'}
                    onChange={handleChange}
                    className="mr-2"
                  />
                  Doctor
                </label>
                
                <label className="flex items-center cursor-pointer">
                  <input
                    type="radio"
                    name="role"
                    value="admin"
                    checked={formData.role === 'admin'}
                    onChange={handleChange}
                    className="mr-2"
                  />
                  Admin
                </label>
              </div>
            </div>
            
            {/* Email field */}
            <div className="form-group">
              <label htmlFor="email" className="form-label">Email</label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className={`form-input ${errors.email ? 'border-danger-color' : ''}`}
                placeholder="you@example.com"
              />
              {errors.email && <div className="form-error">{errors.email}</div>}
            </div>
            
            {/* Password field */}
            <div className="form-group">
              <div className="flex items-center justify-between">
                <label htmlFor="password" className="form-label">Password</label>
                <Link to="/forgot-password" className="text-sm text-primary">
                  Forgot password?
                </Link>
              </div>
              
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                className={`form-input ${errors.password ? 'border-danger-color' : ''}`}
                placeholder="••••••••"
              />
              {errors.password && <div className="form-error">{errors.password}</div>}
            </div>
            
            {/* Remember me checkbox */}
            <div className="form-group flex items-center">
              <input
                type="checkbox"
                id="remember"
                name="remember"
                className="mr-2"
              />
              <label htmlFor="remember" className="text-sm">Remember me</label>
            </div>
            
            {/* Submit button */}
            <button 
              type="submit" 
              className="btn btn-primary w-full"
              disabled={isLoading}
            >
              {isLoading ? (
                <span className="flex items-center justify-center">
                  <span className="loading-spinner w-5 h-5 mr-2"></span>
                  Signing in...
                </span>
              ) : 'Sign in'}
            </button>
            
            {/* Register link */}
            <div className="text-center mt-4">
              <p className="text-sm text-gray-600">
                Don't have an account?{' '}
                <Link to="/register" className="text-primary font-medium">
                  Create account
                </Link>
              </p>
            </div>
          </form>
        </div>
        
        {/* Right side - Image/Illustration */}
        <div className="w-full md:w-1/2 mt-8 md:mt-0 hidden md:block">
          <img 
            src="/images/doctor-illustration.svg" 
            alt="Healthcare illustration" 
            className="w-full max-w-md mx-auto"
          />
        </div>
      </div>
    </div>
  );
};

export default Login;
