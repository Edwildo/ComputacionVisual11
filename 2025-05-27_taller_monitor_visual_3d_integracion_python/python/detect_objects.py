import cv2
from ultralytics import YOLO
import socket, json

# 1. Carga modelo YOLO
model = YOLO('yolov8n.pt')

# 2. Configura socket UDP destino
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 10000)

# 3. Abre cámara
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret: break

    # 4. Detección
    results = model(frame)
    detections = len(results.pandas().xywh)

    # 5. Envío JSON
    msg = json.dumps({'detections': detections})
    sock.sendto(msg.encode(), server_address)

    # 6. Muestra video
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()
