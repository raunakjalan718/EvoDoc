import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../services/auth';
import Button from '../components/Button';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [userType, setUserType] = useState('patient');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  const { login } = useAuth();
  const navigate = useNavigate();
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      setError('');
      setLoading(true);
      
      await login(email, password, userType);
      
      // Redirect based on user type
      if (userType === 'patient') {
        navigate('/patient/dashboard');
      } else if (userType === 'doctor') {
        navigate('/doctor/dashboard');
      } else if (userType === 'admin') {
        navigate('/admin/dashboard');
      }
    } catch (err) {
      setError('Failed to log in. Please check your credentials.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="min-h-screen flex items-center justify-center py-12 px-4">
      <div className="max-w-md w-full">
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold">Welcome Back</h2>
          <p className="mt-2 text-gray-600">Sign in to your EvoDoc account</p>
        </div>
        
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}
        
        <form onSubmit={handleSubmit} className="card">
          <div className="mb-4">
            <p className="mb-2 font-medium">I am a:</p>
            <div className="flex gap-4">
              <label className="flex items-center">
                <input
                  type="radio"
                  name="userType"
                  value="patient"
                  checked={userType === 'patient'}
                  onChange={() => setUserType('patient')}
                  className="mr-2"
                />
                Patient
              </label>
              <label className="flex items-center">
                <input
                  type="radio"
                  name="userType"
                  value="doctor"
                  checked={userType === 'doctor'}
                  onChange={() => setUserType('doctor')}
                  className="mr-2"
                />
                Doctor
              </label>
              <label className="flex items-center">
                <input
                  type="radio"
                  name="userType"
                  value="admin"
                  checked={userType === 'admin'}
                  onChange={() => setUserType('admin')}
                  className="mr-2"
                />
                Admin
              </label>
            </div>
          </div>
          
          <div className="mb-4">
            <label className="block mb-2 font-medium">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="input"
              placeholder="you@example.com"
            />
          </div>
          
          <div className="mb-6">
            <div className="flex justify-between mb-2">
              <label className="font-medium">Password</label>
              <Link to="/forgot-password" className="text-sm text-red-700">
                Forgot password?
              </Link>
            </div>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="input"
            />
          </div>
          
          <div className="mb-6">
            <label className="flex items-center">
              <input type="checkbox" className="mr-2" />
              Remember me
            </label>
          </div>
          
          <Button
            type="submit"
            disabled={loading}
            className="w-full"
          >
            {loading ? 'Signing in...' : 'Sign in'}
          </Button>
          
          <div className="text-center mt-4">
            Don't have an account? <Link to="/register" className="text-red-700">Create account</Link>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Login;
