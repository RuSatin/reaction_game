"""
Скрипт для запуска игры
"""
import sys
import os

# Добавляем путь к src в PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from main import ReactionTrainer

if __name__ == "__main__":
    try:
        print("Игра запущена")
        app = ReactionTrainer()
        app.run()
        print("Выход из игры")
    except Exception as e:
        import traceback
        print(f"Возникла ошибка: {e}")
