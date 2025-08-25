import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/common/Navbar';
import Footer from './components/common/Footer';
import { AuthProvider } from './contexts/AuthContext';

// Public pages
import Landing from './pages/public/Landing';
import Login from './pages/public/Login';
import Register from './pages/public/Register';
import NotFound from './pages/public/NotFound';

// Patient pages
import PatientDashboard from './pages/patient/Dashboard';
import PatientTreatments from './pages/patient/Treatments';
import PatientProfile from './pages/patient/Profile';

// Doctor pages
import DoctorDashboard from './pages/doctor/Dashboard';
import DoctorPatients from './pages/doctor/Patients';
import DoctorPrescribe from './pages/doctor/Prescribe';

// Admin pages
import AdminDashboard from './pages/admin/Dashboard';

// Protected route component
const ProtectedRoute = ({ children, requiredRole }) => {
  // In a real app, you would check if the user is authenticated
  // and has the required role
  const isAuthenticated = localStorage.getItem('token');
  const userRole = localStorage.getItem('userRole');
  
  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }
  
  if (requiredRole && userRole !== requiredRole) {
    return <Navigate to="/" />;
  }
  
  return children;
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <Navbar />
        <main className="app-main">
          <Routes>
            {/* Public routes */}
            <Route path="/" element={<Landing />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            
            {/* Patient routes */}
            <Route 
              path="/patient/dashboard" 
              element={
                <ProtectedRoute requiredRole="patient">
                  <PatientDashboard />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/patient/treatments" 
              element={
                <ProtectedRoute requiredRole="patient">
                  <PatientTreatments />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/patient/profile" 
              element={
                <ProtectedRoute requiredRole="patient">
                  <PatientProfile />
                </ProtectedRoute>
              } 
            />
            
            {/* Doctor routes */}
            <Route 
              path="/doctor/dashboard" 
              element={
                <ProtectedRoute requiredRole="doctor">
                  <DoctorDashboard />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/doctor/patients" 
              element={
                <ProtectedRoute requiredRole="doctor">
                  <DoctorPatients />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/doctor/prescribe" 
              element={
                <ProtectedRoute requiredRole="doctor">
                  <DoctorPrescribe />
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
            
            {/* 404 route */}
            <Route path="*" element={<NotFound />} />
          </Routes>
        </main>
        <Footer />
      </Router>
    </AuthProvider>
  );
}

export default App;
