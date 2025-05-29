// src/App.js
import React, { useEffect, useRef, useState } from 'react'
import { Canvas } from '@react-three/fiber'
import { PerspectiveCamera, OrthographicCamera, OrbitControls } from '@react-three/drei'
import SceneObjects from './SceneObjects'

export default function App() {
  const [mode, setMode] = useState('perspective')
  const [orthoSize, setOrthoSize] = useState(5)
  const camRef = useRef()

  useEffect(() => {
    if (camRef.current && mode === 'orthographic') {
      camRef.current.zoom = orthoSize
      camRef.current.updateProjectionMatrix()
    }
  }, [orthoSize, mode])  

  return (
    <>
      {/* ——————— CONTROLES HTML ——————— */}
      <div style={{ position: 'absolute', top: 20, left: 20, zIndex: 1 }}>
        <button
          onClick={() =>
            setMode((m) =>
              m === 'perspective' ? 'orthographic' : 'perspective'
            )
          }
        >
          {mode === 'perspective'
            ? 'Switch to Orthographic'
            : 'Switch to Perspective'}
        </button>
        <p>Mode: {mode}</p>
        {mode === 'orthographic' && (
          <div>
            <label>Ortho Size: {orthoSize}</label>
            <input
              type="range"
              min={2}
              max={50}          // ← antes era 10
              value={orthoSize}
              onChange={(e) => setOrthoSize(Number(e.target.value))}
            />
          </div>
        )}

      </div>

      {/* ——————— ESCENA 3D ——————— */}
      <Canvas style={{ width: '100vw', height: '100vh' }}>
        {mode === 'perspective' ? (
          <PerspectiveCamera
            makeDefault
            position={[0, 2, 5]}
            fov={75}
          />
        ) : (
          <OrthographicCamera
            ref={camRef}
            makeDefault
            position={[0, 2, 5]}
            near={0.1}
            far={100}
          // El zoom se aplica en el useEffect
          />
        )}
        <ambientLight />
        <SceneObjects />
        <OrbitControls />
      </Canvas>
    </>
  )
}
