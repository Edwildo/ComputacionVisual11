# main.py

import cv2
import numpy as np
from ultralytics import YOLO

def main():
    # Cargar modelo YOLO (YOLOv8)
    model = YOLO('yolov8n.pt')  # o 'yolov5s.pt'

    # Iniciar captura de la webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: no se pudo abrir la cámara.")
        return

    # Modo de filtro: 0=original, 1=gris, 2=binary, 3=canny
    filter_mode = 0
    paused = False

    while True:
        if not paused:
            ret, frame = cap.read()
            if not ret:
                print("Error: no se recibió frame.")
                break

            # Filtros clásicos
            gray   = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            edges  = cv2.Canny(gray, 100, 200)

            # Detección con YOLO
            det_frame = frame.copy()
            results = model(frame)
            detections = 0
            for r in results:
                for box in r.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    conf = box.conf[0]
                    cls  = int(box.cls[0])
                    label = r.names[cls]
                    # Dibujar caja y etiqueta
                    cv2.rectangle(det_frame, (x1, y1), (x2, y2), (0,255,0), 2)
                    cv2.putText(det_frame, f"{label} {conf:.2f}",
                                (x1, y1-10),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.6, (0,255,0), 2)
                    detections += 1

            # Selección del frame a mostrar según filtro
            if filter_mode == 0:
                display = frame
            elif filter_mode == 1:
                display = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            elif filter_mode == 2:
                display = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
            else:
                display = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

            # Mostrar contadores en el frame de detección
            cv2.putText(det_frame, f"Detecciones: {detections}",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                        1.0, (0, 255, 0), 2)

            # Mostrar ventanas
            cv2.imshow('Original / Filtro', display)
            cv2.imshow('Detección YOLO', det_frame)

        # Lectura de tecla
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('p'):
            paused = not paused
        elif key in (ord('0'), ord('1'), ord('2'), ord('3')):
            filter_mode = int(chr(key))
        elif key == ord('s'):
            cv2.imwrite('captura.png', display)
            print("Imagen guardada como captura.png")
        elif key == ord('v'):
            # Grabar 5 segundos de vídeo
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter('clip.avi', fourcc, 20.0,
                                  (frame.shape[1], frame.shape[0]))
            print("Grabando video clip.avi...")
            for _ in range(100):  # ~5 segundos a 20 FPS
                ret2, f2 = cap.read()
                if not ret2:
                    break
                out.write(f2)
            out.release()
            print("Grabación finalizada.")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()