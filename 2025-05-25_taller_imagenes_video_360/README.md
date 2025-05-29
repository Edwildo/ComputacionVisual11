## 1. Introducción
En este taller aprenderás a cargar y mostrar **imágenes panorámicas equirectangulares** y **videos 360°** dentro de un entorno 3D inmersivo usando **Three.js con React Three Fiber**. Además implementaremos un **UI** sencillo para alternar entre foto y video en tiempo real.

## 2. Estructura del proyecto
```bash
taller_360_threejs/
├── public/
│   ├── panorama.jpg      # Imagen panorámica equirectangular 2:1
│   ├── video360.mp4      # Video 360° en formato H.264/AAC
│   └── favicon.ico       # (opcional)
├── src/
│   ├── components/
│   │   ├── Panorama360.jsx  # Componente para foto 360°
│   │   ├── Video360.jsx     # Componente para video 360°
│   │   └── DragControls.jsx # Controles pointer-drag para rotación
│   ├── App.jsx            # Lógica principal y UI toggle
│   └── main.jsx           # Punto de entrada React
├── package.json           # Dependencias y scripts
└── vite.config.js         # Configuración de Vite
```

## 3. Componentes clave

### 3.1 `Panorama360.jsx`
Genera una esfera invertida con textura de imagen panorámica:
```jsx
import { useLoader } from '@react-three/fiber'
import * as THREE from 'three'

export default function Panorama360() {
  const texture = useLoader(THREE.TextureLoader, '/panorama.jpg')
  return (
    <mesh scale={[-10, 10, 10]}>   
      <sphereGeometry args={[10, 64, 32]} />
      <meshBasicMaterial map={texture} side={THREE.BackSide} />
    </mesh>
  )
}
```

### 3.2 `Video360.jsx`
Reproduce un video como textura dentro de la esfera:
```jsx
import React, { useRef, useEffect } from 'react'
import * as THREE from 'three'

export default function Video360() {
  const meshRef = useRef()
  useEffect(() => {
    const video = document.createElement('video')
    video.src = '/video360.mp4'
    video.crossOrigin = 'anonymous'
    video.loop = true
    video.muted = true
    video.playsInline = true
    video.play().catch(() => {})

    const texture = new THREE.VideoTexture(video)
    texture.minFilter = THREE.LinearFilter
    texture.magFilter = THREE.LinearFilter
    meshRef.current.material.map = texture
    meshRef.current.material.needsUpdate = true
  }, [])

  return (
    <mesh ref={meshRef} scale={[-10, 10, 10]}>
      <sphereGeometry args={[10, 64, 32]} />
      <meshBasicMaterial side={THREE.BackSide} />
    </mesh>
  )
}
```

### 3.3 `DragControls.jsx`
Permite rotar la cámara haciendo click & drag:
```jsx
import { useThree, useFrame } from '@react-three/fiber'
import { useRef, useEffect } from 'react'

export default function DragControls() {
  const { camera, gl } = useThree()
  const dragging = useRef(false)
  const prev = useRef([0, 0])

  useEffect(() => {
    const onDown = e => { dragging.current = true; prev.current = [e.clientX, e.clientY]; gl.domElement.style.cursor = 'grabbing' }
    const onUp = () => { dragging.current = false; gl.domElement.style.cursor = 'grab' }
    const onMove = e => {
      if (!dragging.current) return
      const [px, py] = prev.current
      const dx = (e.clientX - px) * 0.005
      const dy = (e.clientY - py) * 0.005
      camera.rotation.y -= dx; camera.rotation.x -= dy
      prev.current = [e.clientX, e.clientY]
    }
    gl.domElement.addEventListener('pointerdown', onDown)
    window.addEventListener('pointerup', onUp)
    window.addEventListener('pointermove', onMove)
    gl.domElement.style.cursor = 'grab'
    return () => {
      gl.domElement.removeEventListener('pointerdown', onDown)
      window.removeEventListener('pointerup', onUp)
      window.removeEventListener('pointermove', onMove)
    }
  }, [camera, gl.domElement])

  useFrame(() => {})
  return null
}
```

### 3.4 `App.jsx`
Maneja el **toggle** entre foto y video:
```jsx
import React, { useState } from 'react'
import { Canvas } from '@react-three/fiber'
import Panorama360 from './components/Panorama360'
import Video360 from './components/Video360'
import DragControls from './components/DragControls'

export default function App() {
  const [mode, setMode] = useState('photo')
  return (
    <div style={{position:'relative',width:'100vw',height:'100vh'}}>
      <div style={{position:'absolute',top:10,left:10,zIndex:1}}>
        <button onClick={() => setMode('photo')} disabled={mode==='photo'}>Foto 360°</button>
        <button onClick={() => setMode('video')} disabled={mode==='video'} style={{marginLeft:8}}>Video 360°</button>
      </div>
      <Canvas camera={{position:[0,0,0],fov:75}} style={{position:'absolute',top:0,left:0,width:'100%',height:'100%'}}>
        <ambientLight intensity={0.5} />
        {mode === 'photo' ? <Panorama360 /> : <Video360 />}
        <DragControls />
      </Canvas>
    </div>
  )
}
```

## 4. Scripts y ejecución
En la carpeta raíz (`taller_360_threejs/`):
```bash
npm install        # instala deps
npm run dev        # levanta http://localhost:5173
```

## 5. Criterios de evaluación
- Alterna correctamente entre imagen y video 360°.
- Interacción fluida (click & drag rota vista completa).
- Calidad visual sin recortes ni artefactos.
- Código modular y limpio.
- README con estructura clara y ejemplos.
