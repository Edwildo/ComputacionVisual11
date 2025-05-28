import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { Canvas } from '@react-three/fiber'
import Scene3D from './components/Scene3D'
import UIOverlay from './components/UIOverlay'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div style={{ width: '100vw', height: '100vh', margin: 0, padding: 0, overflow: 'hidden' }}>
      <Canvas camera={{ position: [0, 0, 5] }}>
        <ambientLight />
        <Scene3D />
        <UIOverlay />
      </Canvas>
    </div>
  )
}

export default App
