from PIL import Image
import numpy as np
from scipy.ndimage import label

def process_image_by_area(filename="Victorialab2.bmp", connectivity=4, n=5):
    """
    Розділяє об'єкти на зображенні на n груп по площі та зберігає результат у файл pictureresult.bmp.
    
    Параметри:
        - filename: Шлях до вхідного зображення (за замовчуванням "Victorialab2.bmp").
        - connectivity: Тип зв'язаності, 4 або 8 (за замовчуванням 4).
        - n: Кількість груп для розподілу об'єктів за площею (за замовчуванням 5).
    """
    # Відкриваємо зображення та конвертуємо у формат чорно-білого зображення
    image = Image.open(filename).convert('L')
    binary_image = np.array(image) > 128  # Конвертуємо в бінарне зображення

    # Структура для маркування об'єктів залежно від зв'язаності
    structure = np.ones((3, 3), dtype=int) if connectivity == 8 else np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])

    # Маркування об'єктів
    labeled_image, num_features = label(binary_image, structure=structure)
    
    # Розрахунок площі кожного об'єкта
    object_areas = np.bincount(labeled_image.ravel())[1:]  # Площі об'єктів (пропускаємо фон)

    # Розподіл на n груп за площею
    area_thresholds = np.linspace(object_areas.min(), object_areas.max(), n + 1)
    grouped_image = np.zeros_like(labeled_image)

    for idx, area in enumerate(object_areas):
        for i in range(1, n + 1):
            if area_thresholds[i - 1] <= area < area_thresholds[i]:
                grouped_image[labeled_image == idx + 1] = i  # Маркуємо відповідною групою

    # Зберігаємо результат у новий файл
    result_image = Image.fromarray((grouped_image * (255 // n)).astype(np.uint8))
    result_image.save("pictureresult.bmp")
    print("Результуюче зображення збережено як pictureresult.bmp")

# Викликаємо функцію з початковим зображенням "Victorialab2.bmp"
process_image_by_area()

input("Натисніть Enter, щоб завершити програму...")