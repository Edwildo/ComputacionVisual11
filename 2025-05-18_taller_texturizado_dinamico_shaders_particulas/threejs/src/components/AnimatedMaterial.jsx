import { shaderMaterial } from '@react-three/drei';
import { extend, useFrame, useThree } from '@react-three/fiber';
import React, { useRef, useMemo } from 'react';
import * as THREE from 'three';
import { dynamicVertexShader, dynamicFragmentShader } from '../shaders/dynamicShader';

const AnimatedMaterialImpl = shaderMaterial(
  { uTime: 0, uMouse: new THREE.Vector2() },
  dynamicVertexShader,
  dynamicFragmentShader
);

extend({ AnimatedMaterialImpl });

export default function AnimatedMaterial({ children }) {
  const ref = useRef();
  const { mouse } = useThree();

  useFrame((state) => {
    if (ref.current) {
      ref.current.uTime = state.clock.getElapsedTime();
      ref.current.uMouse.set(mouse.x * 0.5 + 0.5, mouse.y * 0.5 + 0.5);
    }
  });

  return (
    <animatedMaterialImpl ref={ref} attach="material" />
  );
}
