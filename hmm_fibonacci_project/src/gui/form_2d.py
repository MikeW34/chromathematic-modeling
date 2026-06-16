"""
Форма для 2D объекта (функция Z = |X+Y| - |X-Y|)
"""

import tkinter as tk
from tkinter import ttk, messagebox

from src.function2d import Function2D
from src.visualizer import Visualizer2D
from src.database import Database

class Form2D:
    """Форма для работы с 2D функцией"""
    
    def __init__(self, parent):
        self.parent = parent
        self.function2d = Function2D()
        self.visualizer = Visualizer2D()
        self.db = Database()
        self.data = []
        
        # Связываем визуализатор с функцией
        self.visualizer.set_function(self.function2d)
        
        self.create_widgets()
    
    def create_widgets(self):
        """Создаёт виджеты формы"""
        # Панель инструментов
        toolbar = ttk.LabelFrame(self.parent, text="Настройки моделирования (Объект 2D)")
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        # Диапазон X
        ttk.Label(toolbar, text="X от:").pack(side=tk.LEFT, padx=5)
        self.x_min_entry = ttk.Entry(toolbar, width=5)
        self.x_min_entry.insert(0, "-10")
        self.x_min_entry.pack(side=tk.LEFT, padx=2)
        
        ttk.Label(toolbar, text="до:").pack(side=tk.LEFT, padx=2)
        self.x_max_entry = ttk.Entry(toolbar, width=5)
        self.x_max_entry.insert(0, "10")
        self.x_max_entry.pack(side=tk.LEFT, padx=5)
        
        # Диапазон Y
        ttk.Label(toolbar, text="Y от:").pack(side=tk.LEFT, padx=5)
        self.y_min_entry = ttk.Entry(toolbar, width=5)
        self.y_min_entry.insert(0, "-10")
        self.y_min_entry.pack(side=tk.LEFT, padx=2)
        
        ttk.Label(toolbar, text="до:").pack(side=tk.LEFT, padx=2)
        self.y_max_entry = ttk.Entry(toolbar, width=5)
        self.y_max_entry.insert(0, "10")
        self.y_max_entry.pack(side=tk.LEFT, padx=5)
        
        # Шаг
        ttk.Label(toolbar, text="Шаг:").pack(side=tk.LEFT, padx=5)
        self.step_entry = ttk.Entry(toolbar, width=3)
        self.step_entry.insert(0, "1")
        self.step_entry.pack(side=tk.LEFT, padx=5)
        
        # Кнопки визуализации
        ttk.Button(toolbar, text="Тепловая карта", 
                  command=self.draw_heatmap).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="3D проекция", 
                  command=self.draw_3d).pack(side=tk.LEFT, padx=5)
        
        # Кнопка заполнения БД
        ttk.Button(toolbar, text="Заполнить БД (1000+)", 
                  command=self.fill_database).pack(side=tk.LEFT, padx=20)
        
        # Информационная панель
        self.info_label = ttk.Label(self.parent, 
                                    text=f"Функция: {self.function2d.get_description()}",
                                    relief=tk.SUNKEN, anchor=tk.W)
        self.info_label.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        
        # Canvas для рисования
        self.canvas = tk.Canvas(self.parent, bg="#1a1a1a")
        self.canvas.pack(pady=10, expand=True, fill=tk.BOTH)
        
        # Загружаем начальные данные
        self.generate_data()
    
    def get_parameters(self):
        """Получает параметры из полей ввода"""
        try:
            x_min = int(self.x_min_entry.get())
            x_max = int(self.x_max_entry.get())
            y_min = int(self.y_min_entry.get())
            y_max = int(self.y_max_entry.get())
            step = int(self.step_entry.get())
            
            if step <= 0:
                raise ValueError("Шаг должен быть положительным")
            
            return x_min, x_max, y_min, y_max, step
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Некорректные параметры: {e}")
            return None
    
    def generate_data(self):
        """Генерирует данные для визуализации"""
        params = self.get_parameters()
        if params is None:
            return
        
        x_min, x_max, y_min, y_max, step = params
        
        # Генерируем сетку
        self.data = self.function2d.generate_grid(x_min, x_max, y_min, y_max, step)
        
        # Обновляем информацию
        z_min, z_max = self.function2d.get_z_range(self.data)
        self.info_label.config(text=f"{self.function2d.get_description()} | Диапазон Z: [{z_min}, {z_max}] | Точек: {len(self.data)}")
        
        return self.data
    
    def fill_database(self):
        """Заполняет БД данными (1000+ значений)"""
        try:
            # Генерируем случайные данные для БД
            data = self.function2d.generate_for_database(1000, (-100, 100), (-100, 100))
            
            with self.db.connect():
                self.db.insert_function2d_data(data)
            
            self.info_label.config(text=f"БД заполнена: {len(data)} значений {self.function2d.get_description()}")
            messagebox.showinfo("Успех", f"В БД добавлено {len(data)} значений")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось заполнить БД: {e}")
    
    def draw_heatmap(self):
        """Рисует тепловую карту"""
        if not self.generate_data():
            return
        
        self.visualizer.draw_heatmap(self.canvas, self.data, width=600, height=500)
        self.info_label.config(text=f"Тепловая карта | {self.info_label.cget('text')}")
    
    def draw_3d(self):
        if not self.generate_data():
            return
        # Очищаем canvas
        self.canvas.delete("all")
        
        # Создаём изометрическую проекцию
        import math
        
        # Параметры проекции
        center_x = self.canvas.winfo_width() // 2 if self.canvas.winfo_width() > 100 else 400
        center_y = self.canvas.winfo_height() // 2 if self.canvas.winfo_height() > 100 else 300
        
        # Находим диапазоны значений
        z_values = [point[2] for point in self.data]
        z_min, z_max = min(z_values), max(z_values)
        
        # Цветовая карта для высот
        colors = ['#0000FF', '#00FF00', '#FFFF00', '#FF0000']  # синий -> зеленый -> желтый -> красный
        
        def get_color(z):
            if z_max == z_min:
                return colors[0]
            ratio = (z - z_min) / (z_max - z_min)
            if ratio < 0.33:
                return '#0000FF'  # синий (низко)
            elif ratio < 0.66:
                return '#00FF00'  # зеленый (средне)
            else:
                return '#FF0000'  # красный (высоко)
        
        # Рисуем каждую точку как 3D-столбик
        for x, y, z in self.data:
            # Преобразуем координаты в изометрическую проекцию
            iso_x = center_x + (x - y) * 3
            iso_y = center_y + (x + y) * 1.5 - z * 2
            
            # Размер точки зависит от высоты
            size = max(3, min(8, int(z / (z_max - z_min + 1) * 10 + 3)))
            
            # Цвет зависит от высоты
            color = get_color(z)
            
            # Рисуем точку/круг
            self.canvas.create_oval(iso_x - size, iso_y - size, 
                                iso_x + size, iso_y + size,
                                fill=color, outline='white', width=1)
            
            # Рисуем линию вниз (для эффекта 3D)
            ground_y = center_y + (x + y) * 1.5
            self.canvas.create_line(iso_x, iso_y, iso_x, ground_y, 
                                fill='#444444', width=1, dash=(2, 2))
        
        # Добавляем легенду
        legend_y = 10
        self.canvas.create_text(10, legend_y, anchor='nw', 
                            text=f"Z: {z_min:.2f} (мин) -> {z_max:.2f} (макс)",
                            fill='white', font=('Arial', 10))
        
        self.info_label.config(text=f"3D изометрическая проекция | {self.info_label.cget('text')}")