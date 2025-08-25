import React from 'react';
import { useAuth } from '../services/auth';

const DoctorDashboard = () => {
  const { currentUser } = useAuth();
  
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6">Doctor Dashboard</h1>
      
      <div className="grid md:grid-cols-3 gap-6">
        <div className="card">
          <h2 className="text-xl font-bold mb-4">My Profile</h2>
          <p><strong>Name:</strong> Dr. {currentUser?.name}</p>
          <p><strong>Email:</strong> {currentUser?.email}</p>
          <button className="btn btn-primary mt-4">Edit Profile</button>
        </div>
        
        <div className="card">
          <h2 className="text-xl font-bold mb-4">Today's Appointments</h2>
          <p className="text-gray-600">No appointments scheduled for today.</p>
          <button className="btn btn-primary mt-4">View Schedule</button>
        </div>
        
        <div className="card">
          <h2 className="text-xl font-bold mb-4">My Patients</h2>
          <p className="text-gray-600">No patients assigned.</p>
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

export default DoctorDashboard;
