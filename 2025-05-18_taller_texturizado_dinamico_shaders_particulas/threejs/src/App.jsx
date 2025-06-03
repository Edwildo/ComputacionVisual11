import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import AnimatedMaterial from './components/AnimatedMaterial';
import ParticleSystem from './components/ParticleSystem';
import ExplosionParticles from './components/ExplosionParticles';
import { useState } from 'react';

export default function App() {
  const [explode, setExplode] = useState(false);

  return (
    <Canvas camera={{ position: [0, 0, 5], fov: 60 }}>
      <OrbitControls />
      <ambientLight />
      <pointLight position={[5, 5, 5]} />
      
      <mesh onClick={() => setExplode(true)}>
        <sphereGeometry args={[1, 64, 64]} />
        <AnimatedMaterial />
      </mesh>

      <ParticleSystem />
      {explode && <ExplosionParticles trigger={explode} />}
    </Canvas>
  );
}
