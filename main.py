from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Rectangle
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader
import random

# ================= WINDOW =================

Window.size = (400, 700)

# ================= GAME AREA =================

GAME_X = 20
GAME_Y = 220
GAME_WIDTH = 360
GAME_HEIGHT = 460

# ================= GAME =================

class SnakeGame(FloatLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # SETTINGS
        self.snake_size = 40
        self.speed = 0.15
        self.music_on = True
        self.running = False
        self.settings_open = False

        # GAME
        self.snake = [(160, 400)]
        self.direction = "RIGHT"
        self.food = self.random_food()
        self.score = 0

        # ================= SOUNDS =================

        self.eat_sound = SoundLoader.load("eat.wav")
        self.gameover_sound = SoundLoader.load("gameover.wav")
        self.click_sound = SoundLoader.load("click.wav")

        # ================= MUSIC =================

        self.music = SoundLoader.load("music.wav")

        if self.music:
            self.music.loop = True
            self.music.play()

        # ================= SCORE =================

        self.score_label = Label(
            text="Score : 0",
            font_size=28,
            bold=True,
            pos=(0, 300)
        )

        self.add_widget(self.score_label)

        # ================= PLAY BUTTON =================

        self.play_btn = Button(
            text="PLAY",
            size_hint=(None, None),
            size=(140, 60),
            pos=(130, 560),
            background_normal='',
            background_color=(0, 0.7, 0, 1)
        )

        self.play_btn.bind(on_press=self.start_game)

        self.add_widget(self.play_btn)

        # ================= SETTINGS BUTTON =================

        self.settings_btn = Button(
            text="SETTINGS",
            size_hint=(None, None),
            size=(140, 60),
            pos=(130, 490),
            background_normal='',
            background_color=(0.2, 0.2, 0.2, 1)
        )

        self.settings_btn.bind(on_press=self.open_settings)

        self.add_widget(self.settings_btn)

        # ================= CONTROLS =================

        self.create_controls()

        # ================= DRAW =================

        self.draw_game()

    # ================= PLAY =================

    def start_game(self, instance):

        self.running = True

        if self.click_sound:
            self.click_sound.play()

        if self.play_btn.parent:
            self.remove_widget(self.play_btn)

        if self.settings_btn.parent:
            self.remove_widget(self.settings_btn)

        Clock.unschedule(self.update)

        Clock.schedule_interval(
            self.update,
            self.speed
        )

    # ================= SETTINGS =================

    def open_settings(self, instance):

        if self.settings_open:
            return

        self.settings_open = True

        # SLOW
        self.slow_btn = Button(
            text="SLOW",
            size_hint=(None, None),
            size=(90, 50),
            pos=(20, 620)
        )

        self.slow_btn.bind(on_press=self.set_slow)

        self.add_widget(self.slow_btn)

        # MEDIUM
        self.medium_btn = Button(
            text="MEDIUM",
            size_hint=(None, None),
            size=(100, 50),
            pos=(140, 620)
        )

        self.medium_btn.bind(on_press=self.set_medium)

        self.add_widget(self.medium_btn)

        # FAST
        self.fast_btn = Button(
            text="FAST",
            size_hint=(None, None),
            size=(90, 50),
            pos=(290, 620)
        )

        self.fast_btn.bind(on_press=self.set_fast)

        self.add_widget(self.fast_btn)

        # MUSIC
        self.music_btn = Button(
            text="MUSIC ON/OFF",
            size_hint=(None, None),
            size=(180, 50),
            pos=(110, 550)
        )

        self.music_btn.bind(on_press=self.toggle_music)

        self.add_widget(self.music_btn)

        # SAVE
        self.save_btn = Button(
            text="SAVE",
            size_hint=(None, None),
            size=(140, 50),
            pos=(130, 480),
            background_normal='',
            background_color=(0, 0.7, 0, 1)
        )

        self.save_btn.bind(on_press=self.close_settings)

        self.add_widget(self.save_btn)

    # ================= CLOSE SETTINGS =================

    def close_settings(self, instance):

        self.remove_widget(self.slow_btn)
        self.remove_widget(self.medium_btn)
        self.remove_widget(self.fast_btn)
        self.remove_widget(self.music_btn)
        self.remove_widget(self.save_btn)

        self.settings_open = False

    # ================= SPEED =================

    def set_slow(self, instance):
        self.speed = 0.25

    def set_medium(self, instance):
        self.speed = 0.15

    def set_fast(self, instance):
        self.speed = 0.08

    # ================= MUSIC =================

    def toggle_music(self, instance):

        if self.music_on:

            if self.music:
                self.music.stop()

            self.music_on = False

        else:

            if self.music:
                self.music.play()
                self.music.loop = True

            self.music_on = True

    # ================= RANDOM FOOD =================

    def random_food(self):

        x = random.randrange(
            GAME_X,
            GAME_X + GAME_WIDTH - 40,
            40
        )

        y = random.randrange(
            GAME_Y,
            GAME_Y + GAME_HEIGHT - 40,
            40
        )

        return (x, y)

    # ================= CONTROLS =================

    def create_controls(self):

        # UP
        up = Button(
            text="UP",
            font_size=20,
            bold=True,
            size_hint=(None, None),
            size=(80, 80),
            pos=(160, 100)
        )

        up.bind(on_press=self.go_up)

        self.add_widget(up)

        # DOWN
        down = Button(
            text="DOWN",
            font_size=20,
            bold=True,
            size_hint=(None, None),
            size=(80, 80),
            pos=(160, 0)
        )

        down.bind(on_press=self.go_down)

        self.add_widget(down)

        # LEFT
        left = Button(
            text="LEFT",
            font_size=20,
            bold=True,
            size_hint=(None, None),
            size=(80, 80),
            pos=(70, 50)
        )

        left.bind(on_press=self.go_left)

        self.add_widget(left)

        # RIGHT
        right = Button(
            text="RIGHT",
            font_size=20,
            bold=True,
            size_hint=(None, None),
            size=(80, 80),
            pos=(250, 50)
        )

        right.bind(on_press=self.go_right)

        self.add_widget(right)

    # ================= DIRECTION =================

    def go_up(self, instance):
        self.direction = "UP"

    def go_down(self, instance):
        self.direction = "DOWN"

    def go_left(self, instance):
        self.direction = "LEFT"

    def go_right(self, instance):
        self.direction = "RIGHT"

    # ================= MOVE SNAKE =================

    def move_snake(self):

        x, y = self.snake[0]

        if self.direction == "UP":
            y += self.snake_size

        elif self.direction == "DOWN":
            y -= self.snake_size

        elif self.direction == "LEFT":
            x -= self.snake_size

        elif self.direction == "RIGHT":
            x += self.snake_size

        new_head = (x, y)

        self.snake.insert(0, new_head)

        # ================= FOOD EAT =================

        if (
            abs(new_head[0] - self.food[0]) < 40
            and
            abs(new_head[1] - self.food[1]) < 40
        ):

            self.food = self.random_food()

            self.score += 1

            self.score_label.text = (
                f"Score : {self.score}"
            )

            if self.eat_sound:
                self.eat_sound.play()

        else:
            self.snake.pop()

    # ================= COLLISION =================

    def collision(self):

        x, y = self.snake[0]

        if (
            x < GAME_X or
            x >= GAME_X + GAME_WIDTH or
            y < GAME_Y or
            y >= GAME_Y + GAME_HEIGHT
        ):
            return True

        if self.snake[0] in self.snake[1:]:
            return True

        return False

    # ================= GAME OVER =================

    def game_over_screen(self):

        # RETRY
        self.retry_btn = Button(
            text="RETRY",
            size_hint=(None, None),
            size=(100, 60),
            pos=(20, 300)
        )

        self.retry_btn.bind(on_press=self.retry_game)

        self.add_widget(self.retry_btn)

        # HOME
        self.home_btn = Button(
            text="HOME",
            size_hint=(None, None),
            size=(100, 60),
            pos=(150, 300)
        )

        self.home_btn.bind(on_press=self.go_home)

        self.add_widget(self.home_btn)

        # QUIT
        self.quit_btn = Button(
            text="QUIT",
            size_hint=(None, None),
            size=(100, 60),
            pos=(280, 300)
        )

        self.quit_btn.bind(on_press=self.quit_game)

        self.add_widget(self.quit_btn)

    # ================= RETRY =================

    def retry_game(self, instance):

        self.remove_widget(self.retry_btn)
        self.remove_widget(self.home_btn)
        self.remove_widget(self.quit_btn)

        self.snake = [(160, 400)]

        self.direction = "RIGHT"

        self.food = self.random_food()

        self.score = 0

        self.score_label.text = "Score : 0"

        self.running = True

        Clock.unschedule(self.update)

        Clock.schedule_interval(
            self.update,
            self.speed
        )

    # ================= HOME =================

    def go_home(self, instance):

        self.remove_widget(self.retry_btn)
        self.remove_widget(self.home_btn)
        self.remove_widget(self.quit_btn)

        self.snake = [(160, 400)]

        self.direction = "RIGHT"

        self.food = self.random_food()

        self.score = 0

        self.running = False

        self.score_label.text = "Score : 0"

        self.play_btn = Button(
            text="PLAY",
            size_hint=(None, None),
            size=(140, 60),
            pos=(130, 560),
            background_normal='',
            background_color=(0, 0.7, 0, 1)
        )

        self.play_btn.bind(on_press=self.start_game)

        self.add_widget(self.play_btn)

        self.settings_btn = Button(
            text="SETTINGS",
            size_hint=(None, None),
            size=(140, 60),
            pos=(130, 490),
            background_normal='',
            background_color=(0.2, 0.2, 0.2, 1)
        )

        self.settings_btn.bind(on_press=self.open_settings)

        self.add_widget(self.settings_btn)

    # ================= QUIT =================

    def quit_game(self, instance):
        App.get_running_app().stop()

    # ================= DRAW =================

    def draw_game(self):

        self.canvas.before.clear()

        with self.canvas.before:

            # BACKGROUND
            Rectangle(
                source="background.png",
                pos=(0, 0),
                size=(400, 700)
            )

            # ================= BORDER IMAGE =================

            Rectangle(
                source="border.png",
                pos=(GAME_X, GAME_Y + GAME_HEIGHT),
                size=(GAME_WIDTH, 20)
            )

            Rectangle(
                source="border.png",
                pos=(GAME_X, GAME_Y - 20),
                size=(GAME_WIDTH, 20)
            )

            Rectangle(
                source="border.png",
                pos=(GAME_X - 20, GAME_Y),
                size=(20, GAME_HEIGHT)
            )

            Rectangle(
                source="border.png",
                pos=(GAME_X + GAME_WIDTH, GAME_Y),
                size=(20, GAME_HEIGHT)
            )

            # FOOD
            Rectangle(
                source="food.png",
                pos=self.food,
                size=(40, 40)
            )

            # SNAKE
            for segment in self.snake:

                Rectangle(
                    source="modi.png",
                    pos=segment,
                    size=(40, 40)
                )

    # ================= UPDATE =================

    def update(self, dt):

        if not self.running:
            return

        self.move_snake()

        # GAME OVER
        if self.collision():

            if self.gameover_sound:
                self.gameover_sound.play()

            Clock.unschedule(self.update)

            self.score_label.text = "GAME OVER"

            self.game_over_screen()

        self.draw_game()

# ================= APP =================

class SnakeApp(App):

    def build(self):
        return SnakeGame()

# ================= RUN =================

SnakeApp().run()