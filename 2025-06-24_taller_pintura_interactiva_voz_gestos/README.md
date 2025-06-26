# Taller - Obras Interactivas: Pintando con Voz y Gestos

## Objetivo

El objetivo de este taller es crear una obra artística digital interactiva, controlada mediante comandos de voz y gestos, utilizando Python, MediaPipe y speech_recognition. Este enfoque permite al usuario dibujar sin utilizar dispositivos tradicionales como el mouse o el teclado, sino mediante su cuerpo y voz.

## Flujo de Trabajo

### 1. Reconocimiento de Gestos:
Se utiliza la cámara web para detectar los movimientos de la mano usando MediaPipe, específicamente la clase "Hands". El dedo índice controla la posición del pincel en el lienzo digital.

### 2. Reconocimiento de Voz:
Mediante la librería `speech_recognition`, se capturan comandos de voz como:
- "rojo": Cambia el color del pincel a rojo.
- "verde": Cambia el color del pincel a verde.
- "pincel": Cambia la herramienta del pincel a un trazo normal.
- "limpiar": Limpia el lienzo digital.
- "guardar": Guarda la imagen generada en el formato .png o .jpg.

### 3. Interacción Visual:
El lienzo se dibuja en tiempo real en la pantalla, y se actualiza según los gestos y los comandos de voz. Los gestos también pueden cambiar la forma del pincel (por ejemplo, abrir la palma cambia la forma del trazo).

### 4. Guardado de la Obra:
La obra final se guarda como una imagen utilizando `cv2.imwrite()`.

### GIFs y Resultados Visuales

A continuación se muestran los GIFs animados del proceso de dibujo y del resultado final.

**[Insertar GIF del proceso de dibujo aquí]**

**[Insertar GIF del resultado final aquí]**

## Código

Aquí está el código relevante para la ejecución del taller:

```python
import cv2
import mediapipe as mp
import speech_recognition as sr
import numpy as np

# Código principal de la aplicación
