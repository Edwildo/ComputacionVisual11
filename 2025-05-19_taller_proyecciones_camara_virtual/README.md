# Taller: Proyecciones 3D - Cómo ve una Cámara Virtual

**Fecha:** 2025-05-19

## 📋 Descripción general

En este taller exploramos cómo se generan proyecciones 3D desde el punto de vista de una cámara, comparando los modos **perspectiva** y **ortográfico**, tanto en **Unity** como en **Three.js** (React Three Fiber).

---

## 🗂️ Estructura de carpetas

```
2025-05-19_taller_proyecciones_camara_virtual/
├── unity/               # Proyecto Unity (Scenes, Scripts, UI)
└── threejs/             # Proyecto React Three Fiber
    ├── threejs-proyecciones/
    │   ├── public/
    │   └── src/
    │       ├── App.js
    │       ├── SceneObjects.js
    │       └── CameraControls.js
    └── package.json
```

---

## 🎯 Objetivos

* Entender la diferencia visual entre proyección en **perspectiva** (objetos se hacen más pequeños con distancia) y **ortográfica** (tamaño constante).
* Visualizar y manipular la **matrix de proyección**.
* Implementar controles (botón y slider) para alternar e interactuar con los modos de cámara.

---

## 🕹️ Unity (Carpeta `unity/`)

### 1. Preparar la escena

1. Crea un proyecto 3D en Unity (LTS).
2. En la escena (`SampleScene`): agrega `Plane`, `Cube`, `Sphere`, `Capsule` distribuidos en distintas profundidades.
3. Ajusta la `Main Camera` en posición `(0,3,-6)`, rotación `(20,0,0)`, **Projection**: Perspective.

### 2. UI - Canvas

* `Canvas` (Screen Space - Overlay + Canvas Scaler: Scale With Screen Size, 1920×1080).
* Botón `Switch Projection`: alterna modos.
* Slider `OrthoSlider`: ajusta `camera.orthographicSize` en ortográfico.
* Texto `Current: ...` (TextMeshPro) muestra el modo activo.

### 3. Script `CameraSwitcher.cs`

```csharp
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class CameraSwitcher : MonoBehaviour
{
    public Camera cam;
    public TMP_Text modeText;
    public Slider orthoSlider;

    void Start()
    {
        // Rango y valor inicial
        orthoSlider.minValue = 2;
        orthoSlider.maxValue = 10;
        orthoSlider.value = 5;
        cam.orthographicSize = 5;
        orthoSlider.onValueChanged.AddListener(AdjustOrthoSize);
        UpdateUI();
    }

    public void ToggleProjection()
    {
        cam.orthographic = !cam.orthographic;
        if (cam.orthographic) cam.orthographicSize = orthoSlider.value;
        UpdateUI();
    }

    public void AdjustOrthoSize(float size)
    {
        if (cam.orthographic)
            cam.orthographicSize = Mathf.Clamp(size, orthoSlider.minValue, orthoSlider.maxValue);
    }

    void UpdateUI()
    {
        modeText.text = "Current: " + (cam.orthographic ? "Orthographic" : "Perspective");
        orthoSlider.gameObject.SetActive(cam.orthographic);
    }

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.P))
            Debug.Log("Projection Matrix:\n" + cam.projectionMatrix);
    }
}
```

### 4. Conexiones en Inspector

* `CameraManager` (GameObject vacío) con `CameraSwitcher`.
* Asigna: `Cam` → Main Camera, `ModeText` → Text (TMP), `OrthoSlider` → Slider.
* `Button` OnClick → `CameraSwitcher.ToggleProjection()`.

### 5. Prueba y evidencias

* Haz clic para alternar modo.
* Presiona **P** para ver la matriz en consola.
* Captura GIFs mostrando ambos modos y el zoom con slider.

---

## 🌐 Three.js (React Three Fiber - Carpeta `threejs/threejs-proyecciones`)

### 1. Instalación

```bash
npx create-react-app threejs-proyecciones
cd threejs-proyecciones
npm install three @react-three/fiber @react-three/drei
```

### 2. Archivos clave

#### `src/App.js`

```jsx
import React, { useEffect, useRef, useState } from 'react'
import { Canvas } from '@react-three/fiber'
import { PerspectiveCamera, OrthographicCamera, OrbitControls } from '@react-three/drei'
import SceneObjects from './SceneObjects'
import CameraControls from './CameraControls'

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
      <CameraControls
        mode={mode}
        setMode={setMode}
        orthoSize={orthoSize}
        setOrthoSize={setOrthoSize}
      />
      <Canvas style={{ width: '100vw', height: '100vh' }}>
        {mode === 'perspective' ? (
          <PerspectiveCamera makeDefault position={[0,2,3]} fov={75} />
        ) : (
          <OrthographicCamera
            ref={camRef}
            makeDefault
            position={[0,2,3]}
            near={0.1}
            far={100}
          />
        )}
        <ambientLight />
        <SceneObjects />
        <OrbitControls />
      </Canvas>
    </>
  )
}
```

#### `src/SceneObjects.js`

```jsx
import React from 'react'
export default function SceneObjects() {
  return (
    <>
      <mesh position={[-2,0.5,-2]}> <boxGeometry args={[1,1,1]} /> <meshStandardMaterial color="red"/> </mesh>
      <mesh position={[0,0.5,0]}>  <sphereGeometry args={[0.5,32,32]}/> <meshStandardMaterial color="green"/> </mesh>
      <mesh position={[2,0.5,2]}>  <boxGeometry args={[1,1,1]} /> <meshStandardMaterial color="blue"/> </mesh>
    </>
  )
}
```

#### `src/CameraControls.js`

```jsx
import React from 'react'
export default function CameraControls({mode,setMode,orthoSize,setOrthoSize}) {
  return (
    <div style={{ position:'absolute', top:20, left:20, zIndex:1 }}>
      <button onClick={() => setMode(m => m==='perspective'?'orthographic':'perspective')}>
        {mode==='perspective'?'Switch to Orthographic':'Switch to Perspective'}
      </button>
      <p>Mode: {mode}</p>
      {mode==='orthographic' && (
        <div>
          <label>Ortho Size: {orthoSize}</label>
          <input type="range" min={2} max={50} value={orthoSize}
            onChange={e => setOrthoSize(Number(e.target.value))} />
        </div>
      )}
    </div>
  )
}
```

### 3. Arrancar la app

```bash
npm start
```

---

## 📝 Reflexión final

* **Perspectiva** simula nuestra visión natural: líneas convergen al horizonte.
* **Ortográfica** es útil en CAD o UI 2D sobre 3D: no hay distorsión por distancia.
* La **matriz de proyección** (4×4) es la responsable de la transformación de coordenadas.

---
