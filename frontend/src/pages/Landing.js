import React from 'react';
import { Link } from 'react-router-dom';
import MedicalScene from '../components/3d/MedicalScene';

const Landing = () => {
  return (
    <div className="bg-gradient-to-b from-white to-gray-50">
      {/* Hero Section */}
      <section className="relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 md:py-20">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
            <div className="order-2 md:order-1">
              <h1 className="text-4xl md:text-5xl font-bold text-gray-900">
                Healthcare that evolves with <span className="text-primary-600">your feedback</span>
              </h1>
              <p className="mt-4 text-xl text-gray-600">
                EvoDoc learns from patient experiences to provide personalized treatment recommendations and predict potential side effects.
              </p>
              <div className="mt-8 flex flex-wrap gap-4">
                <Link to="/register" className="btn bg-primary-600 text-white hover:bg-primary-700 transform hover:scale-105 transition-all shadow-md">
                  Get Started
                </Link>
                <Link to="/how-it-works" className="btn border border-primary-600 text-primary-600 hover:bg-primary-50 hover:shadow-md transition-all">
                  How It Works
                </Link>
              </div>
            </div>
            <div className="h-64 md:h-96 order-1 md:order-2">
              <MedicalScene height={400} />
            </div>
          </div>
        </div>
      </section>
      
      {/* Features Section */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="text-3xl font-extrabold text-gray-900">Why Choose <span className="text-primary-600">EvoDoc</span>?</h2>
            <p className="mt-4 text-lg text-gray-600 max-w-2xl mx-auto">
              Our platform combines cutting-edge technology with real patient experiences to deliver better healthcare outcomes.
            </p>
          </div>
          
          <div className="mt-16 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
            {/* Feature 1 */}
            <div className="bg-white rounded-xl shadow-xl p-8 transform hover:scale-105 transition-all border-t-4 border-primary-500">
              <div className="h-12 w-12 rounded-md bg-primary-500 text-white flex items-center justify-center mb-6">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900">Personalized Treatment</h3>
              <p className="mt-3 text-gray-600">
                AI-powered recommendations based on your unique health profile and similar patients' experiences.
              </p>
            </div>
            
            {/* Feature 2 */}
            <div className="bg-white rounded-xl shadow-xl p-8 transform hover:scale-105 transition-all border-t-4 border-primary-600">
              <div className="h-12 w-12 rounded-md bg-primary-600 text-white flex items-center justify-center mb-6">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900">Side Effect Prediction</h3>
              <p className="mt-3 text-gray-600">
                Know what to expect with treatments, with ML-powered predictions of potential side effects.
              </p>
            </div>
            
            {/* Feature 3 */}
            <div className="bg-white rounded-xl shadow-xl p-8 transform hover:scale-105 transition-all border-t-4 border-primary-700">
              <div className="h-12 w-12 rounded-md bg-primary-700 text-white flex items-center justify-center mb-6">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900">Treatment Tracking</h3>
              <p className="mt-3 text-gray-600">
                Monitor your treatment progress and share your experiences to help others.
              </p>
            </div>
          </div>
        </div>
      </section>
      
      {/* Testimonials */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="text-3xl font-extrabold text-gray-900">What Our Users Say</h2>
            <p className="mt-4 text-lg text-gray-600 max-w-2xl mx-auto">
              Hear from patients and doctors who've experienced the EvoDoc difference.
            </p>
          </div>
          
          <div className="mt-12 grid grid-cols-1 gap-8 md:grid-cols-2">
            {/* Testimonial 1 */}
            <div className="bg-white p-8 rounded-xl shadow-md">
              <div className="flex items-center mb-4">
                <div className="h-12 w-12 rounded-full bg-primary-100 text-primary-600 flex items-center justify-center">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                </div>
                <div className="ml-4">
                  <h3 className="text-lg font-medium text-gray-900">Sarah Johnson</h3>
                  <p className="text-gray-500">Patient</p>
                </div>
              </div>
              <p className="text-gray-600 italic">
                "EvoDoc helped me understand potential side effects of my medication that my doctor hadn't mentioned. I was able to prepare and manage them much better."
              </p>
            </div>
            
            {/* Testimonial 2 */}
            <div className="bg-white p-8 rounded-xl shadow-md">
              <div className="flex items-center mb-4">
                <div className="h-12 w-12 rounded-full bg-primary-100 text-primary-600 flex items-center justify-center">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                </div>
                <div className="ml-4">
                  <h3 className="text-lg font-medium text-gray-900">Dr. Michael Chen</h3>
                  <p className="text-gray-500">Cardiologist</p>
                </div>
              </div>
              <p className="text-gray-600 italic">
                "The insights from patient reviews have transformed how I prescribe. I now have a better understanding of how medications affect different patient demographics."
              </p>
            </div>
          </div>
        </div>
      </section>
      
      {/* CTA Section */}
      <section className="bg-primary-600 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold text-white">Ready to Experience Better Healthcare?</h2>
          <p className="mt-4 text-xl text-white opacity-90 max-w-2xl mx-auto">
            Join EvoDoc today and be part of the healthcare revolution.
          </p>
          <div className="mt-8">
            <Link to="/register" className="btn bg-white text-primary-600 hover:bg-gray-100 transform hover:scale-105 transition-all shadow-md text-lg px-8 py-3">
              Create Free Account
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Landing;
