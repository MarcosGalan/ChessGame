import random
import sys
import pygame

import SceneManager
from MainMenuScreen import MainMenuScreen
from Utils.constants import screen_width, screen_height
from Utils.InputStream import InputStream


"""Archivo inicializador encargado

Diseño De Interfaz encargados Jaime, Esteban, Sandra, Oscar Fabris y Antonio
Algoritmo de Evaluacion encargados Santino, Oscar Haotian, Gonzalo y Antonio
Encargados de Base de Datos Rodrigo, Alberto Yesares, Marco, Jorge y Carolina
Encargados de la programacion de interfaz, logica, ia e integracion de base de datos Adrian y Marcos

"""

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('AJEDREZ')
clock = pygame.time.Clock()

sceneManager = SceneManager.SceneManager()
mainMenu = MainMenuScreen()
sceneManager.push(mainMenu)

inputStream = InputStream()

running = True
if __name__ == '__main__':

    while running:
        events = pygame.event.get()
        inputStream.events = events
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        inputStream.processInput()

        if sceneManager.isEmpty():
            running = False

        sceneManager.input(inputStream)
        sceneManager.update(inputStream)
        sceneManager.draw(screen)

        clock.tick(60)

pygame.quit()
sys.exit()
