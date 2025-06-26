import cv2
import mediapipe as mp
import speech_recognition as sr
import numpy as np

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Inicializar el reconocimiento de voz
recognizer = sr.Recognizer()

# Configurar la webcam
cap = cv2.VideoCapture(0)

# Variables
brush_color = (0, 0, 255)  # Color inicial: rojo
brush_size = 10  # Tamaño del pincel
canvas = np.ones((600, 800, 3), dtype=np.uint8) * 255  # Lienzo blanco

# Función para escuchar comandos de voz
def listen_for_commands():
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            print("Comando de voz:", command)
            return command
        except sr.UnknownValueError:
            return None

# Función para detectar gestos de la mano
def detect_hand_gestures(frame):
    results = hands.process(frame)
    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)
            index_finger = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            return index_finger.x, index_finger.y
    return None, None

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)  # Voltear la imagen para que el usuario vea su reflejo
    h, w, _ = frame.shape
    x, y = detect_hand_gestures(frame)

    if x is not None and y is not None:
        x, y = int(x * w), int(y * h)
        cv2.circle(frame, (x, y), brush_size, brush_color, -1)
        canvas[y - brush_size:y + brush_size, x - brush_size:x + brush_size] = brush_color

    # Leer comando de voz
    command = listen_for_commands()
    if command:
        if "rojo" in command:
            brush_color = (0, 0, 255)  # Rojo
        elif "verde" in command:
            brush_color = (0, 255, 0)  # Verde
        elif "pincel" in command:
            brush_size = 10  # Tamaño de pincel normal
        elif "limpiar" in command:
            canvas.fill(255)  # Limpiar el lienzo
        elif "guardar" in command:
            cv2.imwrite('obra.png', canvas)  # Guardar la imagen

    # Mostrar el lienzo y la cámara
    cv2.imshow('Lienzo Digital', canvas)
    cv2.imshow('Cámara', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
