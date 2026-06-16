"""
Модуль для работы с числами Фибоначчи
"""

class FibonacciGenerator:
    """Генератор последовательностей Фибоначчи"""
    
    def __init__(self):
        self.cache = {}
    
    def get_fibonacci_sequence(self, n_terms, mod=None):
        """
        Генерирует последовательность Фибоначчи
        
        Args:
            n_terms: количество членов последовательности
            mod: модуль для взятия остатка (если указан)
        
        Returns:
            list: последовательность чисел Фибоначчи
        """
        if n_terms <= 0:
            return []
        if n_terms == 1:
            return [0] if mod else [0]
        if n_terms == 2:
            return [0, 1] if mod else [0, 1]
        
        fib = [0, 1]
        for i in range(2, n_terms):
            next_val = fib[-1] + fib[-2]
            if mod is not None:
                next_val = next_val % mod
            fib.append(next_val)
        return fib
    
    def get_fibonacci_mod(self, n_terms, mod):
        """Генерирует последовательность Фибоначчи по модулю (строковый формат)"""
        fib = self.get_fibonacci_sequence(n_terms, mod)
        return [str(x) for x in fib]
    
    def get_fibonacci_raw(self, n_terms):
        """Генерирует полную последовательность Фибоначчи (без модуля)"""
        return self.get_fibonacci_sequence(n_terms)
    
    def get_pisano_period(self, mod):
        """
        Вычисляет период Пизано для заданного модуля
        """
        if mod == 1:
            return 1
        
        previous = 0
        current = 1
        
        for i in range(mod * mod):
            previous, current = current, (previous + current) % mod
            if previous == 0 and current == 1:
                return i + 1
        return mod * mod
    
    def get_fibonacci_spiral_coordinates(self, n_terms, size_factor=3, start_x=400, start_y=400):
        """
        Генерирует координаты для построения спирали Фибоначчи
        
        Returns:
            list: список словарей с координатами квадратов и дуг
        """
        fib_seq = self.get_fibonacci_raw(n_terms)
        directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]
        
        squares = []
        x, y = start_x, start_y
        dir_index = 0
        
        for i, fib_num in enumerate(fib_seq):
            side = fib_num * size_factor
            
            if dir_index == 0:  # Вправо
                x1, y1 = x, y - side
                x2, y2 = x + side, y
                arc_coords = (x, y - side, x + side, y)
                arc_start = 90
                x += side
            elif dir_index == 1:  # Вверх
                x1, y1 = x - side, y - side
                x2, y2 = x, y
                arc_coords = (x - side, y - side, x, y)
                arc_start = 180
                y -= side
            elif dir_index == 2:  # Влево
                x1, y1 = x - side, y
                x2, y2 = x, y + side
                arc_coords = (x - side, y, x, y + side)
                arc_start = 270
                x -= side
            else:  # Вниз
                x1, y1 = x, y
                x2, y2 = x + side, y + side
                arc_coords = (x, y, x + side, y + side)
                arc_start = 0
                y += side
            
            squares.append({
                'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2,
                'value': fib_num,
                'arc_coords': arc_coords,
                'arc_start': arc_start,
                'index': i
            })
            
            dir_index = (dir_index + 1) % 4
        
        return squares
