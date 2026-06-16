#!/usr/bin/env python3
"""
Главный модуль приложения "Хромоматематическое моделирование"
Вариант №1: Объект 1D - Числа Фибоначчи по модулю, Объект 2D - |X+Y|-|X-Y|
"""

import tkinter as tk
import sys
import os

# Добавляем путь для импорта модулей
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.gui.main_window import MainWindow

def main():
    """Точка входа в приложение"""
    root = tk.Tk()
    
    app = MainWindow(root)
    
    # Центрируем окно
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()
