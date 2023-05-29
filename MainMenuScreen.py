import pygame

from GameTypeSelection import GameTypeSelection
from SceneManager import SceneManager
from Utils.InputStream import InputStream
from Utils.Scene import Scene
from Utils.constants import *


class MainMenuScreen(Scene):

    def __init__(self):
        super().__init__()

        self.bg = pygame.image.load("assets/images/background.png")
        self.bg = pygame.transform.scale(self.bg, (screen_width,screen_height))

        self.font = pygame.font.Font("assets/fonts/LexendExa-VariableFont_wght.ttf", 42)
        self.big_font = pygame.font.Font("assets/fonts/LexendExa-ExtraBold.ttf", 124)

        self.main_text = self.big_font.render("I-CHESS", True, (235, 235, 235))

        self.start_text = self.font.render("START", True, (235, 235, 235))
        self.start_text_rect = self.start_text.get_rect(center=(screen_width * 0.35, screen_height * 0.5))

        self.quit_text = self.font.render("QUIT", True, (235, 235, 235))
        self.quit_text_rect = self.quit_text.get_rect(center=(screen_width * 0.65, screen_height * 0.5))

        pygame.mixer.music.load('assets/sounds/musica_fondo.mp3')
        pygame.mixer.music.play(-1)

    def input(self, sm: SceneManager, inputStream: InputStream):
        if inputStream.mouse.isKeyDown(0) and self.start_text_rect.collidepoint(inputStream.mouse.getMousePos()):
            sm.push(GameTypeSelection())
            pygame.mixer.music.pause()
            pygame.mixer.music.unload()
        elif inputStream.mouse.isKeyDown(0) and self.quit_text_rect.collidepoint(inputStream.mouse.getMousePos()):
            sm.pop()


    def update(self, sm: SceneManager, inputStream: InputStream):
        pass

    def draw(self, sm: SceneManager, screen: pygame.surface.Surface):
        screen.blit(self.bg, (0, 0))

        pos = self.main_text.get_rect(center=(screen_width * 0.5, screen_height * 0.250))
        screen.blit(self.main_text, pos)


        screen.blit(self.start_text, self.start_text_rect)


        screen.blit(self.quit_text, self.quit_text_rect)

