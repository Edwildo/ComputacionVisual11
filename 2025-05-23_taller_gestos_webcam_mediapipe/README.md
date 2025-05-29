# Taller: Gestos con Cámara Web – Control Visual con MediaPipe

**Fecha:** 2025-05-23

## 📋 Descripción general

En este taller usaremos la webcam y la librería MediaPipe para detectar gestos de mano en tiempo real y ejecutar acciones visuales con OpenCV. Aprenderás a crear una interfaz natural que reaccione al número de dedos extendidos y a la distancia entre puntos de referencia de la mano.

---

## 🗂️ Estructura de carpetas

```
2025-05-23_taller_gestos_webcam_mediapipe/
├── python/                # Notebooks o scripts .py
│   └── hand_gestures.py   # Implementación principal
└── README.md              # Documentación del taller
```

---

## 🎯 Objetivos

* Capturar video de la webcam en tiempo real con OpenCV.
* Detectar la posición de las manos usando MediaPipe Hands.
* Medir:

  * Número de dedos extendidos.
  * Distancia entre el índice y el pulgar.
* Generar respuestas visuales basadas en gestos (cambio de color, movimiento de objetos, cambio de escena).

---

## 💻 Python – Notebook / Script

En `python/hand_gestures.py` (o Notebook) implementa:

1. **Inicialización**

   ```python
   import cv2
   from mediapipe import solutions
   import numpy as np

   cap = cv2.VideoCapture(0)
   hands = solutions.hands.Hands(min_detection_confidence=0.7,
                                 min_tracking_confidence=0.5)
   mp_draw = solutions.drawing_utils
   ```

2. **Loop principal**

   ```python
   while True:
       ret, frame = cap.read()
       if not ret: break
       img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
       results = hands.process(img_rgb)

       if results.multi_hand_landmarks:
           for handLms in results.multi_hand_landmarks:
               mp_draw.draw_landmarks(frame, handLms, solutions.hands.HAND_CONNECTIONS)
               # Extraer coordenadas de dedos
               # Calcular número de dedos arriba
               # Calcular distancia índice-pulgar
               # Acciones visuales según condición
       cv2.imshow("Gestos WebCam", frame)
       if cv2.waitKey(1) & 0xFF == 27: break
   cap.release()
   cv2.destroyAllWindows()
   ```

3. **Detección de dedos**

   * Compara la posición de cada punta de dedo con su articulación inferior.
   * Suma cuántos están extendidos.

4. **Distancia entre índice y pulgar**

   ```python
   idx = handLms.landmark[solutions.hands.HandLandmark.INDEX_FINGER_TIP]
   thumb = handLms.landmark[solutions.hands.HandLandmark.THUMB_TIP]
   dist = np.linalg.norm(np.array([idx.x, idx.y]) - np.array([thumb.x, thumb.y]))
   ```

5. **Acciones visuales**

   * Si 5 dedos: fondo verde.
   * Si distancia < umbral: dibuja un círculo rojo.
   * Gestos compuestos para cambiar de escena o mover un sprite.

---

## 📚 Entrega y evidencias

* **GIFs** animados mostrando cada gesto y su respuesta visual.
* **Explicación** breve de cómo funciona MediaPipe Hands y los gestos implementados.
* **Prompts** utilizados (si se apoyó en prompts o documentación externa).
* **Reflexión** sobre precisión, latencia y mejoras posibles (filtrado de ruido, calibración).

---

✅ ¡Listo para comenzar! Realiza commits descriptivos en inglés, documenta tu código y prepara evidencias gráficas para el repositorio.
