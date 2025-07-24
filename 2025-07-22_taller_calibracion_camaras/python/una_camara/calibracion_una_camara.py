#!/usr/bin/env python3
"""
Calibración de una cámara usando patrón de tablero de ajedrez
Detecta esquinas del patrón y calcula parámetros intrínsecos de la cámara
"""

import cv2
import numpy as np
import glob
import os
import json

class CalibradorCamara:
    def __init__(self, patron_size=(9, 6), tam_cuadrado=1.0):
        """
        Inicializa el calibrador
        patron_size: tupla (ancho, alto) del patrón en esquinas internas
        tam_cuadrado: tamaño del cuadrado en unidades del mundo real
        """
        self.patron_size = patron_size
        self.tam_cuadrado = tam_cuadrado
        
        # Preparar puntos del mundo real del patrón
        self.objp = np.zeros((patron_size[0] * patron_size[1], 3), np.float32)
        self.objp[:, :2] = np.mgrid[0:patron_size[0], 0:patron_size[1]].T.reshape(-1, 2)
        self.objp *= tam_cuadrado
        
        # Arrays para almacenar puntos del objeto y puntos de imagen
        self.objpoints = []  # Puntos 3D en el mundo real
        self.imgpoints = []  # Puntos 2D en el plano de imagen
        
    def capturar_imagenes_webcam(self, num_imagenes=20, carpeta_salida="../imagenes"):
        """
        Captura imágenes desde la webcam para calibración
        """
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Error: No se pudo abrir la cámara")
            return False
            
        os.makedirs(carpeta_salida, exist_ok=True)
        
        contador = 0
        print(f"Capturando {num_imagenes} imágenes. Presiona ESPACIO para capturar, ESC para salir")
        
        while contador < num_imagenes:
            ret, frame = cap.read()
            if not ret:
                break
                
            # Mostrar frame con instrucciones
            cv2.putText(frame, f"Imagenes: {contador}/{num_imagenes}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, "ESPACIO: Capturar | ESC: Salir", 
                       (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            cv2.imshow('Captura de Calibracion', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC
                break
            elif key == 32:  # ESPACIO
                filename = os.path.join(carpeta_salida, f"calibracion_{contador:02d}.jpg")
                cv2.imwrite(filename, frame)
                print(f"Imagen guardada: {filename}")
                contador += 1
                
        cap.release()
        cv2.destroyAllWindows()
        return contador > 0
        
    def detectar_esquinas(self, ruta_imagenes="../imagenes/*.jpg"):
        """
        Detecta esquinas del patrón en las imágenes
        """
        imagenes = glob.glob(ruta_imagenes)
        
        if not imagenes:
            print(f"No se encontraron imágenes en: {ruta_imagenes}")
            return False
            
        print(f"Procesando {len(imagenes)} imágenes...")
        
        for i, fname in enumerate(imagenes):
            img = cv2.imread(fname)
            if img is None:
                continue
                
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Encontrar esquinas del tablero de ajedrez
            ret, corners = cv2.findChessboardCorners(gray, self.patron_size, None)
            
            # Si se encuentran esquinas, añadir puntos del objeto y de imagen
            if ret:
                self.objpoints.append(self.objp)
                
                # Refinar coordenadas de esquinas
                criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
                corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
                self.imgpoints.append(corners2)
                
                # Dibujar y mostrar esquinas
                cv2.drawChessboardCorners(img, self.patron_size, corners2, ret)
                
                # Guardar imagen con esquinas detectadas
                output_path = f"../resultados/esquinas_detectadas_{i:02d}.jpg"
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                cv2.imwrite(output_path, img)
                
                print(f"Esquinas detectadas en: {os.path.basename(fname)}")
            else:
                print(f"No se detectaron esquinas en: {os.path.basename(fname)}")
                
        print(f"Total de imágenes válidas para calibración: {len(self.objpoints)}")
        return len(self.objpoints) > 0
        
    def calibrar_camara(self):
        """
        Realiza la calibración de la cámara
        """
        if len(self.objpoints) == 0:
            print("Error: No hay puntos para calibración")
            return None
            
        # Obtener tamaño de imagen
        img = cv2.imread(glob.glob("../imagenes/*.jpg")[0])
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_size = gray.shape[::-1]
        
        print("Realizando calibración...")
        
        # Calibrar cámara
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
            self.objpoints, self.imgpoints, img_size, None, None)
        
        if ret:
            print(f"Calibración exitosa! Error de reproyección: {ret:.4f}")
            
            # Guardar parámetros de calibración
            calibracion_data = {
                'matriz_camara': mtx.tolist(),
                'coeficientes_distorsion': dist.tolist(),
                'error_reproyeccion': float(ret),
                'tamaño_imagen': img_size,
                'patron_usado': self.patron_size,
                'imagenes_usadas': len(self.objpoints)
            }
            
            with open('../resultados/calibracion_camara.json', 'w') as f:
                json.dump(calibracion_data, f, indent=2)
                
            return mtx, dist, rvecs, tvecs
        else:
            print("Error en la calibración")
            return None
            
    def validar_calibracion(self, mtx, dist):
        """
        Valida la calibración mediante reproyección
        """
        print("Validando calibración...")
        
        total_error = 0
        for i in range(len(self.objpoints)):
            # Reproyectar puntos
            imgpoints2, _ = cv2.projectPoints(
                self.objpoints[i], None, None, mtx, dist)
            
            # Calcular error
            error = cv2.norm(self.imgpoints[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
            total_error += error
            
        error_medio = total_error / len(self.objpoints)
        print(f"Error medio de reproyección: {error_medio:.4f} píxeles")
        
        # Crear imagen de validación
        img = cv2.imread(glob.glob("../imagenes/*.jpg")[0])
        h, w = img.shape[:2]
        
        # Obtener matriz de cámara optimizada
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
        
        # Corregir distorsión
        dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
        
        # Recortar imagen
        x, y, w_roi, h_roi = roi
        dst = dst[y:y+h_roi, x:x+w_roi]
        
        # Guardar comparación
        comparison = np.hstack((img, cv2.resize(dst, (img.shape[1], img.shape[0]))))
        cv2.imwrite('../resultados/comparacion_distorsion.jpg', comparison)
        
        print("Validación completada. Imágenes guardadas en ../resultados/")
        
    def mostrar_parametros(self, mtx, dist):
        """
        Muestra los parámetros de calibración de forma legible
        """
        print("\n" + "="*50)
        print("PARÁMETROS DE CALIBRACIÓN")
        print("="*50)
        
        print(f"Distancia focal X: {mtx[0,0]:.2f} píxeles")
        print(f"Distancia focal Y: {mtx[1,1]:.2f} píxeles")
        print(f"Centro óptico X: {mtx[0,2]:.2f} píxeles")
        print(f"Centro óptico Y: {mtx[1,2]:.2f} píxeles")
        
        print(f"\nCoeficientes de distorsión:")
        print(f"k1: {dist[0,0]:.6f}")
        print(f"k2: {dist[0,1]:.6f}")
        print(f"p1: {dist[0,2]:.6f}")
        print(f"p2: {dist[0,3]:.6f}")
        print(f"k3: {dist[0,4]:.6f}")
        
        print("="*50)


def main():
    """
    Función principal para ejecutar la calibración
    """
    # Crear calibrador (9x6 esquinas internas, cuadrados de 2.5cm)
    calibrador = CalibradorCamara(patron_size=(9, 6), tam_cuadrado=2.5)
    
    print("Calibración de Cámara - Taller 68")
    print("="*40)
    
    # Opción 1: Capturar imágenes desde webcam
    print("\n1. Capturar imágenes desde webcam")
    respuesta = input("¿Desea capturar nuevas imágenes? (s/n): ")
    
    if respuesta.lower() in ['s', 'si', 'sí', 'y', 'yes']:
        calibrador.capturar_imagenes_webcam(num_imagenes=15)
    
    # Opción 2: Usar imágenes existentes
    print("\n2. Detectar esquinas en imágenes")
    if calibrador.detectar_esquinas():
        
        # Opción 3: Calibrar
        print("\n3. Calibrar cámara")
        resultado = calibrador.calibrar_camara()
        
        if resultado:
            mtx, dist, rvecs, tvecs = resultado
            
            # Mostrar parámetros
            calibrador.mostrar_parametros(mtx, dist)
            
            # Validar calibración
            print("\n4. Validar calibración")
            calibrador.validar_calibracion(mtx, dist)
            
            print("\n✅ Calibración completada exitosamente!")
            print("Archivos generados en ../resultados/:")
            print("- calibracion_camara.json (parámetros)")
            print("- esquinas_detectadas_XX.jpg (detección)")
            print("- comparacion_distorsion.jpg (validación)")
            
        else:
            print("❌ Error en la calibración")
    else:
        print("❌ No se pudieron detectar esquinas en las imágenes")


if __name__ == "__main__":
    main()
