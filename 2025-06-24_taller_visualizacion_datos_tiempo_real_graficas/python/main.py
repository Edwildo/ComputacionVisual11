import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
from ultralytics import YOLO
import cv2

# 1. Simulando datos (ejemplo: coordenada Y de un objeto en movimiento)
time = np.linspace(0, 2 * np.pi, 128)
data = np.sin(time)

# 2. Configuración de la visualización con Matplotlib
fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'r-', animated=True)

# Definir los límites del gráfico
ax.set_xlim(0, 2 * np.pi)
ax.set_ylim(-1, 1)

# Función para actualizar el gráfico en tiempo real
def update(frame):
    ydata.append(np.sin(frame))  # Simulando datos dinámicos
    xdata.append(frame)
    ln.set_data(xdata, ydata)
    return ln,

# Crear la animación
ani = FuncAnimation(fig, update, frames=np.linspace(0, 2 * np.pi, 128),
                    blit=True, interval=50)

# Mostrar el gráfico
plt.show()

# 3. Exportar los datos a un archivo CSV
data_to_export = {'time': time, 'value': data}
df = pd.DataFrame(data_to_export)
df.to_csv('datos.csv', index=False)

# 4. Guardar el gráfico como una imagen PNG
fig.savefig('grafico.png')

# 5. Integración con YOLO para contar objetos (opcional)
model = YOLO('yolov8n.pt')  # O 'yolov5s.pt'

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)  # Detección de objetos
    detections = len(results.pandas().xywh)  # Conteo de objetos

    # Mostrar los objetos detectados en consola
    print(f"Objetos detectados: {detections}")

    # Opcional: Puedes visualizar el video con los resultados de detección
    # cv2.imshow('Video', frame)
    
    # Salir si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
