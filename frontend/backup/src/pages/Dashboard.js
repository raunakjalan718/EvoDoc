import React from 'react';
import { useAuth } from '../contexts/AuthContext';

const Dashboard = () => {
  const { currentUser, isPatient, isDoctor } = useAuth();

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Dashboard</h1>
      
      <div className="bg-white shadow overflow-hidden sm:rounded-lg">
        <div className="px-4 py-5 sm:px-6">
          <h2 className="text-lg leading-6 font-medium text-gray-900">
            Welcome, {currentUser?.first_name || currentUser?.username}!
          </h2>
          <p className="mt-1 max-w-2xl text-sm text-gray-500">
            {isPatient ? 'Patient Dashboard' : isDoctor ? 'Doctor Dashboard' : 'Admin Dashboard'}
          </p>
        </div>
        <div className="border-t border-gray-200 px-4 py-5 sm:p-6">
          <p className="text-gray-700">
            This is a placeholder for the full dashboard. In a complete implementation, this would show:
          </p>
          {isPatient && (
            <ul className="list-disc list-inside mt-4 space-y-2 text-gray-600">
              <li>Your active treatments</li>
              <li>Recent health metrics</li>
              <li>Upcoming appointments</li>
              <li>Treatment recommendations</li>
            </ul>
          )}
          {isDoctor && (
            <ul className="list-disc list-inside mt-4 space-y-2 text-gray-600">
              <li>Your upcoming appointments</li>
              <li>Recent patient updates</li>
              <li>Treatment effectiveness statistics</li>
              <li>Patient follow-up reminders</li>
            </ul>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
