import React, { useEffect, useRef } from 'react';
import '../../styles/animations.css';

const DnaAnimation = ({ height = 600 }) => {
  const containerRef = useRef(null);
  const particlesRef = useRef([]);
  
  // Generate DNA pairs
  const generateDnaPairs = () => {
    const pairs = [];
    const pairCount = 20;
    
    for (let i = 0; i < pairCount; i++) {
      const yPos = (i / pairCount) * 100;
      const rotateY = (i / pairCount) * 360;
      
      pairs.push(
        <div 
          className="dna-pair" 
          key={i}
          style={{ 
            top: `${yPos}%`, 
            transform: `rotateY(${rotateY}deg)` 
          }}
        >
          <div className="strand strand-left"></div>
          {i % 3 === 0 && <div className="connector"></div>}
          <div className="strand strand-right"></div>
        </div>
      );
    }
    
    return pairs;
  };
  
  // Create background particles
  useEffect(() => {
    if (!containerRef.current) return;
    
    // Create particles
    const container = containerRef.current;
    particlesRef.current = [];
    
    for (let i = 0; i < 30; i++) {
      const particle = document.createElement('div');
      particle.className = 'particle';
      
      // Random properties
      const size = Math.random() * 5 + 2;
      const xPos = Math.random() * 100;
      const yPos = Math.random() * 100;
      const opacity = Math.random() * 0.2 + 0.05;
      const animDuration = Math.random() * 10 + 5;
      const animDelay = Math.random() * 5;
      
      // Apply styles
      particle.style.width = `${size}px`;
      particle.style.height = `${size}px`;
      particle.style.left = `${xPos}%`;
      particle.style.top = `${yPos}%`;
      particle.style.opacity = opacity;
      particle.style.animation = `drift ${animDuration}s ease-in-out infinite ${animDelay}s`;
      
      container.appendChild(particle);
      particlesRef.current.push(particle);
    }
    
    // Cleanup
    return () => {
      particlesRef.current.forEach(particle => {
        if (particle.parentNode === container) {
          container.removeChild(particle);
        }
      });
    };
  }, []);
  
  return (
    <div className="dna-container" ref={containerRef} style={{ height: `${height}px` }}>
      <div className="dna-helix">
        {generateDnaPairs()}
      </div>
      
      {/* Pills */}
      <div className="pill pill-red pill-1"></div>
      <div className="pill pill-dark pill-2"></div>
      <div className="pill pill-red pill-3"></div>
      
      {/* Medical Cross */}
      <div className="medical-cross"></div>
    </div>
  );
};

export default DnaAnimation;
