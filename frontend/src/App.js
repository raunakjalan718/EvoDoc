import React, { useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { getCurrentUser } from './redux/slices/authSlice';
import AuthService from './services/auth';

// Public pages
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import ForgotPassword from './pages/ForgotPassword';
import ResetPassword from './pages/ResetPassword';
import VerifyEmailRequired from './pages/VerifyEmailRequired';

// Doctor pages
import DoctorDashboard from './pages/doctor/Dashboard';
import ApprovalPending from './pages/doctor/ApprovalPending';

// Patient pages
import PatientDashboard from './pages/patient/Dashboard';

// Admin pages
import AdminDashboard from './pages/admin/Dashboard';

// Layout components
import Header from './components/Header';
import Footer from './components/Footer';

// Protected route component
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  const dispatch = useDispatch();
  const { isLoading } = useSelector(state => state.auth);
  
  useEffect(() => {
    // Check if user is already logged in on app load
    if (AuthService.isLoggedIn()) {
      dispatch(getCurrentUser());
    }
  }, [dispatch]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <BrowserRouter>
      <div className="min-h-screen flex flex-col">
        <Header />
        <main className="flex-grow">
          <Routes>
            {/* Public routes */}
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/forgot-password" element={<ForgotPassword />} />
            <Route path="/reset-password/:uidb64/:token" element={<ResetPassword />} />
            <Route path="/verify-email-required" element={<VerifyEmailRequired />} />
            
            {/* Doctor routes */}
            <Route 
              path="/doctor/dashboard" 
              element={
                <ProtectedRoute requiredRole="doctor">
                  <DoctorDashboard />
                </ProtectedRoute>
              } 
            />
            <Route path="/doctor/approval-pending" element={<ApprovalPending />} />
            
            {/* Patient routes */}
            <Route 
              path="/patient/dashboard" 
              element={
                <ProtectedRoute requiredRole="patient">
                  <PatientDashboard />
                </ProtectedRoute>
              } 
            />
            
            {/* Admin routes */}
            <Route 
              path="/admin/dashboard" 
              element={
                <ProtectedRoute requiredRole="admin">
                  <AdminDashboard />
                </ProtectedRoute>
              } 
            />
            
            {/* Catch-all route */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </BrowserRouter>
  );
}

export default App;
