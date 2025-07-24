    # 🧠 Mini-Sistema de Monitoreo Inteligente con Visión Artificial

## 🎯 Descripción general

Este sistema permite monitorear en tiempo real lo que ocurre frente a la cámara usando visión por computador. Se detectan personas con ayuda del modelo YOLOv5, se visualizan estadísticas en pantalla y se registran eventos automáticamente en archivos CSV y capturas de imagen.

### 🔍 ¿Cómo funciona?

- Se activa la cámara y se analiza el video en tiempo real.
- Se usa el modelo `YOLOv5n` de la librería `ultralytics` para detectar objetos.
- Si se detecta una persona:
  - Se guarda una captura de la imagen con timestamp.
  - Se escribe un log en formato CSV con los datos del evento (hora, clase detectada, confianza).
- Se muestra un panel con:
  - Conteo en tiempo real de personas detectadas.
  - Estado del sistema (Inactivo / Detectando).

---

## 📦 Estructura del proyecto

2025-06-24_taller_sistema_monitoreo_inteligente_vision_dashboard/
├── python/
│ ├── monitoreo_panel.py # Script principal
│ └── yolov5n.pt # Modelo YOLOv5n (si no se descarga solo)
├── capturas/ # Capturas de personas detectadas
├── logs/
│ └── eventos.csv # Registros de eventos detectados
├── README.md # Este archivo

📊 Visualización

✅ Ventana en tiempo real con las detecciones.

✅ Contador de personas detectadas.

✅ Registro en tiempo real (archivo eventos.csv).

📁 Evidencias (GIFs)

🎥 GIF del monitoreo en tiempo real con boxes.

![Monitoreo en vivo](0624-ezgif.com-video-to-gif-converter.gif)



🤔 Reflexión final
Este sistema cumple con lo esencial de un sistema de vigilancia: detección, visualización y registro automático. Para hacerlo más robusto se podrían integrar:

-Detección de múltiples clases con acciones diferentes.

-Panel gráfico más avanzado con Dash o Tkinter.

-Notificaciones automáticas por correo o sonido.

-Implementación remota (dashboard web o servidor Flask).

🤖 Prompts usados
“Crear script de detección de personas con YOLOv5 y guardar logs y capturas.”

“Mostrar contador en vivo y generar archivo CSV.”

“Adaptar código para entrega del taller con estructura de carpetas específica.”

yaml
Copiar
Editar

---

## ✅ `.gitignore`

```gitignore
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
*.DS_Store

# Entornos virtuales
venv/
.env/

# Archivos de log
*.log

# Capturas generadas
capturas/