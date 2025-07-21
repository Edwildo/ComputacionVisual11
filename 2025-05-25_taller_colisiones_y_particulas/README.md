# 🧪 Taller Colisiones y Efectos de Partículas en Three.js

## 📅 Fecha
`2025-05-25`    

---

## 🎯 Objetivo del Taller

Explorar la simulación de colisiones físicas y la generación de efectos de partículas en tiempo real usando Three.js y React. El taller integra la detección de colisiones, la respuesta visual mediante partículas y la interacción física en un entorno 3D web, utilizando @react-three/fiber y @react-three/cannon.

---

## 🧠 Conceptos Aprendidos

- Simulación de física en 3D con @react-three/cannon
- Detección y manejo de colisiones entre objetos
- Generación y animación de partículas en respuesta a eventos
- Integración de componentes visuales y físicos en React
- Uso de hooks y estados para gestionar efectos temporales
- Renderizado interactivo y control de cámara con OrbitControls

---

## 🔧 Herramientas y Entornos

- React + Vite
- Three.js y @react-three/fiber
- @react-three/drei (OrbitControls, helpers)
- @react-three/cannon para física y colisiones
- vite-plugin-glsl para shaders personalizados (opcional)
- ESLint para control de calidad de código

---

## 📁 Estructura del Proyecto
2025-05-25_taller_colisiones_y_particulas/ 
└── threejs/ 
├── src/ 
│ ├── App.jsx 
│ ├── main.jsx 
│ ├── assets/ 
│ │ └── textures/ 
│ ├── components/ 
│ │ ├── BoxObject.jsx │
│ ├── Ground.jsx 
│ │ ├── Particles.jsx 
│ │ └── Scene.jsx 
│ └── shaders/ 
│ └── dynamicShader.js 
├── public/ 
│ └── vite.svg 
├── index.html 
├── package.json 
├── vite.config.js 
├── README.md 
└── .gitignore

---

## 🧪 Implementación

### 🔹 Etapas realizadas
1. Configuración del entorno React + Vite + Three.js + Cannon.
2. Creación de un plano (Ground) y un cubo físico (BoxObject) con @react-three/cannon.
3. Implementación de la detección de colisiones entre el cubo y el suelo.
4. Generación de un efecto de partículas en la posición de la colisión.
5. Uso de estados para mostrar y eliminar partículas temporalmente.
6. Integración de controles de cámara y luces para mejorar la visualización.

### 🔹 Código relevante

**BoxObject.jsx**  
Cubo físico que dispara un callback al colisionar:
```javascript
import React from 'react'
import { useBox } from '@react-three/cannon'

export default function BoxObject({ onCollide }) {
  const [ref] = useBox(() => ({
    mass: 1,
    position: [0, 5, 0],
    onCollide: (e) => onCollide(e.contact),
  }))

  return (
    <mesh ref={ref} castShadow>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color="orange" />
    </mesh>
  )
}
```

**Particles.jsx**  
Sistema de partículas que se generan en la posición de colisión:

```javascript
import React, { useRef } from 'react'

export default function Particles({ position }) {
  const group = useRef()
  const particles = Array.from({ length: 20 }, (_, i) => ({
    id: i,
    position: [
      position[0] + (Math.random() - 0.5) * 0.5,
      position[1] + (Math.random() - 0.5) * 0.5,
      position[2] + (Math.random() - 0.5) * 0.5,
    ],
  }))

  return (
    <group ref={group}>
      {particles.map(p => (
        <mesh key={p.id} position={p.position}>
          <sphereGeometry args={[0.05, 8, 8]} />
          <meshStandardMaterial color="hotpink" emissive="hotpink" />
        </mesh>
      ))}
    </group>
  )
}
```

**Scene.jsx**  
Configuración de la escena, incluyendo el manejo de colisiones y explosiones:

```javascript
import React, { useState } from 'react'
import { OrbitControls } from '@react-three/drei'
import { Physics } from '@react-three/cannon'
import Ground from './Ground'
import BoxObject from './BoxObject'
import Particles from './Particles'

export default function Scene() {
  const [explosions, setExplosions] = useState([])

  const handleCollision = (contact) => {
    const point = contact.bi.position
    setExplosions((prev) => [...prev, { id: Math.random(), position: [...point] }])
    setTimeout(() => {
      setExplosions((prev) => prev.slice(1))
    }, 1000)
  }

  return (
    <>
      <OrbitControls />
      <ambientLight intensity={0.5} />
      <directionalLight position={[5, 10, 5]} castShadow intensity={1} />
      <Physics gravity={[0, -9.81, 0]}>
        <Ground />
        <BoxObject onCollide={handleCollision} />
      </Physics>
      {explosions.map(e => (
        <Particles key={e.id} position={e.position} />
      ))}
    </>
  )
}
```

---

## 📊 Resultados Visuales

El cubo cae y, al colisionar con el suelo, se genera un efecto de partículas en la zona de impacto.  
Las partículas desaparecen automáticamente tras un breve tiempo, simulando una explosión o dispersión.  
La escena es interactiva y permite rotar la cámara con el mouse.

![Resultados](./results/colision.gif)
---

## 💬 Reflexión Final

Este taller permitió experimentar con la integración de física, colisiones y efectos visuales en entornos 3D web modernos. El uso de React y hooks facilita la gestión de eventos y estados, mientras que la combinación de @react-three/fiber y @react-three/cannon habilita simulaciones físicas realistas y visualmente atractivas. Los efectos de partículas enriquecen la experiencia visual y abren la puerta a simulaciones y videojuegos interactivos en la web.