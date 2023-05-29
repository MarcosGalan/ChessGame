import pygame

from MainGameScreen import MainGameScreen
from PlayerSelectionScreen import PlayerSelectionScreen
from SceneManager import SceneManager
from Utils.InputStream import InputStream
from Utils.Scene import Scene
from Utils.constants import screen_width, screen_height


class GameTypeSelection(Scene):

    def __init__(self):
        super().__init__()

        self.first =True

        self.board_border = pygame.image.load('assets/images/bordes_tablero.png')
        self.board_border = pygame.transform.scale(self.board_border, (screen_height * 0.8, screen_height * 0.8))

        self.board = pygame.image.load("assets/images/tablero.png")
        self.board = pygame.transform.scale(self.board,
                                            (self.board_border.get_width() * 0.9, self.board_border.get_height() * 0.9))

        self.game_selected = float('+inf')
        self.game_selected_text = "Juego clásico"

        self.info_surface = pygame.surface.Surface(
            (screen_width - self.board_border.get_width() - (screen_width * 0.20), screen_height * 0.85),
            pygame.SRCALPHA)
        self.info_surface_rect = self.info_surface.get_rect(
            topleft=(screen_width * 0.1 + self.board_border.get_width(), screen_height * 0.05))

        self.brown_card = pygame.image.load("assets/images/brown_card.png")
        self.brown_card = pygame.transform.scale(self.brown_card, self.info_surface.get_size())

        self.big_font = pygame.font.Font("assets/fonts/LexendExa-ExtraBold.ttf", 42)
        self.font = pygame.font.Font("assets/fonts/LexendExa-VariableFont_wght.ttf", 32)

        self.new_game = self.big_font.render("NUEVA PARTIDA", False, (236, 236, 236))

        self.blitz_text = self.font.render("BLITZ", False, (236, 236, 236))
        self.quick_text = self.font.render("RAPIDA", False, (236, 236, 236))
        self.classic_text = self.font.render("CLASICA", False, (236, 236, 236))

        self.blitz_icon = pygame.image.load("assets/images/icons/rayo.png")
        self.blitz_icon = pygame.transform.scale(self.blitz_icon, (
        self.info_surface.get_width() * 0.1, self.info_surface.get_width() * 0.1))
        self.blitz_icon_rect = self.blitz_icon.get_rect(
            topleft=(self.info_surface.get_width() * 0.10, self.info_surface.get_height() * 0.15))

        self.clock_icon = pygame.image.load("assets/images/icons/clock.png")
        self.clock_icon = pygame.transform.scale(self.clock_icon, (
        self.info_surface.get_width() * 0.1, self.info_surface.get_width() * 0.1))
        self.clock_icon_rect = self.clock_icon.get_rect(
            topleft=(self.info_surface.get_width() * 0.55, self.info_surface.get_height() * 0.15))

        self.classic_icon = pygame.image.load("assets/images/icons/classic_icon.png")
        self.classic_icon = pygame.transform.scale(self.classic_icon, (
        self.info_surface.get_width() * 0.1, self.info_surface.get_width() * 0.1))
        self.classic_icon_rect = self.classic_icon.get_rect(
            topleft=(self.info_surface.get_width() * 0.3, self.info_surface.get_height() * 0.4))

        self.cream_card = pygame.image.load("assets/images/cream_card.png")
        self.cream_card = pygame.transform.scale(self.cream_card, (
            self.info_surface.get_width() * 0.35, self.info_surface.get_height() * 0.1))

        self.blitz_cream_card = self.cream_card.get_rect(
            topleft=(self.blitz_icon_rect.left, self.blitz_icon_rect.bottom + 15))
        self.quick_cream_card = self.cream_card.get_rect(
            topleft=(self.clock_icon_rect.left, self.clock_icon_rect.bottom + 15))
        self.classic_cream_card = self.cream_card.get_rect(
            topleft=(self.classic_icon_rect.left, self.classic_icon_rect.bottom + 15))

        self.blitz_time_text = self.font.render("5 min", False, (236, 236, 236))
        self.blitz_time_text_rect = self.blitz_time_text.get_rect(center=self.blitz_cream_card.center)
        self.quick_time_text = self.font.render("10 min", False, (236, 236, 236))
        self.quick_time_text_rect = self.quick_time_text.get_rect(center=self.quick_cream_card.center)
        self.classic_time_text = self.font.render("∞", False, (236, 236, 236))
        self.classic_time_text_rect = self.classic_time_text.get_rect(center=self.classic_cream_card.center)

        self.yellow_card = pygame.image.load("assets/images/yellow_card.png")
        self.yellow_card = pygame.transform.scale(self.yellow_card,(self.info_surface.get_width() * 0.35, self.info_surface.get_height() * 0.1))
        self.yellow_card_rect= self.yellow_card.get_rect(center=(self.info_surface.get_width()*0.5,self.info_surface.get_height()*0.8))

        self.start_text = self.font.render("JUGAR",False, (236, 236, 236))
        self.start_text_rect = self.start_text.get_rect(center = self.yellow_card_rect.center)

        self.active_ia = True
        self.player_chess_icon = True

    def input(self, sm: SceneManager, inputStream: InputStream):

        if self.classic_cream_card.collidepoint((inputStream.mouse.getMousePos()[0]-self.info_surface_rect.left,inputStream.mouse.getMousePos()[1]-self.info_surface_rect.top)) and inputStream.mouse.isKeyDown(0):
            self.game_selected = float('+inf')
            self.game_selected_text = "Juego Clasico"
        elif self.blitz_cream_card.collidepoint((inputStream.mouse.getMousePos()[0]-self.info_surface_rect.left,inputStream.mouse.getMousePos()[1]-self.info_surface_rect.top))and inputStream.mouse.isKeyDown(0):
            self.game_selected = 5 * 60
            self.game_selected_text = "Juego Blitz"
        elif self.quick_cream_card.collidepoint((inputStream.mouse.getMousePos()[0]-self.info_surface_rect.left,inputStream.mouse.getMousePos()[1]-self.info_surface_rect.top))and inputStream.mouse.isKeyDown(0):
            self.game_selected = 10*60
            self.game_selected_text = "Juego Rapido"
        elif self.yellow_card_rect.collidepoint((inputStream.mouse.getMousePos()[0]-self.info_surface_rect.left,inputStream.mouse.getMousePos()[1]-self.info_surface_rect.top))and inputStream.mouse.isKeyDown(0):

            sm.set([sm.scenes[0],MainGameScreen(self.player_chess_icon,self.active_ia,self.game_selected)])


    def update(self, sm: SceneManager, inputStream: InputStream):

        if self.first:
            sm.push(PlayerSelectionScreen(self))
            self.first = False

    def draw(self, sm: SceneManager, screen: pygame.surface.Surface):
        screen.fill((189, 162, 114))

        screen.blit(self.board_border, (screen_width * 0.05, screen_height * 0.1))
        screen.blit(self.board, (screen_width * 0.05 + self.board_border.get_width() * 0.0525,
                                 screen_height * 0.1 + self.board_border.get_height() * 0.055))

        screen.blit(self.info_surface, self.info_surface_rect)

        self.info_surface.blit(self.brown_card, (0, 0))
        o = self.new_game.get_rect(center=(self.info_surface.get_width() * 0.5, self.info_surface.get_height() * 0.05))
        self.info_surface.blit(self.new_game, o)

        self.info_surface.blit(self.blitz_icon, self.blitz_icon_rect)
        self.info_surface.blit(self.blitz_text, (self.blitz_icon_rect.right, self.blitz_icon_rect.top))

        self.info_surface.blit(self.clock_icon, self.clock_icon_rect)
        self.info_surface.blit(self.quick_text, (self.clock_icon_rect.right + 5, self.blitz_icon_rect.top))

        self.info_surface.blit(self.classic_icon, self.classic_icon_rect)
        self.info_surface.blit(self.classic_text, (self.classic_icon_rect.right + 5, self.classic_icon_rect.top))

        self.info_surface.blit(self.cream_card, self.blitz_cream_card)
        self.info_surface.blit(self.cream_card, self.quick_cream_card)
        self.info_surface.blit(self.cream_card, self.classic_cream_card)

        self.info_surface.blit(self.blitz_time_text, self.blitz_time_text_rect)
        self.info_surface.blit(self.quick_time_text, self.quick_time_text_rect)
        self.info_surface.blit(self.classic_time_text, self.classic_time_text_rect)

        selected_game_text = self.font.render(self.game_selected_text, False, (236, 236, 236))
        selected_game_text_rect = selected_game_text.get_rect(center=(self.info_surface.get_width()*0.5,self.info_surface.get_height()*0.7))
        self.info_surface.blit(selected_game_text,selected_game_text_rect)

        self.info_surface.blit(self.yellow_card, self.yellow_card_rect)
        self.info_surface.blit(self.start_text,self.start_text_rect)