// src/CameraControls.js
import React from 'react'

export default function CameraControls({ mode, setMode, orthoSize, setOrthoSize }) {
  return (
    <div style={{ position: 'absolute', top: 20, left: 20, zIndex: 1 }}>
      <button onClick={() => setMode(m => (m === 'perspective' ? 'orthographic' : 'perspective'))}>
        Switch to {mode === 'perspective' ? 'Orthographic' : 'Perspective'}
      </button>
      <p>Mode: {mode}</p>
      {mode === 'orthographic' && (
        <div>
          <label>Ortho Size: {orthoSize}</label>
          <input
            type="range"
            min="2"
            max="10"
            value={orthoSize}
            onChange={e => setOrthoSize(Number(e.target.value))}
          />
        </div>
      )}
    </div>
  )
}
