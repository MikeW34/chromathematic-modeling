"""
Модуль визуализации для 1D и 2D объектов
"""

import tkinter as tk
import math

class Visualizer1D:
    """Визуализатор для 1D объектов (ленточная диаграмма, спираль)"""
    
    def draw_ribbon(self, canvas, data, hmm, mod):
        """Рисует ленточную диаграмму"""
        canvas.delete("all")
        
        if not data:
            return 0
        
        # Обновляем canvas для получения правильных размеров
        canvas.update_idletasks()
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        
        if canvas_width <= 1:
            canvas_width = 800
            canvas_height = 400
            canvas.config(width=canvas_width, height=canvas_height)
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8']
        
        # Параметры отрисовки
        margin_left = 50
        margin_right = 20
        margin_top = 20
        margin_bottom = 30
        
        plot_width = canvas_width - margin_left - margin_right
        plot_height = canvas_height - margin_top - margin_bottom
        
        # Количество отображаемых элементов
        max_items = min(len(data), plot_width)
        
        if max_items == 0:
            return 0
        
        # Ширина одного столбца
        bar_width = plot_width / max_items
        
        # Конвертируем данные в числа
        numeric_data = [float(x) for x in data]
        
        # Нормализация значений
        max_val = max(numeric_data) if numeric_data else 1
        min_val = min(numeric_data) if numeric_data else 0
        
        if max_val == min_val:
            max_val = min_val + 1
        
        # Рисуем оси
        canvas.create_line(margin_left, margin_top, margin_left, canvas_height - margin_bottom, fill='white', width=2)
        canvas.create_line(margin_left, canvas_height - margin_bottom, canvas_width - margin_right, canvas_height - margin_bottom, fill='white', width=2)
        
        # Подписи осей
        canvas.create_text(margin_left - 5, margin_top, text=f"{max_val:.1f}", anchor='e', fill='white', font=('Arial', 8))
        canvas.create_text(margin_left - 5, canvas_height - margin_bottom, text=f"{min_val:.1f}", anchor='e', fill='white', font=('Arial', 8))
        canvas.create_text(canvas_width / 2, canvas_height - 5, text="Индекс", fill='white', font=('Arial', 10))
        canvas.create_text(margin_left - 15, canvas_height / 2, text="Значение", fill='white', font=('Arial', 10), angle=90)
        
        # Рисуем столбцы
        drawn = 0
        for i in range(max_items):
            if i >= len(numeric_data):
                break
            
            value = numeric_data[i]
            
            # Нормализуем высоту
            height = (value - min_val) / (max_val - min_val) * plot_height
            if height < 1:
                height = 1
            
            # Вычисляем координаты
            x1 = margin_left + i * bar_width
            x2 = x1 + bar_width - 1
            y1 = canvas_height - margin_bottom - height
            y2 = canvas_height - margin_bottom
            
            # Определяем цвет
            try:
                color_idx = hmm.predict(i % mod) % len(colors)
            except:
                color_idx = (i % mod) % len(colors)
            
            color = colors[color_idx]
            
            # Рисуем прямоугольник
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)
            drawn += 1
        
        return drawn
    



    def draw_spiral_canvas(self, canvas, squares, hmm, mod):
        """Рисует спираль Фибоначчи на Canvas"""
        if not squares:
            return
        
        canvas.delete("all")
        
        # Получаем размеры canvas
        canvas.update_idletasks()
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        
        if canvas_width <= 1:
            canvas_width = 600
            canvas_height = 600
            canvas.config(width=canvas_width, height=canvas_height)
        
        # Находим границы всех квадратов
        all_x = []
        all_y = []
        
        for square in squares:
            if isinstance(square, dict):
                all_x.append(square.get('x1', 0))
                all_x.append(square.get('x2', 0))
                all_y.append(square.get('y1', 0))
                all_y.append(square.get('y2', 0))
        
        if not all_x or not all_y:
            return
        
        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)
        
        # Вычисляем размер спирали
        spiral_width = max_x - min_x
        spiral_height = max_y - min_y
        spiral_size = max(spiral_width, spiral_height)
        
        # Отступ от краев canvas (в пикселях)
        margin = 20
        
        # Вычисляем масштаб, чтобы спираль поместилась в canvas
        available_width = canvas_width - 2 * margin
        available_height = canvas_height - 2 * margin
        available_size = min(available_width, available_height)
        
        # Масштабируем так, чтобы спираль занимала 80% доступного пространства
        scale = (available_size * 0.8) / spiral_size if spiral_size > 0 else 1
        
        # Вычисляем смещение для центрирования
        spiral_center_x = (min_x + max_x) / 2
        spiral_center_y = (min_y + max_y) / 2
        
        canvas_center_x = canvas_width / 2
        canvas_center_y = canvas_height / 2
        
        offset_x = canvas_center_x - spiral_center_x * scale
        offset_y = canvas_center_y - spiral_center_y * scale
        
        # Цвета для разных состояний HMM
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F39C12', '#E74C3C', '#2ECC71']
        
        # Рисуем квадраты от последнего к первому (чтобы большие квадраты были на заднем плане)
        for square in reversed(squares):
            if not isinstance(square, dict):
                continue
            
            x1 = square.get('x1', 0)
            y1 = square.get('y1', 0)
            x2 = square.get('x2', 0)
            y2 = square.get('y2', 0)
            index = square.get('index', 0)
            
            # Масштабируем
            x1_s = x1 * scale + offset_x
            y1_s = y1 * scale + offset_y
            x2_s = x2 * scale + offset_x
            y2_s = y2 * scale + offset_y
            
            # Проверяем, что квадрат видим
            if x2_s < 0 or x1_s > canvas_width or y2_s < 0 or y1_s > canvas_height:
                continue
            
            # ИСПРАВЛЕНО: Цвет на основе HMM модели
            # Используем ТОЛЬКО индекс, без mod, чтобы каждая модель давала свой паттерн
            state = hmm.predict(index)  # <--- ЭТО ГЛАВНОЕ ИЗМЕНЕНИЕ
            color_idx = state % len(colors)
            color = colors[color_idx]
            
            # Рисуем квадрат с полупрозрачной заливкой для лучшей видимости
            canvas.create_rectangle(x1_s, y1_s, x2_s, y2_s, 
                                outline='white', fill=color, width=2, stipple='gray25')
            
            # Рисуем дугу (часть спирали)
            arc_coords = square.get('arc_coords')
            arc_start = square.get('arc_start', 0)
            
            if arc_coords and len(arc_coords) == 4:
                ax1, ay1, ax2, ay2 = arc_coords
                ax1_s = ax1 * scale + offset_x
                ay1_s = ay1 * scale + offset_y
                ax2_s = ax2 * scale + offset_x
                ay2_s = ay2 * scale + offset_y
                
                # Рисуем дугу - основную линию спирали
                canvas.create_arc(ax1_s, ay1_s, ax2_s, ay2_s,
                                start=arc_start, extent=90,
                                outline='yellow', width=3, style=tk.ARC)
        
        # Добавляем информационную надпись с названием модели
        model_name = hmm.current_model
        model_desc = hmm.get_model_names().get(model_name, model_name)
        info_text = f"Модель: {model_desc} | Квадратов: {len(squares)} | Масштаб: {scale:.2f}"
        canvas.create_text(10, 20, anchor='nw', text=info_text, 
                        fill='white', font=('Arial', 10))
class Visualizer2D:
    """Визуализатор для 2D объектов"""
    
    def __init__(self):
        self.function2d = None
    
    def set_function(self, function2d):
        self.function2d = function2d
    
    def draw_heatmap(self, canvas, data, width=600, height=500):
        """Рисует тепловую карту"""
        canvas.delete("all")
        
        if not data:
            return
        
        canvas.config(width=width, height=height)
        
        # Находим диапазоны
        x_vals = list(set([p[0] for p in data]))
        y_vals = list(set([p[1] for p in data]))
        z_vals = [p[2] for p in data]
        
        x_vals.sort()
        y_vals.sort()
        
        z_min, z_max = min(z_vals), max(z_vals)
        
        if z_min == z_max:
            z_max = z_min + 1
        
        # Размеры ячейки
        margin = 60
        cell_width = (width - 2 * margin) / len(x_vals)
        cell_height = (height - 2 * margin) / len(y_vals)
        
        # Создаем словарь для быстрого доступа
        z_dict = {(p[0], p[1]): p[2] for p in data}
        
        # Рисуем сетку
        for i, x in enumerate(x_vals):
            for j, y in enumerate(y_vals):
                z = z_dict.get((x, y), z_min)
                
                # Нормализуем значение для цвета
                ratio = (z - z_min) / (z_max - z_min)
                r = int(ratio * 255)
                g = int((1 - abs(ratio - 0.5) * 2) * 255)
                b = int((1 - ratio) * 255)
                color = f'#{r:02x}{g:02x}{b:02x}'
                
                x1 = margin + i * cell_width
                y1 = margin + j * cell_height
                x2 = x1 + cell_width
                y2 = y1 + cell_height
                
                canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='gray')
                
                # Добавляем значение
                if cell_width > 20 and cell_height > 15:
                    canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, 
                                      text=f"{z:.1f}", fill='white', font=('Arial', 8))
        
        # Рисуем оси
        canvas.create_line(margin, margin, margin, height - margin, fill='white', width=2)
        canvas.create_line(margin, height - margin, width - margin, height - margin, fill='white', width=2)
        
        # Подписи
        for i, x in enumerate(x_vals):
            canvas.create_text(margin + i * cell_width + cell_width / 2, height - margin + 15, 
                              text=str(x), fill='white', font=('Arial', 8))
        
        for j, y in enumerate(y_vals):
            canvas.create_text(margin - 10, margin + j * cell_height + cell_height / 2, 
                              text=str(y), fill='white', font=('Arial', 8))
        
        canvas.create_text(width / 2, height - 10, text="X", fill='white', font=('Arial', 12))
        canvas.create_text(20, height / 2, text="Y", fill='white', font=('Arial', 12), angle=90)
    
    def draw_3d_projection(self, canvas, data, width=600, height=500):
        """Рисует 3D проекцию"""
        canvas.delete("all")
        
        if not data:
            return
        
        canvas.config(width=width, height=height)
        
        # Находим диапазоны
        z_vals = [p[2] for p in data]
        z_min, z_max = min(z_vals), max(z_vals)
        
        if z_min == z_max:
            z_max = z_min + 1
        
        # Центр
        center_x = width / 2
        center_y = height / 2
        
        # Функция проекции
        def project(x, y, z):
            angle = 0.7854  # 45 градусов
            scale = 2
            x_proj = center_x + (x - y) * scale
            y_proj = center_y + (x + y) * scale / 2 - (z - z_min) * 3
            return x_proj, y_proj
        
        # Рисуем линии и точки
        for x, y, z in data:
            x_proj, y_proj = project(x, y, z)
            
            # Цвет
            ratio = (z - z_min) / (z_max - z_min)
            r = int(ratio * 255)
            g = int((1 - abs(ratio - 0.5) * 2) * 255)
            b = int((1 - ratio) * 255)
            color = f'#{r:02x}{g:02x}{b:02x}'
            
            # Размер точки
            size = 4 + ratio * 6
            
            # Рисуем точку
            canvas.create_oval(x_proj - size, y_proj - size,
                              x_proj + size, y_proj + size,
                              fill=color, outline='white', width=1)
            
            # Рисуем линию вниз
            _, ground_y = project(x, y, z_min)
            canvas.create_line(x_proj, y_proj, x_proj, ground_y,
                              fill='#444444', width=1, dash=(2, 2))
    
    def add_3d_legend(self, canvas, z_min, z_max, width):
        """Добавляет легенду для 3D графика"""
        legend_x = width - 80
        legend_y = 20
        legend_height = 100
        
        for i in range(legend_height):
            ratio = i / legend_height
            r = int(ratio * 255)
            g = int((1 - abs(ratio - 0.5) * 2) * 255)
            b = int((1 - ratio) * 255)
            color = f'#{r:02x}{g:02x}{b:02x}'
            canvas.create_line(legend_x, legend_y + i, legend_x + 20, legend_y + i, fill=color, width=1)
        
        canvas.create_text(legend_x + 10, legend_y - 5, text=f"{z_max:.1f}", fill='white', font=('Arial', 8))
        canvas.create_text(legend_x + 10, legend_y + legend_height + 5, text=f"{z_min:.1f}", fill='white', font=('Arial', 8))