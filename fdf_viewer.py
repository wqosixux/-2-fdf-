import pygame
import sys
import math

# Инициализация Pygame
pygame.init()

# Константы
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
BACKGROUND_COLOR = (20, 20, 30)
GRID_COLOR = (100, 150, 200)
SURFACE_COLOR = (50, 150, 200)
LINE_COLOR = (80, 120, 180)

# Создание окна
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("FDF Viewer - 3D Визуализация")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

def read_fdf(filename):
    """Чтение FDF файла и возврат матрицы высот"""
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
        
        heights = []
        for line in lines:
            line = line.strip()
            if line:
                # Разделяем строку по пробелам и преобразуем в числа
                row = []
                for value in line.split():
                    try:
                        # Убираем возможные запятые и преобразуем в int
                        height = int(value.replace(',', ''))
                        row.append(height)
                    except ValueError:
                        continue
                if row:
                    heights.append(row)
        
        return heights
    except FileNotFoundError:
        print(f"Ошибка: Файл {filename} не найден!")
        return None
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None

def isometric_projection(x, y, z, scale=20, offset_x=0, offset_y=0, angle_x=0.5, angle_y=0.5):
    """Изометрическая проекция 3D точки на 2D экран"""
    # Простая изометрическая проекция
    # x, y - координаты на плоскости, z - высота
    
    # Поворот вокруг вертикальной оси (angle_y)
    cos_y = math.cos(angle_y)
    sin_y = math.sin(angle_y)
    
    # Поворачиваем в горизонтальной плоскости
    rotated_x = x * cos_y - y * sin_y
    rotated_y = x * sin_y + y * cos_y
    
    # Изометрическая проекция (вид под углом 30 градусов)
    # Стандартная изометрическая формула
    iso_x = (rotated_x - rotated_y) * scale
    iso_y = (rotated_x + rotated_y) * scale * 0.5 - z * scale
    
    # Центрирование и смещение
    screen_x = iso_x + WINDOW_WIDTH // 2 + offset_x
    screen_y = iso_y + WINDOW_HEIGHT // 2 + offset_y
    
    return int(screen_x), int(screen_y)

def draw_3d_surface(heights, scale=20, offset_x=0, offset_y=0, angle_x=0.5, angle_y=0.5):
    """Отрисовка 3D поверхности"""
    if not heights:
        return
    
    rows = len(heights)
    cols = len(heights[0]) if rows > 0 else 0
    
    if cols == 0:
        return
    
    # Находим максимальную высоту для нормализации цветов
    max_height = max(max(row) for row in heights)
    min_height = min(min(row) for row in heights)
    height_range = max_height - min_height if max_height != min_height else 1
    
    # Отрисовка линий сетки
    for row in range(rows):
        for col in range(cols):
            x = col - cols // 2
            y = row - rows // 2
            z = heights[row][col]
            
            # Цвет в зависимости от высоты
            if height_range > 0:
                normalized_height = (z - min_height) / height_range
            else:
                normalized_height = 0.5
            
            # Яркие цвета для лучшей видимости
            # Синий для низких точек, зеленый для средних, красный для высоких
            if normalized_height < 0.33:
                # Низкие точки - синие
                r = int(50 + normalized_height * 100)
                g = int(100 + normalized_height * 100)
                b = 255
            elif normalized_height < 0.66:
                # Средние точки - зеленые
                r = int(100 + (normalized_height - 0.33) * 200)
                g = 255
                b = int(255 - (normalized_height - 0.33) * 200)
            else:
                # Высокие точки - красные/желтые
                r = 255
                g = int(255 - (normalized_height - 0.66) * 200)
                b = int(50 - (normalized_height - 0.66) * 50)
            
            color = (max(50, min(255, r)), max(50, min(255, g)), max(50, min(255, b)))
            
            # Проекция текущей точки
            screen_x, screen_y = isometric_projection(x, y, z, scale, offset_x, offset_y, angle_x, angle_y)
            
            # Рисуем линии к соседним точкам
            if col < cols - 1:  # Горизонтальная линия
                next_x = (col + 1) - cols // 2
                next_z = heights[row][col + 1]
                next_screen_x, next_screen_y = isometric_projection(
                    next_x, y, next_z, scale, offset_x, offset_y, angle_x, angle_y
                )
                pygame.draw.line(screen, color, (screen_x, screen_y), (next_screen_x, next_screen_y), 2)
            
            if row < rows - 1:  # Вертикальная линия
                next_y = (row + 1) - rows // 2
                next_z = heights[row + 1][col]
                next_screen_x, next_screen_y = isometric_projection(
                    x, next_y, next_z, scale, offset_x, offset_y, angle_x, angle_y
                )
                pygame.draw.line(screen, color, (screen_x, screen_y), (next_screen_x, next_screen_y), 2)
            
            # Рисуем точку (только если в пределах экрана для производительности)
            if 0 <= screen_x < WINDOW_WIDTH and 0 <= screen_y < WINDOW_HEIGHT:
                pygame.draw.circle(screen, color, (screen_x, screen_y), 4)

def draw_ui(scale, angle_x, angle_y, filename):
    """Отрисовка интерфейса"""
    # Информация о файле
    info_text = font.render(f"Файл: {filename}", True, (255, 255, 255))
    screen.blit(info_text, (10, 10))
    
    # Управление
    controls = [
        "Управление:",
        "WASD - перемещение",
        "Q/E - масштаб",
        "R/F - поворот X",
        "T/G - поворот Y",
        f"Масштаб: {scale:.1f}",
        f"Угол X: {angle_x:.2f}",
        f"Угол Y: {angle_y:.2f}"
    ]
    
    y_offset = 50
    for i, text in enumerate(controls):
        text_surface = pygame.font.Font(None, 24).render(text, True, (200, 200, 200))
        screen.blit(text_surface, (10, y_offset + i * 25))

def main():
    if len(sys.argv) < 2:
        print("Использование: python fdf_viewer.py <файл.fdf>")
        print("Пример: python fdf_viewer.py example.fdf")
        sys.exit(1)
    
    filename = sys.argv[1]
    heights = read_fdf(filename)
    
    if heights is None:
        sys.exit(1)
    
    rows = len(heights)
    cols = len(heights[0]) if heights else 0
    print(f"Загружено {rows} строк, {cols} столбцов")
    
    # Находим диапазон высот для отладки
    if heights:
        all_heights = [h for row in heights for h in row]
        print(f"Минимальная высота: {min(all_heights)}, Максимальная высота: {max(all_heights)}")
    
    # Параметры визуализации
    # Автоматический масштаб в зависимости от размера карты
    if rows > 0 and cols > 0:
        # Увеличиваем масштаб для лучшей видимости
        scale = min(600 // max(rows, cols), 25)
        if scale < 10:
            scale = 10
    else:
        scale = 15
    
    print(f"Начальный масштаб: {scale}")
    
    offset_x = 0
    offset_y = 0
    angle_x = 0.5
    angle_y = 0.785  # 45 градусов для лучшего вида
    
    # Тестовая проекция для отладки
    test_x, test_y = isometric_projection(0, 0, 0, scale, offset_x, offset_y, angle_x, angle_y)
    print(f"Тестовая проекция центра (0,0,0): ({test_x}, {test_y})")
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Обработка нажатых клавиш
        keys = pygame.key.get_pressed()
        
        # Перемещение
        if keys[pygame.K_w]:
            offset_y -= 2
        if keys[pygame.K_s]:
            offset_y += 2
        if keys[pygame.K_a]:
            offset_x -= 2
        if keys[pygame.K_d]:
            offset_x += 2
        
        # Масштаб
        if keys[pygame.K_q]:
            scale = max(5, scale - 0.5)
        if keys[pygame.K_e]:
            scale = min(100, scale + 0.5)
        
        # Поворот по оси X
        if keys[pygame.K_r]:
            angle_x = min(1.5, angle_x + 0.02)
        if keys[pygame.K_f]:
            angle_x = max(0.1, angle_x - 0.02)
        
        # Поворот по оси Y
        if keys[pygame.K_t]:
            angle_y = min(1.5, angle_y + 0.02)
        if keys[pygame.K_g]:
            angle_y = max(0.1, angle_y - 0.02)
        
        # Отрисовка
        screen.fill(BACKGROUND_COLOR)
        draw_3d_surface(heights, scale, offset_x, offset_y, angle_x, angle_y)
        draw_ui(scale, angle_x, angle_y, filename)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

