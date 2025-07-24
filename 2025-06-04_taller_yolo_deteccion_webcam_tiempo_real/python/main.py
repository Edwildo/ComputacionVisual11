# Real-time Object Detection with YOLOv8 and OpenCV
import cv2  # Se usa OpenCV para la captura de video y visualización
import time  # Se usa time para calcular el FPS
from ultralytics import YOLO  # Se usa la librería ultralytics para cargar el modelo YOLOv8

# Carga el modelo (YOLOv8n)
model = YOLO("yolov8n.pt")

# Filtra opcionalmente según las clases que deseas detectar
filter_labels = [None, "person", "cat", "cell phone"]

# Inicializa la captura de video
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: no se pudo acceder a la cámara.")
    cap.release()
    exit(1)

print("Presiona 'q' para salir")
print("Presiona 'f' para cambiar el modo de filtrado")

# Filtrado activado o desactivado
filter_index = 0

# Almacena histórico de FPS
fps_vals = []

# Loop principal
try:
    while True:
        inicio = time.time()
        ret, frame = cap.read()
        if not ret:
            print("Error: no se pudo leer el fotograma.")
            break

        # Realiza detección de objetos en el fotograma
        resultados = model.predict(source=frame, stream=False)
        detections = resultados[0]

        # Filtra según el modo vigente
        if filter_labels[filter_index] is not None:
            filter_name = filter_labels[filter_index]
            filtered_boxes = []
            for box in detections.boxes:
                class_id = int(box.cls.item())  # el id de la detección
                class_name = model.names[class_id]  # nombre de la detección
                if class_name == filter_name:
                    filtered_boxes.append(box)
            detections.boxes = filtered_boxes

        # Dibuja las detecciones en el fotograma
        annotated = detections.plot()

        # Calcula el FPS
        fin = time.time()
        fps = 1.0 / (fin - inicio)
        fps_vals.append(fps)
        if len(fps_vals) > 50:
            fps_vals.pop(0)

        fps_text = f"FPS: {fps:.2f}"

        # Muestra el número de FPS en la parte superior izquierda
        color = (0, 255, 0) if filter_index == 0 else (0, 0, 255)
        cv2.putText(annotated, fps_text, (20, 60),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1, color=color, thickness=2)

        # Muestra el modo de filtrado
        modo = filter_labels[filter_index]
        modo_txt = f"Filtro: {modo or 'Sin Filtro'}"

        cv2.putText(annotated, modo_txt, (20, 30),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1, color=color, thickness=2)

        # --- Dibujar gráfica de los FPS --- 
        graph_height = 100
        graph_width = 200
        graph_background_color = (50, 50, 50)
        base = annotated.copy()

        
        # Dibuja el fondo de la gráfica
        cv2.rectangle(base, (base.shape[1] - graph_width - 10, base.shape[0] - graph_height - 10),
                       (base.shape[1] - 10, base.shape[0] - 10),
                       graph_background_color, -1)

        if len(fps_vals) > 1:
            max_fps = max(fps_vals)
            min_fps = min(fps_vals)
            range_fps = max_fps - min_fps if max_fps - min_fps > 0 else 1
            for i in range(1, len(fps_vals)):
                x1 = base.shape[1] - graph_width - 10 + (i - 1) * (graph_width // len(fps_vals))
                y1 = base.shape[0] - 10 - int((fps_vals[i - 1] - min_fps) * graph_height / range_fps)
                x2 = base.shape[1] - graph_width - 10 + i * (graph_width // len(fps_vals))
                y2 = base.shape[0] - 10 - int((fps_vals[i] - min_fps) * graph_height / range_fps)
                color = (0, 255, 0)
                cv2.line(base, (x1, y1), (x2, y2), color, 2)

        # Muestra el resultado
        cv2.imshow("Deteccion en Tiempo Real", base)

        # Control con teclado
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):  # presiona q para salir
            break
        elif key == ord('f'):  # f para cambiar el filtro
            filter_index = (filter_index + 1) % len(filter_labels)
            print(f"Filtro cambiado a: {filter_labels[filter_index] or 'Sin Filtro'}")

finally:
    cap.release()
    cv2.destroyAllWindows()
