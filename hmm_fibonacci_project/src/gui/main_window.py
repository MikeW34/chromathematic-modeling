"""
Главное окно программы
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Добавляем путь для импорта модулей
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.gui.form_1d import Form1D
from src.gui.form_2d import Form2D
from src.gui.dialogs import AboutDialog, HelpDialog

class MainWindow:
    """Главное окно приложения"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Хромоматематическое моделирование - Вариант №1")
        self.root.geometry("1200x1200")
        self.root.minsize(1000, 640)
        
        # Создаём меню
        self.create_menu()
        
        # Создаём основную область с вкладками
        self.create_notebook()
        
        # Создаём строку статуса
        self.create_statusbar()
    
    def create_menu(self):
        """Создаёт главное меню"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Меню Файл
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Экспорт изображения", command=self.export_image)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)
        
        # Меню Модели
        models_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Модели", menu=models_menu)
        models_menu.add_command(label="Объект 1D (Фибоначчи)", command=self.show_1d_models)
        models_menu.add_command(label="Объект 2D (|X+Y|-|X-Y|)", command=self.show_2d_models)
        
        # Меню Справка
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="Содержание", command=self.show_help)
        help_menu.add_separator()
        help_menu.add_command(label="О программе", command=self.show_about)
    
    def create_notebook(self):
        """Создаёт вкладки для 1D и 2D объектов"""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Вкладка 1D
        self.tab_1d = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_1d, text="Объект 1D: Числа Фибоначчи по модулю")
        self.form_1d = Form1D(self.tab_1d)
        
        # Вкладка 2D
        self.tab_2d = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_2d, text="Объект 2D: |X+Y| - |X-Y|")
        self.form_2d = Form2D(self.tab_2d)
    
    def create_statusbar(self):
        """Создаёт строку статуса"""
        self.statusbar = ttk.Label(self.root, text="Готово", relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def export_image(self):
        """Экспортирует текущее изображение"""
        messagebox.showinfo("Экспорт", "Функция экспорта будет добавлена")
    
    def show_1d_models(self):
        """Показывает информацию о моделях 1D"""
        messagebox.showinfo("Модели 1D",
            "Доступные хромоматематические модели для Объекта 1D:\n\n"
            "1. Parity - цвет от чётности позиции\n"
            "2. Value Parity - цвет от чётности значения\n"
            "3. Modulo Gradient - градиент по модулю\n"
            "4. Golden Ratio - цвета на основе золотого сечения")
    
    def show_2d_models(self):
        """Показывает информацию о моделях 2D"""
        messagebox.showinfo("Модели 2D",
            "Доступные хромоматематические модели для Объекта 2D:\n\n"
            "1. Тепловая карта (Heatmap) - цветовое кодирование Z\n"
            "2. 3D проекция - изометрическое отображение")
    
    def show_help(self):
        """Показывает справочную систему"""
        HelpDialog(self.root)
    
    def show_about(self):
        """Показывает окно 'О программе'"""
        AboutDialog(self.root)
    
    def set_status(self, text):
        """Устанавливает текст в строке статуса"""
        self.statusbar.config(text=text)
