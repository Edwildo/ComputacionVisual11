# 🧪 Taller 66 – Optimización Gráfica en Three.js

## 📅 Fecha  
2025-05-26 – Fecha de realización

---

## 🎯 Objetivo del Taller  
Aprender y aplicar técnicas de optimización visual en proyectos desarrollados con Three.js o React Three Fiber, con el fin de mejorar el rendimiento, reducir tiempos de carga y garantizar una experiencia fluida.

---

## 🧠 Conceptos Aprendidos

- Optimización visual en entornos 3D
- Técnicas de simplificación de geometría (low poly)
- Uso de LOD (Level of Detail) con tres niveles de calidad
- Compresión de texturas 

---

## 🔧 Herramientas y Entornos

- React Three Fiber
- Three.js
- Blender (para simplificación de modelos)
- [squoosh.app](https://squoosh.app) (para compresión de texturas)
- Vite

---

## 📁 Estructura del Proyecto
```
2025-04-XX\taller\optimizar\graficos/
├── threejs/
├── resultados/
├── README.md
```
---

## 🧪 Implementación

### 🔹 Etapas realizadas

1. Conversión de texturas PNG  para reducir tamaño.
2. Simplificación de modelos en Blender (Low Poly).
3. Implementación de `LOD` en `SceneModels.jsx`.

### 🔹 Código relevante

```jsx
// Implementación de LOD
function createLOD(model) {
  const lod = new LOD();

  const high = model.scene.clone();
  const medium = model.scene.clone();
  const low = model.scene.clone();

  medium.traverse((child) => {
    if (child.isMesh) {
      child.geometry = child.geometry.clone();
      child.geometry = child.geometry.toNonIndexed();
      child.geometry.deleteAttribute("normal");
    }
  });

  low.traverse((child) => {
    if (child.isMesh) {
      child.geometry = child.geometry.clone();
      child.geometry = child.geometry.toNonIndexed();
      child.geometry.deleteAttribute("normal");
      child.geometry.deleteAttribute("uv");
    }
  });

  lod.addLevel(high, 0);   // cerca
  lod.addLevel(medium, 30); // media distancia
  lod.addLevel(low, 70);   // lejos

  return lod;
}
```
---
## 🧩 Prompts Usados

"Implementa LOD para tres modelos GLB en Three.js."

"Integra Stats  para visualizar el rendimiento de la escena."

---
## 📊 Resultados Visuales

## Aplicacion LOD
![aplicacionLOD (1)](https://github.com/user-attachments/assets/6cb10566-340e-431b-bf7a-33d6f3463629)

## Compresion de texturas
![2025-05-26 18-29-19 (1)](https://github.com/user-attachments/assets/91d61397-336e-4a7d-8d14-c50baeef75fd)

## Low Poly aplicado para no perder tanta calidad
![2025-05-26 18-28-34 (1)](https://github.com/user-attachments/assets/4968a152-61c3-48d9-9f53-b85ab85ee918)

## Low Poly aplicado para la mayor simplifacion posible
![2025-05-26 18-28-12 (1)](https://github.com/user-attachments/assets/f9e7b004-7171-43f3-a1c3-98927e559d06)

---

## 💬 Reflexión Final

Este taller fue muy útil para comprender cómo afectan distintas técnicas de optimización al rendimiento en entornos 3D. Ver la diferencia entre usar modelos pesados sin compresión versus usar versiones simplificadas y optimizadas fue interesante.

La técnica más util fue LOD, ya que permite balancear calidad y rendimiento dinámicamente según la distancia. Además, la compresión de texturas fue fácil de implementar.


## 🛠️ Criterios de evaluación

✅ Aplicación de al menos 3 técnicas de optimización

✅ Evidencias visuales claras

✅ Fluidez mejorada o justificada

✅ Código organizado (aunque no requerido mostrarlo aquí)

✅ README bien documentado y reflexivo

✅ Commits descriptivos en inglés

