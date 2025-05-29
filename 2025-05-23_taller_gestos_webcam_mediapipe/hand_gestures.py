import cv2
import numpy as np
import mediapipe as mp

# Inicialización de MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

# Umbrales de gestos
DIST_THRESHOLD = 0.05  # Ejemplo: distancia relativa mínima

# Función para contar dedos extendidos
FINGER_TIPS = [mp_hands.HandLandmark.INDEX_FINGER_TIP,
               mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
               mp_hands.HandLandmark.RING_FINGER_TIP,
               mp_hands.HandLandmark.PINKY_TIP]
FINGER_DIP = [mp_hands.HandLandmark.INDEX_FINGER_DIP,
             mp_hands.HandLandmark.MIDDLE_FINGER_DIP,
             mp_hands.HandLandmark.RING_FINGER_DIP,
             mp_hands.HandLandmark.PINKY_DIP]
THUMB_TIP = mp_hands.HandLandmark.THUMB_TIP
THUMB_IP = mp_hands.HandLandmark.THUMB_IP


def count_extended_fingers(hand_landmarks):
    """
    Cuenta cuántos dedos (excepto pulgar) están extendidos comparando la punta vs la articulación DIP.
    """
    count = 0
    for tip, dip in zip(FINGER_TIPS, FINGER_DIP):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[dip].y:
            count += 1
    # Pulgar (eje x para mano derecha)
    if hand_landmarks.landmark[THUMB_TIP].x > hand_landmarks.landmark[THUMB_IP].x:
        count += 1
    return count


def calc_thumb_index_distance(hand_landmarks):
    """
    Calcula la distancia euclidiana normalizada entre pulgar y dedo índice.
    """
    thumb = hand_landmarks.landmark[THUMB_TIP]
    index = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    dx = thumb.x - index.x
    dy = thumb.y - index.y
    return np.sqrt(dx*dx + dy*dy)


def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: No se puede abrir la cámara")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Voltear para espejo
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        # Procesar con MediaPipe
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        background = frame.copy()
        color = (0, 0, 0)

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Conteo de dedos
            fingers = count_extended_fingers(hand_landmarks)
            # Distancia pulgar-índice
            dist = calc_thumb_index_distance(hand_landmarks)

            # Acciones visuales
            if fingers == 5:
                color = (0, 255, 0)  # fondo verde
            elif dist < DIST_THRESHOLD:
                cv2.circle(frame, (int(w/2), int(h/2)), 50, (0, 0, 255), -1)
            else:
                color = (255, 255, 255)

        # Aplicar fondo
        overlay = np.full((h, w, 3), color, dtype=np.uint8)
        frame = cv2.addWeighted(overlay, 0.3, frame, 0.7, 0)

        cv2.imshow('Gestos WebCam', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
