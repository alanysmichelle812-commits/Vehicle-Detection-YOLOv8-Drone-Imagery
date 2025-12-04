# 🚁 Vehicle-Detection-YOLOv8-Drone-Imagery
Modelo de detección de objetos entrenado con YOLOv8 (Medium) para identificar vehículos (Coches, Buses, Minibuses) en imágenes aéreas de tráfico.

---

## 💡 Introducción y Objetivo

Este repositorio aloja los resultados y el código de entrenamiento de un modelo de detección de objetos. El objetivo principal es la **identificación automática de vehículos** (`Car`, `Bus`, `Minibus`, `Truck`) en imágenes aéreas para tareas de monitoreo de tráfico o conteo vehicular.

El entrenamiento se realizó sobre el *Aerial Cars Dataset* por **10 épocas**.

---

## ⚙️ Configuración y Código

### Archivos Clave

* **`training.py`**: Contiene la lógica Python utilizada para la organización y división de los datos (Train/Val), y las referencias de los comandos de entrenamiento.
* **`aerial_cars_data.yaml`**: Archivo de configuración para YOLOv8.
* **`requirements.txt`**: Lista todas las librerías necesarias para ejecutar el código.

### Comandos de Referencia

Para replicar el entrenamiento o probar la inferencia:

| Propósito | Comando Shell |
| :--- | :--- |
| **Entrenamiento** | `yolo train model=yolov8m.pt data=aerial_cars_data.yaml epochs=10 imgsz=640 project=aerial_cars_project` |
| **Predicción** | `yolo predict model=best.pt source='path/a/tu/imagen.jpg' imgsz=640` |

---

## 📈 Resultados y Métricas de Rendimiento

El modelo mostró un rendimiento sólido, destacando en la detección de vehículos comunes (`Car`).

### Métricas Generales Finales

| Métrica | Valor Final |
| :--- | :--- |
| **mAP50** (Mean Average Precision @ 50% IOU) | **0.652** |
| **mAP50-95** (Promedio estricto) | **0.494** |

### Rendimiento por Clase (mAP50)

| Clase | mAP50 | Comentario |
| :--- | :--- | :--- |
| **Car** (Coche) | **0.979** | Rendimiento casi perfecto. |
| **Bus** (Autobús) | 0.883 | Muy buen rendimiento. |
| **Truck** (Camión) | 0.044 | Baja precisión debido a la escasez de muestras en el conjunto de validación. |

**[Gráfica de Rendimiento results.png]** (Sube la imagen aquí)

---

## 🖼️ Demostración de Uso (Inferencia)

El modelo detectó 25 coches, 3 autobuses y 4 minibuses en la imagen de prueba:

| Detección | Conteo |
| :--- | :--- |
| Cars | 25 |
| Buss | 3 |
| Minibuss | 4 |

**[Imagen de Detección DJI-00760-00003.jpg]** (Sube la imagen aquí)

---

## ⬇️ Descarga del Modelo Entrenado (`best.pt`)

El archivo de pesos entrenado (`best.pt`) es grande (52 MB) y no se puede subir directamente a GitHub.

Puedes descargarlo desde el siguiente enlace de Google Drive:

**[Descargar best.pt (Google Drive)] (https://drive.google.com/file/d/1Ma6N_ZKbEVr_7hQHNuOO9_cW81xEtt4_/view?usp=drive_link)**
