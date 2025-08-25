import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

// Mock data for doctor dashboard
const mockAppointments = [
  {
    id: 1,
    patient: "John Doe",
    age: 42,
    date: "2023-08-28",
    time: "10:00 AM",
    type: "Follow-up",
    status: "confirmed"
  },
  {
    id: 2,
    patient: "Emily Clark",
    age: 35,
    date: "2023-08-28",
    time: "11:00 AM",
    type: "New Patient",
    status: "confirmed"
  },
  {
    id: 3,
    patient: "Michael Smith",
    age: 50,
    date: "2023-08-28",
    time: "2:30 PM",
    type: "Consultation",
    status: "confirmed"
  }
];

const mockPatientAlerts = [
  {
    id: 1,
    patient: "Robert Johnson",
    age: 65,
    alert: "Abnormal blood pressure reading",
    severity: "high",
    time: "2 hours ago"
  },
  {
    id: 2,
    patient: "Sarah Williams",
    age: 28,
    alert: "New lab results uploaded",
    severity: "medium",
    time: "1 day ago"
  }
];

const mockStats = [
  {
    id: 1,
    title: "Total Patients",
    value: 124,
    change: "+4",
    changeType: "increase"
  },
  {
    id: 2,
    title: "Today's Appointments",
    value: 8,
    change: "-1",
    changeType: "decrease"
  },
  {
    id: 3,
    title: "Patient Satisfaction",
    value: "4.8/5",
    change: "+0.2",
    changeType: "increase"
  },
  {
    id: 4,
    title: "Pending Reviews",
    value: 5,
    change: "+2",
    changeType: "increase"
  }
];

const DoctorDashboard = () => {
  const { currentUser } = useAuth();
  const [appointments, setAppointments] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [stats, setStats] = useState([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    // Simulate API call to fetch data
    const fetchData = async () => {
      // In a real app, these would be actual API calls
      setTimeout(() => {
        setAppointments(mockAppointments);
        setAlerts(mockPatientAlerts);
        setStats(mockStats);
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
          <h1 className="text-3xl font-bold">Welcome, {currentUser?.name || 'Doctor'}</h1>
          <p className="text-gray-600">Here's your practice overview for today.</p>
        </div>
        
        {/* Stats cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {stats.map(stat => (
            <div key={stat.id} className="card p-6">
              <h3 className="text-gray-600 font-medium text-sm">{stat.title}</h3>
              <div className="flex items-center mt-2">
                <span className="text-3xl font-bold">{stat.value}</span>
                {stat.change && (
                  <span className={`ml-2 text-sm ${stat.changeType === 'increase' ? 'text-green-500' : 'text-red-500'}`}>
                    {stat.change}
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main content - 2/3 width */}
          <div className="lg:col-span-2">
            {/* Today's appointments */}
            <div className="card mb-8">
              <div className="card-header flex justify-between items-center">
                <h2 className="text-xl font-semibold">Today's Appointments</h2>
                <Link to="/doctor/appointments" className="text-primary text-sm">View all</Link>
              </div>
              
              <div className="card-body p-0">
                {appointments.length > 0 ? (
                  <table className="table">
                    <thead>
                      <tr>
                        <th>Patient</th>
                        <th>Time</th>
                        <th>Type</th>
                        <th>Status</th>
                        <th>Action</th>
                      </tr>
                    </thead>
                    <tbody>
                      {appointments.map(appointment => (
                        <tr key={appointment.id}>
                          <td>
                            <div>
                              <div className="font-medium">{appointment.patient}</div>
                              <div className="text-sm text-gray-600">{appointment.age} years</div>
                            </div>
                          </td>
                          <td>{appointment.time}</td>
                          <td>{appointment.type}</td>
                          <td>
                            <span className={`badge ${appointment.status === 'confirmed' ? 'badge-success' : 'badge-warning'}`}>
                              {appointment.status.charAt(0).toUpperCase() + appointment.status.slice(1)}
                            </span>
                          </td>
                          <td>
                            <div className="flex space-x-2">
                              <Link to={`/doctor/appointments/${appointment.id}`} className="btn btn-sm btn-outline">
                                View
                              </Link>
                              <Link to={`/doctor/consultations/start/${appointment.id}`} className="btn btn-sm btn-primary">
                                Start
                              </Link>
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                ) : (
                  <p className="text-center py-4 text-gray-600">No appointments scheduled for today.</p>
                )}
              </div>
            </div>
            
            {/* AI Insights for Doctors */}
            <div className="card">
              <div className="card-header">
                <h2 className="text-xl font-semibold">AI-Assisted Insights</h2>
              </div>
              
              <div className="card-body">
                <div className="space-y-4">
                  <div className="p-4 border rounded-md bg-blue-50">
                    <div className="flex items-start">
                      <div className="p-2 bg-blue-100 rounded-full mr-4">
                        <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                      </div>
                      
                      <div>
                        <h3 className="font-medium">Treatment Effectiveness Analysis</h3>
                        <p className="text-sm text-gray-600 mt-1">
                          Based on 8 similar patients, Lisinopril 10mg has shown 85% effectiveness for 
                          hypertension management with minimal side effects in patients similar to Emily Clark.
                        </p>
                      </div>
                    </div>
                  </div>
                  
                  <div className="p-4 border rounded-md bg-green-50">
                    <div className="flex items-start">
                      <div className="p-2 bg-green-100 rounded-full mr-4">
                        <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                      </div>
                      
                      <div>
                        <h3 className="font-medium">Patient Adherence Prediction</h3>
                        <p className="text-sm text-gray-600 mt-1">
                          John Doe has a 92% medication adherence score based on past history and follow-up attendance.
                          Low risk of treatment non-compliance.
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          {/* Sidebar - 1/3 width */}
          <div>
            {/* Patient alerts */}
            <div className="card mb-8">
              <div className="card-header">
                <h2 className="text-xl font-semibold">Patient Alerts</h2>
              </div>
              
              <div className="card-body p-0">
                {alerts.length > 0 ? (
                  <div>
                    {alerts.map(alert => (
                      <div key={alert.id} className="p-4 border-b hover:bg-gray-50">
                        <div className="flex items-start">
                          <div className={`p-2 rounded-full mr-4 ${
                            alert.severity === 'high' ? 'bg-red-100' : 
                            alert.severity === 'medium' ? 'bg-yellow-100' : 'bg-blue-100'
                          }`}>
                            <svg className={`w-5 h-5 ${
                              alert.severity === 'high' ? 'text-red-600' : 
                              alert.severity === 'medium' ? 'text-yellow-600' : 'text-blue-600'
                            }`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                            </svg>
                          </div>
                          
                          <div>
                            <h3 className="font-medium">{alert.patient}, {alert.age}</h3>
                            <p className="text-sm text-gray-600 mt-1">{alert.alert}</p>
                            <p className="text-xs text-gray-500 mt-2">{alert.time}</p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-center py-4 text-gray-600">No patient alerts.</p>
                )}
              </div>
            </div>
            
            {/* Quick actions */}
            <div className="card">
              <div className="card-header">
                <h2 className="text-xl font-semibold">Quick Actions</h2>
              </div>
              
              <div className="card-body p-0">
                <Link to="/doctor/appointments/schedule" className="flex items-center p-4 border-b hover:bg-gray-50">
                  <div className="p-2 bg-primary-100 rounded-full mr-4">
                    <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <span>Manage Schedule</span>
                </Link>
                
                <Link to="/doctor/patients" className="flex items-center p-4 border-b hover:bg-gray-50">
                  <div className="p-2 bg-primary-100 rounded-full mr-4">
                    <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                    </svg>
                  </div>
                  <span>Patient Directory</span>
                </Link>
                
                <Link to="/doctor/reviews" className="flex items-center p-4 border-b hover:bg-gray-50">
                  <div className="p-2 bg-primary-100 rounded-full mr-4">
                    <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
                    </svg>
                  </div>
                  <span>View Reviews</span>
                </Link>
                
                <Link to="/doctor/analytics" className="flex items-center p-4 hover:bg-gray-50">
                  <div className="p-2 bg-primary-100 rounded-full mr-4">
                    <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                    </svg>
                  </div>
                  <span>Performance Analytics</span>
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DoctorDashboard;
