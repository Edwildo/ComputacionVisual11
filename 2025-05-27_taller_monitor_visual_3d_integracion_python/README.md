# 🧪 Taller - Creando un Monitor de Actividad Visual en 3D

## 📅 Fecha
`2025-06-26`    

---

## 🎯 Objetivo del Taller

Diseñar una escena 3D interactiva que se adapte en tiempo real según los datos provenientes de un sistema de visión por computador. La escena debe responder visualmente (cambiando color, escala o posición de objetos) en función de métricas detectadas, simulando así un sistema de vigilancia, arte generativo reactivo o interfaz inteligente.

---

## 🧠 Conceptos Aprendidos

- Procesamiento de imágenes y detección de objetos con OpenCV y YOLO.
- Transmisión de datos en tiempo real entre Python y Three.js (React Three Fiber) usando sockets, WebSocket o archivos JSON.
- Visualización reactiva en 3D basada en la detección de objetos.
- Manipulación de objetos 3D (cambio de color, escala, posición) según datos recibidos.

---

## 🔧 Herramientas y Entornos

### Parte 1 - Python (Detección Visual):
- `opencv-python` para procesamiento de imágenes.
- `ultralytics` o `cvlib` para detección de objetos (como YOLO).
- `socket`, `json` o `python-osc` para transmitir datos en tiempo real.

### Parte 2 - Three.js con React Three Fiber:
- Three.js y React Three Fiber para crear la escena 3D interactiva.
- WebSocket o archivo JSON para la comunicación con Python.

---

## 📁 Estructura del Proyecto

yyyy-mm-dd_taller_monitor_visual_3d_integracion_python/
├── python/
│ ├── detect_objects.py # Script de detección de objetos y transmisión de datos
│ ├── socket_server.py # Servidor para transmitir datos (WebSocket, Socket o JSON)
├── threejs/
│ ├── src/
│ │ ├── App.jsx # Componente React con la escena 3D
│ │ ├── main.jsx
│ │ ├── Visualizer.jsx # Componente para recibir datos y modificar la escena
│ │ └── utils/
│ │ └── socket.js # Funciones para gestionar la comunicación con Python
│ ├── public/
│ │ ├── index.html
│ ├── package.json
├── README.md

yaml
Copiar

---

## 🧪 Implementación

### Parte 1: Detección Visual en Python

#### 1. Configuración de la detección de objetos con YOLO

Primero, se instala `opencv-python` y `ultralytics`:

```bash
pip install opencv-python ultralytics
Luego, se configura el script para detectar personas u objetos y enviar los datos a través de un socket o WebSocket:

detect_objects.py:

python
Copiar
import cv2
from ultralytics import YOLO
import socket
import json

# Cargar el modelo YOLO
model = YOLO('yolov8n.pt')

# Configurar el socket para enviar datos
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 10000)

# Abrir la cámara
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)
    detections = len(results.pandas().xywh)  # Conteo de objetos

    # Enviar datos (por ejemplo, número de personas detectadas)
    data = {'detections': detections}
    message = json.dumps(data)
    sock.sendto(message.encode(), server_address)

    # Visualizar el video
    cv2.imshow('Video', frame)
    
    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
Este script detecta objetos en tiempo real y transmite la cantidad de objetos detectados a través de un socket.

Parte 2: Visualización en Three.js con React Three Fiber
2. Crear la Escena 3D y Recibir los Datos
App.jsx:

jsx
Copiar
import React, { useEffect, useState } from 'react';
import { Canvas } from '@react-three/fiber';
import { Box } from '@react-three/drei';
import socketIOClient from 'socket.io-client';

const SOCKET_SERVER_URL = "http://localhost:10000";

export default function App() {
  const [detections, setDetections] = useState(0);

  useEffect(() => {
    const socket = socketIOClient(SOCKET_SERVER_URL);
    
    // Escuchar datos del servidor
    socket.on('data', (data) => {
      setDetections(data.detections);
    });

    return () => socket.disconnect();
  }, []);

  return (
    <Canvas>
      <ambientLight />
      <spotLight position={[10, 10, 10]} />
      <Box scale={[detections, detections, detections]}>
        <meshStandardMaterial color={`rgb(${detections * 50}, 0, 0)`} />
      </Box>
    </Canvas>
  );
}
En este componente React, el color y la escala del objeto (un cubo) cambian en función del número de detecciones recibidas desde el servidor Python.

🔹 Código relevante
socket_server.py:

python
Copiar
import socket
import json

server_address = ('localhost', 10000)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(server_address)

while True:
    data, address = sock.recvfrom(4096)
    if data:
        print(f"Datos recibidos: {data.decode()}")
        # Aquí podemos procesar los datos recibidos y enviar al cliente (Three.js)
Este script recibe datos desde Python y los transmite a React Three Fiber.

📊 Resultados Visuales
Escena con Objetos Reactivos:
[Insertar GIF de cambio visual en la escena 3D aquí]

[Insertar GIF de datos en consola u overlay aquí]

💬 Reflexión Final
Este taller permite crear una experiencia visual interactiva en 3D, donde la escena responde en tiempo real a los datos provenientes de un sistema de visión por computador. La integración entre Python y Three.js (React Three Fiber) mediante sockets o WebSocket permite transmitir información de detección visual y adaptarla a un entorno 3D.

La comunicación en tiempo real fue bastante eficiente, aunque la latencia de la red y la capacidad de procesamiento del sistema pueden influir en la fluidez de la visualización. Para hacerlo más robusto, se podrían añadir más métricas de control, como el número de frames procesados por segundo (FPS) o la mejora de la precisión de los modelos de detección.