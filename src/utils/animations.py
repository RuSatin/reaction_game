"""
Модуль с утилитами для анимаций
"""
import tkinter as tk
from typing import List, Callable, Optional
from src.utils.settings import ANIMATION


def create_gradient(canvas: tk.Canvas, color1: str, color2: str) -> None:
    """Создает градиентный фон на канвасе"""
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    
    if width <= 1 or height <= 1:
        canvas.update()
        width = canvas.winfo_width()
        height = canvas.winfo_height()
    
    for i in range(height):
        # Вычисляем цвет для текущей строки
        ratio = i / height
        r1, g1, b1 = [int(color1[i:i+2], 16) for i in (1, 3, 5)]
        r2, g2, b2 = [int(color2[i:i+2], 16) for i in (1, 3, 5)]
        r = int(r1 * (1 - ratio) + r2 * ratio)
        g = int(g1 * (1 - ratio) + g2 * ratio)
        b = int(b1 * (1 - ratio) + b2 * ratio)
        color = f'#{r:02x}{g:02x}{b:02x}'
        canvas.create_line(0, i, width, i, fill=color)


def animate_shape(canvas: tk.Canvas, shape_id: int, 
                 start_scale: float = 0.1, end_scale: float = 1.0,
                 on_complete: Optional[Callable] = None) -> str:
    """
    Анимация появления фигуры
    
    :return: ID анимации
    """
    coords = canvas.coords(shape_id)
    if not coords:
        return ""
        
    # Находим центр фигуры
    center_x = sum(coords[::2]) / len(coords[::2])
    center_y = sum(coords[1::2]) / len(coords[1::2])
    
    def animate_step(step: int) -> None:
        if not canvas.winfo_exists():
            return
            
        scale = start_scale + (end_scale - start_scale) * (step / ANIMATION["steps"])
        
        # Масштабируем координаты относительно центра
        new_coords = []
        for i in range(0, len(coords), 2):
            x = center_x + (coords[i] - center_x) * scale
            y = center_y + (coords[i+1] - center_y) * scale
            new_coords.extend([x, y])
            
        canvas.coords(shape_id, *new_coords)
        
        if step < ANIMATION["steps"]:
            return canvas.after(ANIMATION["speed"], lambda: animate_step(step + 1))
        elif on_complete:
            on_complete()
            return ""
    
    return animate_step(0) or ""


def create_flash_effect(canvas: tk.Canvas, x: int, y: int, color: str) -> List[str]:
    """
    Создает эффект вспышки при клике
    
    :return: Список ID анимаций
    """
    animation_ids = []
    rings = []
    
    for i in range(ANIMATION["flash_rings"]):
        radius = ANIMATION["flash_radius"] * (1 - i/ANIMATION["flash_rings"])
        ring = canvas.create_oval(
            x - radius, y - radius,
            x + radius, y + radius,
            fill=color,
            outline="",
            width=2
        )
        rings.append(ring)
    
    def fade_step(step: int, rings: List[int]) -> Optional[str]:
        if not canvas.winfo_exists():
            return None
            
        if step >= 10 or not rings:
            for ring in rings:
                canvas.delete(ring)
            return None
        
        # Изменяем размер колец
        for i, ring in enumerate(rings):
            radius = ANIMATION["flash_radius"] * (1 - i/ANIMATION["flash_rings"]) * (1 + step/10)
            canvas.coords(
                ring,
                x - radius, y - radius,
                x + radius, y + radius
            )
        
        return canvas.after(20, lambda: fade_step(step + 1, rings))
    
    animation_id = fade_step(0, rings)
    if animation_id:
        animation_ids.append(animation_id)
    
    return animation_ids


def animate_text(canvas: tk.Canvas, text_id: int, center_x: int, center_y: int,
                start_scale: float = 0.1, end_scale: float = 1.0,
                on_complete: Optional[Callable] = None) -> str:
    """
    Анимация появления текста
    
    :return: ID анимации
    """
    canvas.scale(text_id, center_x, center_y, start_scale, start_scale)
    
    def animate_step(step: int) -> Optional[str]:
        if not canvas.winfo_exists():
            return None
            
        if step <= 10:
            scale = start_scale + (end_scale - start_scale) * (step / 10)
            canvas.scale(text_id, center_x, center_y, scale, scale)
            return canvas.after(ANIMATION["speed"], lambda: animate_step(step + 1))
        elif on_complete:
            on_complete()
            return None
    
    return animate_step(0) or ""