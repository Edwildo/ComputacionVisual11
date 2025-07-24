// src/App.jsx
import React, { useState } from 'react'
import { Canvas } from '@react-three/fiber'
import Panorama360 from './components/Panorama360'
import Video360 from './components/Video360'
import DragControls from './components/DragControls'

export default function App() {
  const [mode, setMode] = useState('photo') // 'photo' | 'video'

  return (
    <div style={{ position: 'relative', width: '100vw', height: '100vh' }}>
      {/* Controles UI */}
      <div style={{ position: 'absolute', top: 10, left: 10, zIndex: 1 }}>
        <button onClick={() => setMode('photo')} disabled={mode === 'photo'}>
          Foto 360°
        </button>
        <button onClick={() => setMode('video')} disabled={mode === 'video'} style={{ marginLeft: 8 }}>
          Video 360°
        </button>
      </div>

      {/* Vista 3D */}
      <Canvas
        camera={{ position: [0, 0, 0], fov: 75 }}
        style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%' }}
      >
        <ambientLight intensity={0.5} />
        {mode === 'photo' ? <Panorama360 /> : <Video360 />}
        <DragControls />
      </Canvas>
    </div>
  )
}