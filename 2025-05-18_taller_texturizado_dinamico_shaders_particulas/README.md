# 🧪 Taller Texturizado Dinámico, Shaders y Partículas en Three.js

## 📅 Fecha
`2025-05-18`    

---

## 🎯 Objetivo del Taller

Explorar la creación de materiales animados y efectos visuales avanzados en tiempo real usando shaders personalizados y sistemas de partículas en Three.js, integrados en una aplicación React con @react-three/fiber. Se busca simular fenómenos como fuego, agua, electricidad o portales, y permitir la interacción del usuario y la respuesta a sensores simulados.

---

## 🧠 Conceptos Aprendidos

- Creación de materiales animados con shaders GLSL (vertex y fragment)
- Uso de uniforms para animación por tiempo y entrada del usuario (mouse)
- Integración de materiales personalizados con `shaderMaterial` de @react-three/drei
- Implementación de sistemas de partículas y efectos de explosión
- Simulación visual de fenómenos naturales y fantásticos
- Interactividad en escenas 3D web

---

## 🔧 Herramientas y Entornos

- React + Vite
- Three.js y @react-three/fiber
- @react-three/drei (shaderMaterial, OrbitControls)
- GLSL para shaders personalizados
- (Opcional) Reconocimiento de voz y entrada de sensores simulados

---

## 📁 Estructura del Proyecto

```
2025-05-18_taller_texturizado_dinamico_shaders_particulas/
└── threejs/
    ├── src/
    │   ├── App.jsx
    │   ├── main.jsx
    │   ├── assets/
    │   │   └── textures/
    │   ├── components/
    │   │   ├── AnimatedMaterial.jsx
    │   │   ├── ExplosionParticles.jsx
    │   │   └── ParticleSystem.jsx
    │   └── shaders/
    │       └── dynamicShader.js
    ├── public/
    │   └── vite.svg
    ├── index.html
    ├── package.json
    ├── vite.config.js
    ├── README.md
    └── .gitignore
```

---

## 🧪 Implementación

### 🔹 Etapas realizadas
1. Configuración del entorno React + Vite + Three.js.
2. Creación de un objeto central (esfera) con material animado mediante shaders GLSL.
3. Animación del material en tiempo real usando uniforms (`uTime`, `uMouse`).
4. Respuesta a la interacción del usuario (posición del mouse, clics).
5. Implementación de un sistema de partículas y efecto de explosión visual.
6. Simulación de fenómenos visuales dinámicos (ejemplo: texturas animadas, explosiones).

### 🔹 Código relevante

**AnimatedMaterial.jsx**  
Material personalizado animado con tiempo y mouse:

```jsx
import { shaderMaterial } from '@react-three/drei';
import { extend, useFrame, useThree } from '@react-three/fiber';
import React, { useRef } from 'react';
import * as THREE from 'three';
import { dynamicVertexShader, dynamicFragmentShader } from '../shaders/dynamicShader';

const AnimatedMaterialImpl = shaderMaterial(
  { uTime: 0, uMouse: new THREE.Vector2() },
  dynamicVertexShader,
  dynamicFragmentShader
);

extend({ AnimatedMaterialImpl });

export default function AnimatedMaterial() {
  const ref = useRef();
  const { mouse } = useThree();

  useFrame((state) => {
    if (ref.current) {
      ref.current.uTime = state.clock.getElapsedTime();
      ref.current.uMouse.set(mouse.x * 0.5 + 0.5, mouse.y * 0.5 + 0.5);
    }
  });

  return (
    <animatedMaterialImpl ref={ref} attach="material" />
  );
}
```

**dynamicShader.js**  
Shader con animación por tiempo y gradiente según mouse:

```js
export const dynamicVertexShader = `
  varying vec2 vUv;
  void main() {
    vUv = uv;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
  }
`;

export const dynamicFragmentShader = `
  uniform float uTime;
  uniform vec2 uMouse;
  varying vec2 vUv;

  void main() {
    float dist = distance(vUv, uMouse);
    vec3 color = vec3(sin(uTime + dist * 10.0), cos(uTime), sin(dist * 10.0));
    gl_FragColor = vec4(color, 1.0);
  }
`;
```

**ParticleSystem.jsx**  
Sistema de partículas animadas:

```jsx
import { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

export default function ParticleSystem() {
  const ref = useRef();
  const count = 1000;

  const positions = new Float32Array(count * 3).map(() => THREE.MathUtils.randFloatSpread(2));

  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));

  const material = new THREE.PointsMaterial({
    color: new THREE.Color('cyan'),
    size: 0.05,
    transparent: true,
    opacity: 0.75,
    depthWrite: false,
  });

  useFrame(() => {
    ref.current.rotation.y += 0.002;
  });

  return <points ref={ref} geometry={geometry} material={material} />;
}
```

**App.jsx**  
Integración de materiales animados y partículas, con efecto de explosión al hacer clic:

```jsx
import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import AnimatedMaterial from './components/AnimatedMaterial';
import ParticleSystem from './components/ParticleSystem';
import ExplosionParticles from './components/ExplosionParticles';
import { useState } from 'react';

export default function App() {
  const [explode, setExplode] = useState(false);

  return (
    <Canvas camera={{ position: [0, 0, 5], fov: 60 }}>
      <OrbitControls />
      <ambientLight />
      <pointLight position={[5, 5, 5]} />
      
      <mesh onClick={() => setExplode(true)}>
        <sphereGeometry args={[1, 64, 64]} />
        <AnimatedMaterial />
      </mesh>

      <ParticleSystem />
      {explode && <ExplosionParticles trigger={explode} />}
    </Canvas>
  );
}
```

---

## 📊 Resultados Visuales

### Escena con material animado y partículas:

![Material animado y partículas](./results/animated_material_particles.gif)

### Efecto de explosión:

![Explosión de partículas](./results/explosion.gif)

---

## 💬 Reflexión Final

Este taller permitió experimentar con la creación de materiales y efectos visuales avanzados en Three.js usando shaders personalizados y sistemas de partículas. La integración con React y @react-three/fiber facilita la interactividad y la actualización en tiempo real de los parámetros visuales, permitiendo simular fenómenos complejos y atractivos en la web.

El uso de shaders y partículas amplía las posibilidades creativas para experiencias interactivas, artísticas y educativas. En el futuro, se pueden explorar integraciones con datos en tiempo real, sensores físicos o inteligencia artificial para enriquecer aún más las escenas generadas.

---