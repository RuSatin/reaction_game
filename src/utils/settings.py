"""
Модуль с настройками игры
"""

# Настройки окна
WINDOW = {
    "title": "Тренировка реакции",
    "width": 800,
    "height": 600
}

# Настройки игры
GAME = {
    "shape_size": 50,
    "spawn_delay": {
        "easy": 2000,
        "medium": 1500,
        "hard": 1000
    },
    "points": {
        "min": 10,
        "max": 100
    }
}

# Настройки анимации
ANIMATION = {
    "speed": 20,
    "steps": 10,
    "flash_radius": 50,
    "flash_rings": 3
}

# Настройки прогрессии
PROGRESSION = {
    # Очки для перехода на следующий уровень
    "difficulty_thresholds": {
        "easy": 5000,     # После 5000 очков -> medium
        "medium": 10000,  # После 10000 очков -> hard
    },
    
    # Очки для добавления режимов
    "mode_thresholds": {
        "color": 0,       # Доступен сразу
        "shape": 7000,    # После 7000 очков
        "sound": 15000    # После 15000 очков
    },
    
    # Порядок режимов и сложности
    "mode_order": ["color", "shape", "sound"],
    "difficulty_order": ["easy", "medium", "hard"],
    
    # Шанс смены режима (0-1)
    "mode_change_chance": 0.3
}

# Локализация
LOCALIZATION = {
    "modes": {
        "color": "Цвета",
        "shape": "Фигуры",
        "sound": "Звуки"
    },
    "difficulties": {
        "easy": "Легкий",
        "medium": "Средний",
        "hard": "Сложный"
    },
    "buttons": {
        "menu": "Меню",
        "start": "Начать",
        "continue": "Продолжить",
        "settings": "Настройки"
    },
    "score": "Счет",
    "best_score": "Рекорд"
}