import pygame

from SceneManager import SceneManager
from Utils.InputStream import InputStream
from Utils.MenuDesplegable import MenuDesplegable
from Utils.Scene import Scene
from Utils.constants import screen_width, screen_height


class SettingsScreen(Scene):

    def __init__(self, last_screen: Scene):
        super().__init__()

        self.last_screen = last_screen

        self.cream_bg = pygame.image.load("assets/images/cream_transparency.png")
        self.cream_bg = pygame.transform.scale(self.cream_bg, (screen_width, screen_height))

        self.options_surface = pygame.surface.Surface((screen_width * 0.4, screen_height * 0.65), pygame.SRCALPHA)
        self.options_surface_rect = self.options_surface.get_rect(center=(screen_width * 0.5, screen_height * 0.45))

        self.brown_card = pygame.image.load("assets/images/brown_card.png")
        self.brown_card = pygame.transform.scale(self.brown_card, self.options_surface.get_size())

        self.big_font = pygame.font.Font("assets/fonts/LexendExa-ExtraBold.ttf", 42)
        self.font = pygame.font.Font("assets/fonts/LexendExa-VariableFont_wght.ttf", 32)

        self.main_text = self.big_font.render("AJUSTES", False, (236, 236, 236))
        self.main_text_rect = self.main_text.get_rect(
            center=(self.options_surface.get_width() * 0.5, self.options_surface.get_height() * 0.1))

        self.yellow_card = pygame.image.load("assets/images/yellow_card.png")
        self.yellow_card = pygame.transform.scale(self.yellow_card, (self.options_surface.get_width() * 0.35, self.options_surface.get_height() * 0.1))
        self.yellow_card_rect = self.yellow_card.get_rect(center=(self.options_surface.get_width() * 0.5, self.options_surface.get_height() * 0.9))

        self.tables_drop_menu = MenuDesplegable(self.options_surface_rect.width*0.2,self.options_surface_rect.height*0.4,["brown", "green", "blue", "purple", "green-plastic", "newspaper"])

        self.save_text = self.font.render("GUARDAR", False, (236, 236, 236))
        self.save_text_rect = self.save_text.get_rect(center=self.yellow_card_rect.center)

    def input(self, sm: SceneManager, inputStream: InputStream):
        pass

    def update(self, sm: SceneManager, inputStream: InputStream):
        pass

    def draw(self, sm: SceneManager, screen: pygame.surface.Surface):
        self.last_screen.draw(sm, screen)
        screen.blit(self.cream_bg, (0, 0))

        screen.blit(self.options_surface, self.options_surface_rect)
        self.options_surface.blit(self.brown_card, (0, 0))
        self.options_surface.blit(self.main_text, self.main_text_rect)

        self.tables_drop_menu.dibujar(self.options_surface)

        self.options_surface.blit(self.yellow_card,self.yellow_card_rect)
        self.options_surface.blit(self.save_text,self.save_text_rect)