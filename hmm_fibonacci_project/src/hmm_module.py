"""
Модуль HMM (Хромоматематические модели)
"""

class HMM:
    """Класс хромоматематических моделей"""
    
    def __init__(self):
        self.current_model = "Parity"
        self.available_models = ["Parity", "Value Parity", "Modulo Gradient", "Golden Ratio"]
        self.model_names = {
            "Parity": "Parity (чередование по позиции)",
            "Value Parity": "Value Parity (чётность значения)",
            "Modulo Gradient": "Modulo Gradient (градиент по модулю)",
            "Golden Ratio": "Golden Ratio (золотое сечение)"
        }
    
    def _validate_color(self, color):
        """Проверяет и исправляет цвет"""
        if color and len(color) == 7 and color.startswith('#'):
            return color
        return "#CCCCCC"  # серый по умолчанию
    
    def model_color_parity(self, index):
        """Модель Parity: цвет от чётности позиции"""
        return "#FF5733" if index % 2 == 0 else "#33FF57"
    
    def model_color_value_parity(self, val):
        """Модель Value Parity: цвет от чётности значения"""
        value = int(val) if isinstance(val, str) else val
        return "#FF5733" if value % 2 == 0 else "#33FF57"
    
    def model_color_modulo(self, val, mod):
        """Модель Modulo Gradient: градиент от синего к красному"""
        value = int(val) if isinstance(val, str) else val
        mod = max(mod, 1)  # защита от деления на ноль
        remainder = value % mod
        ratio = remainder / mod
        # Ограничиваем ratio в пределах [0, 1]
        ratio = max(0, min(1, ratio))
        r = int(255 * ratio)
        b = int(255 * (1 - ratio))
        # Убеждаемся что значения в пределах 0-255
        r = max(0, min(255, r))
        b = max(0, min(255, b))
        return f"#{r:02x}00{b:02x}"
    
    def model_color_golden_ratio(self, index):
        """Модель Golden Ratio: цвета на основе золотого сечения"""
        phi = 1.618033988749895
        hue = (index * phi) % 1.0
        hue = max(0, min(1, hue))
        r = int(255 * abs(hue * 6 - 3) / 3)
        g = int(255 * (1 - abs(hue * 6 - 2) / 2))
        b = int(255 * (1 - abs(hue * 6 - 4) / 2))
        # Ограничиваем значения
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def get_available_models(self):
        return self.available_models
    
    def get_model_names(self):
        return self.model_names
    
    def apply_model(self, model_name, value, index, mod=10):
        """Применяет выбранную модель"""
        try:
            if model_name == "Parity":
                return self.model_color_parity(index)
            elif model_name == "Value Parity":
                return self.model_color_value_parity(value)
            elif model_name == "Modulo Gradient":
                return self.model_color_modulo(value, mod)
            elif model_name == "Golden Ratio":
                return self.model_color_golden_ratio(index)
            else:
                return self.model_color_parity(index)
        except Exception as e:
            print(f"Ошибка в модели {model_name}: {e}")
            return "#CCCCCC"  # серый при ошибке
    
    def set_model(self, model_name):
        if model_name in self.available_models:
            self.current_model = model_name
            return True
        return False
    def predict(self, index):
        """Предсказывает состояние для данного индекса"""
        # Убеждаемся, что index - число
        try:
            idx = int(index)
        except:
            idx = 0
        
        if self.current_model == "parity":
            return idx % 2
        elif self.current_model == "mod3":
            return idx % 3
        elif self.current_model == "mod4":
            return idx % 4
        elif self.current_model == "fib_pattern":
            if idx < 2:
                return idx
            a, b = 0, 1
            for _ in range(idx):
                a, b = b, a + b
            return a % 3
        else:
            return idx % 2
    def print_model_pattern(self, n=20):
        """Выводит паттерн модели для первых n индексов"""
        pattern = []
        for i in range(n):
            pattern.append(str(self.predict(i)))
        print(f"Модель {self.current_model}: {' '.join(pattern)}")