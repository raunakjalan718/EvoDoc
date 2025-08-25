import React from 'react';
import { useAuth } from '../services/auth';

const AdminDashboard = () => {
  const { currentUser } = useAuth();
  
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6">Admin Dashboard</h1>
      
      <div className="grid md:grid-cols-4 gap-6">
        <div className="card">
          <h2 className="text-xl font-bold mb-4">Users</h2>
          <p className="text-3xl font-bold text-red-700">0</p>
          <button className="btn btn-primary mt-4 w-full">Manage Users</button>
        </div>
        
        <div className="card">
          <h2 className="text-xl font-bold mb-4">Doctors</h2>
          <p className="text-3xl font-bold text-red-700">0</p>
          <button className="btn btn-primary mt-4 w-full">Manage Doctors</button>
        </div>
        
        <div className="card">
          <h2 className="text-xl font-bold mb-4">Patients</h2>
          <p className="text-3xl font-bold text-red-700">0</p>
          <button className="btn btn-primary mt-4 w-full">Manage Patients</button>
        </div>
        
        <div className="card">
          <h2 className="text-xl font-bold mb-4">Appointments</h2>
          <p className="text-3xl font-bold text-red-700">0</p>
          <button className="btn btn-primary mt-4 w-full">View All</button>
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

export default AdminDashboard;
