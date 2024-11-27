import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *


class Menu:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = pg.font.SysFont("arial", 50)
        self.options = ["Iniciar Juego", "Configuración", "Salir"]
        self.selected_option = 0

    def draw(self):
        self.screen.fill("black")
        title_surface = self.font.render("Miedo a lo Desconocido", True, "white")
        title_rect = title_surface.get_rect(center=(self.game.screen.get_width() // 2, 100))
        self.screen.blit(title_surface, title_rect)

        for i, option in enumerate(self.options):
            color = "yellow" if i == self.selected_option else "white"
            option_surface = self.font.render(option, True, color)
            option_rect = option_surface.get_rect(center=(self.game.screen.get_width() // 2, 200 + i * 80))
            self.screen.blit(option_surface, option_rect)

        pg.display.flip()

    def handle_input(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pg.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pg.K_RETURN:
                    if self.selected_option == 0:  # Iniciar Juego
                        self.game.start_game()
                    elif self.selected_option == 1:  # Configuración
                        self.game.open_config_menu()
                    elif self.selected_option == 2:  # Salir
                        pg.quit()
                        sys.exit()


class PauseMenu:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = pg.font.SysFont("arial", 50)
        self.options = ["Continuar", "Salir al Menú Principal", "Salir del Juego"]
        self.selected_option = 0

    def draw(self):
        self.screen.fill("black")
        pause_surface = self.font.render("Pausa", True, "white")
        pause_rect = pause_surface.get_rect(center=(self.game.screen.get_width() // 2, 100))
        self.screen.blit(pause_surface, pause_rect)

        for i, option in enumerate(self.options):
            color = "yellow" if i == self.selected_option else "white"
            option_surface = self.font.render(option, True, color)
            option_rect = option_surface.get_rect(center=(self.game.screen.get_width() // 2, 200 + i * 80))
            self.screen.blit(option_surface, option_rect)

        pg.display.flip()

    def handle_input(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pg.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pg.K_RETURN:
                    if self.selected_option == 0:  # Continuar
                        self.game.resume_game()
                    elif self.selected_option == 1:  # Salir al Menú Principal
                        self.game.return_to_main_menu()
                    elif self.selected_option == 2:  # Salir del Juego
                        pg.quit()
                        sys.exit()


class Slider:
    def __init__(self, x, y, width, min_val, max_val, value, label):
        self.rect = pg.Rect(x, y, width, 10)
        self.handle_rect = pg.Rect(x + (value - min_val) / (max_val - min_val) * width - 5, y - 10, 10, 30)
        self.min_val = min_val
        self.max_val = max_val
        self.value = value
        self.label = label
        self.font = pg.font.SysFont("arial", 25)
        self.dragging = False

    def draw(self, screen):
        pg.draw.rect(screen, "white", self.rect)
        pg.draw.rect(screen, "yellow", self.handle_rect)
        label_surface = self.font.render(f"{self.label}: {self.value:.1f}", True, "white")
        label_rect = label_surface.get_rect(center=(self.rect.x + self.rect.width // 2, self.rect.y - 20))
        screen.blit(label_surface, label_rect)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and self.handle_rect.collidepoint(event.pos):
            self.dragging = True
        elif event.type == pg.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pg.MOUSEMOTION and self.dragging:
            new_x = max(self.rect.x, min(event.pos[0], self.rect.x + self.rect.width))
            self.handle_rect.x = new_x - 5
            self.value = self.min_val + (new_x - self.rect.x) / self.rect.width * (self.max_val - self.min_val)


class ConfigMenu:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = pg.font.SysFont("arial", 50)
        self.sliders = [
            Slider(300, 200, 400, 0, 1, 0.5, "Volumen"),
            Slider(300, 300, 400, 0.1, 2, 1, "Sensibilidad del Mouse")
        ]

    def draw(self):
        self.screen.fill("black")
        title_surface = self.font.render("Configuración", True, "white")
        title_rect = title_surface.get_rect(center=(self.game.screen.get_width() // 2, 100))
        self.screen.blit(title_surface, title_rect)

        for slider in self.sliders:
            slider.draw(self.screen)

        back_surface = self.font.render("Presiona ESC para regresar", True, "gray")
        back_rect = back_surface.get_rect(center=(self.game.screen.get_width() // 2, 500))
        self.screen.blit(back_surface, back_rect)

        pg.display.flip()

    def handle_input(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.game.exit_config_menu()
            for slider in self.sliders:
                slider.handle_event(event)

    def apply_settings(self):
        volume = self.sliders[0].value
        sensitivity = self.sliders[1].value
        pg.mixer.music.set_volume(volume)
        self.game.player.sensitivity = sensitivity


class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        pg.event.set_grab(True)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)
        self.menu = Menu(self)
        self.pause_menu = PauseMenu(self)
        self.config_menu = ConfigMenu(self)
        self.in_game = False
        self.paused = False
        self.in_config = False

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)
        pg.mixer.music.play(-1)

    def update(self):
        if self.in_game and not self.paused and not self.in_config:
            self.player.update()
            self.raycasting.update()
            self.object_handler.update()
            self.weapon.update()
            pg.display.flip()
            self.delta_time = self.clock.tick(FPS)
            pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        if self.in_game and not self.paused and not self.in_config:
            self.object_renderer.draw()
            self.weapon.draw()

    def check_events(self):
        self.global_trigger = False
        if self.in_config:
            self.config_menu.handle_input()
        elif self.paused:
            self.pause_menu.handle_input()
        elif self.in_game:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    self.paused = True
                elif event.type == self.global_event:
                    self.global_trigger = True
                self.player.single_fire_event(event)
        else:
            self.menu.handle_input()

    def run(self):
        while True:
            self.check_events()
            if self.in_config:
                self.config_menu.draw()
            elif self.paused:
                self.pause_menu.draw()
            elif self.in_game:
                self.update()
                self.draw()
            else:
                self.menu.draw()

    def start_game(self):
        self.in_game = True
        self.paused = False
        self.new_game()

    def resume_game(self):
        self.paused = False

    def open_config_menu(self):
        self.in_config = True

    def exit_config_menu(self):
        self.in_config = False
        self.config_menu.apply_settings()

    def return_to_main_menu(self):
        self.in_game = False
        self.paused = False
        self.in_config = False


if __name__ == '__main__':
    game = Game()
    game.run()