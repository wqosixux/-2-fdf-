"""
Генератор примеров FDF файлов для тестирования
"""

import random
import math

def generate_simple_mountain():
    """Генерация простой горы"""
    size = 20
    heights = []
    center_x, center_y = size // 2, size // 2
    
    for row in range(size):
        heights_row = []
        for col in range(size):
            # Расстояние от центра
            dx = col - center_x
            dy = row - center_y
            distance = math.sqrt(dx*dx + dy*dy)
            
            # Высота уменьшается с расстоянием
            height = int(30 * math.exp(-distance / 5))
            heights_row.append(height)
        heights.append(heights_row)
    
    return heights

def generate_wave_pattern():
    """Генерация волнового паттерна"""
    size = 25
    heights = []
    
    for row in range(size):
        heights_row = []
        for col in range(size):
            # Синусоидальная волна
            height = int(10 + 15 * math.sin(row * 0.3) * math.cos(col * 0.3))
            heights_row.append(height)
        heights.append(heights_row)
    
    return heights

def generate_random_terrain():
    """Генерация случайного рельефа"""
    size = 30
    heights = []
    
    for row in range(size):
        heights_row = []
        for col in range(size):
            # Случайная высота с плавными переходами
            base_height = random.randint(0, 20)
            if row > 0 and col > 0:
                # Смешивание с соседними значениями для плавности
                base_height = (base_height + heights[row-1][col] + heights_row[col-1]) // 3
            heights_row.append(base_height)
        heights.append(heights_row)
    
    return heights

def generate_pyramid():
    """Генерация пирамиды"""
    size = 15
    heights = []
    center = size // 2
    max_height = 25
    
    for row in range(size):
        heights_row = []
        for col in range(size):
            # Расстояние от центра
            dx = abs(col - center)
            dy = abs(row - center)
            distance = max(dx, dy)
            
            # Высота пирамиды
            height = max(0, max_height - distance * 2)
            heights_row.append(height)
        heights.append(heights_row)
    
    return heights

def save_fdf(heights, filename):
    """Сохранение матрицы высот в FDF файл"""
    with open(filename, 'w') as f:
        for row in heights:
            # Записываем строку с пробелами между значениями
            line = ' '.join(str(int(h)) for h in row)
            f.write(line + '\n')
    print(f"Файл {filename} создан успешно!")
    print(f"Размер: {len(heights)}x{len(heights[0]) if heights else 0}")

def main():
    print("Генератор примеров FDF файлов")
    print("=" * 40)
    
    # Генерируем несколько примеров
    examples = [
        ("example_mountain.fdf", generate_simple_mountain, "Гора"),
        ("example_wave.fdf", generate_wave_pattern, "Волновой паттерн"),
        ("example_random.fdf", generate_random_terrain, "Случайный рельеф"),
        ("example_pyramid.fdf", generate_pyramid, "Пирамида")
    ]
    
    for filename, generator, description in examples:
        print(f"\nСоздание: {description} -> {filename}")
        heights = generator()
        save_fdf(heights, filename)
    
    print("\n" + "=" * 40)
    print("Все примеры созданы!")
    print("\nДля просмотра используйте:")
    print("  python fdf_viewer.py example_mountain.fdf")
    print("  python fdf_viewer.py example_wave.fdf")
    print("  python fdf_viewer.py example_random.fdf")
    print("  python fdf_viewer.py example_pyramid.fdf")

if __name__ == "__main__":
    main()

