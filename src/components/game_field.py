"""
Модуль с компонентом игрового поля
"""
import tkinter as tk
import random
import time
from typing import Callable, Dict, Optional
from ..utils.colors import COLORS
from ..utils.settings import SHAPE_SIZE, DELAYS
from ..utils.animations import (
    create_gradient, animate_shape, 
    create_flash_effect, animate_text
)


class GameField:
    def __init__(self, parent: tk.Tk, on_menu_click: Callable):
        """
        Инициализация игрового поля
        
        :param parent: Родительское окно
        :param on_menu_click: Функция обратного вызова для кнопки меню
        """
        self.parent = parent
        self.frame = tk.Frame(parent, bg=COLORS['bg'])
        self.game_active = False
        self.start_time = 0
        self.current_score = 0
        self.best_score = 0
        self.game_mode = "color"
        self.difficulty = "medium"
        self.stimulus_id: Optional[str] = None
        
        self._create_widgets(on_menu_click)
        
    def _create_widgets(self, on_menu_click: Callable) -> None:
        """Создает виджеты игрового поля"""
        # Создаем верхнюю панель для счета
        score_panel = tk.Frame(self.frame, bg=COLORS['bg'])
        score_panel.pack(fill="x", padx=20, pady=5)

        # Лучший счет
        self.best_score_label = tk.Label(
            score_panel,
            text=f"Лучший: {self.best_score}",
            font=("Helvetica", 14, "bold"),
            bg=COLORS['bg'],
            fg=COLORS['text']
        )
        self.best_score_label.pack(side="left", padx=10)

        # Текущий счет
        self.current_score_label = tk.Label(
            score_panel,
            text=f"Текущий: {self.current_score}",
            font=("Helvetica", 14, "bold"),
            bg=COLORS['bg'],
            fg=COLORS['text']
        )
        self.current_score_label.pack(side="right", padx=10)

        # Создаем фрейм для игрового поля
        game_area_frame = tk.Frame(
            self.frame,
            bg=COLORS['bg']
        )
        game_area_frame.pack(expand=True, fill="both", padx=20, pady=10)

        # Игровое поле
        self.canvas = tk.Canvas(
            game_area_frame,
            bg="white",
            width=600,
            height=400,
            highlightthickness=0
        )
        self.canvas.pack(expand=True, fill="both")
        self.canvas.bind("<Button-1>", self._on_click)

        # Кнопка выхода в меню
        menu_button = tk.Button(
            self.frame,
            text="Меню",
            command=on_menu_click,
            font=("Helvetica", 12),
            bg=COLORS['button'],
            fg=COLORS['text'],
            relief='flat',
            width=10
        )
        menu_button.pack(pady=10)

    def show(self) -> None:
        """Показывает игровое поле"""
        self.frame.pack(expand=True, fill="both")

    def hide(self) -> None:
        """Скрывает игровое поле"""
        self.frame.pack_forget()

    def start_game(self, game_mode: str, difficulty: str,
                  current_score: int = 0, best_score: int = 0) -> None:
        """Начинает новую игру"""
        self.game_mode = game_mode
        self.difficulty = difficulty
        self.current_score = current_score
        self.best_score = best_score
        self.game_active = True
        self._update_score_labels()
        
        # Показать сообщение о начале игры
        self.canvas.delete("all")
        create_gradient(self.canvas, COLORS['bg'], COLORS['primary'])
        self.canvas.create_text(
            300, 200,
            text="Приготовьтесь!\nИгра начнется через 2 секунды...",
            font=("Arial", 16),
            justify="center",
            fill=COLORS['text']
        )
        self.parent.update()
        
        # Задержка перед первым стимулом
        self.parent.after(2000, self._schedule_stimulus)

    def stop_game(self) -> None:
        """Останавливает игру"""
        self.game_active = False
        if self.stimulus_id:
            self.parent.after_cancel(self.stimulus_id)
            self.stimulus_id = None

    def _schedule_stimulus(self) -> None:
        """Запланировать появление стимула"""
        if not self.game_active:
            return

        # Очистить холст
        self.canvas.delete("all")
        create_gradient(self.canvas, COLORS['bg'], COLORS['primary'])

        # Определить задержку в зависимости от сложности
        min_delay, max_delay = DELAYS[self.difficulty]
        delay = random.randint(min_delay, max_delay)

        # Запланировать появление стимула
        self.stimulus_id = self.parent.after(delay, self._show_stimulus)

    def _show_stimulus(self) -> None:
        """Показывает стимул в зависимости от режима"""
        if not self.game_active:
            return

        # Получить размеры холста
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Случайные координаты
        x = random.randint(SHAPE_SIZE, canvas_width - SHAPE_SIZE)
        y = random.randint(SHAPE_SIZE, canvas_height - SHAPE_SIZE)

        # Показать стимул в зависимости от режима
        shape_id = None
        if self.game_mode == "color":
            shape_id = self.canvas.create_rectangle(
                x - SHAPE_SIZE//2, y - SHAPE_SIZE//2,
                x + SHAPE_SIZE//2, y + SHAPE_SIZE//2,
                fill=COLORS['secondary'],
                outline="",
                tags="stimulus"
            )
        elif self.game_mode == "shape":
            shape_id = self.canvas.create_oval(
                x - SHAPE_SIZE//2, y - SHAPE_SIZE//2,
                x + SHAPE_SIZE//2, y + SHAPE_SIZE//2,
                fill=COLORS['highlight'],
                outline="",
                tags="stimulus"
            )
        else:  # sound
            points = [
                x, y - SHAPE_SIZE//2,
                x - SHAPE_SIZE//2, y + SHAPE_SIZE//2,
                x + SHAPE_SIZE//2, y + SHAPE_SIZE//2
            ]
            shape_id = self.canvas.create_polygon(
                points,
                fill=COLORS['secondary'],
                outline="",
                tags="stimulus"
            )
            self.parent.bell()

        # Анимация появления
        animate_shape(self.canvas, shape_id)
        
        # Запомнить время появления стимула
        self.start_time = time.time()

    def _on_click(self, event: tk.Event) -> None:
        """Обработчик клика по игровому полю"""
        if not self.game_active or self.start_time == 0:
            return

        # Проверить, кликнул ли пользователь по стимулу
        clicked_items = self.canvas.find_withtag("current")
        if clicked_items and "stimulus" in self.canvas.gettags(clicked_items[0]):
            # Создать эффект вспышки
            create_flash_effect(self.canvas, event.x, event.y, COLORS['highlight'])
            
            # Рассчитать время реакции
            reaction_time = (time.time() - self.start_time) * 1000

            # Начислить очки
            base_points = {
                "easy": 1000,
                "medium": 1200,
                "hard": 1500
            }.get(self.difficulty, 1000)

            points = max(0, int(base_points - reaction_time / 2))
            self.current_score += points

            if self.current_score > self.best_score:
                self.best_score = self.current_score

            # Обновить интерфейс
            self._update_score_labels()

            # Показать результат с анимацией
            self._show_result_animation(reaction_time, points)

            # Сбросить время начала
            self.start_time = 0

            # Запланировать следующий стимул
            self.parent.after(1000, self._schedule_stimulus)

    def _show_result_animation(self, reaction_time: float, points: int) -> None:
        """Показывает анимированный результат"""
        self.canvas.delete("all")
        create_gradient(self.canvas, COLORS['bg'], COLORS['primary'])

        # Создаем текст с результатом
        result_text = self.canvas.create_text(
            300, 200,
            text=f"Время реакции: {reaction_time:.0f} мс\nОчки: +{points}",
            font=("Arial", 24, "bold"),
            fill=COLORS['text'],
            justify="center",
            tags="result"
        )

        # Анимация появления текста
        animate_text(self.canvas, result_text, 300, 200)

    def _update_score_labels(self) -> None:
        """Обновляет метки с очками"""
        self.current_score_label.config(text=f"Текущий: {self.current_score}")
        self.best_score_label.config(text=f"Лучший: {self.best_score}")

    def get_scores(self) -> Dict[str, int]:
        """Возвращает текущие очки"""
        return {
            'current_score': self.current_score,
            'best_score': self.best_score
        } 