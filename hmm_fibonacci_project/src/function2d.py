"""
Модуль для 2D объекта: функция Z = |X+Y| - |X-Y|
"""

import random

class Function2D:
    """Класс для работы с 2D функцией Z = |X+Y| - |X-Y|"""
    
    def __init__(self):
        self.last_results = []
        self.x_range = (-10, 10)
        self.y_range = (-10, 10)
    
    def compute_z(self, x, y):
        """
        Вычисляет значение функции Z = |X+Y| - |X-Y|
        
        Свойства функции:
        - Z = 2 * min(|X|, |Y|) при X*Y >= 0
        - Z = 0 при X*Y < 0
        """
        return abs(x + y) - abs(x - y)
    
    def compute_z_vectorized(self, x_vals, y_vals):
        """Векторизованное вычисление для списков значений"""
        return [self.compute_z(x, y) for x, y in zip(x_vals, y_vals)]
    
    def generate_grid(self, x_min, x_max, y_min, y_max, step=1):
        """
        Генерирует сетку значений функции
        
        Args:
            x_min, x_max: диапазон по X
            y_min, y_max: диапазон по Y
            step: шаг сетки
        
        Returns:
            list: список кортежей (x, y, z)
        """
        results = []
        for x in range(x_min, x_max + 1, step):
            for y in range(y_min, y_max + 1, step):
                z = self.compute_z(x, y)
                results.append((x, y, z))
        
        self.last_results = results
        return results
    
    def get_z_range(self, values):
        """Возвращает мин и макс Z для цветового масштабирования"""
        if not values:
            return (0, 0)
        z_vals = [z for _, _, z in values]
        return (min(z_vals), max(z_vals))
    
    def get_color_for_z(self, z, z_min, z_max):
        """
        Преобразует значение Z в цвет для визуализации
        Градиент от синего (мин) к красному (макс)
        """
        if z_max == z_min:
            ratio = 0
        else:
            ratio = (z - z_min) / (z_max - z_min)
        
        r = int(255 * ratio)
        b = int(255 * (1 - ratio))
        return f"#{r:02x}00{b:02x}"
    
    def generate_for_database(self, n_points=1000, x_range=(-100, 100), y_range=(-100, 100)):
        """
        Генерирует n_points значений для заполнения БД
        """
        results = []
        for _ in range(n_points):
            x = random.randint(x_range[0], x_range[1])
            y = random.randint(y_range[0], y_range[1])
            z = self.compute_z(x, y)
            results.append((x, y, z))
        
        self.last_results = results
        return results
    
    def get_description(self):
        """Возвращает описание функции"""
        return "Z = |X+Y| - |X-Y|"
