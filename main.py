
import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import json



class ReactionTrainer:
    def __init__(self, root):
        self.root = root
        self.root.title("Тренировка реакции")
        self.root.geometry("1000x800")
        self.root.resizable(False, False)

        # Современные цвета
        self.colors = {
            'bg': "#1a1a2e",  # Темно-синий фон
            'primary': "#0f3460",  # Основной цвет
            'secondary': "#e94560",  # Акцентный цвет
            'text': "#ffffff",  # Белый текст
            'button': "#16213e",  # Цвет кнопок
            'highlight': "#00ff88"  # Цвет подсветки
        }

        # Настройки анимации
        self.animation_speed = 10  # мс между кадрами
        self.animation_steps = 10  # количество кадров
        self.current_animation = None
        
        # Настройки приложения
        self.best_score = 0
        self.current_score = 0
        self.game_mode = "color"
        self.difficulty = "medium"
        self.game_active = False
        self.reaction_time = 0
        self.start_time = 0
        self.first_run = True

        # Загрузка лучшего счета
        self.load_best_score()

        # Создание интерфейса
        self.create_menu()
        self.create_game_field()

        # Показать меню при запуске
        self.show_menu()

        # Показать инструкцию при первом запуске
        if self.first_run:
            self.show_instructions()
            self.first_run = False

    def load_best_score(self):
        """Загружает лучший счет из файла"""
        try:
            with open('best_score.json', 'r') as f:
                data = json.load(f)
                self.best_score = data.get('best_score', 0)
                self.game_mode = data.get('game_mode', "color")
                self.difficulty = data.get('difficulty', "medium")
        except (FileNotFoundError, json.JSONDecodeError):
            self.best_score = 0
            self.game_mode = "color"
            self.difficulty = "medium"

    def save_best_score(self):
        """Сохраняет лучший счет и настройки в файл"""
        with open('best_score.json', 'w') as f:
            json.dump({
                'best_score': self.best_score,
                'game_mode': self.game_mode,
                'difficulty': self.difficulty
            }, f)

    def create_menu(self):
        """Создает меню приложения согласно прототипу Рисунок 5"""
        self.menu_frame = tk.Frame(self.root, bg=self.colors['bg'])

        # Заголовок
        title_label = tk.Label(
            self.menu_frame,
            text="Тренировка реакции",
            font=("Helvetica", 24, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        title_label.pack(pady=(20, 30))

        # Стиль кнопок
        button_style = {
            'font': ("Helvetica", 14),
            'width': 25,
            'height': 2,
            'bg': self.colors['button'],
            'fg': self.colors['text'],
            'relief': 'flat'
        }

        # Кнопки меню
        buttons_data = [
            ("Продолжить", self.continue_game),
            ("Новая игра", self.start_new_game),
            ("Режим игры", self.select_mode),
            ("Инструкция", self.show_instructions)
        ]

        for text, command in buttons_data:
            btn = tk.Button(
                self.menu_frame,
                text=text,
                command=command,
                **button_style
            )
            btn.pack(pady=5)
            btn.bind('<Enter>', lambda e, b=btn: self.on_button_hover(b, True))
            btn.bind('<Leave>', lambda e, b=btn: self.on_button_hover(b, False))
            if text == "Продолжить":
                self.continue_button = btn
                self.continue_button.config(state="disabled")

        # Информация о текущих настройках
        settings_frame = tk.Frame(self.menu_frame, bg=self.colors['bg'])
        settings_frame.pack(pady=20)

        tk.Label(
            settings_frame,
            text=f"Режим: {self.get_mode_name()}",
            font=("Helvetica", 12),
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).pack(side="left", padx=10)

        tk.Label(
            settings_frame,
            text=f"Сложность: {self.get_difficulty_name()}",
            font=("Helvetica", 12),
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).pack(side="right", padx=10)

        # Лучший результат
        tk.Label(
            self.menu_frame,
            text=f"Лучший результат: {self.best_score}",
            font=("Helvetica", 16, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['secondary']
        ).pack(pady=20)

    def create_game_field(self):
        """Создает игровое поле согласно прототипу Рисунок 4"""
        self.game_frame = tk.Frame(self.root, bg=self.colors['bg'])

        # Создаем верхнюю панель для счета (элементы 2 и 3 из прототипа)
        score_panel = tk.Frame(self.game_frame, bg=self.colors['bg'])
        score_panel.pack(fill="x", padx=20, pady=5)

        # Лучший счет (элемент 2)
        self.best_score_label = tk.Label(
            score_panel,
            text=f"Лучший: {self.best_score}",
            font=("Helvetica", 14, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        self.best_score_label.pack(side="left", padx=10)

        # Текущий счет (элемент 3)
        self.current_score_label = tk.Label(
            score_panel,
            text=f"Текущий: {self.current_score}",
            font=("Helvetica", 14, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        self.current_score_label.pack(side="right", padx=10)

        # Создаем фрейм для игрового поля (элемент 1)
        game_area_frame = tk.Frame(
            self.game_frame,
            bg=self.colors['bg']
        )
        game_area_frame.pack(expand=True, fill="both", padx=20, pady=10)

        # Игровое поле (элемент 1)
        self.game_canvas = tk.Canvas(
            game_area_frame,
            bg="white",
            width=600,
            height=400,
            highlightthickness=0
        )
        self.game_canvas.pack(expand=True, fill="both")
        self.game_canvas.bind("<Button-1>", self.reaction_click)

        # Кнопка выхода в меню (элемент 4)
        menu_button = tk.Button(
            self.game_frame,
            text="Меню",
            command=self.show_menu,
            font=("Helvetica", 12),
            bg=self.colors['button'],
            fg=self.colors['text'],
            relief='flat',
            width=10
        )
        menu_button.pack(pady=10)
        menu_button.bind('<Enter>', lambda e: self.on_button_hover(menu_button, True))
        menu_button.bind('<Leave>', lambda e: self.on_button_hover(menu_button, False))

        # Принудительное обновление размеров
        self.game_canvas.update()

    def get_mode_name(self):
        """Возвращает читаемое название режима"""
        names = {
            "color": "Цвет",
            "shape": "Фигура",
            "sound": "Звук"
        }
        return names.get(self.game_mode, "Цвет")

    def get_difficulty_name(self):
        """Возвращает читаемое название уровня сложности"""
        names = {
            "easy": "Легкий",
            "medium": "Средний",
            "hard": "Сложный"
        }
        return names.get(self.difficulty, "Средний")

    def show_menu(self):
        """Показывает меню и скрывает игровое поле"""
        self.game_frame.pack_forget()
        self.menu_frame.pack(expand=True, fill="both")
        self.stop_game()
        self.update_menu_info()

    def show_game(self):
        """Показывает игровое поле и скрывает меню"""
        self.menu_frame.pack_forget()
        self.game_frame.pack(expand=True, fill="both")

    def update_menu_info(self):
        """Обновляет информацию в меню"""
        # Обновляем информацию о режиме и сложности в меню
        for widget in self.menu_frame.winfo_children():
            if isinstance(widget, tk.Frame) and widget.winfo_children():
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label):
                        if "Режим:" in child.cget("text"):
                            child.config(text=f"Режим: {self.get_mode_name()}")
                        elif "Сложность:" in child.cget("text"):
                            child.config(text=f"Сложность: {self.get_difficulty_name()}")
                        elif "Лучший результат:" in child.cget("text"):
                            child.config(text=f"Лучший результат: {self.best_score}")

    def show_instructions(self):
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
        
        # Создаем временную метку с сообщением
        temp_label = tk.Label(
            self.menu_frame,
            text="Ознакомьтесь с инструкцией перед началом игры",
            font=("Helvetica", 12),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        temp_label.pack(pady=10)
        
        # Удаляем метку через 3 секунды
        self.root.after(3000, temp_label.destroy)

    def select_mode(self):
        """Окно выбора режима игры"""
        mode_window = tk.Toplevel(self.root)
        mode_window.title("Настройки")
        mode_window.geometry("400x500")
        mode_window.resizable(False, False)
        mode_window.configure(bg=self.colors['bg'])
        mode_window.grab_set()  # Делаем окно модальным

        # Заголовок
        tk.Label(
            mode_window,
            text="Настройки игры",
            font=("Helvetica", 18, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).pack(pady=20)

        # Фрейм для режимов
        modes_frame = tk.LabelFrame(
            mode_window,
            text="Режим игры",
            font=("Helvetica", 12),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        modes_frame.pack(padx=20, pady=10, fill="x")

        self.mode_var = tk.StringVar(value=self.game_mode)

        modes = [
            ("Цвет", "color", "Реагируйте на появление цветного квадрата"),
            ("Фигура", "shape", "Реагируйте на появление геометрической фигуры"),
            ("Звук", "sound", "Реагируйте на звуковой сигнал")
        ]

        for text, mode, desc in modes:
            frame = tk.Frame(modes_frame, bg=self.colors['bg'])
            frame.pack(fill="x", padx=10, pady=5)
            
            rb = tk.Radiobutton(
                frame,
                text=text,
                value=mode,
                variable=self.mode_var,
                font=("Helvetica", 12),
                bg=self.colors['bg'],
                fg=self.colors['text'],
                selectcolor=self.colors['primary'],
                activebackground=self.colors['bg']
            )
            rb.pack(side="left")
            
            tk.Label(
                frame,
                text=desc,
                font=("Helvetica", 10),
                bg=self.colors['bg'],
                fg=self.colors['text']
            ).pack(side="left", padx=10)

        # Фрейм для сложности
        difficulty_frame = tk.LabelFrame(
            mode_window,
            text="Уровень сложности",
            font=("Helvetica", 12),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        difficulty_frame.pack(padx=20, pady=20, fill="x")

        self.difficulty_var = tk.StringVar(value=self.difficulty)

        difficulties = [
            ("Легкий", "easy", "Больше времени на реакцию"),
            ("Средний", "medium", "Стандартное время"),
            ("Сложный", "hard", "Минимальное время на реакцию")
        ]

        for text, diff, desc in difficulties:
            frame = tk.Frame(difficulty_frame, bg=self.colors['bg'])
            frame.pack(fill="x", padx=10, pady=5)
            
            rb = tk.Radiobutton(
                frame,
                text=text,
                value=diff,
                variable=self.difficulty_var,
                font=("Helvetica", 12),
                bg=self.colors['bg'],
                fg=self.colors['text'],
                selectcolor=self.colors['primary'],
                activebackground=self.colors['bg']
            )
            rb.pack(side="left")
            
            tk.Label(
                frame,
                text=desc,
                font=("Helvetica", 10),
                bg=self.colors['bg'],
                fg=self.colors['text']
            ).pack(side="left", padx=10)

        # Кнопки
        buttons_frame = tk.Frame(mode_window, bg=self.colors['bg'])
        buttons_frame.pack(pady=20)

        save_button = tk.Button(
            buttons_frame,
            text="Сохранить",
            command=lambda: self.save_mode(mode_window),
            font=("Helvetica", 12),
            bg=self.colors['button'],
            fg=self.colors['text'],
            relief='flat',
            width=15
        )
        save_button.pack(side="left", padx=10)
        save_button.bind('<Enter>', lambda e: self.on_button_hover(save_button, True))
        save_button.bind('<Leave>', lambda e: self.on_button_hover(save_button, False))

        cancel_button = tk.Button(
            buttons_frame,
            text="Отмена",
            command=mode_window.destroy,
            font=("Helvetica", 12),
            bg=self.colors['button'],
            fg=self.colors['text'],
            relief='flat',
            width=15
        )
        cancel_button.pack(side="left", padx=10)
        cancel_button.bind('<Enter>', lambda e: self.on_button_hover(cancel_button, True))
        cancel_button.bind('<Leave>', lambda e: self.on_button_hover(cancel_button, False))

    def save_mode(self, window):
        """Сохраняет выбранный режим и сложность"""
        self.game_mode = self.mode_var.get()
        self.difficulty = self.difficulty_var.get()
        self.save_best_score()
        self.update_menu_info()
        window.destroy()
        messagebox.showinfo(
            "Настройки сохранены",
            f"Режим: {self.get_mode_name()}\nСложность: {self.get_difficulty_name()}"
        )

    def start_new_game(self):
        """Начинает новую игру (элемент 1 из прототипа меню)"""
        self.difficulty = self.difficulty_var.get() if hasattr(self, 'difficulty_var') else self.difficulty
        self.game_mode = self.mode_var.get() if hasattr(self, 'mode_var') else self.game_mode
        self.current_score = 0
        self.continue_button.config(state="normal")
        self.update_score_labels()
        self.show_game()
        self.game_active = True
        
        # Показать сообщение о начале игры
        self.game_canvas.create_text(
            300, 200,
            text="Приготовьтесь!\nИгра начнется через 2 секунды...",
            font=("Arial", 16),
            justify="center"
        )
        self.root.update()
        
        # Задержка перед первым стимулом
        self.root.after(2000, self.schedule_stimulus)

    def continue_game(self):
        """Продолжает текущую игру (элемент 1 из прототипа меню)"""
        self.show_game()
        self.game_active = True
        
        # Показать сообщение о продолжении игры
        self.game_canvas.create_text(
            300, 200,
            text="Приготовьтесь!\nИгра продолжится через 2 секунды...",
            font=("Arial", 16),
            justify="center"
        )
        self.root.update()
        
        # Задержка перед следующим стимулом
        self.root.after(2000, self.schedule_stimulus)

    def stop_game(self):
        """Останавливает игру"""
        self.game_active = False
        if hasattr(self, 'stimulus_id'):
            self.root.after_cancel(self.stimulus_id)

    def schedule_stimulus(self):
        """Запланировать появление стимула"""
        if not self.game_active:
            return

        # Очистить холст
        self.game_canvas.delete("all")
        self.game_canvas.config(bg="white")

        # Определить задержку в зависимости от сложности
        if self.difficulty == "easy":
            delay = random.randint(1500, 3000)  # 1.5-3 секунды
        elif self.difficulty == "hard":
            delay = random.randint(500, 1500)  # 0.5-1.5 секунды
        else:  # medium
            delay = random.randint(1000, 2000)  # 1-2 секунды

        # Запланировать появление стимула
        self.stimulus_id = self.root.after(delay, self.show_stimulus)

    def create_gradient(self, canvas, color1, color2):
        """Создает градиентный фон"""
        try:
            print(f"Creating gradient with colors {color1} and {color2}")
            width = canvas.winfo_width()
            height = canvas.winfo_height()
            print(f"Canvas dimensions: {width}x{height}")
            
            if width <= 1 or height <= 1:  # Проверка размеров
                print("Warning: Canvas dimensions too small, waiting for proper initialization")
                self.root.update()  # Принудительное обновление
                width = canvas.winfo_width()
                height = canvas.winfo_height()
                print(f"Updated canvas dimensions: {width}x{height}")
            
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
        except Exception as e:
            print(f"Error in create_gradient: {e}")
            import traceback
            print(traceback.format_exc())

    def animate_shape(self, shape_id, start_scale=0.1, end_scale=1.0):
        """Анимация появления фигуры"""
        try:
            print(f"Starting shape animation for ID: {shape_id}")
            if not shape_id:
                print("No shape ID provided")
                return
                
            coords = self.game_canvas.coords(shape_id)
            if not coords:
                print("No coordinates found for shape")
                return
                
            print(f"Initial coordinates: {coords}")
            # Находим центр фигуры
            center_x = sum(coords[::2]) / len(coords[::2])
            center_y = sum(coords[1::2]) / len(coords[1::2])
            print(f"Center point: ({center_x}, {center_y})")
            
            def animate_step(step):
                try:
                    if not self.game_active:
                        print("Game not active, stopping animation")
                        return
                        
                    scale = start_scale + (end_scale - start_scale) * (step / self.animation_steps)
                    print(f"Animation step {step}, scale: {scale}")
                    
                    # Масштабируем координаты относительно центра
                    new_coords = []
                    for i in range(0, len(coords), 2):
                        x = center_x + (coords[i] - center_x) * scale
                        y = center_y + (coords[i+1] - center_y) * scale
                        new_coords.extend([x, y])
                        
                    self.game_canvas.coords(shape_id, *new_coords)
                    print(f"New coordinates: {new_coords}")
                    
                    if step < self.animation_steps:
                        self.current_animation = self.root.after(
                            self.animation_speed,
                            lambda: animate_step(step + 1)
                        )
                except Exception as e:
                    print(f"Error in animation step: {e}")
                    import traceback
                    print(traceback.format_exc())
            
            animate_step(0)
            
        except Exception as e:
            print(f"Error in animate_shape: {e}")
            import traceback
            print(traceback.format_exc())

    def create_flash_effect(self, x, y):
        """Создает эффект вспышки при клике"""
        try:
            print("Creating flash effect")
            # Создаем несколько концентрических кругов для эффекта вспышки
            rings = []
            max_radius = 50
            num_rings = 5
            
            for i in range(num_rings):
                radius = max_radius * (1 - i/num_rings)
                ring = self.game_canvas.create_oval(
                    x - radius, y - radius,
                    x + radius, y + radius,
                    fill=self.colors['highlight'],
                    outline="",
                    width=2
                )
                rings.append(ring)
            
            def fade_step(step, rings):
                if step >= 10 or not rings:
                    for ring in rings:
                        self.game_canvas.delete(ring)
                    return
                
                # Изменяем размер колец
                for i, ring in enumerate(rings):
                    radius = max_radius * (1 - i/num_rings) * (1 + step/10)
                    self.game_canvas.coords(
                        ring,
                        x - radius, y - radius,
                        x + radius, y + radius
                    )
                
                self.root.after(20, lambda: fade_step(step + 1, rings))
            
            fade_step(0, rings)
            print("Flash effect created")
            
        except Exception as e:
            print(f"Error in create_flash_effect: {e}")
            import traceback
            print(traceback.format_exc())

    def show_stimulus(self):
        """Показывает стимул в зависимости от режима"""
        try:
            if not self.game_active:
                print("Game not active, skipping stimulus")
                return

            print("Showing stimulus")
            # Очистить холст и создать градиентный фон
            self.game_canvas.delete("all")
            print("Canvas cleared")
            
            # Получить размеры холста
            canvas_width = self.game_canvas.winfo_width()
            canvas_height = self.game_canvas.winfo_height()
            print(f"Canvas size: {canvas_width}x{canvas_height}")
            
            if canvas_width <= 1 or canvas_height <= 1:
                print("Canvas not properly initialized, forcing update")
                self.root.update()
                canvas_width = self.game_canvas.winfo_width()
                canvas_height = self.game_canvas.winfo_height()
                print(f"Updated canvas size: {canvas_width}x{canvas_height}")

            self.create_gradient(self.game_canvas, self.colors['bg'], self.colors['primary'])
            print("Gradient created")

            # Размеры фигур
            shape_size = 100

            # Случайные координаты
            x = random.randint(shape_size, canvas_width - shape_size)
            y = random.randint(shape_size, canvas_height - shape_size)
            print(f"Shape position: ({x}, {y})")

            # Показать стимул в зависимости от режима
            shape_id = None
            if self.game_mode == "color":
                print("Creating color stimulus (rectangle)")
                shape_id = self.game_canvas.create_rectangle(
                    x - shape_size//2, y - shape_size//2,
                    x + shape_size//2, y + shape_size//2,
                    fill=self.colors['secondary'],
                    outline="",
                    tags="stimulus"
                )
            elif self.game_mode == "shape":
                print("Creating shape stimulus (oval)")
                shape_id = self.game_canvas.create_oval(
                    x - shape_size//2, y - shape_size//2,
                    x + shape_size//2, y + shape_size//2,
                    fill=self.colors['highlight'],
                    outline="",
                    tags="stimulus"
                )
            else:  # sound
                print("Creating sound stimulus (triangle)")
                points = [
                    x, y - shape_size//2,
                    x - shape_size//2, y + shape_size//2,
                    x + shape_size//2, y + shape_size//2
                ]
                shape_id = self.game_canvas.create_polygon(
                    points,
                    fill=self.colors['secondary'],
                    outline="",
                    tags="stimulus"
                )
                self.root.bell()

            print(f"Shape created with ID: {shape_id}")
            # Анимация появления
            self.animate_shape(shape_id)
            print("Animation started")
            
            # Запомнить время появления стимула
            self.start_time = time.time()
            print("Stimulus display completed")
            
        except Exception as e:
            print(f"Error in show_stimulus: {e}")
            import traceback
            print(traceback.format_exc())

    def reaction_click(self, event):
        """Обработчик клика по игровому полю"""
        if not self.game_active or self.start_time == 0:
            return

        # Проверить, кликнул ли пользователь по стимулу
        clicked_items = self.game_canvas.find_withtag("current")
        if clicked_items and "stimulus" in self.game_canvas.gettags(clicked_items[0]):
            # Создать эффект вспышки
            self.create_flash_effect(event.x, event.y)
            
            # Рассчитать время реакции
            reaction_time = (time.time() - self.start_time) * 1000
            self.reaction_time = reaction_time

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
                self.save_best_score()

            # Обновить интерфейс
            self.update_score_labels()

            # Показать результат с анимацией
            self.show_result_animation(reaction_time, points)

            # Сбросить время начала
            self.start_time = 0

            # Запланировать следующий стимул
            self.root.after(1000, self.schedule_stimulus)

    def show_result_animation(self, reaction_time, points):
        """Показывает анимированный результат"""
        self.game_canvas.delete("all")
        self.create_gradient(self.game_canvas, self.colors['bg'], self.colors['primary'])

        # Создаем текст с результатом
        result_text = self.game_canvas.create_text(
            300, 200,
            text=f"Время реакции: {reaction_time:.0f} мс\nОчки: +{points}",
            font=("Arial", 24, "bold"),
            fill=self.colors['text'],
            justify="center",
            tags="result"
        )

        # Анимация появления текста
        self.game_canvas.scale(result_text, 300, 200, 0.1, 0.1)
        
        def animate_text(step):
            if step <= 10:
                scale = 0.1 + (1 - 0.1) * (step / 10)
                self.game_canvas.scale(result_text, 300, 200, scale, scale)
                self.root.after(20, lambda: animate_text(step + 1))
        
        animate_text(0)

    def update_score_labels(self):
        """Обновляет метки с очками во всех окнах"""
        self.current_score_label.config(text=f"Текущий: {self.current_score}")
        self.best_score_label.config(text=f"Лучший: {self.best_score}")

        # Обновить в меню, если оно существует
        if hasattr(self, 'menu_frame'):
            for widget in self.menu_frame.winfo_children():
                if isinstance(widget, tk.Label):  # Check if widget is a Label
                    try:
                        widget_text = widget.cget("text")
                        if isinstance(widget_text, str) and "Лучший результат:" in widget_text:
                            widget.config(text=f"Лучший результат: {self.best_score}")
                    except tk.TclError:
                        continue  # Skip widgets that don't support text property

    def on_button_hover(self, button, entering):
        """Эффект при наведении на кнопку"""
        if entering:
            button.config(
                bg=self.colors['primary'],
                fg=self.colors['text']
            )
        else:
            button.config(
                bg=self.colors['button'],
                fg=self.colors['text']
            )


if __name__ == "__main__":
    try:
        print("Creating main window...")
        root = tk.Tk()
        root.withdraw()  # Hide window initially
        print("Window created, configuring...")
        
        # Configure window
        root.title("Тренировка реакции")
        root.geometry("1000x800")
        root.resizable(False, False)
        
        print("Creating application...")
        app = ReactionTrainer(root)
        
        print("Showing window...")
        root.deiconify()  # Show window
        root.lift()  # Bring to front
        root.focus_force()  # Force focus
        
        print("Starting main loop...")
        root.mainloop()
        print("Main loop ended.")
    except Exception as e:
        import traceback
        print(f"Error occurred: {e}")
        print("Full traceback:")
        print(traceback.format_exc())
        input("Press Enter to exit...")