import React from 'react';
import { useAuth } from '../services/auth';

const PatientDashboard = () => {
  const { currentUser } = useAuth();
  
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6">Patient Dashboard</h1>
      
      <div className="grid md:grid-cols-3 gap-6">
        <div className="card">
          <h2 className="text-xl font-bold mb-4">My Profile</h2>
          <p><strong>Name:</strong> {currentUser?.name}</p>
          <p><strong>Email:</strong> {currentUser?.email}</p>
          <button className="btn btn-primary mt-4">Edit Profile</button>
        </div>
        
        <div className="card">
          <h2 className="text-xl font-bold mb-4">Upcoming Appointments</h2>
          <p className="text-gray-600">You have no upcoming appointments.</p>
          <button className="btn btn-primary mt-4">Book Appointment</button>
        </div>
        
        <div className="card">
          <h2 className="text-xl font-bold mb-4">My Treatments</h2>
          <p className="text-gray-600">No active treatments.</p>
          <button className="btn btn-primary mt-4">View All</button>
        </div>
      </div>
      
      <div className="mt-8">
        <h2 className="text-xl font-bold mb-4">Recent Activity</h2>
        <div className="card">
          <p className="text-gray-600">No recent activity.</p>
        </div>
      </div>
    </div>
  );
};

export default PatientDashboard;
