"""
Модуль с настройками игры
"""

# Настройки анимации
ANIMATION_SPEED = 10  # мс между кадрами
ANIMATION_STEPS = 10  # количество кадров

# Настройки окна
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800

# Настройки игры
SHAPE_SIZE = 100
MAX_FLASH_RADIUS = 50
FLASH_RINGS = 5

# Очки за сложность
DIFFICULTY_POINTS = {
    "easy": 1000,
    "medium": 1200,
    "hard": 1500
}

# Задержки для разных уровней сложности (в мс)
DELAYS = {
    "easy": (1500, 3000),  # 1.5-3 секунды
    "medium": (1000, 2000),  # 1-2 секунды
    "hard": (500, 1500)  # 0.5-1.5 секунды
}

# Названия режимов
MODE_NAMES = {
    "color": "Цвет",
    "shape": "Фигура",
    "sound": "Звук"
}

# Названия уровней сложности
DIFFICULTY_NAMES = {
    "easy": "Легкий",
    "medium": "Средний",
    "hard": "Сложный"
} 