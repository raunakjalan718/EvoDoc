import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import './styles/animations.css'; // Include animations CSS
import App from './App';

// Add Vanta.js dependencies to head
const threeScript = document.createElement('script');
threeScript.src = 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js';
document.head.appendChild(threeScript);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
