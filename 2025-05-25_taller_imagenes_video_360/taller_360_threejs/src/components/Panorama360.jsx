import React from 'react'
import { useLoader } from '@react-three/fiber'
import * as THREE from 'three'

export default function Panorama360() {
  const texture = useLoader(THREE.TextureLoader, '/panorama.jpg')
  return (
    <mesh scale={[-10, 10, 10]}> {/* Esfera invertida */}
      <sphereGeometry args={[10, 32, 16]} />
      <meshBasicMaterial map={texture} side={THREE.BackSide} />
    </mesh>
  )
}