# 🧪 Taller - Interfaces Multimodales: Control por Voz y Gesto

## 📅 Fecha
`2025-07-20`    

---

## 🎯 Objetivo del Taller

Desarrollar una interfaz multimodal que combine reconocimiento de voz y detección de gestos con las manos para controlar elementos visuales en tiempo real. Se busca explorar la integración de múltiples modalidades de entrada (voz y gestos) para crear experiencias de usuario más naturales e intuitivas, aplicables en sistemas de realidad aumentada, interfaces de usuario avanzadas y control de aplicaciones.

---

## 🧠 Conceptos Aprendidos

- Detección de gestos con las manos usando `MediaPipe`.
- Reconocimiento de voz en tiempo real con `SpeechRecognition`.
- Integración multimodal para control de interfaces.
- Programación concurrente con `threading` para manejo simultáneo de múltiples entradas.
- Renderizado en tiempo real con `pygame`.
- Combinación de comandos de voz con gestos para acciones específicas.
- Manejo de estado compartido entre diferentes hilos de ejecución.

---

## 🔧 Herramientas y Entornos

- Python (local)
- `mediapipe` para detección de gestos de manos
- `opencv-python` para captura y procesamiento de video
- `speechrecognition` para reconocimiento de voz
- `pyaudio` para captura de audio
- `pygame` para renderizado gráfico
- `numpy` para manipulación de datos
- `python-osc` para comunicación (opcional)

---

## 📁 Estructura del Proyecto

```
2025-07-20_taller_interfaces_multimodales_voz_gesto/
├── taller_interfaces_multimodales.ipynb  # Notebook principal con el código del taller
├── README.md                              # Documentación del taller
```

---

## 🧪 Implementación

### 🔹 Etapas realizadas

1. **Configuración del Entorno**: Instalación de las librerías necesarias para detección de gestos, reconocimiento de voz y renderizado.

   ```python
   pip install mediapipe opencv-python speechrecognition pyaudio python-osc numpy pygame
   ```

2. **Detección de Gestos**: Implementación de detección de gestos de manos usando MediaPipe para reconocer patrones específicos como mano abierta y dos dedos levantados.

   **Código relevante:**
   ```python
   import mediapipe as mp
   
   mp_hands = mp.solutions.hands
   hands = mp_hands.Hands()
   
   def detectar_gestos():
       # Detección simple basada en landmarks
       if results.multi_hand_landmarks:
           dedos_arriba = 0
           # Lógica para contar dedos levantados
           estado_gesto["mano_abierta"] = dedos_arriba >= 4
           estado_gesto["dos_dedos"] = dedos_arriba == 2
   ```

3. **Reconocimiento de Voz**: Implementación de captura y reconocimiento de comandos de voz en español para controlar la aplicación.

   **Código relevante:**
   ```python
   import speech_recognition as sr
   
   def reconocer_comando():
       r = sr.Recognizer()
       with sr.Microphone() as source:
           audio = r.listen(source, timeout=3)
           texto = r.recognize_google(audio, language="es-ES")
           return texto.lower()
   ```

4. **Integración Multimodal**: Combinación de gestos y comandos de voz para ejecutar acciones específicas en la interfaz visual.

   **Lógica de control:**
   - **Mano abierta + comando "cambiar"**: Cambia color a azul
   - **Mano abierta + comando "rojo"**: Cambia color a rojo  
   - **Mano abierta + comando "verde"**: Cambia color a verde
   - **Dos dedos + comando "mover"**: Mueve el objeto
   - **Dos dedos + comando "ocultar/mostrar"**: Controla visibilidad

5. **Renderizado en Tiempo Real**: Visualización de los resultados de la interacción multimodal usando pygame con elementos gráficos que responden a los comandos.

   **Código relevante:**
   ```python
   import pygame
   
   # Renderizar escena basada en estado actual
   if mostrar:
       pygame.draw.circle(pantalla, color, (x, 300), 50)
   texto = font.render(f"Comando: {ultimo_comando}", True, (255, 255, 255))
   ```

6. **Programación Concurrente**: Uso de hilos para manejar simultáneamente la detección de gestos, reconocimiento de voz y renderizado de la interfaz.

   **Código relevante:**
   ```python
   import threading
   
   threading.Thread(target=detectar_gestos, daemon=True).start()
   threading.Thread(target=escuchar_voz, daemon=True).start()
   ```

### 🔹 Funcionalidades Implementadas

- **Detección de gestos de mano**: Reconocimiento de mano abierta y dos dedos levantados
- **Reconocimiento de voz**: Captura y procesamiento de comandos en español
- **Control multimodal**: Combinación de gesto + voz para acciones específicas
- **Interfaz visual responsiva**: Círculo que cambia color, posición y visibilidad
- **Feedback visual**: Mostrar el último comando reconocido en pantalla
- **Ejecución concurrente**: Manejo simultáneo de múltiples entradas

---

## 📊 Resultados Visuales

**Interfaz Multimodal en Funcionamiento:**
- Ventana de cámara mostrando detección de gestos de mano
- Interfaz gráfica con círculo que responde a comandos
- Texto mostrando el último comando de voz reconocido

**Comandos Implementados:**
- "cambiar" + mano abierta → Cambio de color a azul
- "rojo" + mano abierta → Cambio de color a rojo
- "verde" + mano abierta → Cambio de color a verde
- "mover" + dos dedos → Movimiento del objeto
- "ocultar" + dos dedos → Ocultar objeto
- "mostrar" + dos dedos → Mostrar objeto

---

## 💬 Reflexión Final

Las interfaces multimodales representan el futuro de la interacción humano-computadora, permitiendo formas más naturales e intuitivas de controlar aplicaciones. Este taller demuestra cómo combinar múltiples modalidades de entrada (voz y gestos) para crear experiencias de usuario ricas y versátiles.

Los principales desafíos incluyen la sincronización entre diferentes modalidades, el manejo de ruido en el reconocimiento de voz, la precisión en la detección de gestos, y la programación concurrente para manejar múltiples entradas simultáneamente. Sin embargo, las bibliotecas modernas como MediaPipe y SpeechRecognition facilitan significativamente la implementación de estas tecnologías.

Las aplicaciones potenciales incluyen interfaces de realidad aumentada, control de presentaciones, sistemas de domótica, asistentes virtuales avanzados, y aplicaciones de accesibilidad para usuarios con diferentes capacidades motoras.