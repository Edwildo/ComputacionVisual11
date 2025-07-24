import cv2
from ultralytics import YOLO
import os
from datetime import datetime
import pandas as pd
import tkinter as tk
from PIL import Image, ImageTk

# Crear carpetas
os.makedirs("../capturas", exist_ok=True)
os.makedirs("../logs", exist_ok=True)

# Cargar modelo
model = YOLO("yolov5n.pt")

# CSV log
log_path = "../logs/eventos.csv"
if not os.path.exists(log_path):
    with open(log_path, "w") as f:
        f.write("timestamp,evento,clase,confianza\n")

# Panel tkinter
root = tk.Tk()
root.title("Panel de Monitoreo Inteligente")

video_label = tk.Label(root)
video_label.pack()

estado_label = tk.Label(root, text="Estado: Inactivo", font=("Arial", 14))
estado_label.pack()

conteo_label = tk.Label(root, text="Personas detectadas: 0", font=("Arial", 14))
conteo_label.pack()

cap = cv2.VideoCapture(0)

def actualizar_frame():
    ret, frame = cap.read()
    if not ret:
        return

    detecciones = model(frame)[0]
    personas = 0

    for r in detecciones.boxes:
        cls_id = int(r.cls)
        conf = float(r.conf)
        label = model.names[cls_id]

        if label == 'person' and conf > 0.5:
            personas += 1
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            img_path = f"../capturas/captura_{timestamp}.jpg"
            cv2.imwrite(img_path, frame)
            with open(log_path, "a") as f:
                f.write(f"{timestamp},Persona detectada,{label},{conf:.2f}\n")

        # Dibujar cajas
        xyxy = r.xyxy[0].cpu().numpy().astype(int)
        cv2.rectangle(frame, (xyxy[0], xyxy[1]), (xyxy[2], xyxy[3]), (0, 255, 0), 2)
        cv2.putText(frame, f"{label} {conf:.2f}", (xyxy[0], xyxy[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Actualizar UI
    estado = "ALERTA" if personas > 0 else "Inactivo"
    estado_label.config(text=f"Estado: {estado}")
    conteo_label.config(text=f"Personas detectadas: {personas}")

    # Mostrar imagen en panel
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(rgb_frame)
    imgtk = ImageTk.PhotoImage(image=img)
    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)

    root.after(100, actualizar_frame)

def cerrar():
    cap.release()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", cerrar)
actualizar_frame()
root.mainloop()
