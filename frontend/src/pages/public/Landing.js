import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';

const Landing = () => {
  // Create animated medical elements
  useEffect(() => {
    const createMedicalElements = () => {
      const container = document.querySelector('.medical-graphics');
      if (!container) return;
      
      // Clear existing elements
      container.innerHTML = '';
      
      // Create pills
      for (let i = 0; i < 8; i++) {
        const pill = document.createElement('div');
        pill.className = 'pill';
        
        // Random properties
        const width = Math.random() * 40 + 20;
        const height = width * 0.4;
        
        pill.style.width = `${width}px`;
        pill.style.height = `${height}px`;
        pill.style.top = `${Math.random() * 70 + 10}%`;
        pill.style.left = `${Math.random() * 70 + 10}%`;
        pill.style.transform = `rotate(${Math.random() * 360}deg)`;
        pill.style.animationDelay = `${i * 0.3}s`;
        
        container.appendChild(pill);
      }
      
      // Create medical cross
      const cross = document.createElement('div');
      cross.className = 'medical-cross';
      cross.style.top = '30%';
      cross.style.right = '30%';
      container.appendChild(cross);
    };
    
    createMedicalElements();
    
    // Re-create elements on window resize
    window.addEventListener('resize', createMedicalElements);
    return () => window.removeEventListener('resize', createMedicalElements);
  }, []);
  
  return (
    <div className="landing-page">
      {/* Hero section */}
      <section className="hero bg-gradient-to-b from-white to-gray-50 py-16">
        <div className="container">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div className="hero-text">
              <h1 className="text-5xl font-bold leading-tight slide-in-left">
                Healthcare that <br />
                <span className="text-primary">evolves</span> with <br />
                your <span className="text-primary">feedback</span>
              </h1>
              
              <p className="text-lg text-gray-600 mt-6 slide-in-left" style={{ animationDelay: '0.2s' }}>
                EvoDoc learns from patient experiences to provide personalized treatment 
                recommendations and predict potential side effects.
              </p>
              
              <div className="flex flex-wrap gap-6 mt-8 slide-in-left" style={{ animationDelay: '0.4s' }}>
                <Link to="/register" className="tilt-button-animated">
                  <span className="btn btn-primary btn-lg">Get Started</span>
                </Link>
                
                <Link to="/login" className="btn btn-outline btn-lg">
                  Book Appointment
                </Link>
              </div>
            </div>
            
            <div className="medical-graphics relative h-[500px]">
              {/* Medical elements will be added by JavaScript */}
            </div>
          </div>
        </div>
      </section>
      
      {/* Features section */}
      <section className="features py-16 bg-white">
        <div className="container">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold">Personalized Healthcare Experience</h2>
            <p className="text-gray-600 mt-4 max-w-3xl mx-auto">
              Our AI-powered platform transforms patient experiences into actionable insights,
              making healthcare more effective and personalized.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mt-12">
            {/* Feature 1 */}
            <div className="card p-6">
              <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-primary" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              
              <h3 className="text-xl font-semibold mb-2">AI Health Insights</h3>
              <p className="text-gray-600">
                Get personalized health recommendations based on your medical history and similar patients' experiences.
              </p>
            </div>
            
            {/* Feature 2 */}
            <div className="card p-6">
              <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-primary" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
              
              <h3 className="text-xl font-semibold mb-2">Easy Appointment Booking</h3>
              <p className="text-gray-600">
                Book appointments with top doctors, get reminders, and manage your schedule all in one place.
              </p>
            </div>
            
            {/* Feature 3 */}
            <div className="card p-6">
              <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-primary" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              
              <h3 className="text-xl font-semibold mb-2">Secure Health Records</h3>
              <p className="text-gray-600">
                Store and access your medical records securely, and share them with healthcare providers as needed.
              </p>
            </div>
          </div>
        </div>
      </section>
      
      {/* Testimonials section */}
      <section className="testimonials py-16 bg-gray-50">
        <div className="container">
          <h2 className="text-3xl font-bold text-center mb-12">What Our Users Say</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {/* Testimonial 1 */}
            <div className="card p-6">
              <div className="flex items-center mb-4">
                <img 
                  src="https://randomuser.me/api/portraits/women/32.jpg" 
                  alt="Sarah Johnson" 
                  className="w-12 h-12 rounded-full"
                />
                <div className="ml-4">
                  <h4 className="font-semibold">Sarah Johnson</h4>
                  <p className="text-sm text-gray-600">Patient</p>
                </div>
              </div>
              
              <p className="text-gray-600">
                "EvoDoc helped me understand potential side effects of my medication that my doctor hadn't mentioned. 
                I was able to prepare and manage them much better."
              </p>
            </div>
            
            {/* Testimonial 2 */}
            <div className="card p-6">
              <div className="flex items-center mb-4">
                <img 
                  src="https://randomuser.me/api/portraits/men/46.jpg" 
                  alt="Dr. Michael Chen" 
                  className="w-12 h-12 rounded-full"
                />
                <div className="ml-4">
                  <h4 className="font-semibold">Dr. Michael Chen</h4>
                  <p className="text-sm text-gray-600">Cardiologist</p>
                </div>
              </div>
              
              <p className="text-gray-600">
                "The insights from patient reviews have transformed how I prescribe. I now have a better understanding 
                of how medications affect different patient demographics."
              </p>
            </div>
            
            {/* Testimonial 3 */}
            <div className="card p-6">
              <div className="flex items-center mb-4">
                <img 
                  src="https://randomuser.me/api/portraits/women/65.jpg" 
                  alt="Rachel Patel" 
                  className="w-12 h-12 rounded-full"
                />
                <div className="ml-4">
                  <h4 className="font-semibold">Rachel Patel</h4>
                  <p className="text-sm text-gray-600">Patient</p>
                </div>
              </div>
              
              <p className="text-gray-600">
                "The appointment booking system is so convenient! I was able to find a specialist, book an appointment, 
                and get reminders all through the app."
              </p>
            </div>
          </div>
        </div>
      </section>
      
      {/* CTA section */}
      <section className="cta py-16 bg-primary">
        <div className="container text-center">
          <h2 className="text-3xl font-bold text-white mb-6">Ready to Experience Better Healthcare?</h2>
          <p className="text-white text-lg mb-8 max-w-2xl mx-auto">
            Join thousands of patients and doctors who are transforming healthcare with EvoDoc.
          </p>
          
          <div className="flex gap-4 justify-center">
            <Link to="/register" className="btn bg-white text-primary btn-lg">
              Create Account
            </Link>
            <Link to="/contact" className="btn btn-outline text-white border-white btn-lg">
              Contact Us
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Landing;
