# Taller - Detección de Objetos en Tiempo Real con YOLO y Webcam

## Objetivo

El objetivo de este taller es implementar detección de objetos en tiempo real utilizando el modelo YOLOv5 o YOLOv8 preentrenado y capturar video desde la webcam. Se busca explorar la eficiencia del modelo y medir el desempeño en vivo (FPS).

## Flujo de Trabajo

### 1. Instalación de Dependencias:

Para comenzar, se deben instalar las dependencias necesarias. En la terminal, ejecutar:

```bash
pip install ultralytics opencv-python
2. Importar Librerías y Cargar el Modelo:
Usamos ultralytics para cargar el modelo YOLO preentrenado y opencv-python para capturar el video de la webcam.

python
Copiar
from ultralytics import YOLO
import cv2, time

model = YOLO('yolov8n.pt')  # o yolov5s.pt si se usa torch.hub
3. Capturar Video en Tiempo Real:
Abrimos la cámara para capturar los frames.

python
Copiar
cap = cv2.VideoCapture(0)  # Captura de la cámara
4. Realizar Detección y Visualización:
Por cada frame capturado:

Medimos el tiempo de inicio.

Realizamos la detección con model.predict().

Dibujamos las cajas de detección, etiquetas y confianza sobre el frame.

Calculamos los FPS y mostramos el resultado con cv2.imshow().

python
Copiar
while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    start_time = time.time()  # Medir tiempo de inicio
    results = model.predict(source=frame, stream=True)  # Detección de objetos

    # Dibujar las detecciones sobre el frame
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Coordenadas de la caja
            conf = box.conf[0]  # Confianza
            label = result.names[int(box.cls[0])]  # Etiqueta

            # Dibujar la caja y la etiqueta
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Calcular FPS
    end_time = time.time()
    fps = 1 / (end_time - start_time)
    
    # Mostrar FPS en el frame
    cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # Mostrar el resultado
    cv2.imshow("Detección de Objetos en Vivo", frame)
    
    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
5. Bonus:
Mostrar solo detecciones específicas: Para filtrar por etiquetas específicas como "persona" o "celular", puedes agregar una condición:

python
Copiar
if label in ["person", "cell phone"]:
    # Dibujar detección
Mostrar FPS gráficamente: El código anterior ya dibuja los FPS en la esquina superior izquierda.

GIFs y Resultados Visuales
A continuación se muestran los GIFs animados del proceso de detección de objetos en vivo y la interfaz con las etiquetas y confianza.

[Insertar GIF de detección de objetos aquí]

[Insertar GIF de interfaz con etiquetas y confianza aquí]

Reflexión
Durante el taller, se pudo observar que el modelo YOLOv5 o YOLOv8 proporciona una detección eficiente y precisa, especialmente con objetos de alto contraste y en un entorno controlado. El FPS promedio depende de la calidad de la webcam y la resolución del video. En general, la detección de objetos como "personas" fue más precisa que otros objetos pequeños como "celulares".

Prompts Utilizados:

model.predict(source=frame, stream=True) para realizar la detección.

box.conf para extraer la confianza de la detección.

cv2.putText() para mostrar las etiquetas y el FPS en la pantalla.

python
Copiar

### 🛠️ Código Principal (`main.py`)

```python
from ultralytics import YOLO
import cv2, time

# Cargar el modelo YOLO preentrenado
model = YOLO('yolov8n.pt')  # Puedes usar 'yolov5s.pt' si prefieres YOLOv5

# Abrir la cámara web
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    start_time = time.time()  # Medir el tiempo de inicio
    results = model.predict(source=frame, stream=True)  # Detección de objetos
    
    # Dibujar las detecciones sobre el frame
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Coordenadas de la caja
            conf = box.conf[0]  # Confianza
            label = result.names[int(box.cls[0])]  # Etiqueta
            
            # Dibujar la caja y la etiqueta
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    
    # Calcular FPS
    end_time = time.time()
    fps = 1 / (end_time - start_time)
    
    # Mostrar FPS en el frame
    cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # Mostrar el resultado
    cv2.imshow("Detección de Objetos en Vivo", frame)
    
    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()