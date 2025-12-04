import os
import random
from collections import Counter

# --- CONFIGURACIÓN CRÍTICA ---
# 🔥 RUTA ABSOLUTA CORREGIDA CON EL NOMBRE EXACTO DE LA CARPETA 🔥
DATASET_PATH = r'C:\Users\UserEliteBook\OneDrive\Documentos\Analisis_YOLO\aerial-cars-dataset-master' 
CLASS_NAMES = ['Car', 'Truck', 'Bus', 'Van', 'Other'] 
TEST_SPLIT = 0.20  

# Directorios de salida
OUTPUT_DIR = 'yolo_dataset_split'
# Asegura que la carpeta de salida exista
os.makedirs(OUTPUT_DIR, exist_ok=True)


def analyze_and_split_dataset(dataset_path):
    """Analiza las etiquetas y divide el dataset en train/test."""
    
    print(f"\nBuscando archivos en: {dataset_path}")

    # 1. Montar los Tags y Contar Clases
    
    # Buscamos solo los archivos de etiquetas (.txt) dentro de la carpeta
    label_files = [f for f in os.listdir(dataset_path) if f.endswith('.txt')]
    all_class_ids = []
    
    print(f"Total de archivos de etiquetas encontrados: {len(label_files)}")
    
    # Verifica si encontró algo
    if not label_files:
        print("\nERROR CRÍTICO: No se encontró NINGÚN archivo de etiquetas (.txt).")
        print("Asegúrate de que la carpeta contenga archivos como MOS164.txt.")
        return # Termina la ejecución si no hay archivos

    for label_file in label_files:
        full_path = os.path.join(dataset_path, label_file)
        
        try:
            with open(full_path, 'r') as f:
                for line in f:
                    try:
                        # Obtenemos el ID de clase (primer elemento de la línea)
                        class_id = int(line.split()[0])
                        all_class_ids.append(class_id)
                    except (ValueError, IndexError):
                        continue
        except Exception as e:
            print(f"Error al leer {label_file}: {e}")
            continue

    # 2. Análisis de Cada Tipo de Clase (Conteo)
    class_counts = Counter(all_class_ids)
    print("\n--- Análisis de Clases (Conteo de Instancias) ---")
    total_instances = sum(class_counts.values())
    print(f"Total de instancias de vehículos detectadas: {total_instances}\n")
    
    for class_id, count in class_counts.items():
        if class_id < len(CLASS_NAMES):
            name = CLASS_NAMES[class_id]
            print(f"ID {class_id} ({name}): {count} instancias")
        else:
            print(f"ID {class_id} (Clase Desconocida): {count} instancias")

    # 3. División en Train y Test
    base_files = [os.path.splitext(f)[0] for f in label_files]
    random.seed(42) # Fija la semilla para reproducibilidad
    random.shuffle(base_files)
    
    split_index = int(len(base_files) * (1 - TEST_SPLIT))
    train_files = base_files[:split_index]
    test_files = base_files[split_index:]
    
    print(f"\n--- División Train/Test ---")
    print(f"Archivos totales de etiquetas: {len(base_files)}")
    print(f"Archivos de Entrenamiento (Train, {100-TEST_SPLIT*100}%): {len(train_files)}")
    print(f"Archivos de Prueba (Test, {TEST_SPLIT*100}%): {len(test_files)}")

    # Guardar las listas de archivos (rutas a las imágenes)
    def write_file_list(filename, file_list):
        with open(os.path.join(OUTPUT_DIR, filename), 'w') as f:
            for base in file_list:
                # Escribe la ruta completa del archivo .jpg o .png 
                img_path = os.path.join(dataset_path, base + '.jpg')
                if not os.path.exists(img_path):
                     img_path = os.path.join(dataset_path, base + '.png') # Por si hay PNGs
                
                # Escribe la ruta con barras diagonales (el formato preferido de YOLO)
                f.write(img_path.replace('\\', '/') + '\n') 
                
    write_file_list('train.txt', train_files)
    write_file_list('test.txt', test_files)
    
    print(f"\nDivisión completada. Archivos 'train.txt' y 'test.txt' guardados en '{OUTPUT_DIR}'")

# --- EJECUTAR ---
if __name__ == '__main__':
    if os.path.isdir(DATASET_PATH):
        analyze_and_split_dataset(DATASET_PATH)
    else:
        print("ERROR: La ruta del dataset NO EXISTE.")
        print(f"Revisa que esta carpeta exista: {DATASET_PATH}")