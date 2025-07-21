import { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

export default function ParticleSystem() {
  const ref = useRef();
  const count = 1000;

  const positions = new Float32Array(count * 3).map(() => THREE.MathUtils.randFloatSpread(2));

  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));

  const material = new THREE.PointsMaterial({
    color: new THREE.Color('cyan'),
    size: 0.05,
    transparent: true,
    opacity: 0.75,
    depthWrite: false,
  });

  useFrame(() => {
    ref.current.rotation.y += 0.002;
  });

  return <points ref={ref} geometry={geometry} material={material} />;
}
