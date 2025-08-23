import React, { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';

// A simple DNA helix model using primitives
const DnaModel = ({ rotation = 0.001 }) => {
  const groupRef = useRef();
  
  useFrame(() => {
    if (groupRef.current) {
      groupRef.current.rotation.y += rotation;
    }
  });

  const strandCount = 10;
  const radius = 2;
  const height = 10;
  
  // Create the helix strands
  const createHelix = () => {
    const elements = [];
    const basePairs = [];
    
    // Create two strands
    for (let i = 0; i < strandCount; i++) {
      const angle = (i / strandCount) * Math.PI * 2;
      const yPos = (i / strandCount) * height - height/2;
      
      // First strand
      elements.push(
        <mesh key={`strand1-${i}`} position={[Math.sin(angle) * radius, yPos, Math.cos(angle) * radius]}>
          <sphereGeometry args={[0.4, 16, 16]} />
          <meshStandardMaterial color="#6366F1" />
        </mesh>
      );
      
      // Second strand (opposite side)
      elements.push(
        <mesh key={`strand2-${i}`} position={[Math.sin(angle + Math.PI) * radius, yPos, Math.cos(angle + Math.PI) * radius]}>
          <sphereGeometry args={[0.4, 16, 16]} />
          <meshStandardMaterial color="#8B5CF6" />
        </mesh>
      );
      
      // Base pairs connecting the strands
      if (i % 2 === 0) {
        basePairs.push(
          <mesh key={`pair-${i}`}>
            <cylinderGeometry args={[0.1, 0.1, radius * 2, 8]} />
            <meshStandardMaterial color="#D1D5DB" />
            <group position={[0, yPos, 0]} rotation={[0, angle, 0]}>
              <mesh position={[0, 0, 0]}>
                <cylinderGeometry args={[0.1, 0.1, radius * 2, 8]} />
                <meshStandardMaterial color="#D1D5DB" />
              </mesh>
            </group>
          </mesh>
        );
      }
    }
    
    return [...elements, ...basePairs];
  };

  return (
    <group ref={groupRef}>
      {createHelix()}
    </group>
  );
};

// The main component that renders the DNA helix
const DnaHelix = ({ height = 300 }) => {
  return (
    <div style={{ height: `${height}px`, width: '100%' }}>
      <Canvas camera={{ position: [0, 0, 10], fov: 50 }}>
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} intensity={1} />
        <DnaModel />
        <OrbitControls enableZoom={false} autoRotate autoRotateSpeed={0.5} />
      </Canvas>
    </div>
  );
};

export default DnaHelix;
