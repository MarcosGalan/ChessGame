import random

import pygame

from SceneManager import SceneManager
from Utils.InputStream import InputStream
from Utils.Scene import Scene
from Utils.constants import screen_width, screen_height


class PlayerSelectionScreen(Scene):

    def __init__(self, last_screen: Scene):
        """
        Funcion encargada de crear pantalla PlayerSelectionScreen
        Encargado de realizarlo,Marcos
        """
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

        self.main_text = self.big_font.render("OPCIONES", False, (236, 236, 236))
        self.main_text_rect = self.main_text.get_rect(
            center=(self.options_surface.get_width() * 0.5, self.options_surface.get_height() * 0.1))

        self.cream_rectangle = pygame.image.load("assets/images/cream_card.png")
        self.cream_rectangle = pygame.transform.scale(self.cream_rectangle, (
            self.brown_card.get_width() * 0.4, self.brown_card.get_height() * 0.18))
        self.cream_square = pygame.transform.scale(self.cream_rectangle, (
            self.brown_card.get_height() * 0.18, self.brown_card.get_height() * 0.18))

        self.first_player_square = self.cream_rectangle.get_rect(
            center=(self.options_surface_rect.width * 0.25, self.options_surface_rect.height * 0.3))
        self.first_player_icon_square = self.cream_square.get_rect(
            center=(self.options_surface_rect.width * 0.25, self.options_surface_rect.height * 0.55))

        self.second_player_square = self.cream_rectangle.get_rect(
            center=(self.options_surface_rect.width * 0.75, self.options_surface_rect.height * 0.3))
        self.second_player_icon_square = self.cream_square.get_rect(
            center=(self.options_surface_rect.width * 0.75, self.options_surface_rect.height * 0.55))

        self.first_player_text = self.font.render("JUGADOR 1", False, (236, 236, 236))
        self.first_player_rect = self.first_player_text.get_rect(center=self.first_player_square.center)

        self.active_ia = True

        # True es blancas False es negras
        self.black_king_image = pygame.image.load("assets/images/pieces/png_alpha/bK.png")
        self.black_king_image = pygame.transform.scale(self.black_king_image, (
            self.cream_square.get_width() * 0.8, self.cream_square.get_height() * 0.8))
        self.white_king_image = pygame.image.load("assets/images/pieces/png_alpha/wK.png")
        self.white_king_image = pygame.transform.scale(self.white_king_image, (
            self.cream_square.get_width() * 0.8, self.cream_square.get_height() * 0.8))

        self.player_chess_icon = True

        # Random piece square
        self.small_cream_square = pygame.transform.scale(self.cream_rectangle, (
            self.brown_card.get_height() * 0.14, self.brown_card.get_height() * 0.14))
        self.small_cream_square_rect = self.small_cream_square.get_rect(
            center=(self.options_surface_rect.width * 0.5, self.options_surface_rect.height * 0.55))

        self.random_dice = pygame.image.load("assets/images/icons/dado.png")
        self.random_dice = pygame.transform.scale(self.random_dice, (
        self.small_cream_square_rect.width * 0.6, self.small_cream_square_rect.height * 0.6))
        self.random_dice_rect = self.random_dice.get_rect(center=(self.small_cream_square_rect.center))

        self.yellow_card = pygame.image.load("assets/images/yellow_card.png")
        self.yellow_card = pygame.transform.scale(self.yellow_card, (self.options_surface.get_width() * 0.35, self.options_surface.get_height() * 0.1))
        self.yellow_card_rect = self.yellow_card.get_rect(center=(self.options_surface.get_width() * 0.5, self.options_surface.get_height() * 0.8))

        self.start_text = self.font.render("JUGAR", False, (236, 236, 236))
        self.start_text_rect = self.start_text.get_rect(center=self.yellow_card_rect.center)

    def input(self, sm: SceneManager, inputStream: InputStream):
        """
        Funcion encargada de los inputs.
        Encargado de realizarlo,Marcos
        """
        if self.small_cream_square_rect.collidepoint((inputStream.mouse.getMousePos()[0] - self.options_surface_rect.left,inputStream.mouse.getMousePos()[1] - self.options_surface_rect.top)) and inputStream.mouse.isKeyPressed(0):
            self.player_chess_icon = True if random.randint(a=0,b=1)==1 else False
        elif self.second_player_square.collidepoint((inputStream.mouse.getMousePos()[0] - self.options_surface_rect.left,inputStream.mouse.getMousePos()[1] - self.options_surface_rect.top)) and inputStream.mouse.isKeyPressed(0):
            self.active_ia = not self.active_ia

        elif self.yellow_card_rect.collidepoint((inputStream.mouse.getMousePos()[0] - self.options_surface_rect.left, inputStream.mouse.getMousePos()[1] - self.options_surface_rect.top)) and inputStream.mouse.isKeyPressed(0):
            self.last_screen.active_ia = self.active_ia
            self.last_screen.player_chess_icon = self.player_chess_icon
            sm.pop()

    def update(self, sm: SceneManager, inputStream: InputStream):
        """
        Funcion encargada de actualizar.
        Encargado de realizarlo,Marcos
        """
        pass

    def draw(self, sm: SceneManager, screen: pygame.surface.Surface):
        """
        Funcion encargada de dibujar.
        Encargado de realizarlo,Marcos
        """
        self.last_screen.draw(sm, screen)
        screen.blit(self.cream_bg, (0, 0))

        screen.blit(self.options_surface, self.options_surface_rect)
        self.options_surface.blit(self.brown_card, (0, 0))
        self.options_surface.blit(self.main_text, self.main_text_rect)
        self.options_surface.blit(self.cream_rectangle, self.first_player_square)
        self.options_surface.blit(self.cream_rectangle, self.second_player_square)

        self.options_surface.blit(self.first_player_text, self.first_player_rect)

        if self.active_ia:
            second_player_text = self.font.render("IA", False, (236, 236, 236))
        else:
            second_player_text = self.font.render("JUGADOR 2", False, (236, 236, 236))

        second_player_rect = second_player_text.get_rect(center=self.second_player_square.center)
        self.options_surface.blit(second_player_text, second_player_rect)

        self.options_surface.blit(self.cream_square, self.first_player_icon_square)
        self.options_surface.blit(self.cream_square, self.second_player_icon_square)

        if self.player_chess_icon:
            o = self.white_king_image.get_rect(center=self.first_player_icon_square.center)
            self.options_surface.blit(self.white_king_image, o)
            o = self.black_king_image.get_rect(center=self.second_player_icon_square.center)
            self.options_surface.blit(self.black_king_image, o)
        else:
            o = self.black_king_image.get_rect(center=self.first_player_icon_square.center)
            self.options_surface.blit(self.black_king_image, o)
            o = self.white_king_image.get_rect(center=self.second_player_icon_square.center)
            self.options_surface.blit(self.white_king_image, o)

        self.options_surface.blit(self.small_cream_square, self.small_cream_square_rect)

        self.options_surface.blit(self.random_dice, self.random_dice_rect)

        self.options_surface.blit(self.yellow_card,self.yellow_card_rect)
        self.options_surface.blit(self.start_text,self.start_text_rect)
