"""
Модуль с игровым полем
"""
import tkinter as tk
import random
import time
from typing import Callable, Dict, List, Optional, Tuple
from src.utils.colors import COLORS
from src.utils.animations import (
    create_gradient, animate_shape,
    create_flash_effect, animate_text
)
from src.utils.settings import GAME, WINDOW, LOCALIZATION


class GameField:
    def __init__(self, parent: tk.Tk, on_menu: Callable):
        """
        Инициализация игрового поля
        
        :param parent: Родительское окно
        :param on_menu: Функция для возврата в меню
        """
        self.parent = parent
        self.on_menu = on_menu
        
        # Создание фрейма и канваса
        self.frame = tk.Frame(parent)
        self.canvas = tk.Canvas(
            self.frame,
            width=WINDOW["width"],
            height=WINDOW["height"],
            bg=COLORS["bg"],
            highlightthickness=0
        )
        self.canvas.pack(expand=True, fill="both")
        
        # Создание кнопки меню
        self.menu_button = tk.Button(
            self.frame,
            text=LOCALIZATION["buttons"]["menu"],
            command=self.on_menu,
            font=("Helvetica", 12),
            bg=COLORS["button"],
            fg=COLORS["text"]
        )
        self.menu_button.place(x=10, y=10)
        
        # Инициализация переменных
        self.current_shape = None
        self.current_score = 0
        self.best_score = 0
        self.score_text = None
        self.game_mode = "color"
        self.difficulty = "medium"
        self.animation_ids = []
        self.next_spawn_id = None
        self.spawn_delay = GAME["spawn_delay"]["medium"]
        self.last_spawn_time = 0
        self.is_running = False
        
        # Привязка событий
        self.canvas.bind("<Button-1>", self.on_click)
        
        # Создание градиентного фона
        self.canvas.bind("<Configure>", lambda e: create_gradient(
            self.canvas, COLORS["gradient1"], COLORS["gradient2"]
        ))

    def start_game(self, mode: str, difficulty: str,
                  current_score: int = 0,
                  best_score: int = 0) -> None:
        """
        Запускает игру
        
        :param mode: Режим игры
        :param difficulty: Уровень сложности
        :param current_score: Текущий счет
        :param best_score: Лучший счет
        """
        self.game_mode = mode
        self.difficulty = difficulty
        self.current_score = current_score
        self.best_score = best_score
        self.spawn_delay = GAME["spawn_delay"][difficulty]
        self.is_running = True
        
        # Очистка анимаций
        self.cleanup_animations()
        
        # Обновление счета
        self.update_score()
        
        # Запуск спавна объектов
        self.spawn_shape()

    def stop_game(self) -> None:
        """Останавливает игру"""
        self.is_running = False
        self.cleanup_animations()

    def cleanup_animations(self) -> None:
        """Очищает все анимации"""
        # Отменяем все анимации
        for anim_id in self.animation_ids:
            if anim_id:
                self.canvas.after_cancel(anim_id)
        self.animation_ids.clear()
        
        # Отменяем следующий спавн
        if self.next_spawn_id:
            self.canvas.after_cancel(self.next_spawn_id)
            self.next_spawn_id = None
        
        # Удаляем все объекты с канваса
        self.canvas.delete("all")
        
        # Пересоздаем градиентный фон
        create_gradient(self.canvas, COLORS["gradient1"], COLORS["gradient2"])

    def spawn_shape(self) -> None:
        """Создает новую фигуру"""
        if not self.is_running:
            return
            
        # Очищаем предыдущую фигуру
        if self.current_shape:
            self.canvas.delete(self.current_shape)
            self.current_shape = None
            
        # Определяем размер и позицию
        size = GAME["shape_size"]
        padding = size + 20
        x = random.randint(padding, WINDOW["width"] - padding)
        y = random.randint(padding, WINDOW["height"] - padding)
        
        # Создаем фигуру в зависимости от режима
        if self.game_mode == "color":
            self.current_shape = self.canvas.create_rectangle(
                x - size/2, y - size/2,
                x + size/2, y + size/2,
                fill=random.choice(list(COLORS["shapes"].values())),
                outline=""
            )
        elif self.game_mode == "shape":
            shape_type = random.choice(["rectangle", "oval", "triangle"])
            if shape_type == "rectangle":
                self.current_shape = self.canvas.create_rectangle(
                    x - size/2, y - size/2,
                    x + size/2, y + size/2,
                    fill=COLORS["shapes"]["default"],
                    outline=""
                )
            elif shape_type == "oval":
                self.current_shape = self.canvas.create_oval(
                    x - size/2, y - size/2,
                    x + size/2, y + size/2,
                    fill=COLORS["shapes"]["default"],
                    outline=""
                )
            else:  # triangle
                points = [
                    x, y - size/2,
                    x - size/2, y + size/2,
                    x + size/2, y + size/2
                ]
                self.current_shape = self.canvas.create_polygon(
                    points,
                    fill=COLORS["shapes"]["default"],
                    outline=""
                )
        
        # Анимация появления
        anim_id = animate_shape(
            self.canvas,
            self.current_shape,
            start_scale=0.1,
            end_scale=1.0
        )
        if anim_id:
            self.animation_ids.append(anim_id)
        
        # Запоминаем время спавна
        self.last_spawn_time = time.time()
        
        # Планируем следующий спавн
        self.next_spawn_id = self.canvas.after(
            self.spawn_delay,
            self.spawn_shape
        )

    def on_click(self, event: tk.Event) -> None:
        """Обработка клика мыши"""
        if not self.is_running or not self.current_shape:
            return
            
        # Проверяем попадание
        clicked = self.canvas.find_overlapping(
            event.x - 1, event.y - 1,
            event.x + 1, event.y + 1
        )
        
        if self.current_shape in clicked:
            # Вычисляем очки в зависимости от времени реакции
            reaction_time = time.time() - self.last_spawn_time
            max_points = GAME["points"]["max"]
            min_points = GAME["points"]["min"]
            points = max(
                min_points,
                int(max_points * (1 - reaction_time / (self.spawn_delay / 1000)))
            )
            
            # Обновляем счет
            self.current_score += points
            if self.current_score > self.best_score:
                self.best_score = self.current_score
            self.update_score()
            
            # Создаем эффект вспышки
            shape_coords = self.canvas.coords(self.current_shape)
            shape_center = (
                sum(shape_coords[::2]) / len(shape_coords[::2]),
                sum(shape_coords[1::2]) / len(shape_coords[1::2])
            )
            
            flash_ids = create_flash_effect(
                self.canvas,
                int(shape_center[0]),
                int(shape_center[1]),
                COLORS["flash"]
            )
            self.animation_ids.extend(flash_ids)
            
            # Удаляем фигуру и запускаем следующий объект
            self.canvas.delete(self.current_shape)
            self.current_shape = None
            
            if self.next_spawn_id:
                self.canvas.after_cancel(self.next_spawn_id)
            self.next_spawn_id = self.canvas.after(
                self.spawn_delay,
                self.spawn_shape
            )

    def update_score(self) -> None:
        """Обновляет счет"""
        if self.score_text:
            self.canvas.delete(self.score_text)
            
        score_text = (
            f"{LOCALIZATION['score']}: {self.current_score}\n"
            f"{LOCALIZATION['best_score']}: {self.best_score}"
        )
        
        self.score_text = self.canvas.create_text(
            WINDOW["width"] - 100,
            30,
            text=score_text,
            font=("Helvetica", 14),
            fill=COLORS["text"],
            anchor="e",
            justify="right"
        )
        
        # Анимация для счета
        anim_id = animate_text(
            self.canvas,
            self.score_text,
            WINDOW["width"] - 100,
            30
        )
        if anim_id:
            self.animation_ids.append(anim_id)

    def get_scores(self) -> Dict[str, int]:
        """
        Возвращает текущий и лучший счет
        
        :return: Словарь с текущим и лучшим счетом
        """
        return {
            'current_score': self.current_score,
            'best_score': self.best_score
        }

    def show(self) -> None:
        """Показывает игровое поле"""
        self.frame.pack(expand=True, fill="both")

    def hide(self) -> None:
        """Скрывает игровое поле"""
        self.frame.pack_forget()