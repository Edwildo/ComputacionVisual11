import React from 'react'
import { Canvas } from '@react-three/fiber'
import Scene from './components/Scene'

export default function App() {
  return (
    <Canvas shadows camera={{ position: [5, 5, 5], fov: 50 }}>
      <Scene />
    </Canvas>
  )
}
