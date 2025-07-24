#!/usr/bin/env python3
"""
Utilidades para la calibración de cámaras
Funciones auxiliares y visualización de resultados
"""

import cv2
import numpy as np
import json
import matplotlib.pyplot as plt
from pathlib import Path

def generar_patron_ajedrez(filas=6, columnas=9, tamaño_cuadrado=30, archivo_salida="patron_ajedrez.png"):
    """
    Genera un patrón de tablero de ajedrez para impresión
    """
    # Crear imagen del patrón
    img_height = filas * tamaño_cuadrado
    img_width = columnas * tamaño_cuadrado
    
    # Crear tablero
    tablero = np.zeros((img_height, img_width), dtype=np.uint8)
    
    for i in range(filas):
        for j in range(columnas):
            if (i + j) % 2 == 0:
                y1, y2 = i * tamaño_cuadrado, (i + 1) * tamaño_cuadrado
                x1, x2 = j * tamaño_cuadrado, (j + 1) * tamaño_cuadrado
                tablero[y1:y2, x1:x2] = 255
    
    # Añadir bordes
    border_size = tamaño_cuadrado // 2
    tablero_con_borde = np.zeros((img_height + 2*border_size, img_width + 2*border_size), dtype=np.uint8)
    tablero_con_borde[border_size:-border_size, border_size:-border_size] = tablero
    
    cv2.imwrite(archivo_salida, tablero_con_borde)
    print(f"Patrón de ajedrez generado: {archivo_salida}")
    print(f"Dimensiones: {columnas}x{filas} esquinas internas")
    print(f"Tamaño de cuadrado: {tamaño_cuadrado} píxeles")

def cargar_parametros_calibracion(archivo_json):
    """
    Carga parámetros de calibración desde archivo JSON
    """
    try:
        with open(archivo_json, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Archivo no encontrado: {archivo_json}")
        return None
    except json.JSONDecodeError:
        print(f"Error al decodificar JSON: {archivo_json}")
        return None

def visualizar_parametros_calibracion(archivo_json):
    """
    Visualiza los parámetros de calibración de forma gráfica
    """
    data = cargar_parametros_calibracion(archivo_json)
    if not data:
        return
    
    # Crear figura con subplots
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Análisis de Calibración de Cámara', fontsize=16)
    
    # 1. Matriz de cámara
    if 'matriz_camara' in data:
        mtx = np.array(data['matriz_camara'])
        ax = axes[0, 0]
        im = ax.imshow(mtx, cmap='viridis', aspect='auto')
        ax.set_title('Matriz de Cámara')
        ax.set_xlabel('Columna')
        ax.set_ylabel('Fila')
        
        # Añadir valores en la matriz
        for i in range(mtx.shape[0]):
            for j in range(mtx.shape[1]):
                ax.text(j, i, f'{mtx[i, j]:.1f}', ha='center', va='center', color='white')
        
        plt.colorbar(im, ax=ax)
    
    # 2. Coeficientes de distorsión
    if 'coeficientes_distorsion' in data:
        dist = np.array(data['coeficientes_distorsion']).flatten()
        ax = axes[0, 1]
        bars = ax.bar(['k1', 'k2', 'p1', 'p2', 'k3'], dist)
        ax.set_title('Coeficientes de Distorsión')
        ax.set_ylabel('Valor')
        ax.grid(True, alpha=0.3)
        
        # Colorear barras según magnitud
        for bar, val in zip(bars, dist):
            if abs(val) > 0.1:
                bar.set_color('red')
            elif abs(val) > 0.01:
                bar.set_color('orange')
            else:
                bar.set_color('green')
    
    # 3. Información del proceso
    ax = axes[1, 0]
    ax.axis('off')
    info_text = f"""
    Información de Calibración:
    
    Error de reproyección: {data.get('error_reproyeccion', 'N/A'):.4f}
    Imágenes utilizadas: {data.get('imagenes_usadas', 'N/A')}
    Tamaño de imagen: {data.get('tamaño_imagen', 'N/A')}
    Patrón usado: {data.get('patron_usado', 'N/A')}
    
    Distancia focal:
    fx = {mtx[0,0]:.2f} px
    fy = {mtx[1,1]:.2f} px
    
    Centro óptico:
    cx = {mtx[0,2]:.2f} px
    cy = {mtx[1,2]:.2f} px
    """
    ax.text(0.1, 0.9, info_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', fontfamily='monospace')
    
    # 4. Gráfico de calidad
    ax = axes[1, 1]
    error = data.get('error_reproyeccion', 0)
    calidad_labels = ['Excelente\n(<0.5)', 'Buena\n(0.5-1.0)', 'Aceptable\n(1.0-2.0)', 'Pobre\n(>2.0)']
    calidad_colors = ['green', 'yellow', 'orange', 'red']
    calidad_values = [0.5, 1.0, 2.0, 5.0]
    
    bars = ax.bar(calidad_labels, [1, 1, 1, 1], color=calidad_colors, alpha=0.3)
    
    # Marcar donde está nuestro error
    if error < 0.5:
        pos = 0
    elif error < 1.0:
        pos = 1
    elif error < 2.0:
        pos = 2
    else:
        pos = 3
    
    bars[pos].set_alpha(1.0)
    ax.axhline(y=error/5, color='blue', linestyle='--', linewidth=2, label=f'Error actual: {error:.4f}')
    ax.set_title('Calidad de Calibración')
    ax.set_ylabel('Error (píxeles)')
    ax.legend()
    
    plt.tight_layout()
    
    # Guardar gráfico
    output_path = archivo_json.replace('.json', '_analisis.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Análisis guardado en: {output_path}")
    plt.show()

def comparar_calibraciones(archivo_una_camara, archivo_estereo=None):
    """
    Compara resultados de calibración de una cámara vs estéreo
    """
    data_una = cargar_parametros_calibracion(archivo_una_camara)
    if not data_una:
        return
    
    print("="*60)
    print("COMPARACIÓN DE CALIBRACIONES")
    print("="*60)
    
    print("\n📷 CALIBRACIÓN UNA CÁMARA:")
    print(f"Error de reproyección: {data_una.get('error_reproyeccion', 'N/A'):.4f} píxeles")
    print(f"Imágenes utilizadas: {data_una.get('imagenes_usadas', 'N/A')}")
    
    if 'matriz_camara' in data_una:
        mtx = np.array(data_una['matriz_camara'])
        print(f"Distancia focal promedio: {(mtx[0,0] + mtx[1,1])/2:.2f} píxeles")
    
    if archivo_estereo:
        data_estereo = cargar_parametros_calibracion(archivo_estereo)
        if data_estereo:
            print("\n🔍 CALIBRACIÓN ESTÉREO:")
            print(f"Error de reproyección: {data_estereo.get('error_reproyeccion', 'N/A'):.4f} píxeles")
            print(f"Baseline: {data_estereo.get('baseline_mm', 'N/A'):.2f} mm")
            print(f"Imágenes utilizadas: {data_estereo.get('imagenes_usadas', 'N/A')}")
            
            print("\n🔬 ANÁLISIS:")
            error_una = data_una.get('error_reproyeccion', float('inf'))
            error_estereo = data_estereo.get('error_reproyeccion', float('inf'))
            
            if error_estereo < error_una:
                print("✅ La calibración estéreo tiene menor error")
            else:
                print("⚠️  La calibración individual tiene menor error")
            
            baseline = data_estereo.get('baseline_mm', 0)
            if baseline > 50:
                print(f"✅ Baseline adecuado ({baseline:.1f}mm) para visión estéreo")
            else:
                print(f"⚠️  Baseline pequeño ({baseline:.1f}mm) - considere mayor separación")
    
    print("="*60)

def test_calibracion_tiempo_real(archivo_calibracion, camara_id=0):
    """
    Prueba la calibración en tiempo real corrigiendo distorsión
    """
    data = cargar_parametros_calibracion(archivo_calibracion)
    if not data:
        return
    
    mtx = np.array(data['matriz_camara'])
    dist = np.array(data['coeficientes_distorsion'])
    
    cap = cv2.VideoCapture(camara_id)
    if not cap.isOpened():
        print("Error: No se pudo abrir la cámara")
        return
    
    print("Presione 'q' para salir, 'c' para cambiar entre original/corregido")
    mostrar_corregido = True
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        h, w = frame.shape[:2]
        
        if mostrar_corregido:
            # Obtener matriz optimizada
            newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
            
            # Corregir distorsión
            dst = cv2.undistort(frame, mtx, dist, None, newcameramtx)
            
            # Recortar
            x, y, w_roi, h_roi = roi
            dst = dst[y:y+h_roi, x:x+w_roi]
            
            # Redimensionar para mostrar
            dst = cv2.resize(dst, (w, h))
            
            cv2.putText(dst, "CORREGIDO (C: cambiar)", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.imshow('Test Calibracion', dst)
        else:
            cv2.putText(frame, "ORIGINAL (C: cambiar)", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            cv2.imshow('Test Calibracion', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('c'):
            mostrar_corregido = not mostrar_corregido
    
    cap.release()
    cv2.destroyAllWindows()

def main():
    """
    Menú principal de utilidades
    """
    print("🛠️  UTILIDADES DE CALIBRACIÓN DE CÁMARAS")
    print("="*50)
    print("1. Generar patrón de ajedrez para impresión")
    print("2. Visualizar parámetros de calibración")
    print("3. Comparar calibraciones")
    print("4. Test en tiempo real")
    print("5. Salir")
    
    while True:
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            print("\nGenerando patrón de ajedrez...")
            generar_patron_ajedrez(filas=6, columnas=9, tamaño_cuadrado=50)
            
        elif opcion == "2":
            archivo = input("Archivo JSON de calibración: ")
            if Path(archivo).exists():
                visualizar_parametros_calibracion(archivo)
            else:
                print("Archivo no encontrado")
                
        elif opcion == "3":
            archivo1 = input("Archivo calibración una cámara: ")
            archivo2 = input("Archivo calibración estéreo (opcional): ")
            if not archivo2.strip():
                archivo2 = None
            comparar_calibraciones(archivo1, archivo2)
            
        elif opcion == "4":
            archivo = input("Archivo JSON de calibración: ")
            if Path(archivo).exists():
                test_calibracion_tiempo_real(archivo)
            else:
                print("Archivo no encontrado")
                
        elif opcion == "5":
            break
        else:
            print("Opción inválida")

if __name__ == "__main__":
    main()
