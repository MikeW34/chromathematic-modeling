"""
Диалоговые окна: Справка и О программе
"""

import tkinter as tk
from tkinter import ttk

class HelpDialog(tk.Toplevel):
    """Немодальное окно справки"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Справка - Хромоматематическое моделирование")
        self.geometry("600x500")
        self.minsize(500, 400)
        
        # Создаём виджеты
        self.create_widgets()
        
        # Делаем окно видимым
        self.transient(parent)
        self.grab_set()
    
    def create_widgets(self):
        """Создаёт содержимое окна справки"""
        # Заголовок
        title_label = ttk.Label(self, text="Справочная система", 
                                font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Создаём текстовую область с прокруткой
        frame = ttk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text = tk.Text(frame, wrap=tk.WORD, yscrollcommand=scrollbar.set,
                            font=("Arial", 10))
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.text.yview)
        
        # Заполняем содержимое
        self.fill_content()
        
        # Делаем текст только для чтения
        self.text.config(state=tk.DISABLED)
        
        # Кнопка закрытия
        close_btn = ttk.Button(self, text="Закрыть", command=self.destroy)
        close_btn.pack(pady=10)
    
    def fill_content(self):
        """Заполняет содержимое справки"""
        content = """
╔══════════════════════════════════════════════════════════════════╗
║              ХРОМОМАТЕМАТИЧЕСКОЕ МОДЕЛИРОВАНИЕ                  ║
║                         Вариант №1                               ║
╚══════════════════════════════════════════════════════════════════╝

ОБЪЕКТ 1D: ЧИСЛА ФИБОНАЧЧИ ПО МОДУЛЮ
═══════════════════════════════════════════════════════════════════

Последовательность Фибоначчи:
    F(0) = 0
    F(1) = 1
    F(n) = F(n-1) + F(n-2) для n >= 2

По модулю N: F(n) mod N


ДОСТУПНЫЕ ХРОМОМАТЕМАТИЧЕСКИЕ МОДЕЛИ (1D)
═══════════════════════════════════════════════════════════════════

1. Parity (чередование по позиции)
   • Оранжевый (#FF5733) - чётные позиции (0,2,4...)
   • Зелёный (#33FF57) - нечётные позиции (1,3,5...)

2. Value Parity (чётность значения)
   • Оранжевый - чётные значения чисел
   • Зелёный - нечётные значения чисел

3. Modulo Gradient (градиент по модулю)
   • Синий (0) → Красный (mod-1)

4. Golden Ratio (золотое сечение)
   • Цвета на основе золотого сечения φ = 1.618


ОБЪЕКТ 2D: ФУНКЦИЯ Z = |X+Y| - |X-Y|
═══════════════════════════════════════════════════════════════════

Функция определена для X, Y из R

Свойства функции:
    • Z = 2*min(|X|,|Y|) при X*Y >= 0
    • Z = 0 при X*Y < 0

Примеры:
    • X=5, Y=3  → |8| - |2| = 6
    • X=5, Y=-3 → |2| - |8| = -6
    • X=0, Y=0  → 0 - 0 = 0


ДОСТУПНЫЕ ВИЗУАЛИЗАЦИИ (2D)
═══════════════════════════════════════════════════════════════════

1. Тепловая карта (Heatmap)
   • Цветовое кодирование значений Z
   • Синий - минимальное Z, Красный - максимальное Z

2. 3D проекция
   • Изометрическое отображение поверхности


ИНТЕРФЕЙС ПРОГРАММЫ
═══════════════════════════════════════════════════════════════════

Объект 1D:
    • Модель - выбор цветовой модели
    • Модуль - модуль для чисел Фибоначчи
    • Кол-во - количество отображаемых чисел
    • Ленточная диаграмма - цветные квадраты
    • Спираль (Canvas) - классическая спираль
    • Спираль (Turtle) - симметричная спираль

Объект 2D:
    • X от/до, Y от/до - диапазон аргументов
    • Шаг - дискретность сетки
    • Тепловая карта - цветовое отображение Z
    • 3D проекция - объёмное отображение
"""
        self.text.insert(tk.END, content)


class AboutDialog(tk.Toplevel):
    """Модальное окно 'О программе'"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.title("О программе")
        self.geometry("400x350")
        self.resizable(False, False)
        
        # Делаем окно модальным
        self.transient(parent)
        self.grab_set()
        
        # Центрируем окно
        self.center_on_parent(parent)
        
        self.create_widgets()
    
    def center_on_parent(self, parent):
        """Центрирует окно относительно родительского"""
        self.update_idletasks()
        
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        
        width = self.winfo_width()
        height = self.winfo_height()
        
        x = parent_x + (parent_width - width) // 2
        y = parent_y + (parent_height - height) // 2
        
        self.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_widgets(self):
        """Создаёт содержимое окна"""
        # Логотип (текстовый)
        logo_frame = ttk.Frame(self)
        logo_frame.pack(pady=20)
        
        logo_text = tk.Text(logo_frame, height=5, width=40, font=("Courier", 8), 
                            bg=self.cget('bg'), bd=0)
        logo_text.insert(tk.END, r"""""")
        logo_text.config(state=tk.DISABLED)
        logo_text.pack()
        
        # Информация
        info_frame = ttk.Frame(self)
        info_frame.pack(pady=5, padx=5, fill=tk.BOTH)
        
        info_text = f"""
Благодарности родителям: Спасибо Любви Алексеевне 
и Денису Сергеевичу
Объект 1D:    Числа Фибоначчи по модулю
Объект 2D:    |X+Y| - |X-Y|

Версия:       1.0.0
Год:          2026

Разработчик:  Студент группы __БСБО-22-24___
Дисциплина:   Методы и средства разработки
              компонент программного обеспечения
Учебное заведение:  РТУ МИРЭА
"""
        info_label = ttk.Label(info_frame, text=info_text, justify=tk.LEFT)
        info_label.pack()
        
        # Кнопка OK
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=20)
        
        ok_btn = ttk.Button(btn_frame, text="OK", command=self.destroy)
        ok_btn.pack()
        
        # Назначаем Enter на кнопку OK
        self.bind('<Return>', lambda e: self.destroy())
        self.bind('<Escape>', lambda e: self.destroy())
