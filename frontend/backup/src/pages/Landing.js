import React, { useEffect, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import DOTS from 'vanta/dist/vanta.dots.min'; // Corrected import path
import * as THREE from 'three';

const Landing = () => {
  const [vantaEffect, setVantaEffect] = useState(null);
  const vantaRef = useRef(null);

  useEffect(() => {
    // Initialize Vanta effect only if it hasn't been created yet
    if (!vantaEffect && vantaRef.current) {
      setVantaEffect(
        DOTS({
          el: vantaRef.current,
          THREE: THREE, // Pass the imported THREE object
          mouseControls: true,
          touchControls: true,
          gyroControls: false,
          minHeight: 200.00,
          minWidth: 200.00,
          scale: 1.00,
          scaleMobile: 1.00,
          color: '#e53e3e',
          color2: '#ffffff',
          backgroundColor: '#ffffff',
          size: 3.00,
          spacing: 30.00,
          showLines: false
        })
      );
    }

    // Cleanup function to destroy the Vanta effect when the component unmounts
    return () => {
      if (vantaEffect) vantaEffect.destroy();
    };
  }, [vantaEffect]); // Dependency array ensures this runs only when vantaEffect changes

  return (
    // Make sure the ref is attached to the element you want the background on
    <div className="relative min-h-screen" ref={vantaRef}>
      
      {/* Hero Section (Your content goes here, inside the main div) */}
      <div className="relative z-10 container mx-auto px-6 pt-24 pb-12"> {/* Added z-10 to ensure content is on top */}
        <div className="flex flex-col lg:flex-row items-center mt-16">
          {/* Left Column - Text */}
          <div className="w-full lg:w-1/2 mb-10 lg:mb-0">
            <h1 className="text-5xl font-bold text-gray-900 leading-tight">
              Healthcare
              <br />that
              <br />
              <span className="text-primary-600">evolves</span>
              <br />with your
              <br />
              <span className="text-primary-600">feedback</span>
            </h1>
            
            <p className="mt-6 text-gray-600 max-w-lg">
              EvoDoc learns from patient experiences to provide
              personalized treatment recommendations and predict
              potential side effects.
            </p>
            
            <div className="mt-10 flex flex-wrap gap-6">
              {/* Angled Get Started Button */}
              <div className="relative transform rotate-[-12deg] hover:rotate-[-6deg] transition-transform duration-300">
                <Link 
                  to="/register" 
                  className="inline-block bg-primary-600 text-white font-bold px-8 py-3 text-lg rounded-md shadow-lg"
                >
                  Get Started
                </Link>
              </div>
              
              <Link 
                to="/how-it-works" 
                className="inline-block border-2 border-primary-600 text-primary-600 font-medium px-8 py-3 text-lg rounded-md hover:bg-primary-50 transition-colors"
              >
                How It Works
              </Link>
            </div>
          </div>
          
          {/* Right Column - Medical Visualization */}
          <div className="w-full lg:w-1/2 relative">
            <div className="animated-medical-elements relative h-96">
              {/* Medical Cross */}
              <div className="absolute top-1/4 right-1/4 w-16 h-16 animate-pulse">
                <svg viewBox="0 0 24 24" className="w-full h-full text-primary-600">
                  <path fill="currentColor" d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z" />
                </svg>
              </div>
              
              {/* Animated Pills */}
              <div className="pill pill-1"></div>
              <div className="pill pill-2"></div>
              <div className="pill pill-3"></div>
              <div className="pill pill-4"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Landing;