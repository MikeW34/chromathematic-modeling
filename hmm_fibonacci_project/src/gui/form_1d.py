"""
Форма для 1D объекта (числа Фибоначчи) - Упрощённая версия без Turtle
"""

import tkinter as tk
from tkinter import ttk, messagebox

from src.fibonacci import FibonacciGenerator
from src.hmm_module import HMM
from src.visualizer import Visualizer1D
from src.database import Database

class Form1D:
    """Форма для работы с числами Фибоначчи"""
    
    def __init__(self, parent):
        self.parent = parent
        self.hmm = HMM()
        self.fib_gen = FibonacciGenerator()
        self.visualizer = Visualizer1D()
        self.db = Database()
        
        self.create_widgets()
        self.load_default_data()
    
    def create_widgets(self):
        """Создаёт виджеты формы"""
        toolbar = ttk.LabelFrame(self.parent, text="Настройки моделирования (Объект 1D)")
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        ttk.Label(toolbar, text="Хромо-Модель:").pack(side=tk.LEFT, padx=5)
        self.model_select = ttk.Combobox(toolbar, 
                                        values=self.hmm.get_available_models(),
                                        state="readonly", width=15)
        self.model_select.current(0)
        self.model_select.pack(side=tk.LEFT, padx=5)
        self.model_select.bind('<<ComboboxSelected>>', self.on_model_change)
        
        ttk.Label(toolbar, text="Модуль:").pack(side=tk.LEFT, padx=(20, 5))
        self.mod_entry = ttk.Entry(toolbar, width=5)
        self.mod_entry.insert(0, "10")
        self.mod_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(toolbar, text="Кол-во:").pack(side=tk.LEFT, padx=(20, 5))
        self.count_entry = ttk.Entry(toolbar, width=8)
        self.count_entry.insert(0, "600")
        self.count_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(toolbar, text="Ленточная диаграмма", 
                  command=self.draw_ribbon).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Спираль (Canvas)", 
                  command=self.draw_spiral_canvas).pack(side=tk.LEFT, padx=5)
        
        # Кнопка turtle временно скрыта
        # ttk.Button(toolbar, text="Спираль (Turtle)", 
        #           command=self.draw_turtle_spiral).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(toolbar, text="Заполнить БД (1000+)", 
                  command=self.fill_database).pack(side=tk.LEFT, padx=5)
        
        self.info_label = ttk.Label(self.parent, 
                                    text="Текущая модель: Parity (чередование по позиции)",
                                    relief=tk.SUNKEN, anchor=tk.W)
        self.info_label.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        
        self.canvas = tk.Canvas(self.parent, bg="#1a1a1a")
        self.canvas.pack(pady=10, expand=True, fill=tk.BOTH)
    
    def load_default_data(self):
        try:
            mod = int(self.mod_entry.get())
            count = int(self.count_entry.get())
            self.data = self.fib_gen.get_fibonacci_mod(count, mod)
            self.draw_ribbon()
        except Exception as e:
            print(f"Ошибка загрузки данных: {e}")
    
    def fill_database(self):
        try:
            mod = int(self.mod_entry.get())
            count = 1000
            data = self.fib_gen.get_fibonacci_mod(count, mod)
            
            with self.db.connect():
                self.db.insert_fibonacci_data(data, mod)
            
            self.info_label.config(text=f"БД заполнена: {len(data)} чисел Фибоначчи по модулю {mod}")
            messagebox.showinfo("Успех", f"В БД добавлено {len(data)} значений")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось заполнить БД: {e}")
    
    def on_model_change(self, event=None):
        try:
            self.hmm.set_model(self.model_select.get())
            model_names = self.hmm.get_model_names()
            self.info_label.config(text=f"Текущая модель: {model_names.get(self.hmm.current_model, self.hmm.current_model)}")
            self.draw_ribbon()
        except Exception as e:
            print(f"Ошибка смены модели: {e}")
    
    def draw_ribbon(self):
        try:
            mod = int(self.mod_entry.get())
            if mod <= 0:
                raise ValueError("Модуль должен быть положительным")
            
            count = min(int(self.count_entry.get()), 600)
            if count <= 0:
                raise ValueError("Количество должно быть положительным")
            
            self.data = self.fib_gen.get_fibonacci_mod(count, mod)
            drawn = self.visualizer.draw_ribbon(self.canvas, self.data, self.hmm, mod)
            self.info_label.config(text=f"{self.info_label.cget('text')} | Отображено: {drawn} чисел")
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось отобразить: {e}")
    
    def draw_spiral_canvas(self):
        try:
            mod = int(self.mod_entry.get())
            n_terms = 12
            squares = self.fib_gen.get_fibonacci_spiral_coordinates(n_terms, size_factor=3)
            self.visualizer.draw_spiral_canvas(self.canvas, squares, self.hmm, mod)
            self.info_label.config(text=f"Спираль Фибоначчи (n={n_terms}) - модель: {self.hmm.current_model}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось нарисовать спираль: {e}")

