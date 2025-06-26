# 🧪 Taller - Visualización de Datos en Tiempo Real: Gráficas en Movimiento

## 📅 Fecha
`2025-06-26`    

---

## 🎯 Objetivo del Taller

Capturar o simular datos (por ejemplo, conteo de objetos, coordenadas, temperatura, pulsos o señales artificiales) y visualizarlos en tiempo real mediante gráficos dinámicos. Se busca explorar cómo enlazar datos numéricos con representaciones gráficas actualizadas en vivo, útiles en monitoreo, visualización científica y dashboards.

---

## 🧠 Conceptos Aprendidos

- Visualización dinámica de datos en tiempo real.
- Uso de `matplotlib.animation.FuncAnimation` para gráficos animados.
- Visualización interactiva con `plotly` y sus callbacks.
- Generación y simulación de datos con `numpy`.
- Integración de datos reales (por ejemplo, desde YOLO) con gráficos en vivo.
- Exportación de resultados a CSV o imágenes.

---

## 🔧 Herramientas y Entornos

- Python (local o Colab)
- `matplotlib` y `numpy` para gráficos y manipulación de datos
- `plotly` para gráficos interactivos
- `opencv-python` (opcional para entrada desde video)
- `ultralytics` (opcional si se usa YOLO para conteo)

---

## 📁 Estructura del Proyecto

yyyy-mm-dd_taller_visualizacion_datos_tiempo_real_graficas/
├── python/
│ ├── main.py # Script principal con el código del taller
├── README.md # Documentación del taller

pgsql
Copiar

---

## 🧪 Implementación

### 🔹 Etapas realizadas

1. **Simulación de Datos**: Generación de datos artificiales para simular un comportamiento dinámico (por ejemplo, temperatura, conteo de objetos).
   
2. **Visualización con `matplotlib`**: Creación de gráficos dinámicos utilizando `FuncAnimation` para actualizar los datos en tiempo real.

   **Código relevante:**

   ```python
   import numpy as np
   import matplotlib.pyplot as plt
   from matplotlib.animation import FuncAnimation

   # Simulando datos
   time = np.linspace(0, 2 * np.pi, 128)
   data = np.sin(time)

   def update(frame):
       ydata.append(np.sin(frame))  # Simulando datos dinámicos
       xdata.append(frame)
       ln.set_data(xdata, ydata)
       return ln,

   fig, ax = plt.subplots()
   xdata, ydata = [], []
   ln, = plt.plot([], [], 'r-', animated=True)

   ax.set_xlim(0, 2 * np.pi)
   ax.set_ylim(-1, 1)

   ani = FuncAnimation(fig, update, frames=np.linspace(0, 2 * np.pi, 128),
                       blit=True, interval=50)
   plt.show()
Visualización con plotly: Uso de gráficos interactivos en Jupyter utilizando plotly.

Código relevante:

python
Copiar
import plotly.graph_objs as go
import numpy as np

time = np.linspace(0, 2 * np.pi, 128)
data = np.sin(time)

fig = go.Figure()
fig.add_trace(go.Scatter(x=time, y=data, mode='lines', name='Sine Wave'))
fig.update_layout(title="Gráfico en Movimiento",
                  xaxis_title="Tiempo",
                  yaxis_title="Valor")
fig.show()
Integración con YOLO (Opcional): Si se utiliza YOLO para contar objetos en video, los datos de conteo se pueden integrar en el gráfico.

Código relevante:

python
Copiar
from ultralytics import YOLO
import cv2

model = YOLO('yolov8n.pt')  # O 'yolov5s.pt'

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)  # Detección de objetos
    detections = len(results.pandas().xywh)  # Conteo de objetos

    # Simulación de datos de detección en tiempo real
    print(f"Objetos detectados: {detections}")
    cap.release()
    cv2.destroyAllWindows()
Exportación de Resultados: Exportar los datos o gráficos a archivos CSV o imágenes PNG para análisis posterior.

Código relevante:

python
Copiar
import pandas as pd

# Guardar datos en CSV
data_to_export = {'time': time, 'value': data}
df = pd.DataFrame(data_to_export)
df.to_csv('datos.csv', index=False)

# Guardar gráfico como imagen PNG
fig.savefig('grafico.png')
🔹 Código relevante
main.py
El script principal donde se implementa la captura de datos, su visualización y exportación:

python
Copiar
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd

# Simulando datos (ejemplo: coordenada Y de un objeto en movimiento)
time = np.linspace(0, 2 * np.pi, 128)
data = np.sin(time)

# Función para actualizar el gráfico en tiempo real
def update(frame):
    ydata.append(np.sin(frame))  # Simulando datos dinámicos
    xdata.append(frame)
    ln.set_data(xdata, ydata)
    return ln,

fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'r-', animated=True)

ax.set_xlim(0, 2 * np.pi)
ax.set_ylim(-1, 1)

ani = FuncAnimation(fig, update, frames=np.linspace(0, 2 * np.pi, 128),
                    blit=True, interval=50)
plt.show()

# Guardar los datos en CSV
data_to_export = {'time': time, 'value': data}
df = pd.DataFrame(data_to_export)
df.to_csv('datos.csv', index=False)

# Guardar gráfico como imagen PNG
fig.savefig('grafico.png')
📊 Resultados Visuales
Gráfico en Movimiento:
[Insertar GIF de gráfico en movimiento aquí]

[Insertar GIF de video fuente y gráfico aquí, si aplica]

💬 Reflexión Final
La visualización de datos en tiempo real es una herramienta poderosa para monitoreo y análisis de datos. Permite observar patrones dinámicos a medida que los datos cambian, lo que es invaluable en contextos de monitoreo en vivo o visualización científica.

Los principales retos incluyen la sincronización de la entrada de datos en tiempo real con la actualización del gráfico y la eficiencia en el manejo de grandes volúmenes de datos. Sin embargo, el uso de bibliotecas como matplotlib y plotly facilita la implementación de gráficos interactivos y atractivos.