import { useRef, useState } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

export default function ExplosionParticles({ trigger }) {
  const mesh = useRef();
  const [positions, setPositions] = useState(() =>
    new Float32Array(300).map(() => THREE.MathUtils.randFloatSpread(2))
  );
  const velocities = useRef(positions.map(() => THREE.MathUtils.randFloatSpread(0.1)));

  useFrame(() => {
    if (!trigger) return;

    for (let i = 0; i < positions.length; i++) {
      positions[i] += velocities.current[i] * 0.1;
    }

    mesh.current.geometry.attributes.position.needsUpdate = true;
  });

  return (
    <points ref={mesh}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={positions.length / 3}
          array={positions}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial color="orange" size={0.1} />
    </points>
  );
}
