# Archivo: training.py
# Este script contiene el código Python utilizado para la organización
# y la referencia de los comandos de entrenamiento y predicción del modelo YOLOv8.

import os
import glob
import shutil
from sklearn.model_selection import train_test_split
from pathlib import Path
# from ultralytics import YOLO # Librería principal de YOLOv8

# --- CONFIGURACIÓN DE RUTAS ---
# Definición de la estructura de carpetas utilizada en Colab
BASE_DIR = 'aerial-cars-dataset-master'
IMG_TRAIN_DIR = os.path.join(BASE_DIR, 'images', 'train')
IMG_VAL_DIR = os.path.join(BASE_DIR, 'images', 'val')
LBL_TRAIN_DIR = os.path.join(BASE_DIR, 'labels', 'train')
LBL_VAL_DIR = os.path.join(BASE_DIR, 'labels', 'val')

# --- 1. ORGANIZACIÓN Y DIVISIÓN DEL DATASET ---
def organize_dataset():
    """
    Función que recrea la lógica de organización del dataset.
    Busca pares de imagen/etiqueta en /content/ y los divide
    en conjuntos de entrenamiento y validación (80/20).
    """
    print("Creando estructura de carpetas YOLOv8...")
    os.makedirs(IMG_TRAIN_DIR, exist_ok=True)
    os.makedirs(IMG_VAL_DIR, exist_ok=True)
    os.makedirs(LBL_TRAIN_DIR, exist_ok=True)
    os.makedirs(LBL_VAL_DIR, exist_ok=True)

    print("Buscando archivos de imagen y etiqueta en /content/...")
    # Buscamos solo las etiquetas del dataset (DJI_XXXX.txt)
    all_labels = glob.glob(os.path.join('/content/', 'DJI_*.txt'))
    image_label_pairs = []
    supported_img_extensions = ['.jpg', '.png', '.jpeg']

    # Intentamos encontrar la imagen correspondiente para cada etiqueta
    for label_path in all_labels:
        base_name = Path(label_path).stem
        found_image_path = None
        for ext in supported_img_extensions:
            img_path = os.path.join('/content/', base_name + ext)
            if os.path.exists(img_path):
                found_image_path = img_path
                break
                
        if found_image_path:
            image_label_pairs.append((found_image_path, label_path))

    if image_label_pairs:
        # 80% para entrenamiento, 20% para validación
        train_pairs, val_pairs = train_test_split(image_label_pairs, test_size=0.2, random_state=42)

        def move_pairs(pairs, img_dest, label_dest):
            for img_src, lbl_src in pairs:
                shutil.move(img_src, os.path.join(img_dest, os.path.basename(img_src)))
                shutil.move(lbl_src, os.path.join(label_dest, os.path.basename(lbl_src)))

        move_pairs(train_pairs, IMG_TRAIN_DIR, LBL_TRAIN_DIR)
        move_pairs(val_pairs, IMG_VAL_DIR, LBL_VAL_DIR)
        print("✅ Reorganización de datos completada.")
    else:
        print("❌ No se encontraron pares de datos válidos. Reorganización omitida.")

# --- 2. COMANDO DE ENTRENAMIENTO (REFERENCIA) ---
# Comando Shell utilizado para el entrenamiento:
# !yolo train model=yolov8m.pt data=aerial_cars_data.yaml epochs=10 imgsz=640 project=aerial_cars_project name=run_217

# --- 3. COMANDO DE PREDICCIÓN (REFERENCIA) ---
# Comando Shell utilizado para la inferencia:
# !yolo predict model=/content/aerial_cars_project/run_214/weights/best.pt source='/content/aerial-cars-dataset-master/images/val/DJI-00760-00003.jpg' name=prediction_cars
