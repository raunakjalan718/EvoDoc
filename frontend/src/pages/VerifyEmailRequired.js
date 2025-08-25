import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import AuthService from '../services/auth';

const VerifyEmailRequired = () => {
  const { user } = useSelector(state => state.auth);
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const handleResendVerification = async () => {
    try {
      setIsLoading(true);
      setMessage('');
      
      // Call API to resend verification email
      await AuthService.resendVerificationEmail();
      
      setSuccess(true);
      setMessage('Verification email has been sent. Please check your inbox.');
    } catch (error) {
      setSuccess(false);
      setMessage(error.message || 'Failed to resend verification email. Please try again later.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          <div className="text-center">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Email Verification Required</h2>
            
            <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-6">
              <div className="flex">
                <div className="flex-shrink-0">
                  <svg className="h-5 w-5 text-yellow-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="ml-3">
                  <p className="text-sm text-yellow-700">
                    Your email address ({user?.email}) has not been verified yet. Please verify your email to access this feature.
                  </p>
                </div>
              </div>
            </div>
            
            {message && (
              <div className={`mb-6 p-4 ${success ? 'bg-green-50 text-green-800 border-green-400' : 'bg-red-50 text-red-800 border-red-400'} border-l-4`}>
                {message}
              </div>
            )}
            
            <div className="mt-6">
              <button
                onClick={handleResendVerification}
                disabled={isLoading}
                className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? 'Sending...' : 'Resend Verification Email'}
              </button>
            </div>
            
            <div className="mt-4">
              <Link
                to="/"
                className="text-sm font-medium text-primary-600 hover:text-primary-500"
              >
                Return to Home
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default VerifyEmailRequired;
