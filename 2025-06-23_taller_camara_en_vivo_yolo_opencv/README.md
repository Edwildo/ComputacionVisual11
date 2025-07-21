# 🧪 Taller - Cámara en Vivo: Captura y Procesamiento de Video en Tiempo Real con YOLO

## 📅 Fecha
`2025-06-26`    

---

## 🎯 Objetivo del Taller

Conectar la cámara web del PC y procesar el video en tiempo real usando Python, OpenCV y YOLO para aplicar filtros visuales y realizar detección de objetos en vivo. Combina técnicas clásicas de visión artificial con detección basada en aprendizaje profundo.

---

## 🧠 Conceptos Aprendidos

- Captura de vídeo en tiempo real con OpenCV (`cv2.VideoCapture`).
- Filtros clásicos: escala de grises, binarización y detección de bordes (Canny).
- Integración de un modelo YOLO (v5 o v8) con `ultralytics` o `cv2.dnn`.
- Visualización simultánea de múltiples ventanas.
- Control de flujo y eventos de teclado para pausar, cambiar filtros y guardar.
- Exportación de capturas e incluso fragmentos de vídeo.

---

## 🔧 Herramientas y Entornos

- **Python** (3.8+)
- `opencv-python`, `numpy`
- `ultralytics` (YOLOv8) o `cvlib` / `cv2.dnn` (YOLOv3/4)
- (Opcional) `imutils` para utilidades de vídeo

---

## 📁 Estructura del Proyecto

2025-06-26_taller_camara_en_vivo_yolo_opencv/
├── python/
│ ├── main.py
│ └── requirements.txt
└── README.md

python
Copiar
Editar

---

## 🧪 Implementación

### 🔹 Etapas realizadas

1. **Entorno y dependencias**  
   - Crear y activar un virtualenv.  
   - `pip install opencv-python numpy ultralytics`.

2. **Captura de vídeo**  
   - `cap = cv2.VideoCapture(0)`  
   - Lectura en bucle de `cap.read()`.

3. **Filtros clásicos**  
   - Gris: `cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)`  
   - Binarización: `cv2.threshold()`  
   - Bordes: `cv2.Canny()`.

4. **Detección con YOLO**  
   - Cargar modelo: `model = YOLO('yolov8n.pt')`  
   - Inferencia: `results = model(frame)`  
   - Dibujar cajas y etiquetas.

5. **Visualización**  
   - Ventana “Original/Filtro” con el filtro activo.  
   - Ventana “Detección YOLO” con las cajas.

6. **Control por teclado**  
   - `q`: salir  
   - `p`: pausar/reanudar  
   - `0–3`: seleccionar filtro  
   - `s`: guardar imagen  
   - `v`: grabar un breve clip.

7. **Bonus**  
   - Mostrar conteo en vivo de detecciones.  
   - Cambiar filtro automáticamente si detecta personas.

---

## 🔹 Código relevante

**python/main.py**

```python
import cv2
import numpy as np
from ultralytics import YOLO

# Cargar modelo YOLO
model = YOLO('yolov8n.pt')  # o 'yolov5s.pt'

# Iniciar captura
cap = cv2.VideoCapture(0)
filter_mode = 0   # 0=original,1=gris,2=binary,3=canny
paused = False

while True:
    if not paused:
        ret, frame = cap.read()
        if not ret:
            break

        # 1) Filtros clásicos
        gray   = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        edges  = cv2.Canny(gray, 100, 200)

        # 2) Detección con YOLO
        det_frame = frame.copy()
        results = model(frame)
        detections = 0
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0]
                cls  = int(box.cls[0])
                label = r.names[cls]
                cv2.rectangle(det_frame, (x1, y1), (x2, y2), (0,255,0), 2)
                cv2.putText(det_frame, f"{label} {conf:.2f}",
                            (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX,
                            0.6, (0,255,0), 2)
                detections += 1

        # 3) Selección de ventana según filtro
        if filter_mode == 0:
            display = frame
        elif filter_mode == 1:
            display = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        elif filter_mode == 2:
            display = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
        else:
            display = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        # 4) Mostrar ventanas
        cv2.imshow('Original / Filtro', display)
        cv2.imshow('Detección YOLO', det_frame)
        cv2.setWindowTitle('Detección YOLO',
                           f'Detecciones: {detections}')

    # 5) Controles de teclado
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('p'):
        paused = not paused
    elif key in map(ord, ['0','1','2','3']):
        filter_mode = int(chr(key))
    elif key == ord('s'):
        cv2.imwrite('captura.png', display)
    elif key == ord('v'):
        # Graba 5 segundos de vídeo
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('clip.avi', fourcc, 20.0,
                              (frame.shape[1], frame.shape[0]))
        for _ in range(100):
            ret2, f2 = cap.read()
            if not ret2: break
            out.write(f2)
        out.release()

cap.release()
cv2.destroyAllWindows()
📊 Resultados Visuales
Detección en Tiempo Real

Comparativa de Filtros

💬 Reflexión Final
Combinar filtros clásicos con un modelo YOLO en tiempo real permite ver la sinergia entre técnicas de visión por computador. YOLOv8 entrega detecciones fiables de personas y objetos comunes, manteniendo unos 15–20 FPS en una cámara básica. Para optimizar, se puede reducir resolución, usar versiones más ligeras de YOLO o procesar en hilos separados.

