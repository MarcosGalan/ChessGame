import pygame
from pygame.locals import *
import sys

# pygame.init()
# ANCHO_VENTANA = 800
# ALTO_VENTANA = 600
# ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
# pygame.display.set_caption("Menú desplegable")

MARRON_OSCLARO = (145,108,72,255)
MARRON_OSCURO = ((95,68,46,255))
MARRON_CLARITO = (145,108,72,255)

COLOR_FONDO = (255, 255, 255)
COLOR_TEXTO = (255, 255, 255)
COLOR_MENU = (145,108,72,255)
COLOR_OPCION = (145,108,72,255)
COLOR_OPCION_SELECCIONADA = (95,68,46,255)
# FUENTE = pygame.font.Font(None, 24)

class MenuDesplegable:
    def __init__(self,  x, y,opciones):
        self.x = x
        self.y = y
        self.opciones = opciones
        self.desplegado = False
        self.opcion_seleccionada = None

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, COLOR_MENU, (self.x, self.y, 100, 30),0,3)
        pygame.draw.line(ventana, COLOR_TEXTO, (self.x + 50, self.y + 10), (self.x + 50, self.y + 20), 0)

        fuente = pygame.font.SysFont(None, 24)
        texto_pestaña = fuente.render('Menú', True, COLOR_TEXTO)
        ventana.blit(texto_pestaña, (self.x + 10, self.y + 5))

        if self.desplegado:
            for i, opcion in enumerate(self.opciones):
                pygame.draw.rect(ventana, COLOR_OPCION, (self.x, self.y + 30 + i * 30, 100, 30),0,3)

                texto_opcion = fuente.render(opcion, True, COLOR_TEXTO)
                ventana.blit(texto_opcion, (self.x + 10, self.y + 35 + i * 30))

                if self.opcion_seleccionada is not None and self.opcion_seleccionada == i:
                    pygame.draw.rect(ventana, COLOR_OPCION_SELECCIONADA, (self.x, self.y + 30 + i * 30, 100, 30),0,3)
                    ventana.blit(texto_opcion, (self.x + 10, self.y + 35 + i * 30))

    def toggle_desplegado(self):
        self.desplegado = not self.desplegado

    def seleccionar_opcion(self, pos):
        if self.desplegado:
            x, y = pos
            if 10 <= x <= 160 and 40 <= y <= 40 + len(self.opciones) * 30:
                indice = (y - 40) // 30
                self.opcion_seleccionada = indice

#
# opciones = ["Tablero 1", "Tablero 2", "Tablero 3"]
# menu = MenuDesplegable(10,10,opciones)
#
#
# while True:
#     for event in pygame.event.get():
#         if event.type == QUIT:
#             pygame.quit()
#             sys.exit()
#         elif event.type == MOUSEBUTTONDOWN:
#             if event.button == 1:
#                 if 10 <= event.pos[0] <= 160 and 10 <= event.pos[1] <= 40:
#                     menu.toggle_desplegado()
#                 else:
#                     menu.seleccionar_opcion(event.pos)
#
#     ventana.fill(COLOR_FONDO)
#     menu.dibujar(ventana)
#     pygame.display.flip()