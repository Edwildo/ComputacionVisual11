# Real-Time Plotting with Optional Object Detection and Simulated Temperature

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time
import csv
import cv2
from ultralytics import YOLO

# Carga el modelo de detección
model = YOLO("yolov8n.pt")  # Asegúrate de tener el modelo downloaded


# 0 = modo simulado, 1 = modo detección, 2 = modo temperatura
modo = 0

# Listas para guardar los datos
datos = []

# CSV opcional
with open("resultados.csv", "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['indice', 'valor'])

# Capture de video opcional
cap = cv2.VideoCapture(0)


def update(frame):
    """Función que se llama en cada frame de la animación.""" 
    global modo, datos, text

    inicio = time.time()

    if modo == 0:
        # Simulamos nuevos datos
        nuevo_dato = np.random.randint(0, 20) # Dato aleatorio entre 0 y 20 para simular datos
        modo_text = "Dato aleatorio"

    elif modo == 1:
        # Detectamos con YOLO el número de personas en el frame de la cámara
        ret, video_frame = cap.read()
        if not ret:
            print("Error: no se pudo leer el fotograma.")
            nuevo_dato = 0
        else:
            resultados = model(video_frame)
            detections = resultados[0]
            # Filtramos solamente detecciones de Persona
            nuevo_dato = sum(1 for box in detections.boxes if int(box.cls.item()) == 0)  # 0 = person

            # También podemos mostrar el video en una ventana aparte
            annotated = resultados[0].plot()
            cv2.imshow("Camara - deteccion de personas", annotated)
            if cv2.waitKey(1) == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return line, text

        modo_text = "Detectar número de personas"

    elif modo == 2:
        nuevo_dato = np.sin(time.time())  # Temperatura simulated
        modo_text = "Temperatura (sin)"

    # Agregar nuevo dato
    datos.append(nuevo_dato)

    # Actualizamos gráfica
    line.set_data(range(len(datos)), datos)
    ax.relim()
    ax.autoscale_view()

    # También podemos guardar CSV opcional
    with open("resultados.csv", "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([len(datos), nuevo_dato])

    # Medir FPS sin division por cero
    fin = time.time()
    duracion = fin - inicio
    fps = 1.0 / (duracion + 1e-6)
    fps_text = f"FPS: {fps:.2f}"

    # Actualizamos texto
    text.set_text(f'{fps_text}\nValor actual: {nuevo_dato}\nModo: {modo_text}')

    return line, text


def key_event(event):
    """Función que se llama cuando el usuario presiona una tecla en el teclado de la gráfica.""" 
    global modo
    if event.key == "f":
        modo = (modo + 1) % 3
        print(f"Cambiado el modo a: {modo}")


# Creamos la gráfica
fig, ax = plt.subplots()
ax.set_xlabel("Valor")
ax.set_ylabel("Conteo")
ax.grid()

line, = ax.plot([], [], color='blue')

# Creamos el texto que se va actualizando
text = ax.text(0.05, 0.95, '',
               transform=ax.transAxes, bbox=dict(boxstyle='round', facecolor='yellow'), verticalalignment='top')

# Animamr
ani = animation.FuncAnimation(fig, update, interval=500, blit=False)
fig.canvas.mpl_connect("key_press_event", key_event)
plt.show()


# Cierre de la cámara
if cap.isOpened():
    cap.release()
    print("Cámara liberada.")
cv2.destroyAllWindows()
print("Ventanas cerradas.")

# Guardamos la gráfica como PNG
output_file = "grafica.png"
fig.savefig(output_file)
print(f"Grafica guardada en {output_file}.")