import React from 'react';
import { Link } from 'react-router-dom';
import Button from '../components/Button';

const Home = () => {
  return (
    <div className="min-h-screen flex flex-col">
      <main className="flex-grow">
        {/* Hero Section */}
        <section className="py-16 md:py-24">
          <div className="container mx-auto px-4">
            <div className="max-w-3xl">
              <h1 className="text-4xl md:text-5xl font-bold mb-6">
                Healthcare that <span className="text-red-700">evolves</span> with your <span className="text-red-700">feedback</span>
              </h1>
              <p className="text-lg md:text-xl text-gray-600 mb-8">
                EvoDoc learns from patient experiences to provide personalized treatment recommendations and predict potential side effects.
              </p>
              <div className="flex flex-wrap gap-4">
                <Link to="/register" className="btn btn-primary">
                  Get Started
                </Link>
                <Link to="/appointments" className="btn btn-outline">
                  Book Appointment
                </Link>
              </div>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="py-16 bg-gray-50">
          <div className="container mx-auto px-4">
            <h2 className="text-3xl font-bold text-center mb-12">Personalized Healthcare Experience</h2>
            <div className="grid md:grid-cols-3 gap-8">
              <div className="card">
                <h3 className="text-xl font-bold mb-3">Personalized Treatment</h3>
                <p className="text-gray-600">AI-powered recommendations based on your unique health profile.</p>
              </div>
              <div className="card">
                <h3 className="text-xl font-bold mb-3">Side Effect Prediction</h3>
                <p className="text-gray-600">Know what to expect with ML-powered side effect predictions.</p>
              </div>
              <div className="card">
                <h3 className="text-xl font-bold mb-3">Treatment Tracking</h3>
                <p className="text-gray-600">Monitor your treatment progress and share your experiences.</p>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
};

export default Home;
