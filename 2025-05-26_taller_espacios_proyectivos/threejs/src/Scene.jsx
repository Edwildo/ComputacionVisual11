import { useState } from 'react'
import { Canvas } from '@react-three/fiber'
import { OrbitControls, PerspectiveCamera, OrthographicCamera } from '@react-three/drei'

const Scene = () => {
  const [cameraType, setCameraType] = useState('perspective')
  
  // Objetos en diferentes profundidades (z)
  const objects = [
    { position: [0, 0, 0], color: 'red' },
    { position: [2, 1, -3], color: 'green' },
    { position: [-2, -1, 3], color: 'blue' }
  ]

  return (
    <div style={{ height: '100vh', position: 'relative' }}>
      <div style={{ position: 'absolute', top: 20, left: 20, zIndex: 100 }}>
        <button 
          onClick={() => setCameraType('perspective')}
          style={{ background: cameraType === 'perspective' ? '#ddd' : '#fff' }}
        >
          Perspectiva
        </button>
        <button 
          onClick={() => setCameraType('orthographic')}
          style={{ background: cameraType === 'orthographic' ? '#ddd' : '#fff' }}
        >
          Ortográfica
        </button>
      </div>

      <Canvas>
        {cameraType === 'perspective' ? (
          <PerspectiveCamera 
            makeDefault 
            position={[0, 0, 10]} 
            fov={50} 
            near={0.1} 
            far={1000} 
          />
        ) : (
          <OrthographicCamera
            makeDefault
            position={[0, 0, 10]}
            zoom={50}
            near={0.1}
            far={1000}
            left={-5}
            right={5}
            top={5}
            bottom={-5}
          />
        )}

        <OrbitControls enablePan={true} enableZoom={true} enableRotate={true} />

        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} />

        {objects.map((obj, index) => (
          <mesh key={index} position={obj.position}>
            <boxGeometry args={[1, 1, 1]} />
            <meshStandardMaterial color={obj.color} />
          </mesh>
        ))}

        {/* Ejes de referencia */}
        <mesh position={[0, 0, 0]}>
          <axesHelper args={[5]} />
        </mesh>
      </Canvas>
    </div>
  )
}

export default Scene