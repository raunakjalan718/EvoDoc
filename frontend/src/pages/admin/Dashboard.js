import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getStats, getRecentUsers, getRecentReviews } from '../../services/adminService';

const Dashboard = () => {
  const [stats, setStats] = useState({
    patients: 0,
    doctors: 0,
    treatments: 0,
    reviews: 0
  });
  
  const [recentUsers, setRecentUsers] = useState([]);
  const [recentReviews, setRecentReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [statsData, usersData, reviewsData] = await Promise.all([
          getStats(),
          getRecentUsers(),
          getRecentReviews()
        ]);
        
        setStats(statsData);
        setRecentUsers(usersData);
        setRecentReviews(reviewsData);
      } catch (err) {
        setError('Failed to load dashboard data. Please try again later.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    
    fetchDashboardData();
  }, []);
  
  if (loading) return <div className="loading-spinner">Loading dashboard data...</div>;
  
  return (
    <div className="admin-dashboard">
      <h1>Admin Dashboard</h1>
      
      {error && <div className="error-message">{error}</div>}
      
      <div className="stats-grid">
        <div className="stat-card">
          <h2>Patients</h2>
          <p className="stat-number">{stats.patients}</p>
        </div>
        <div className="stat-card">
          <h2>Doctors</h2>
          <p className="stat-number">{stats.doctors}</p>
        </div>
        <div className="stat-card">
          <h2>Treatments</h2>
          <p className="stat-number">{stats.treatments}</p>
        </div>
        <div className="stat-card">
          <h2>Reviews</h2>
          <p className="stat-number">{stats.reviews}</p>
        </div>
      </div>
      
      <div className="admin-panels">
        <div className="admin-panel">
          <h2>Recent Users</h2>
          <table className="admin-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Type</th>
                <th>Date Joined</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {recentUsers.map(user => (
                <tr key={user.id}>
                  <td>{user.name}</td>
                  <td><span className={`user-badge ${user.type}`}>{user.type}</span></td>
                  <td>{user.date}</td>
                  <td><Link to={`/admin/users/${user.id}`} className="view-button">View</Link></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        
        <div className="admin-panel">
          <h2>Recent Reviews</h2>
          <table className="admin-table">
            <thead>
              <tr>
                <th>Treatment</th>
                <th>Rating</th>
                <th>Comment</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              {recentReviews.map(review => (
                <tr key={review.id}>
                  <td>{review.treatment}</td>
                  <td>
                    <div className="star-rating">
                      {[...Array(5)].map((_, i) => (
                        <span key={i} className={i < review.rating ? 'star filled' : 'star'}>★</span>
                      ))}
                    </div>
                  </td>
                  <td className="comment-cell">{review.comment}</td>
                  <td>{review.date}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
