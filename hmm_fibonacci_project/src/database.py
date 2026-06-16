"""
Модуль для работы с базой данных
"""

import sqlite3
import os

class Database:
    """Класс для управления базой данных"""
    
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'fibonacci.db')
        
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        
        # Создаём директорию для БД если её нет
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    def connect(self):
        """Устанавливает соединение с БД"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        return self
    
    def disconnect(self):
        """Закрывает соединение с БД"""
        if self.conn:
            self.conn.close()
        self.conn = None
        self.cursor = None
    
    def init_fibonacci_table(self):
        """Создаёт таблицу для чисел Фибоначчи"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS fibonacci (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                position INTEGER,
                value INTEGER,
                value_mod INTEGER,
                mod_value INTEGER
            )
        ''')
        self.conn.commit()
    
    def init_function2d_table(self):
        """Создаёт таблицу для 2D функции"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS function2d (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                x INTEGER,
                y INTEGER,
                z INTEGER
            )
        ''')
        self.conn.commit()
    
    def insert_fibonacci_data(self, data, mod):
        """
        Вставляет данные Фибоначчи в БД
        
        Args:
            data: список значений
            mod: модуль
        """
        self.init_fibonacci_table()
        self.cursor.execute('DELETE FROM fibonacci')
        
        for i, val in enumerate(data):
            self.cursor.execute(
                'INSERT INTO fibonacci (position, value, value_mod, mod_value) VALUES (?, ?, ?, ?)',
                (i, int(val), int(val) % mod if mod > 0 else int(val), mod)
            )
        self.conn.commit()
    
    def insert_function2d_data(self, data):
        """Вставляет данные 2D функции в БД"""
        self.init_function2d_table()
        self.cursor.execute('DELETE FROM function2d')
        
        for x, y, z in data:
            self.cursor.execute(
                'INSERT INTO function2d (x, y, z) VALUES (?, ?, ?)',
                (x, y, z)
            )
        self.conn.commit()
    
    def get_fibonacci_data(self, limit=1000):
        """Получает данные Фибоначчи из БД"""
        self.cursor.execute('SELECT position, value, value_mod FROM fibonacci LIMIT ?', (limit,))
        return self.cursor.fetchall()
    
    def get_function2d_data(self, limit=1000):
        """Получает данные 2D функции из БД"""
        self.cursor.execute('SELECT x, y, z FROM function2d LIMIT ?', (limit,))
        return self.cursor.fetchall()
    
    def get_fibonacci_count(self):
        """Возвращает количество записей в таблице fibonacci"""
        self.cursor.execute('SELECT COUNT(*) FROM fibonacci')
        return self.cursor.fetchone()[0]
    
    def clear_all(self):
        """Очищает все таблицы"""
        self.cursor.execute('DELETE FROM fibonacci')
        self.cursor.execute('DELETE FROM function2d')
        self.conn.commit()
    
    def __enter__(self):
        return self.connect()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
