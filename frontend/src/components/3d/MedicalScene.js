import React, { useRef, useState, useEffect } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, useGLTF, Environment, ContactShadows, Text } from '@react-three/drei';
import * as THREE from 'three';

// 3D Pill Component
const Pill = ({ position, rotation, color = '#E53E3E', ...props }) => {
  const pillRef = useRef();
  
  useFrame((state) => {
    pillRef.current.rotation.y += 0.01;
    pillRef.current.position.y = position[1] + Math.sin(state.clock.getElapsedTime()) * 0.1;
  });
  
  return (
    <group ref={pillRef} position={position} rotation={rotation} {...props}>
      {/* Pill Body */}
      <mesh>
        <capsuleGeometry args={[0.5, 1.5, 10, 20]} />
        <meshStandardMaterial color={color} roughness={0.3} metalness={0.2} />
      </mesh>
      
      {/* Pill Divider */}
      <mesh position={[0, 0, 0]} rotation={[Math.PI/2, 0, 0]}>
        <cylinderGeometry args={[0.51, 0.51, 0.05, 32]} />
        <meshStandardMaterial color="white" roughness={0.2} metalness={0.3} />
      </mesh>
    </group>
  );
};

// Floating DNA Component
const DNA = ({ position = [0, 0, 0], scale = 1, color1 = '#E53E3E', color2 = '#FFFFFF' }) => {
  const dnaRef = useRef();
  
  useFrame((state) => {
    dnaRef.current.rotation.y += 0.005;
    dnaRef.current.rotation.z = Math.sin(state.clock.getElapsedTime() * 0.3) * 0.1;
  });
  
  const height = 10;
  const turns = 4;
  const segments = 30;
  const radius = 2;

  return (
    <group ref={dnaRef} position={position} scale={scale}>
      {/* Generate the DNA structure */}
      {Array.from({ length: segments }).map((_, i) => {
        const angle = (i / segments) * Math.PI * 2 * turns;
        const y = (i / segments) * height - height/2;
        
        return (
          <React.Fragment key={i}>
            {/* First strand */}
            <mesh position={[Math.sin(angle) * radius, y, Math.cos(angle) * radius]}>
              <sphereGeometry args={[0.3, 16, 16]} />
              <meshStandardMaterial color={color1} roughness={0.3} />
            </mesh>
            
            {/* Second strand */}
            <mesh position={[Math.sin(angle + Math.PI) * radius, y, Math.cos(angle + Math.PI) * radius]}>
              <sphereGeometry args={[0.3, 16, 16]} />
              <meshStandardMaterial color={color2} roughness={0.3} />
            </mesh>
            
            {/* Base pairs (connecting bars) */}
            {i % 3 === 0 && (
              <mesh position={[0, y, 0]}>
                <group rotation={[0, angle, 0]}>
                  <mesh>
                    <cylinderGeometry args={[0.05, 0.05, radius * 2, 8]} />
                    <meshStandardMaterial color="#FFFFFF" transparent opacity={0.7} />
                  </mesh>
                </group>
              </mesh>
            )}
          </React.Fragment>
        );
      })}
    </group>
  );
};

// Floating Medical Cross
const MedicalCross = ({ position = [0, 0, 0], rotation = [0, 0, 0], scale = 1 }) => {
  const crossRef = useRef();
  
  useFrame((state) => {
    crossRef.current.rotation.y += 0.01;
    crossRef.current.position.y = position[1] + Math.sin(state.clock.getElapsedTime() * 0.5) * 0.2;
  });
  
  return (
    <group ref={crossRef} position={position} rotation={rotation} scale={scale}>
      {/* Horizontal bar */}
      <mesh>
        <boxGeometry args={[2, 0.5, 0.5]} />
        <meshStandardMaterial color="#E53E3E" roughness={0.2} metalness={0.3} />
      </mesh>
      
      {/* Vertical bar */}
      <mesh>
        <boxGeometry args={[0.5, 2, 0.5]} />
        <meshStandardMaterial color="#E53E3E" roughness={0.2} metalness={0.3} />
      </mesh>
    </group>
  );
};

// Main 3D Scene
const MedicalScene = ({ height = 500 }) => {
  return (
    <div style={{ height: `${height}px`, width: '100%' }}>
      <Canvas camera={{ position: [0, 0, 15], fov: 50 }}>
        <color attach="background" args={['#F8FAFC']} />
        
        <ambientLight intensity={0.5} />
        <spotLight position={[10, 10, 10]} angle={0.15} penumbra={1} intensity={1} castShadow />
        
        <DNA position={[0, 0, 0]} scale={0.7} color1="#E53E3E" color2="#FFFFFF" />
        <Pill position={[-5, 1, 2]} rotation={[0, 0, Math.PI/2]} color="#E53E3E" />
        <Pill position={[5, -1, 1]} rotation={[0, 0, Math.PI/3]} color="#C53030" />
        <MedicalCross position={[0, 3, 0]} scale={0.8} />
        
        <Text
          position={[0, -4, 0]}
          color="#E53E3E"
          fontSize={1.5}
          font="/fonts/Inter-Bold.woff"
          anchorX="center"
          anchorY="middle"
        >
          EvoDoc
        </Text>
        
        <ContactShadows position={[0, -5, 0]} opacity={0.4} scale={20} blur={1.5} far={5} />
        <OrbitControls enableZoom={false} autoRotate autoRotateSpeed={0.5} />
        <Environment preset="city" />
      </Canvas>
    </div>
  );
};

export default MedicalScene;
