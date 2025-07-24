#!/usr/bin/env python3
"""
Calibración estéreo de dos cámaras usando patrón de tablero de ajedrez
Calcula la relación espacial entre dos cámaras para visión estéreo
"""

import cv2
import numpy as np
import glob
import os
import json

class CalibradorEstereo:
    def __init__(self, patron_size=(9, 6), tam_cuadrado=1.0):
        """
        Inicializa el calibrador estéreo
        """
        self.patron_size = patron_size
        self.tam_cuadrado = tam_cuadrado
        
        # Preparar puntos del mundo real del patrón
        self.objp = np.zeros((patron_size[0] * patron_size[1], 3), np.float32)
        self.objp[:, :2] = np.mgrid[0:patron_size[0], 0:patron_size[1]].T.reshape(-1, 2)
        self.objp *= tam_cuadrado
        
        # Arrays para almacenar puntos
        self.objpoints = []     # Puntos 3D en el mundo real
        self.imgpoints_l = []   # Puntos 2D en imagen izquierda
        self.imgpoints_r = []   # Puntos 2D en imagen derecha
        
    def capturar_imagenes_estereo(self, num_imagenes=15, carpeta_salida="../imagenes"):
        """
        Captura pares de imágenes estéreo desde dos cámaras
        """
        cap_l = cv2.VideoCapture(0)  # Cámara izquierda
        cap_r = cv2.VideoCapture(1)  # Cámara derecha
        
        if not cap_l.isOpened() or not cap_r.isOpened():
            print("Error: No se pudieron abrir las cámaras")
            # Si no hay dos cámaras, simular con una sola
            print("Usando una sola cámara para simular estéreo")
            return self.simular_captura_estereo(num_imagenes, carpeta_salida)
            
        os.makedirs(f"{carpeta_salida}/izquierda", exist_ok=True)
        os.makedirs(f"{carpeta_salida}/derecha", exist_ok=True)
        
        contador = 0
        print(f"Capturando {num_imagenes} pares de imágenes estéreo")
        
        while contador < num_imagenes:
            ret_l, frame_l = cap_l.read()
            ret_r, frame_r = cap_r.read()
            
            if not ret_l or not ret_r:
                break
                
            # Mostrar ambas cámaras
            combined = np.hstack((frame_l, frame_r))
            cv2.putText(combined, f"Pares: {contador}/{num_imagenes}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(combined, "ESPACIO: Capturar | ESC: Salir", 
                       (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            cv2.imshow('Captura Estereo (Izq | Der)', combined)
            
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC
                break
            elif key == 32:  # ESPACIO
                # Guardar par de imágenes
                filename_l = f"{carpeta_salida}/izquierda/estereo_l_{contador:02d}.jpg"
                filename_r = f"{carpeta_salida}/derecha/estereo_r_{contador:02d}.jpg"
                
                cv2.imwrite(filename_l, frame_l)
                cv2.imwrite(filename_r, frame_r)
                
                print(f"Par guardado: {contador:02d}")
                contador += 1
                
        cap_l.release()
        cap_r.release()
        cv2.destroyAllWindows()
        return contador > 0
        
    def simular_captura_estereo(self, num_imagenes=15, carpeta_salida="../imagenes"):
        """
        Simula captura estéreo con una sola cámara (para pruebas)
        """
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Error: No se pudo abrir la cámara")
            return False
            
        os.makedirs(f"{carpeta_salida}/izquierda", exist_ok=True)
        os.makedirs(f"{carpeta_salida}/derecha", exist_ok=True)
        
        contador = 0
        print(f"Simulando captura estéreo con una cámara")
        print("Mueva el patrón ligeramente entre capturas para simular parallax")
        
        while contador < num_imagenes:
            ret, frame = cap.read()
            if not ret:
                break
                
            cv2.putText(frame, f"Simulacion Estereo: {contador}/{num_imagenes}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, "ESPACIO: Izq | D: Der | ESC: Salir", 
                       (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            cv2.imshow('Simulacion Estereo', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC
                break
            elif key == 32:  # ESPACIO - imagen izquierda
                filename_l = f"{carpeta_salida}/izquierda/estereo_l_{contador:02d}.jpg"
                cv2.imwrite(filename_l, frame)
                print(f"Imagen izquierda guardada: {contador:02d}")
                
            elif key == ord('d'):  # D - imagen derecha
                filename_r = f"{carpeta_salida}/derecha/estereo_r_{contador:02d}.jpg"
                cv2.imwrite(filename_r, frame)
                print(f"Imagen derecha guardada: {contador:02d}")
                contador += 1
                
        cap.release()
        cv2.destroyAllWindows()
        return contador > 0
        
    def detectar_esquinas_estereo(self, carpeta_imagenes="../imagenes"):
        """
        Detecta esquinas en pares de imágenes estéreo
        """
        imagenes_l = sorted(glob.glob(f"{carpeta_imagenes}/izquierda/*.jpg"))
        imagenes_r = sorted(glob.glob(f"{carpeta_imagenes}/derecha/*.jpg"))
        
        if not imagenes_l or not imagenes_r:
            print(f"No se encontraron pares de imágenes en: {carpeta_imagenes}")
            return False
            
        print(f"Procesando {min(len(imagenes_l), len(imagenes_r))} pares de imágenes...")
        
        for i, (fname_l, fname_r) in enumerate(zip(imagenes_l, imagenes_r)):
            img_l = cv2.imread(fname_l)
            img_r = cv2.imread(fname_r)
            
            if img_l is None or img_r is None:
                continue
                
            gray_l = cv2.cvtColor(img_l, cv2.COLOR_BGR2GRAY)
            gray_r = cv2.cvtColor(img_r, cv2.COLOR_BGR2GRAY)
            
            # Encontrar esquinas en ambas imágenes
            ret_l, corners_l = cv2.findChessboardCorners(gray_l, self.patron_size, None)
            ret_r, corners_r = cv2.findChessboardCorners(gray_r, self.patron_size, None)
            
            # Solo usar si se detectan esquinas en ambas imágenes
            if ret_l and ret_r:
                # Refinar coordenadas
                criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
                corners_l = cv2.cornerSubPix(gray_l, corners_l, (11, 11), (-1, -1), criteria)
                corners_r = cv2.cornerSubPix(gray_r, corners_r, (11, 11), (-1, -1), criteria)
                
                # Añadir puntos
                self.objpoints.append(self.objp)
                self.imgpoints_l.append(corners_l)
                self.imgpoints_r.append(corners_r)
                
                # Dibujar esquinas
                cv2.drawChessboardCorners(img_l, self.patron_size, corners_l, ret_l)
                cv2.drawChessboardCorners(img_r, self.patron_size, corners_r, ret_r)
                
                # Guardar visualización
                combined = np.hstack((img_l, img_r))
                output_path = f"../resultados/estereo_esquinas_{i:02d}.jpg"
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                cv2.imwrite(output_path, combined)
                
                print(f"Esquinas detectadas en par: {i}")
            else:
                print(f"Esquinas no detectadas en par: {i}")
                
        print(f"Total de pares válidos para calibración: {len(self.objpoints)}")
        return len(self.objpoints) > 0
        
    def calibrar_camaras_individuales(self):
        """
        Calibra cada cámara individualmente primero
        """
        if len(self.objpoints) == 0:
            print("Error: No hay puntos para calibración")
            return None, None, None, None
            
        # Obtener tamaño de imagen
        img_l = cv2.imread(glob.glob("../imagenes/izquierda/*.jpg")[0])
        gray_l = cv2.cvtColor(img_l, cv2.COLOR_BGR2GRAY)
        img_size = gray_l.shape[::-1]
        
        print("Calibrando cámara izquierda...")
        ret_l, mtx_l, dist_l, rvecs_l, tvecs_l = cv2.calibrateCamera(
            self.objpoints, self.imgpoints_l, img_size, None, None)
        
        print("Calibrando cámara derecha...")
        ret_r, mtx_r, dist_r, rvecs_r, tvecs_r = cv2.calibrateCamera(
            self.objpoints, self.imgpoints_r, img_size, None, None)
        
        if ret_l and ret_r:
            print(f"Calibración izquierda - Error: {ret_l:.4f}")
            print(f"Calibración derecha - Error: {ret_r:.4f}")
            return (mtx_l, dist_l), (mtx_r, dist_r), img_size
        else:
            print("Error en calibraciones individuales")
            return None, None, None
            
    def calibrar_estereo(self, params_l, params_r, img_size):
        """
        Realiza la calibración estéreo
        """
        mtx_l, dist_l = params_l
        mtx_r, dist_r = params_r
        
        print("Realizando calibración estéreo...")
        
        # Calibración estéreo
        flags = cv2.CALIB_FIX_INTRINSIC
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 1e-5)
        
        ret, mtx_l, dist_l, mtx_r, dist_r, R, T, E, F = cv2.stereoCalibrate(
            self.objpoints, self.imgpoints_l, self.imgpoints_r,
            mtx_l, dist_l, mtx_r, dist_r, img_size,
            criteria=criteria, flags=flags)
        
        if ret:
            print(f"Calibración estéreo exitosa! Error: {ret:.4f}")
            
            # Rectificación estéreo
            R1, R2, P1, P2, Q, validPixROI1, validPixROI2 = cv2.stereoRectify(
                mtx_l, dist_l, mtx_r, dist_r, img_size, R, T)
            
            # Guardar parámetros estéreo
            calibracion_estereo = {
                'error_reproyeccion': float(ret),
                'matriz_camara_izq': mtx_l.tolist(),
                'matriz_camara_der': mtx_r.tolist(),
                'distorsion_izq': dist_l.tolist(),
                'distorsion_der': dist_r.tolist(),
                'matriz_rotacion': R.tolist(),
                'vector_traslacion': T.tolist(),
                'matriz_esencial': E.tolist(),
                'matriz_fundamental': F.tolist(),
                'rectificacion_izq': R1.tolist(),
                'rectificacion_der': R2.tolist(),
                'proyeccion_izq': P1.tolist(),
                'proyeccion_der': P2.tolist(),
                'matriz_disparidad': Q.tolist(),
                'baseline_mm': float(abs(T[0, 0]) * 1000),  # Baseline en mm
                'imagenes_usadas': len(self.objpoints)
            }
            
            with open('../resultados/calibracion_estereo.json', 'w') as f:
                json.dump(calibracion_estereo, f, indent=2)
                
            return R, T, E, F, R1, R2, P1, P2, Q
        else:
            print("Error en la calibración estéreo")
            return None
            
    def generar_rectificacion(self, params_l, params_r, R1, R2, P1, P2, img_size):
        """
        Genera mapas de rectificación y muestra resultados
        """
        mtx_l, dist_l = params_l
        mtx_r, dist_r = params_r
        
        # Crear mapas de rectificación
        map1_l, map2_l = cv2.initUndistortRectifyMap(
            mtx_l, dist_l, R1, P1, img_size, cv2.CV_16SC2)
        map1_r, map2_r = cv2.initUndistortRectifyMap(
            mtx_r, dist_r, R2, P2, img_size, cv2.CV_16SC2)
        
        # Aplicar rectificación a un par de imágenes
        img_l = cv2.imread(glob.glob("../imagenes/izquierda/*.jpg")[0])
        img_r = cv2.imread(glob.glob("../imagenes/derecha/*.jpg")[0])
        
        # Rectificar imágenes
        rectified_l = cv2.remap(img_l, map1_l, map2_l, cv2.INTER_LINEAR)
        rectified_r = cv2.remap(img_r, map1_r, map2_r, cv2.INTER_LINEAR)
        
        # Crear comparación
        original = np.hstack((img_l, img_r))
        rectified = np.hstack((rectified_l, rectified_r))
        
        # Añadir líneas horizontales para verificar rectificación
        h = rectified.shape[0]
        for i in range(0, h, 50):
            cv2.line(rectified, (0, i), (rectified.shape[1], i), (0, 255, 0), 1)
            
        # Guardar comparación
        comparison = np.vstack((original, rectified))
        cv2.imwrite('../resultados/rectificacion_estereo.jpg', comparison)
        
        print("Rectificación completada y guardada")
        
    def mostrar_parametros_estereo(self, R, T, baseline_mm):
        """
        Muestra los parámetros estéreo de forma legible
        """
        print("\n" + "="*60)
        print("PARÁMETROS DE CALIBRACIÓN ESTÉREO")
        print("="*60)
        
        # Extraer ángulos de rotación
        angles = cv2.Rodrigues(R)[0] * 180 / np.pi
        
        print(f"Baseline (distancia entre cámaras): {baseline_mm:.2f} mm")
        print(f"Traslación X: {T[0,0]:.4f}")
        print(f"Traslación Y: {T[1,0]:.4f}")
        print(f"Traslación Z: {T[2,0]:.4f}")
        
        print(f"\nRotación entre cámaras:")
        print(f"Roll:  {angles[0,0]:.2f}°")
        print(f"Pitch: {angles[1,0]:.2f}°")
        print(f"Yaw:   {angles[2,0]:.2f}°")
        
        print("="*60)


def main():
    """
    Función principal para calibración estéreo
    """
    calibrador = CalibradorEstereo(patron_size=(9, 6), tam_cuadrado=2.5)
    
    print("Calibración Estéreo - Taller 68")
    print("="*40)
    
    # Capturar imágenes
    print("\n1. Capturar pares de imágenes estéreo")
    respuesta = input("¿Desea capturar nuevas imágenes? (s/n): ")
    
    if respuesta.lower() in ['s', 'si', 'sí', 'y', 'yes']:
        calibrador.capturar_imagenes_estereo(num_imagenes=12)
    
    # Detectar esquinas
    print("\n2. Detectar esquinas en pares estéreo")
    if calibrador.detectar_esquinas_estereo():
        
        # Calibrar cámaras individualmente
        print("\n3. Calibrar cámaras individuales")
        params_l, params_r, img_size = calibrador.calibrar_camaras_individuales()
        
        if params_l and params_r:
            # Calibración estéreo
            print("\n4. Calibrar sistema estéreo")
            resultado = calibrador.calibrar_estereo(params_l, params_r, img_size)
            
            if resultado:
                R, T, E, F, R1, R2, P1, P2, Q = resultado
                
                # Mostrar parámetros
                baseline_mm = abs(T[0, 0]) * 1000
                calibrador.mostrar_parametros_estereo(R, T, baseline_mm)
                
                # Generar rectificación
                print("\n5. Generar rectificación estéreo")
                calibrador.generar_rectificacion(params_l, params_r, R1, R2, P1, P2, img_size)
                
                print("\n✅ Calibración estéreo completada!")
                print("Archivos generados en ../resultados/:")
                print("- calibracion_estereo.json (parámetros completos)")
                print("- estereo_esquinas_XX.jpg (detección de esquinas)")
                print("- rectificacion_estereo.jpg (validación)")
                
            else:
                print("❌ Error en calibración estéreo")
        else:
            print("❌ Error en calibraciones individuales")
    else:
        print("❌ No se pudieron detectar esquinas en los pares")


if __name__ == "__main__":
    main()
