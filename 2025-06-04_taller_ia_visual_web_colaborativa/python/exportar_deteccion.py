import cv2
import mediapipe as mp
import json
import os
from datetime import datetime

# ⚠️ NUEVAS RUTAS INTERNAS
input_image_path = 'resultados/persona.jpg'
output_folder = 'resultados'
os.makedirs(output_folder, exist_ok=True)

image_path = os.path.join(output_folder, 'deteccion.png')
json_path = os.path.join(output_folder, 'deteccion.json')

# Leer imagen
image = cv2.imread(input_image_path)
if image is None:
    print(f"❌ No se pudo cargar la imagen en '{input_image_path}'")
    exit()

# Inicializar MediaPipe
mp_face = mp.solutions.face_detection
face_detection = mp_face.FaceDetection(model_selection=0, min_detection_confidence=0.5)

# Procesar detección
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
results = face_detection.process(rgb)

# Datos a exportar
export_data = {
    "timestamp": datetime.now().isoformat(),
    "objects": []
}

# Dibujar detecciones y recolectar datos
if results.detections:
    for detection in results.detections:
        bbox = detection.location_data.relative_bounding_box
        ih, iw, _ = image.shape
        x = int(bbox.xmin * iw)
        y = int(bbox.ymin * ih)
        w = int(bbox.width * iw)
        h = int(bbox.height * ih)
        conf = float(detection.score[0])

        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        export_data["objects"].append({
            "class": "face",
            "confidence": round(conf, 2),
            "x": x,
            "y": y,
            "w": w,
            "h": h
        })

# Guardar resultados
cv2.imwrite(image_path, image)
with open(json_path, 'w') as f:
    json.dump(export_data, f, indent=2)

print("✅ Detección completada. Resultados guardados en 'resultados/'")
