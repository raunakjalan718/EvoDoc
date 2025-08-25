import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

// Mock data for patient dashboard
const mockAppointments = [
  {
    id: 1,
    doctor: "Dr. Sarah Johnson",
    specialty: "Cardiologist",
    date: "2023-08-28",
    time: "10:00 AM",
    status: "confirmed"
  },
  {
    id: 2,
    doctor: "Dr. Michael Chen",
    specialty: "Dermatologist",
    date: "2023-09-05",
    time: "2:30 PM",
    status: "pending"
  }
];

const mockHealthInsights = [
  {
    id: 1,
    title: "Blood Pressure Analysis",
    description: "Your blood pressure readings show improvement over the last month.",
    recommendation: "Continue with your current medication and lifestyle changes.",
    date: "2023-08-20"
  },
  {
    id: 2,
    title: "Medication Reminder",
    description: "Don't forget to take your prescribed antibiotics for the full course.",
    recommendation: "Set daily reminders for best results.",
    date: "2023-08-22"
  }
];

const mockNotifications = [
  {
    id: 1,
    title: "New Lab Results",
    message: "Your blood work results are now available.",
    time: "2 hours ago",
    read: false
  },
  {
    id: 2,
    title: "Appointment Confirmation",
    message: "Your appointment with Dr. Sarah Johnson has been confirmed.",
    time: "1 day ago",
    read: true
  },
  {
    id: 3,
    title: "Prescription Refill",
    message: "Your prescription for Lisinopril is ready for refill.",
    time: "3 days ago",
    read: true
  }
];

const PatientDashboard = () => {
  const { currentUser } = useAuth();
  const [appointments, setAppointments] = useState([]);
  const [insights, setInsights] = useState([]);
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    // Simulate API call to fetch data
    const fetchData = async () => {
      // In a real app, these would be actual API calls
      setTimeout(() => {
        setAppointments(mockAppointments);
        setInsights(mockHealthInsights);
        setNotifications(mockNotifications);
        setLoading(false);
      }, 1000);
    };
    
    fetchData();
  }, []);
  
  // Format date to readable format
  const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };
  
  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="loading-spinner"></div>
      </div>
    );
  }
  
  return (
    <div className="page-wrapper">
      <div className="container py-8">
        {/* Welcome section */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold">Welcome, {currentUser?.name || 'Patient'}</h1>
          <p className="text-gray-600">Here's an overview of your health and upcoming appointments.</p>
        </div>
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main content - 2/3 width */}
          <div className="lg:col-span-2">
            {/* Upcoming appointments */}
            <div className="card mb-8">
              <div className="card-header flex justify-between items-center">
                <h2 className="text-xl font-semibold">Upcoming Appointments</h2>
                <Link to="/patient/appointments" className="text-primary text-sm">View all</Link>
              </div>
              
              <div className="card-body">
                {appointments.length > 0 ? (
                  <div className="space-y-4">
                    {appointments.map(appointment => (
                      <div key={appointment.id} className="p-4 border rounded-md flex justify-between items-center">
                        <div>
                          <h3 className="font-medium">{appointment.doctor}</h3>
                          <p className="text-sm text-gray-600">{appointment.specialty}</p>
                          <p className="text-sm text-gray-600">
                            {formatDate(appointment.date)} at {appointment.time}
                          </p>
                        </div>
                        
                        <div>
                          <span className={`badge ${appointment.status === 'confirmed' ? 'badge-success' : 'badge-warning'}`}>
                            {appointment.status.charAt(0).toUpperCase() + appointment.status.slice(1)}
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-center py-4 text-gray-600">No upcoming appointments.</p>
                )}
              </div>
              
              <div className="card-footer text-center">
                <Link to="/patient/appointments/new" className="btn btn-primary">
                  Book New Appointment
                </Link>
              </div>
            </div>
            
            {/* Health insights */}
            <div className="card">
              <div className="card-header">
                <h2 className="text-xl font-semibold">AI Health Insights</h2>
              </div>
              
              <div className="card-body">
                {insights.length > 0 ? (
                  <div className="space-y-4">
                    {insights.map(insight => (
                      <div key={insight.id} className="p-4 border rounded-md bg-gray-50">
                        <div className="flex items-start">
                          <div className="p-2 bg-primary-100 rounded-full mr-4">
                            <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                          </div>
                          
                          <div>
                            <h3 className="font-medium">{insight.title}</h3>
                            <p className="text-sm text-gray-600 mt-1">{insight.description}</p>
                            
                            {insight.recommendation && (
                              <div className="mt-2 p-2 bg-blue-50 border-l-4 border-blue-400 text-sm">
                                <strong>Recommendation:</strong> {insight.recommendation}
                              </div>
                            )}
                            
                            <p className="text-xs text-gray-500 mt-2">Generated on {formatDate(insight.date)}</p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-center py-4 text-gray-600">No health insights available.</p>
                )}
              </div>
            </div>
          </div>
          
          {/* Sidebar - 1/3 width */}
          <div>
            {/* Quick actions */}
            <div className="card mb-8">
              <div className="card-header">
                <h2 className="text-xl font-semibold">Quick Actions</h2>
              </div>
              
              <div className="card-body p-0">
                <Link to="/patient/appointments/new" className="flex items-center p-4 border-b hover:bg-gray-50">
                  <div className="p-2 bg-primary-100 rounded-full mr-4">
                    <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <span>Book Appointment</span>
                </Link>
                
                <Link to="/patient/health-records/upload" className="flex items-center p-4 border-b hover:bg-gray-50">
                  <div className="p-2 bg-primary-100 rounded-full mr-4">
                    <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                    </svg>
                  </div>
                  <span>Upload Health Record</span>
                </Link>
                
                <Link to="/patient/doctors" className="flex items-center p-4 border-b hover:bg-gray-50">
                  <div className="p-2 bg-primary-100 rounded-full mr-4">
                    <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                  </div>
                  <span>Find Doctor</span>
                </Link>
                
                <Link to="/patient/reviews/new" className="flex items-center p-4 hover:bg-gray-50">
                  <div className="p-2 bg-primary-100 rounded-full mr-4">
                    <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                  </div>
                  <span>Write Review</span>
                </Link>
              </div>
            </div>
            
            {/* Notifications */}
            <div className="card">
              <div className="card-header flex justify-between items-center">
                <h2 className="text-xl font-semibold">Notifications</h2>
                <span className="badge badge-primary">{notifications.filter(n => !n.read).length}</span>
              </div>
              
              <div className="card-body p-0">
                {notifications.length > 0 ? (
                  <div>
                    {notifications.map(notification => (
                      <div key={notification.id} className={`p-4 border-b ${!notification.read ? 'bg-blue-50' : ''}`}>
                        <h3 className="font-medium">{notification.title}</h3>
                        <p className="text-sm text-gray-600 mt-1">{notification.message}</p>
                        <p className="text-xs text-gray-500 mt-2">{notification.time}</p>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-center py-4 text-gray-600">No notifications.</p>
                )}
              </div>
              
              {notifications.length > 0 && (
                <div className="card-footer text-center">
                  <button className="text-primary text-sm">Mark all as read</button>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PatientDashboard;
