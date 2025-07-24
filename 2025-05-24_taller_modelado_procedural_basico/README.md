# Taller: Modelado Procedural Básico

## 1. Introducción

**Modelado procedural** consiste en la generación de geometría y escenas 3D completamente por código en lugar de esculpir mallas a mano. Esto ofrece:

* **Parametrización:** múltiples variantes cambiando pocos valores.
* **Escalabilidad:** escenas complejas con bucles y recursión.
* **Dinámico:** interacción en tiempo real y animaciones algorítmicas.

## 2. Three.js + React Three Fiber

### 2.1 Estructura de carpetas

```
threejs/
├── public/
│   └── index.html        # Root HTML
├── src/
│   ├── main.jsx          # Punto de entrada
│   ├── App.jsx           # Canvas y lógica principal
│   └── components/
│       ├── Grid.jsx      # Rejilla de cubos elevados
│       ├── Spiral.jsx    # Espiral de cilindros
│       └── CustomMesh.jsx# Malla definida por BufferGeometry
└── package.json          # Dependencias y scripts
```

### 2.2 Componentes clave

* **`Grid.jsx`**: genera una rejilla de cubos posicionados en Y=0.5 para que descansen sobre “suelo”.
* **`Spiral.jsx`**: crea cilindros distribuidos en espiral con `useMemo` para optimizar.
* **`CustomMesh.jsx`**: define una malla manual con `BufferGeometry`, atributos de vértices e índices.
* **`App.jsx`**: `<Canvas>` con cámara personalizada, luz ambiental y direccional, y controles con `OrbitControls`.

### 2.3 Actividades realizadas

* **Mapeo de arrays:** uso de JavaScript para generar posiciones.
* **BufferGeometry:** edición de atributos en tiempo real.
* **Animación (bonus):** sugerencia de usar `useFrame` para transformar vértices.

### 2.4 Evidencias visuales

![Grid R3F](./gifs/threejs_grid.gif)
![Spiral R3F](./gifs/threejs_spiral.gif)
![Custom Mesh R3F](./gifs/threejs_custommesh.gif)

## 3. Diferencias clave entre manual y procedural

| Aspecto             | Modelado Manual | Modelado Procedural           |
| ------------------- | --------------- | ----------------------------- |
| Flexibilidad        | Fija            | Paramétrica                   |
| Escalabilidad       | Laboriosa       | Automática (bucle/recursión)  |
| Diseño dinámico     | Estático        | Interactivo y animable        |
| Complejidad inicial | Baja            | Requiere programación inicial |

## 4. Prompts (si usaste IA)

> *Prompt ejemplo para generar assets GIF:*
>
> ```
> Generate a looping GIF of a 5×5 grid of gray cubes rotating on the Y-axis, background transparent.
> ```

## 5. Conclusión

El **modelado procedural** agiliza la creación de escenas repetitivas y parametrizables, ideal para prototipos, visualizaciones científicas o mundos de videojuegos.

---

### Commits sugeridos

```
feat: elevate Y in R3F grid to avoid overlaps
feat: procedural spiral & custom mesh in React Three Fiber
chore: add GIF evidences and update README
```
