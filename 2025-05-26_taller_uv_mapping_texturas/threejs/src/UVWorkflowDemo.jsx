import React, { useState, useRef, Suspense } from 'react'
import { Canvas, useThree } from '@react-three/fiber'
import { OrbitControls, useGLTF, useTexture, TransformControls } from '@react-three/drei'
import { Leva, useControls } from 'leva'
import * as THREE from 'three'

// Componente para cargar y mostrar modelos
const ModelViewer = ({ modelType }) => {
  const meshRef = useRef()
  
  // Cargar textura UV checker
  const texture = useTexture('/uv-checker-map.png')
  
  // Controles para manipulación UV
  const { repeatX, repeatY, offsetX, offsetY, rotation, wrapS, wrapT } = useControls('UV Controls', {
    repeatX: { value: 1, min: 0.1, max: 5, step: 0.1 },
    repeatY: { value: 1, min: 0.1, max: 5, step: 0.1 },
    offsetX: { value: 0, min: -1, max: 1, step: 0.01 },
    offsetY: { value: 0, min: -1, max: 1, step: 0.01 },
    rotation: { value: 0, min: 0, max: Math.PI * 2, step: 0.01 },
    wrapS: { options: { Repeat: THREE.RepeatWrapping, Clamp: THREE.ClampToEdgeWrapping, Mirror: THREE.MirroredRepeatWrapping } },
    wrapT: { options: { Repeat: THREE.RepeatWrapping, Clamp: THREE.ClampToEdgeWrapping, Mirror: THREE.MirroredRepeatWrapping } }
  })

  // Aplicar parámetros UV a la textura
  texture.wrapS = wrapS
  texture.wrapT = wrapT
  texture.repeat.set(repeatX, repeatY)
  texture.offset.set(offsetX, offsetY)
  texture.rotation = rotation
  texture.center.set(0.5, 0.5)
  texture.needsUpdate = true

  // Renderizar modelo según selección
  const renderModel = () => {
    switch (modelType) {
      case 'cube':
        return (
          <mesh ref={meshRef}>
            <boxGeometry args={[2, 2, 2]} />
            <meshStandardMaterial map={texture} />
          </mesh>
        )
      case 'sphere':
        return (
          <mesh ref={meshRef}>
            <sphereGeometry args={[1, 32, 32]} />
            <meshStandardMaterial map={texture} />
          </mesh>
        )
      case 'character':
        return <CharacterModel texture={texture} />
      default:
        return null
    }
  }

  return (
    <>
      {renderModel()}
      {/* Remove TransformControls or fix its usage if needed */}
    </>
  )
}

// Componente para cargar modelo complejo (GLTF)
const CharacterModel = ({ texture }) => {
  const { scene } = useGLTF('/Duck.glb')
  
  // Aplicar textura a todos los materiales del modelo
  scene.traverse((child) => {
    if (child.isMesh) {
      child.material = new THREE.MeshStandardMaterial({ 
        map: texture,
        roughness: 0.7,
        metalness: 0.1
      })
    }
  })

  return <primitive object={scene} scale={0.5} />
}

// Componente de estado de carga (overlay fuera del Canvas)
import { useProgress } from '@react-three/drei'

const LoaderOverlay = () => {
  const { active } = useProgress()
  if (!active) return null
  return (
    <div style={{
      position: 'absolute',
      top: 0,
      left: 0,
      width: '100%',
      height: '100%',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'rgba(0, 0, 0, 0.7)',
      color: 'white',
      zIndex: 1000
    }}>
      <div style={{
        border: '5px solid #f3f3f3',
        borderTop: '5px solid #3498db',
        borderRadius: '50%',
        width: '50px',
        height: '50px',
        animation: 'spin 1s linear infinite',
        marginBottom: '20px'
      }}></div>
      <style>
        {`@keyframes spin { 0% { transform: rotate(0deg);} 100% { transform: rotate(360deg);} }`}
      </style>
      <p>Cargando modelos y texturas...</p>
    </div>
  )
}

// Componente principal de la aplicación
export default function UVWorkflowDemo() {
  const [modelType, setModelType] = useState('cube')

  // Controles para selección de modelo
  useControls('Model Selection', {
    modelType: {
      value: 'cube',
      options: {
        Cubo: 'cube',
        Esfera: 'sphere',
        Personaje: 'character'
      },
      onChange: (value) => setModelType(value)
    }
  })

  return (
    <div style={{ width: '100vw', height: '100vh', position: 'relative' }}>
      <Leva collapsed={false} />
      <Canvas camera={{ position: [0, 0, 5], fov: 50 }}>
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} intensity={1} />
        <Suspense fallback={null}>
          <ModelViewer modelType={modelType} />
        </Suspense>
        <OrbitControls makeDefault />
      </Canvas>
      <LoaderOverlay />
      <div style={{
        position: 'absolute', bottom: '20px', left: '20px', background: 'rgba(0, 0, 0, 0.7)', color: 'white', padding: '15px',
        borderRadius: '5px', maxWidth: '300px'
      }}>
        <h3>Problemas comunes de UV:</h3>
        <ul style={{ margin: '10px 0 0 0', paddingLeft: '20px' }}>
          <li style={{ marginBottom: '8px', fontSize: '14px' }}>
            <strong>Stretching:</strong> Distorsión cuando las caras tienen diferentes tamaños en UV
          </li>
          <li style={{ marginBottom: '8px', fontSize: '14px' }}>
            <strong>Seams:</strong> Bordes visibles donde los UV no coinciden correctamente
          </li>
          <li style={{ marginBottom: '8px', fontSize: '14px' }}>
            <strong>Misalignment:</strong> Texturas desalineadas en los bordes del modelo
          </li>
        </ul>
      </div>
    </div>
  )
}