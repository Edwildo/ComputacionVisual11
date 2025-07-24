# Taller - Animaciones por Esqueleto: Importando y Reproduciendo Animaciones

## Objetivo

Esta sesión práctica se enfoca en la implementación de sistemas de animación esquelética aplicados a modelos tridimensionales mediante Three.js. El desarrollo consistió en manipular un archivo `.gltf` con animaciones integradas, permitiendo comprender los procesos de carga, ejecución y gestión de clips animados en entornos interactivos y dinámicos.

---

## Tecnologías utilizadas

- [React](https://reactjs.org/)
- [Vite](https://vitejs.dev/)
- [Three.js](https://threejs.org/)
- [React Three Fiber](https://docs.pmnd.rs/react-three-fiber)
- [Drei](https://github.com/pmndrs/drei)

---

## ¿Qué es una animación por esqueleto?

El sistema de animación esquelética opera mediante una **estructura ósea interna (armature)** que gobierna el movimiento de objetos tridimensionales. En contraposición a la manipulación directa de vértices, este método emplea un esqueleto virtual donde las deformaciones de la geometría resultan de la influencia jerárquica de cada hueso sobre la superficie del modelo.

Cada secuencia animada se estructura en **clips**, que representan series temporales de transformaciones aplicadas a los elementos óseos. Estos segmentos pueden ser ejecutados, detenidos o combinados mediante técnicas de interpolación (blending/fading).

---

## Animaciones en Three.js

La implementación aprovechó la función `useGLTF()` para el proceso de carga del modelo, mientras que `useAnimations()` proporcionó acceso completo a los clips disponibles en el archivo. El sistema configuró la reproducción automática de la secuencia principal durante la inicialización de la escena:

```jsx
const { actions, names } = useAnimations(gltf.animations, gltf.scene)

useEffect(() => {
  if (names.length > 0 && actions[names[0]]) {
    actions[names[0]].reset().fadeIn(0.5).play()
  }
}, [actions, names])


---
## Resultado
![Resultado](./resultado.png)
---

## Observaciones
La carga del modelo se completó exitosamente, ejecutándose la animación primaria con rendimiento óptimo y fluidez visual.

El ciclo animado mantiene continuidad perpetua sin presentar fallos en la estructura de rigging implementada.

La compatibilidad con React Three Fiber demostró ser intuitiva y permitió un desarrollo componetizado eficiente.

Aunque las transiciones entre múltiples secuencias animadas no fueron desarrolladas en esta iteración, la arquitectura actual facilita su implementación futura.

## Conclusión
Esta experiencia práctica facilitó la comprensión profunda de los mecanismos que rigen las animaciones esqueléticas en el ecosistema Three.js, incluyendo la organización estructural de clips animados y su ejecución en contextos interactivos. Resultó particularmente valioso el aprendizaje diferencial entre la manipulación directa de objetos versus el trabajo con arquitecturas jerárquicas basadas en sistemas óseos.

Para desarrollos posteriores, sería enriquecedor incorporar controles de interfaz para alternar entre diferentes clips, o establecer sincronización entre eventos del usuario y las secuencias animadas (como desplegar texto contextual durante movimientos específicos o vocalizaciones del modelo).
