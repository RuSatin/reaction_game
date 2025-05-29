"""
Модуль с компонентом меню
"""
import tkinter as tk
from tkinter import messagebox
from typing import Callable, Dict
from src.utils.colors import COLORS
from src.utils.settings import WINDOW, LOCALIZATION


class Menu:
    def __init__(self, parent: tk.Tk, callbacks: Dict[str, Callable]):
        """
        Инициализация меню
        
        :param parent: Родительское окно
        :param callbacks: Словарь с функциями обратного вызова
        """
        self.parent = parent
        self.callbacks = callbacks
        self.frame = tk.Frame(parent, bg=COLORS['bg'])
        
        self._create_widgets()
        
    def _create_widgets(self) -> None:
        """Создает виджеты меню"""
        # Заголовок
        title_label = tk.Label(
            self.frame,
            text=WINDOW["title"],
            font=("Helvetica", 24, "bold"),
            bg=COLORS['bg'],
            fg=COLORS['text']
        )
        title_label.pack(pady=(20, 30))

        # Стиль кнопок
        button_style = {
            'font': ("Helvetica", 14),
            'width': 25,
            'height': 2,
            'bg': COLORS['button'],
            'fg': COLORS['text'],
            'relief': 'flat'
        }

        # Кнопки меню
        buttons_data = [
            ("Продолжить", 'continue_game'),
            ("Новая игра", 'new_game'),
            ("Режим игры", 'select_mode'),
            ("Инструкция", 'show_instructions')
        ]

        for text, callback_key in buttons_data:
            btn = tk.Button(
                self.frame,
                text=text,
                command=self.callbacks[callback_key],
                **button_style
            )
            btn.pack(pady=5)
            btn.bind('<Enter>', lambda e, b=btn: self._on_button_hover(b, True))
            btn.bind('<Leave>', lambda e, b=btn: self._on_button_hover(b, False))
            if text == "Продолжить":
                self.continue_button = btn
                self.continue_button.config(state="disabled")

    def _on_button_hover(self, button: tk.Button, entering: bool) -> None:
        """Эффект при наведении на кнопку"""
        if entering:
            button.config(
                bg=COLORS['primary'],
                fg=COLORS['text']
            )
        else:
            button.config(
                bg=COLORS['button'],
                fg=COLORS['text']
            )

    def show(self) -> None:
        """Показывает меню"""
        self.frame.pack(expand=True, fill="both")

    def hide(self) -> None:
        """Скрывает меню"""
        self.frame.pack_forget()

    def update_continue_button(self, enabled: bool) -> None:
        """Обновляет состояние кнопки продолжения"""
        self.continue_button.config(state="normal" if enabled else "disabled")

    @staticmethod
    def show_mode_selection(parent: tk.Tk, current_mode: str, 
                          current_difficulty: str,
                          on_save: Callable[[str, str], None]) -> None:
        """Показывает окно выбора режима игры"""
        mode_window = tk.Toplevel(parent)
        mode_window.title("Настройки")
        mode_window.geometry("400x500")
        mode_window.resizable(False, False)
        mode_window.configure(bg=COLORS['bg'])
        mode_window.grab_set()

        # Заголовок
        tk.Label(
            mode_window,
            text="Настройки игры",
            font=("Helvetica", 18, "bold"),
            bg=COLORS['bg'],
            fg=COLORS['text']
        ).pack(pady=20)

        mode_var = tk.StringVar(value=current_mode)
        difficulty_var = tk.StringVar(value=current_difficulty)

        # Создаем фреймы для режимов и сложности
        modes_frame = Menu._create_radio_group(
            mode_window, "Режим игры", mode_var,
            [(LOCALIZATION["modes"][mode], mode) for mode in ["color", "shape", "sound"]]
        )
        modes_frame.pack(padx=20, pady=10, fill="x")

        difficulty_frame = Menu._create_radio_group(
            mode_window, "Уровень сложности", difficulty_var,
            [(LOCALIZATION["difficulties"][diff], diff) 
             for diff in ["easy", "medium", "hard"]]
        )
        difficulty_frame.pack(padx=20, pady=20, fill="x")

        # Кнопки
        buttons_frame = tk.Frame(mode_window, bg=COLORS['bg'])
        buttons_frame.pack(pady=20)

        save_button = tk.Button(
            buttons_frame,
            text="Сохранить",
            command=lambda: [
                on_save(mode_var.get(), difficulty_var.get()),
                mode_window.destroy()
            ],
            font=("Helvetica", 12),
            bg=COLORS['button'],
            fg=COLORS['text'],
            relief='flat',
            width=15
        )
        save_button.pack(side="left", padx=10)

        cancel_button = tk.Button(
            buttons_frame,
            text="Отмена",
            command=mode_window.destroy,
            font=("Helvetica", 12),
            bg=COLORS['button'],
            fg=COLORS['text'],
            relief='flat',
            width=15
        )
        cancel_button.pack(side="left", padx=10)

    @staticmethod
    def _create_radio_group(parent: tk.Widget, title: str, 
                          variable: tk.StringVar,
                          options: list) -> tk.LabelFrame:
        """Создает группу радиокнопок"""
        frame = tk.LabelFrame(
            parent,
            text=title,
            font=("Helvetica", 12),
            bg=COLORS['bg'],
            fg=COLORS['text']
        )

        for text, value in options:
            radio_frame = tk.Frame(frame, bg=COLORS['bg'])
            radio_frame.pack(fill="x", padx=10, pady=5)
            
            rb = tk.Radiobutton(
                radio_frame,
                text=text,
                value=value,
                variable=variable,
                font=("Helvetica", 12),
                bg=COLORS['bg'],
                fg=COLORS['text'],
                selectcolor=COLORS['primary'],
                activebackground=COLORS['bg']
            )
            rb.pack(side="left")

        return frame

    @staticmethod
    def show_instructions() -> None:
        """Показывает инструкцию к игре"""
        instructions = """
        ИНСТРУКЦИЯ

        Цель игры: как можно быстрее реагировать на появляющиеся стимулы.

        Правила:
        1. В центре экрана появится стимул (цветной квадрат, фигура или звук)
        2. Необходимо как можно быстрее кликнуть по нему
        3. Чем быстрее вы реагируете, тем больше очков получаете

        Режимы игры:
        - Цвет: реагируйте на цветной квадрат
        - Фигура: реагируйте на определенную фигуру
        - Звук: реагируйте на звуковой сигнал (нужны колонки)

        Уровни сложности:
        - Легкий: больше времени на реакцию
        - Средний: стандартное время
        - Сложный: очень мало времени на реакцию

        Управление:
        - Нажмите 'Новая игра' для начала
        - 'Продолжить' - вернуться к текущей игре
        - 'Меню' - вернуться в главное меню
        """
        messagebox.showinfo("Инструкция", instructions)