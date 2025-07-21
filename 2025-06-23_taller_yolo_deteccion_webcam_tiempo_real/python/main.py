from ultralytics import YOLO
import cv2, time

# Cargar el modelo YOLO preentrenado
model = YOLO('yolov8n.pt')  # Puedes usar 'yolov5s.pt' si prefieres YOLOv5

# Abrir la cámara web
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    start_time = time.time()  # Medir el tiempo de inicio
    results = model.predict(source=frame, stream=True)  # Detección de objetos
    
    # Dibujar las detecciones sobre el frame
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Coordenadas de la caja
            conf = box.conf[0]  # Confianza
            label = result.names[int(box.cls[0])]  # Etiqueta
            
            # Dibujar la caja y la etiqueta
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    
    # Calcular FPS
    end_time = time.time()
    fps = 1 / (end_time - start_time)
    
    # Mostrar FPS en el frame
    cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # Mostrar el resultado
    cv2.imshow("Detección de Objetos en Vivo", frame)
    
    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
