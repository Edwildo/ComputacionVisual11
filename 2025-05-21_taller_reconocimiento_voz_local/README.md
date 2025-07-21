# 🧪 Taller Reconocimiento de Voz Local e Interacción Visual

## 📅 Fecha
`2025-05-21`    

---

## 🎯 Objetivo del Taller

Explorar el reconocimiento de voz local en Python y su integración con visualizaciones interactivas en tiempo real usando Pygame. El taller muestra cómo mapear comandos de voz a acciones visuales, permitiendo el control por voz de una interfaz gráfica local sin depender de servicios en la nube.

---

## 🧠 Conceptos Aprendidos

- Uso de la librería `speech_recognition` para reconocimiento de voz offline (Sphinx)
- Manejo de micrófono y captura de audio en Python
- Diccionario de comandos y mapeo a acciones visuales
- Integración de reconocimiento de voz y visualización con Pygame
- Control de animaciones y colores mediante comandos hablados
- Manejo de hilos para separar la escucha de voz y la visualización

---

## 🔧 Herramientas y Entornos

- Python 3.12+
- speech_recognition
- PyAudio (para acceso al micrófono)
- Pygame para visualización
- Jupyter Notebook para experimentación

---

## 📁 Estructura del Proyecto

```
2025-05-21_taller_reconocimiento_voz_local/
├── python/
│   └── reconocimiento.ipynb
├── README.md
```

---

## 🧪 Implementación

### 🔹 Etapas realizadas
1. Instalación y prueba de `speech_recognition` y `PyAudio` para reconocimiento de voz local.
2. Definición de un diccionario de comandos y sus acciones asociadas.
3. Implementación de una función para escuchar y reconocer comandos usando Sphinx.
4. Integración con Pygame para visualizar y modificar elementos gráficos según el comando recibido.
5. Uso de hilos para mantener la visualización y el reconocimiento de voz funcionando simultáneamente.

### 🔹 Código relevante

**Reconocimiento de voz local**
```python
import speech_recognition as sr

def reconocer_comando():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Habla ahora...")
        audio = r.listen(source)
    try:
        texto = r.recognize_sphinx(audio, language="es-ES")
        print(f"Comando reconocido: {texto}")
        return texto.lower()
    except sr.UnknownValueError:
        print("No se entendió el audio.")
        return ""
    except sr.RequestError as e:
        print(f"Error con Sphinx: {e}")
        return ""
```

**Diccionario de comandos**
```python
comandos = {
    "rojo": "color_rojo",
    "azul": "color_azul",
    "girar": "accion_girar",
    "iniciar": "accion_iniciar",
    "detener": "accion_detener"
}
```

**Visualización y actualización en Pygame**
```python
import pygame

color = (0, 200, 255)
angulo = 0

def actualizar_visualizacion(accion):
    global color, angulo
    if accion == "color_rojo":
        color = (255, 0, 0)
    elif accion == "color_azul":
        color = (0, 0, 255)
    elif accion == "accion_girar":
        angulo += 30
    elif accion == "accion_iniciar":
        print("Inicio...")
    elif accion == "accion_detener":
        print("Detenido.")

def loop_visual():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Visualización Pygame")
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((30, 30, 30))
        rotated_surface = pygame.transform.rotate(
            pygame.Surface((160, 160), pygame.SRCALPHA), angulo)
        pygame.draw.circle(rotated_surface, color, (80, 80), 80)
        screen.blit(rotated_surface, (240, 160))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
```

**Integración con hilos**
```python
import threading

if __name__ == "__main__":
    visual_thread = threading.Thread(target=loop_visual)
    visual_thread.start()

    while True:
        comando_voz = reconocer_comando()
        if comando_voz in comandos:
            accion = comandos[comando_voz]
            actualizar_visualizacion(accion)
```

---

## 📊 Resultados Visuales

- **Círculo cambia de color o gira según el comando de voz reconocido.**
- **La ventana de Pygame responde en tiempo real a los comandos hablados.**

---

## 💬 Reflexión Final

Este taller permitió experimentar con el reconocimiento de voz local y su integración directa con visualizaciones interactivas. El control por voz de interfaces gráficas abre posibilidades para accesibilidad, arte digital y prototipos de sistemas interactivos sin depender de servicios externos. El manejo de hilos y la sincronización entre audio y gráficos son aspectos clave para lograr una experiencia fluida.

---