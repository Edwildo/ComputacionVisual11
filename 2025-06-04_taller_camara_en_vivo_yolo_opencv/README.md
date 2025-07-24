# 🧪 Taller 48 - Detección de Objetos en Tiempo Real con YOLO y Webcam


📅 Fecha  

2025-06-04 – Fecha de asignación

2025-06-15 – Fecha de realización

2025-06-24 – Fecha de entrega


----------

### 🔍 Objetivo del taller

Conectar la cámara web del PC y procesar el video en tiempo real utilizando **Python, OpenCV y YOLO** para aplicar filtros visuales y realizar detección de objetos en vivo.  
Este taller combina técnicas de visión artificial clásica con modelos de detección basados en aprendizaje profundo.

----------

### 🔹 Actividades por entorno

Este taller se realiza **exclusivamente en Python (local)**, utilizando `opencv-python` y un modelo preentrenado de YOLO (por ejemplo, **YOLOv5 o YOLOv8** de `ultralytics`) o `cv2.dnn`.

----------

## 💻 Python (Ejecución local con webcam)

**Herramientas necesarias:**

-   opencv-python
    
-   numpy
    
-   ultralytics (o) cvlib (o) cv2.dnn (según la versión de YOLO usada)
    

----------

**Pasos a implementar:**

-   Capturar video en tiempo real con `cv2.VideoCapture(0)`.
    
-   Leer frame por frame en un bucle.
    
-   Aplicar filtros básicos:
    
    -   Escala de grises (`cv2.cvtColor`)
        
    -   Binarización (`cv2.threshold`)
        
    -   Detección de bordes (`cv2.Canny`)
        
-   Integrar **YOLO** para detección de objetos:
    
    -   Utilizar **YOLOv5** o **YOLOv8** con `ultralytics` o `cv2.dnn`.
        
    -   Dibujar cajas junto con nombre de la clase y la confianza.
        

----------

## 🔹 Fragmento de código relevante:

```python
# Loop principal
filter_option = 0
running = True

  

while  running:
	ret, frame = cap.read()
	if  not  ret:
		print("Error: no se pudo leer el fotograma.")
		break
		
	# Aplicar filtro
	filtro = aplicar_filtros(frame.copy(), filter_option)
	# Realizar detección de objetos
	resultados = model(frame)
	detections = resultados[0]
	  
	# dibujar detecciones en el frame original
	deteccion = detections.plot()

	#Mostrar varias ventanas
	cv2.imshow("Original con deteccion", deteccion)
	cv2.imshow("Filtro Aplicado", filtro)

	# Control con teclado
	key = cv2.waitKey(1) & 0xFF
	if  key == ord('q'): # presiona q para salir
	running = False
	elif  key == ord('f'): # f para cambiar de filtro
	filter_option = (filter_option + 1) % 4
	elif  key == ord('s'): # guardar captura
	cv2.imwrite("captura.jpg", deteccion)
	print("Captura guardada.")


cap.release()
cv2.destroyAllWindows()
```

🧩 Prompts Usados

- _Refactoriza este código "...."_
-  "Mejora la redacción de estos parrafos: "..".


----------

## 📚 Entrega
```
2025-06-04_taller_camara_en_vivo_yolo_opencv/
 └── python/
 └── resultados/
 └── README.md 
```

### 🧩 Prompts Usados

- _Refactoriza este código "...."_
-  "Mejora la redacción de estos parrafos: "..".

----------




## 💬 Reflexión Final

En el taller, implementar la detección de objetos en vivo junto con el procesamiento de imágenes en tiempo real fue una experiencia muy enriquecedora.
Combinamos tanto técnicas de visión artificial clásica —como la aplicación de filtros en escala de grises y detección de bordes— con el poder de los modelos de detección basados en aprendizaje profundo (YOLO).

Durante las pruebas, el modelo fue capaz de detectar con seguridad algunos de los objetos presentes en el lugar, como personas, botellas o sillas, dibujándoles un marco junto con el nombre de la clase y el puntaje de confianza. Esto proporciona una aplicación práctica muy útil en el análisis de video en entornos dinámicos.

Sin embargo, también aparecieron algunos retos, como detecciones erróneas o poca estabilidad en algunos fotogramas, que muestran que el modelo puede confundir determinados grupos de píxeles, o que el rendimiento puede descender en entornos con poca luz o muchos movimientos. Esto pone en evidencia que el modelo tiene limitaciones y que el resultado final puede optimizarse aumentando el conjunto de datos de entrenamiento, modificando los umbrales de detección, o aumentando la resolución de la cámara.

----------

## 🛠 Criterios de evaluación

✅ Captura funcional desde la cámara web en tiempo real.  
✅ Aplicación de al menos **2 filtros** junto con detección de objetos con **YOLO**.  
✅ Ventanas sincronizadas mostrando cada resultado.  
✅ Visualización adecuada de cajas, nombre de clases y confianza.  
✅ Código funcional, modular y adecuadamente comentado.  
✅ `README.md` completo, con explicación, evidencias visuales (GIF) y prompts.  
✅ Commits descriptivos en Inglés.
