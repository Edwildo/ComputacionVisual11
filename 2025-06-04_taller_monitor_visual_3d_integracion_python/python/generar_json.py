# python/deteccion_completa.py
import cv2
import json
import os
import time
import mediapipe as mp
from ultralytics import YOLO

# Ruta al archivo que Unity va a leer
base_dir = os.path.dirname(__file__)  # Ruta de la carpeta actual (python/)
unity_json_path = os.path.abspath(os.path.join(base_dir, "../unity/Assets/person_data.json"))

# Inicializar YOLO y MediaPipe
model = YOLO("yolov8n.pt")
mp_hands = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)

cap = cv2.VideoCapture(0)

def contar_dedos(mano_landmarks):
    dedos = [False, False, False, False, False]
    tips = [4, 8, 12, 16, 20]

    # Dedo pulgar
    if mano_landmarks.landmark[4].x < mano_landmarks.landmark[3].x:
        dedos[0] = True

    # Otros dedos
    for i, tip in enumerate(tips[1:], start=1):
        if mano_landmarks.landmark[tip].y < mano_landmarks.landmark[tip - 2].y:
            dedos[i] = True

    return sum(dedos)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # YOLO detección de personas
    results = model(frame, verbose=False)[0]
    persons = [d for d in results.boxes.data.tolist() if int(d[5]) == 0]
    person_count = len(persons)

    # MediaPipe detección de manos
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    hand_result = mp_hands.process(frame_rgb)

    total_dedos = 0
    if hand_result.multi_hand_landmarks:
        for hand_landmarks in hand_result.multi_hand_landmarks:
            dedos = contar_dedos(hand_landmarks)
            total_dedos += dedos

    # Mostrar texto en pantalla
    texto = f"Personas: {person_count} | Dedos: {total_dedos}"
    cv2.putText(frame, texto, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    # Guardar los datos para Unity
    data = {
        "person_count": person_count,
        "finger_count": total_dedos,
        "frame_width": frame.shape[1],
        "frame_height": frame.shape[0]
    }

    os.makedirs(os.path.dirname(unity_json_path), exist_ok=True)
    with open(unity_json_path, "w") as f:
        json.dump(data, f)

    print(f"[JSON] {data}")
    cv2.imshow("Cam", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
