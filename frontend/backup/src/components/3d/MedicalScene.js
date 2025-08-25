import React, { useRef, useState, useEffect, Suspense } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { OrbitControls, PresentationControls, Float, Sparkles, Text } from '@react-three/drei';
import { useSpring, animated } from '@react-spring/three';
import * as THREE from 'three';

// Fallback component in case of rendering issues
const FallbackComponent = () => (
  <div className="w-full h-full flex items-center justify-center bg-primary-50 rounded-xl">
    <div className="text-center">
      <div className="animate-spin-slow w-16 h-16 border-4 border-primary-200 border-t-primary-600 rounded-full mx-auto mb-4"></div>
      <p className="text-primary-600 font-medium">Loading 3D visualization...</p>
    </div>
  </div>
);

// Loading monitor component
const LoadingMonitor = () => {
  const { gl } = useThree();
  
  useEffect(() => {
    // Log context creation success
    console.log('WebGL context created successfully');
    
    // Add error handling for WebGL context loss
    const handleContextLost = (event) => {
      event.preventDefault();
      console.error('WebGL context lost');
    };
    
    const handleContextRestored = () => {
      console.log('WebGL context restored');
    };
    
    const canvas = gl.domElement;
    canvas.addEventListener('webglcontextlost', handleContextLost, false);
    canvas.addEventListener('webglcontextrestored', handleContextRestored, false);
    
    return () => {
      canvas.removeEventListener('webglcontextlost', handleContextLost);
      canvas.removeEventListener('webglcontextrestored', handleContextRestored);
    };
  }, [gl]);
  
  return null;
};

// DNA Helix Component
const DNA = ({ position = [0, 0, 0], scale = 1, color1 = '#E53E3E', color2 = '#FFFFFF' }) => {
  const dnaRef = useRef();
  
  useFrame((state) => {
    if (dnaRef.current) {
      dnaRef.current.rotation.y += 0.005;
      dnaRef.current.rotation.z = Math.sin(state.clock.getElapsedTime() * 0.3) * 0.1;
    }
  });
  
  const height = 10;
  const turns = 4;
  const segments = 20; // Reduced segment count for better performance
  const radius = 2;

  return (
    <group ref={dnaRef} position={position} scale={scale}>
      {Array.from({ length: segments }).map((_, i) => {
        const angle = (i / segments) * Math.PI * 2 * turns;
        const y = (i / segments) * height - height/2;
        
        return (
          <React.Fragment key={i}>
            {/* First strand */}
            <mesh position={[Math.sin(angle) * radius, y, Math.cos(angle) * radius]}>
              <sphereGeometry args={[0.3, 10, 10]} /> {/* Reduced geometry complexity */}
              <meshStandardMaterial color={color1} roughness={0.3} />
            </mesh>
            
            {/* Second strand */}
            <mesh position={[Math.sin(angle + Math.PI) * radius, y, Math.cos(angle + Math.PI) * radius]}>
              <sphereGeometry args={[0.3, 10, 10]} /> {/* Reduced geometry complexity */}
              <meshStandardMaterial color={color2} roughness={0.3} />
            </mesh>
            
            {/* Base pairs (connecting bars) */}
            {i % 3 === 0 && (
              <mesh position={[0, y, 0]}>
                <group rotation={[0, angle, 0]}>
                  <mesh>
                    <cylinderGeometry args={[0.05, 0.05, radius * 2, 6]} /> {/* Reduced geometry complexity */}
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

// Pill Component
const Pill = ({ position, rotation = [0, 0, 0], color = '#E53E3E', ...props }) => {
  const pillRef = useRef();
  const [hovered, setHovered] = useState(false);
  
  // Spring animations for hover effect
  const { scale, pillColor } = useSpring({
    scale: hovered ? 1.1 : 1,
    pillColor: hovered ? '#FF6B6B' : color,
  });
  
  useFrame((state) => {
    if (pillRef.current) {
      pillRef.current.rotation.y += 0.01;
      pillRef.current.position.y = position[1] + Math.sin(state.clock.getElapsedTime()) * 0.1;
    }
  });
  
  return (
    <animated.group 
      ref={pillRef} 
      position={position} 
      rotation={rotation} 
      scale={scale}
      onPointerOver={() => setHovered(true)}
      onPointerOut={() => setHovered(false)}
      {...props}
    >
      <mesh>
        <capsuleGeometry args={[0.5, 1.5, 8, 16]} /> {/* Reduced geometry complexity */}
        <animated.meshStandardMaterial color={pillColor} roughness={0.3} metalness={0.2} />
      </mesh>
      
      <mesh position={[0, 0, 0]} rotation={[Math.PI/2, 0, 0]}>
        <cylinderGeometry args={[0.51, 0.51, 0.05, 16]} />
        <meshStandardMaterial color="white" roughness={0.2} metalness={0.3} />
      </mesh>
    </animated.group>
  );
};

// Main 3D Scene Component
const MedicalScene = ({ height = 700 }) => {
  // Error state
  const [hasError, setHasError] = useState(false);
  
  // Error boundary
  useEffect(() => {
    const handleError = (event) => {
      console.error('WebGL error:', event);
      setHasError(true);
    };
    
    window.addEventListener('error', handleError);
    return () => window.removeEventListener('error', handleError);
  }, []);
  
  if (hasError) {
    return <FallbackComponent />;
  }
  
  return (
    <div className="w-full" style={{ height: `${height}px`, minHeight: '500px' }}>
      <Suspense fallback={<FallbackComponent />}>
        <Canvas 
          shadows 
          camera={{ position: [0, 0, 15], fov: 60 }}
          onCreated={state => console.log('Canvas created successfully')}
          gl={{ 
            antialias: true, 
            alpha: true,
            powerPreference: 'high-performance',
            failIfMajorPerformanceCaveat: false,
          }}
        >
          <LoadingMonitor />
          <color attach="background" args={['transparent']} />
          
          <ambientLight intensity={0.5} />
          <spotLight position={[10, 10, 10]} angle={0.15} penumbra={1} intensity={1} castShadow />
          
          <PresentationControls
            global
            rotation={[0, 0, 0]}
            polar={[-Math.PI / 6, Math.PI / 6]}
            azimuth={[-Math.PI / 6, Math.PI / 6]}
            config={{ mass: 2, tension: 400 }}
            snap
          >
            <Float rotationIntensity={0.4} floatIntensity={0.8} speed={2}>
              <DNA position={[0, 0, 0]} scale={0.8} color1="#E53E3E" color2="#FFFFFF" />
            </Float>
            
            <Float rotationIntensity={0.2} floatIntensity={0.5} speed={3}>
              <Pill position={[-5, 1, 2]} rotation={[0, 0, Math.PI/2]} color="#E53E3E" />
            </Float>
            
            <Float rotationIntensity={0.2} floatIntensity={0.5} speed={2.5}>
              <Pill position={[5, -1, 1]} rotation={[0, 0, Math.PI/3]} color="#C53030" />
            </Float>
            
            <Text
              position={[0, -4, 0]}
              color="#E53E3E"
              fontSize={1.5}
              font="https://fonts.gstatic.com/s/inter/v12/UcCO3FwrK3iLTeHuS_fvQtMwCp50KnMw2boKoduKmMEVuGKYMZs.woff"
              anchorX="center"
              anchorY="middle"
            >
              EvoDoc
            </Text>
          </PresentationControls>
          
          <Sparkles count={50} scale={10} size={1} speed={0.3} opacity={0.2} color="#FFCACA" />
          <OrbitControls enableZoom={false} enablePan={false} />
        </Canvas>
      </Suspense>
    </div>
  );
};

export default MedicalScene;
