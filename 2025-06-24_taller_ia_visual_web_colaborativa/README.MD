# Taller - IA Visual Colaborativa: Comparte tus Resultados en Web

## 🎯 Objetivo del taller

Desarrollar una solución donde los resultados de un modelo visual de IA (detecciones, métricas o imágenes) puedan compartirse en una página web sencilla. Esto permite que otros usuarios o compañeros vean y comprendan visualmente qué fue detectado, cómo se comportó el sistema y qué resultados produjo.

---

## 🧠 Parte 1 - Captura y Exportación (Python)

Utilicé **MediaPipe** para detectar rostros en una imagen y generar:

- `deteccion.png`: imagen con la detección visual.
- `deteccion.json`: archivo con bounding boxes, clase (`face`) y confianza.
- Carpeta: `/resultados`

### 📸 Imagen procesada:
- Se utilizó una imagen estática (`persona.jpg`) ubicada en `resultados/`.
- Se exportaron las coordenadas del rostro detectado y se dibujó un rectángulo verde.

### 🧪 Herramientas utilizadas:
- `opencv-python`
- `mediapipe`
- `json`
- `datetime`
- `os`

---

## 🌐 Parte 2 - Visualización en Web (HTML + JS)

La visualización se realizó en `web/index.html`, mostrando:

- La imagen `deteccion.png`.
- Los datos cargados desde `deteccion.json`.
- Detecciones dibujadas directamente sobre el canvas.
- Las clases y confianzas como etiquetas flotantes.

### 👁️ Evidencia visual

#### 🔹 GIF - Interfaz Web
![Interfaz Web](../0625.gif)

---

## 💾 Estructura del proyecto

2025-06-24_taller_ia_visual_web_colaborativa/
├── python/
│ └── exportar_deteccion.py
├── web/
│ ├── index.html
│ ├── script.js
│ └── style.css
├── resultados/
│ ├── persona.jpg
│ ├── deteccion.png
│ └── deteccion.json
├── 0625.gif
└── README.md

🤔## Reflexión
Compartir visualmente los resultados ayuda enormemente a validar el funcionamiento del modelo, comunicar los hallazgos y fomentar la colaboración entre desarrolladores y usuarios. Tener una interfaz sencilla pero clara permite que cualquier persona entienda qué está pasando, incluso sin saber programar.

✅ Criterios cumplidos
✅ Captura funcional y exportación desde Python.

✅ Visualización clara con imagen y JSON.

✅ Web simple y navegable.

✅ Código modular y comentado.

✅ Evidencias visuales (GIF incluido).

✅ README completo.