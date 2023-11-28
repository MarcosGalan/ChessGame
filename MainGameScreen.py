import datetime

import pygame

from SceneManager import SceneManager

from SceneManager import SceneManager
from Utils.InputStream import InputStream
from Utils.Scene import Scene
from Utils.constants import screen_width, screen_height

import gc
import os
import sys
from pygame import mixer
import chess.engine
import time
from mejora_ia import *
import random
import math

class MainGameScreen(Scene):
    def __init__(self, white_colors, active_ia, start_time):
        """
        Funcion encargada de crear pantalla MainGameScreen
        Encargado de realizarlo,Marcos
        """

        super().__init__()
        self.board_border = pygame.image.load('assets/images/bordes_tablero.png')
        self.board_border = pygame.transform.scale(self.board_border, (screen_height * 0.8, screen_height * 0.8))

        # Cambiar el choice por algo seleccionado por el usuario
        self.board = pygame.image.load(f"assets/images/boards/brown.png")
        self.board = pygame.transform.scale(self.board,
                                            (self.board_border.get_width() * 0.9, self.board_border.get_height() * 0.9))

        self.white_colors = white_colors
        if self.white_colors is False:
            self.board = pygame.transform.flip(self.board, False, True)

        self.active_ia = active_ia
        self.info_surface = pygame.surface.Surface(
            (screen_width - self.board_border.get_width() - (screen_width * 0.20), screen_height * 0.85),
            pygame.SRCALPHA)
        self.info_surface_rect = self.info_surface.get_rect(
            topleft=(screen_width * 0.1 + self.board_border.get_width(), screen_height * 0.05))

        self.brown_card = pygame.image.load("assets/images/brown_card.png")
        self.brown_card = pygame.transform.scale(self.brown_card, self.info_surface.get_size())

        self.cream_card = pygame.image.load("assets/images/cream_card_big.png")
        self.cream_card = pygame.transform.scale(self.cream_card, (
            self.info_surface.get_width() * 0.95, self.info_surface.get_height() * 0.7))
        self.cream_card_rect = self.cream_card.get_rect(
            topleft=(self.info_surface_rect.width * 0.025, self.info_surface_rect.height * 0.025))

        self.font = pygame.font.Font("assets/fonts/LexendExa-ExtraBold.ttf", 42)
        font_path = 'assets/fonts/LexendExa-VariableFont_wght.ttf'
        self.font_move_san = pygame.font.Font(font_path, 32)

        self.new_game = self.font.render("MOVIMIENTOS", False, (236, 236, 236))

        self.clear_brown_card = pygame.image.load("assets/images/clear_brown_card.png")
        self.clear_brown_card = pygame.transform.scale(self.clear_brown_card, (
            self.info_surface_rect.width * 0.6, self.info_surface_rect.height * 0.2))
        self.clear_brown_card_rect = self.clear_brown_card.get_rect(
            center=(self.info_surface_rect.width * 0.5, self.info_surface_rect.height * 0.9))

        self.small_cream_card = pygame.transform.scale(self.cream_card, (
            self.clear_brown_card_rect.width * 0.4, self.clear_brown_card_rect.height * 0.4))
        self.left_small_cream_card = self.small_cream_card.get_rect(center=(
            self.clear_brown_card_rect.centerx - self.clear_brown_card_rect.width * 0.225,
            self.clear_brown_card_rect.centery))
        self.right_small_cream_card = self.small_cream_card.get_rect(center=(
            self.clear_brown_card_rect.centerx + self.clear_brown_card_rect.width * 0.225,
            self.clear_brown_card_rect.centery))

        self.time_button = pygame.image.load("assets/images/botton_tiempo.png")
        self.time_button = pygame.transform.scale(self.time_button, (
            self.info_surface_rect.width * 0.1, self.info_surface_rect.width * 0.05))
        self.left_time_button_rect = self.time_button.get_rect(
            center=(self.clear_brown_card_rect.left + self.clear_brown_card_rect.width * 0.25,
                    self.clear_brown_card_rect.top - 8))
        self.right_time_button_rect = self.time_button.get_rect(
            center=(self.clear_brown_card_rect.left + self.clear_brown_card_rect.width * 0.75,
                    self.clear_brown_card_rect.top - 8))


        self.exit_img = pygame.image.load("assets/images/icons/salida.png")
        self.exit_img = pygame.transform.scale(self.exit_img,(screen_width*0.05,screen_width*0.045))
        self.exit_img_rect = self.exit_img.get_rect(bottomright = (screen_width-screen_width*0.02,screen_height-screen_height*0.04))

        self.settings_img = pygame.image.load("assets/images/icons/configuraciones.png")
        self.settings_img = pygame.transform.scale(self.settings_img,(screen_width*0.05,screen_width*0.05))
        self.settings_img_rect = self.settings_img.get_rect(bottomright = (screen_width-screen_width*0.02,self.settings_img.get_width()+screen_height*0.04))

        self.help_img = pygame.image.load("assets/images/icons/help.png")
        self.help_img = pygame.transform.scale(self.help_img,(screen_width*0.05,screen_width*0.05))
        self.help_img_rect = self.help_img.get_rect(topright = (screen_width-screen_width*0.02,self.settings_img_rect.bottom+screen_height*0.04))



        # -----------------------------------------------------------------------------
        self.screen = None

        # # pygame.init()
        # Obtener el tamaño de la pantalla del dispositivo
        info = pygame.display.Info()
        window_width = info.current_w
        window_height = info.current_h
        self.aspect_radio_width = window_width / 1920
        self.aspect_radio_height = window_height / 1080

        # Crear la ventana con la relación de aspecto deseada
        # #screen = pygame.display.set_mode((window_width, window_height))

        # #pygame.display.set_caption("Ajedrez IA")
        if self.white_colors is True:
            x = 141
            y = 155
            self.positions = {}
            for rank in range(8):
                for file in range(8):
                    key = f"{chr(file + ord('a'))}{8 - rank}"
                    value = (x + file * 97, y + rank * 97)
                    self.positions[key] = value
        else:
            x = 820
            y = 834
            self.positions = {}
            for rank in range(8):
                for file in range(8):
                    key = f"{chr(file + ord('a'))}{8 - rank}"
                    value = (x - file * 97, y - rank * 97)
                    self.positions[key] = value

        # Posicion inicial rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
        # Probar posicion final "r2k2q1/8/8/8/8/8/8/3K4 w - - 0 1"
        # Probar posicion final "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        self.table = Ia(starting_FEN="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", depth=2, time=5,
                        positions=self.positions)
        self.table.append_history_actual_board()

        self.invisible_square = pygame.image.load("assets/images/img_in_board/cuadrado_invisible.png").convert_alpha()
        self.invisible_square = pygame.transform.scale(self.invisible_square,
                                                       (97 * self.aspect_radio_height, 97 * self.aspect_radio_width))

        self.circle = pygame.image.load("assets/images/img_in_board/gris.png").convert_alpha()
        self.circle = pygame.transform.scale(self.circle,
                                             (38.8 * self.aspect_radio_height, 38.8 * self.aspect_radio_width))
        self.circle.set_alpha(200)

        self.circle2 = pygame.image.load("assets/images/img_in_board/circulo_rojo.png").convert_alpha()
        self.circle2 = pygame.transform.scale(self.circle2,
                                              (97 * self.aspect_radio_height, 97 * self.aspect_radio_width))
        self.circle2.set_alpha(150)

        self.circle3 = pygame.image.load("assets/images/img_in_board/rojo.png").convert_alpha()
        self.circle3 = pygame.transform.scale(self.circle3,
                                              (97 * self.aspect_radio_height, 97 * self.aspect_radio_width))
        self.circle3.set_alpha(200)

        self.circle4 = pygame.image.load("assets/images/img_in_board/verde.png").convert_alpha()
        self.circle4 = pygame.transform.scale(self.circle4,
                                              (97 * self.aspect_radio_height, 97 * self.aspect_radio_width))
        self.circle4.set_alpha(200)

        # Cargar Sonidos
        self.sound_move_piece = mixer.Sound('assets/sounds/move.wav')
        self.sound_capture_piece = mixer.Sound('assets/sounds/capture.wav')

        # Variables usadas en la interfaz del tablero
        self.valid_moves_piece = []  # Es una lista con los movimientos validos de la pieza pulsada
        self.hitbox_valid_moves = []  # Guarda la hitbox de los movimientos
        self.pieces_instances = []  # Es una lista con la instancia de las piezas que estan tablero

        self.ia_time = False
        if self.white_colors is False and self.active_ia is True:
            self.ia_time = True  # Si es True significa que le toca mover a la IA

        self.ia_time_2 = False  # Si es True significa que le toca mover a la IA
        self.history_activated = False  # Si es True significa que se esta visualizando una jugada anterior
        self.history_count = 0  # Lo que hay que sumarle a la posicion de la lista history
        self.active_recomend_move = False
        self.actual_recomend_move = None
        self.press_activated = False  # Si es True significa que el usuario esta pulsando con click izquierdo
        self.piece_pressed = Ia.Piece(self.table, self.screen)  # Es la instancia de la pieza que se esta arrastrando
        self.time_press_arrow = 0  # Contador para el tiempo de pulsado de las flechas

        self.white_player_time = start_time
        self.black_player_time = start_time

        self.current_turn = True
        self.time_counter = time.time()

    def input(self, sm: SceneManager, inputStream: InputStream):
        """
        Funcion encargada de los inputs.
        Encargado de realizarlo,Marcos
        """

        if inputStream.mouse.isKeyDown(0) and self.exit_img_rect.collidepoint(inputStream.mouse.getMousePos()):
            sm.set([sm.scenes[0]])
        elif inputStream.mouse.isKeyDown(0) and self.settings_img_rect.collidepoint(inputStream.mouse.getMousePos()):
            pass
        elif inputStream.mouse.isKeyDown(0) and self.help_img_rect.collidepoint(inputStream.mouse.getMousePos()):
            self.press_recomend_move()

        self.input_board(inputStream)
        self.input_mouse(inputStream)

    def update(self, sm: SceneManager, inputStream: InputStream):
        """
        Funcion encargada de actualizar.
        Encargado de realizarlo,Marcos
        """
        if self.table.get_board().turn:
            self.white_player_time -= (time.time() - self.time_counter)
        else:
            self.black_player_time -= (time.time() - self.time_counter)


        self.time_counter = time.time()


    def draw(self, sm: SceneManager, screen2: pygame.surface.Surface):
        """
        Funcion encargada de dibujar.
        Encargado de realizarlo,Marcos
        """
        self.screen = screen2
        self.screen.fill((189, 162, 114))

        self.screen.blit(self.board_border, (screen_width * 0.05, screen_height * 0.1))
        self.screen.blit(self.board, (screen_width * 0.05 + self.board_border.get_width() * 0.0525,
                                      screen_height * 0.1 + self.board_border.get_height() * 0.055))

        self.screen.blit(self.info_surface, self.info_surface_rect)

        self.info_surface.blit(self.brown_card, (0, 0))

        self.info_surface.blit(self.cream_card, self.cream_card_rect)

        o = self.new_game.get_rect(center=(self.info_surface.get_width() * 0.5, self.info_surface.get_height() * 0.08))
        self.info_surface.blit(self.new_game, o)

        self.info_surface.blit(self.clear_brown_card, self.clear_brown_card_rect)

        self.info_surface.blit(self.small_cream_card, self.left_small_cream_card)
        self.info_surface.blit(self.small_cream_card, self.right_small_cream_card)

        self.info_surface.blit(self.time_button, self.left_time_button_rect)
        self.info_surface.blit(self.time_button, self.right_time_button_rect)

        if self.black_player_time == float('+inf') or self.white_player_time == float('+inf'):
            whites_text = self.font.render("∞", False,(236, 236, 236))
            blacks_text = self.font.render("∞",False, (236, 236, 236))
        else:
            if self.white_player_time <= 0:
                self.white_player_time = 0
            if self.black_player_time <= 0:
                self.black_player_time = 0
            whites_text = self.font.render(f"{int(self.white_player_time // 60)}:{int(self.white_player_time % 60)}", False,(236, 236, 236))
            blacks_text = self.font.render(f"{int(self.black_player_time//60)}:{int(self.black_player_time%60)}",False, (236, 236, 236))


        text_rect =whites_text.get_rect(center = self.left_small_cream_card.center)
        self.info_surface.blit(whites_text,text_rect)

        text_rect = blacks_text.get_rect(center=self.right_small_cream_card.center)
        self.info_surface.blit(blacks_text, text_rect)

        screen2.blit(self.exit_img,self.exit_img_rect)
        screen2.blit(self.settings_img,self.settings_img_rect)
        screen2.blit(self.help_img,self.help_img_rect)

        self.draw_check_king()
        self.draw_recomend_move()
        self.draw_pieces()
        self.draw_valid_moves_piece()
        self.draw_press_activated()
        self.draw_history_moves_san()
        self.check_ia_time()
        self.check_status_game()

    def input_board(self, inputStream):
        """
        Funcion encargada de los inputs del tablero.
        Encargado de realizarlo,Adrian
        """

        history_list = self.table.get_history()
        time_to_charge = 0.2
        actual_time = time.time()

        if inputStream.keyboard.isKeyDown(pygame.K_LEFT) and len(history_list) != 0 \
                and actual_time - self.time_press_arrow > time_to_charge:
            self.time_press_arrow = actual_time
            self.history_activated = True
            self.history_count -= 1
            history_list = self.table.get_history()
            # Se combrueba si se ha llegado a la primera jugada
            if self.history_count <= -(len(history_list) - 1):
                self.history_count = -(len(history_list) - 1)

            self.table.change_board_FEN(history_list[(len(history_list) - 1) + self.history_count])

            if self.history_count >= 0:
                self.history_activated = False

        elif inputStream.keyboard.isKeyDown(pygame.K_RIGHT) and len(history_list) != 0 \
                and actual_time - self.time_press_arrow > time_to_charge:
            self.time_press_arrow = actual_time
            self.history_activated = True
            self.history_count += 1
            # Se combrueba si se ha llegado a la ultima jugada
            if self.history_count >= 0:
                self.history_count = 0
                self.history_activated = False

            self.table.change_board_FEN(history_list[(len(history_list) - 1) + self.history_count])

        elif inputStream.keyboard.isKeyDown(pygame.K_UP) and len(history_list) != 0:
            self.history_activated = True
            self.history_count = -(len(history_list) - 1)

            self.table.change_board_FEN(history_list[0])

        elif inputStream.keyboard.isKeyDown(pygame.K_DOWN) and len(history_list) != 0:
            self.history_activated = False
            self.history_count = 0

            self.table.change_board_FEN(history_list[len(history_list) - 1])

    def input_mouse(self, inputStream):
        """
        Funcion encargada de los inputs del raton.
        Encargado de realizarlo,Adrian
        """
        # Botón izquierdo del ratón
        if inputStream.mouse.isKeyDown(0) and self.history_activated is False and inputStream.mouse.isKeyPressed(0):
            collision_1 = False
            mouse_pos = pygame.mouse.get_pos()
            # Se chequea la colision de los movimientos legales de la pieza pulsada
            for actual_hitbox_valid_moves in self.hitbox_valid_moves:
                if actual_hitbox_valid_moves[0].collidepoint(mouse_pos):
                    # Se carga el sonido correspondiente
                    if self.table.get_board().piece_at(
                            chess.parse_square(actual_hitbox_valid_moves[1][2:4])) is None:
                        self.sound_move_piece.play()
                    else:
                        self.sound_capture_piece.play()

                    self.table.append_history_moves_san(self.table.uci_to_san(
                        actual_hitbox_valid_moves[1][:2] + actual_hitbox_valid_moves[1][2:]))
                    self.table.move_piece(actual_hitbox_valid_moves[1][:2], actual_hitbox_valid_moves[1][2:])
                    self.table.append_history_actual_board()
                    self.hitbox_valid_moves.clear()
                    self.valid_moves_piece.clear()
                    self.history_count = 0
                    self.active_recomend_move = False
                    if self.active_ia is True:
                        self.ia_time = True
                    collision_1 = True

            if collision_1 is False:
                collision_2 = False
                # Se chequea la colision si se ha pulsado una pieza
                for actual_piece in self.pieces_instances:
                    if actual_piece.hitbox_piece.collidepoint(mouse_pos):
                        self.press_activated = True
                        self.hitbox_valid_moves.clear()
                        self.valid_moves_piece = self.table.piece_movements(actual_piece.position)
                        self.piece_pressed = actual_piece
                        collision_2 = True

                if collision_2 is False:
                    self.hitbox_valid_moves.clear()
                    self.valid_moves_piece.clear()

        if inputStream.mouse.isKeyReleased(0):
            self.press_activated = False
            self.piece_pressed = Ia.Piece(self.table, self.screen)
            if self.history_activated is False:
                # Se obtiene la posición del ratón al levantar el click izquierdo
                mouse_pos = pygame.mouse.get_pos()

                for actual_hitbox_valid_moves in self.hitbox_valid_moves:
                    if actual_hitbox_valid_moves[0].collidepoint(mouse_pos):
                        # Se carga el sonido correspondiente
                        if self.table.get_board().piece_at(
                                chess.parse_square(actual_hitbox_valid_moves[1][2:4])) is None:
                            self.sound_move_piece.play()
                        else:
                            self.sound_capture_piece.play()

                        self.table.append_history_moves_san(self.table.uci_to_san(
                            actual_hitbox_valid_moves[1][:2] + actual_hitbox_valid_moves[1][2:]))
                        self.table.move_piece(actual_hitbox_valid_moves[1][:2],
                                              actual_hitbox_valid_moves[1][2:])
                        self.table.append_history_actual_board()
                        self.hitbox_valid_moves.clear()
                        self.valid_moves_piece.clear()
                        self.active_recomend_move = False
                        self.history_count = 0
                        if self.active_ia is True:
                            self.ia_time = True

    def press_recomend_move(self):
        """
        Funcion encargada de reomendar movimiento
        Encargado de realizarlo,Adrian
        """
        if self.ia_time is False and self.history_activated is False and self.active_recomend_move is False:
            self.actual_recomend_move = self.table.recomend_move()
            self.active_recomend_move = True

    def draw_recomend_move(self):
        """
        Funcion encargada de dibujar el movimiento recomenado
        Encargado de realizarlo,Adrian
        """
        if self.active_recomend_move is True and self.history_activated is False:
            self.screen.blit(self.circle4,
                             (self.positions[self.actual_recomend_move[0]][0] * self.aspect_radio_height,
                              self.positions[self.actual_recomend_move[0]][1] * self.aspect_radio_width))
            self.screen.blit(self.circle4,
                             (self.positions[self.actual_recomend_move[1]][0] * self.aspect_radio_height,
                              self.positions[self.actual_recomend_move[1]][1] * self.aspect_radio_width))

    def draw_check_king(self):
        """
        Funcion encargada de dibujar el rey en jaque
        Encargado de realizarlo,Adrian
        """
        if self.table.get_board().is_check():
            def num_a_casilla(num):
                if num < 0 or num > 63:
                    raise ValueError("El número debe estar entre 0 y 63")
                fila = num // 8
                columna = num % 8
                return chr(columna + ord('a')) + str(fila + 1)

            turn = self.table.get_board().turn
            if turn:
                position_king = self.table.get_board().king(chess.WHITE)
            else:
                position_king = self.table.get_board().king(chess.BLACK)

            self.screen.blit(self.circle3,
                             (self.positions[num_a_casilla(position_king)][0] * self.aspect_radio_height,
                              self.positions[num_a_casilla(position_king)][1] * self.aspect_radio_width))

    def draw_pieces(self):
        """
        Funcion encargada de dibujar las piezas
        Encargado de realizarlo,Adrian
        """
        def num_a_casilla(num):
            if num < 0 or num > 63:
                raise ValueError("El número debe estar entre 0 y 63")
            fila = num // 8
            columna = num % 8
            return chr(columna + ord('a')) + str(fila + 1)

        self.pieces_instances.clear()
        # # screen.blit(tablero, (0, 0))
        for square in chess.SQUARES:
            piece = self.table.get_board().piece_at(square)
            if piece:
                if num_a_casilla(square) != self.piece_pressed.position:
                    piece_name = piece.symbol()
                    p = Ia.Piece(self.table, self.screen)
                    p.change_piece_image(piece_name)  # Cambiamos la imagen que hay en la clase pieza
                    p.blit_image(num_a_casilla(square))  # Proyectamos la imagen con hitbox en el tablero
                    self.pieces_instances.append(p)  # Metemos la instancia de la piece en la lista

    def draw_valid_moves_piece(self):
        """
        Funcion encargada de dibujar los movimientos posibles
        Encargado de realizarlo,Adrian
        """
        if self.valid_moves_piece is not None and self.history_activated is False:  # Cambiar
            # Se recorren los movimientos validos de la pieza pulsada para mostrarlo por pantalla
            for legal_moves_touch_piece in self.valid_moves_piece:
                hitbox_r = self.invisible_square.get_rect()
                hitbox_r.x = (self.positions[legal_moves_touch_piece[2:4]][0] + 3) * self.aspect_radio_height
                hitbox_r.y = self.positions[legal_moves_touch_piece[2:4]][1] * self.aspect_radio_width

                circle_x = self.positions[legal_moves_touch_piece[2:4]][0]
                circle_y = self.positions[legal_moves_touch_piece[2:4]][1]

                if self.table.get_board().piece_at(chess.parse_square(legal_moves_touch_piece[2:4])) is None:
                    self.screen.blit(self.circle,
                                     ((circle_x + 30) * self.aspect_radio_height,
                                      (circle_y + 30) * self.aspect_radio_width))
                else:
                    self.screen.blit(self.circle2, (
                        (circle_x + 1.5) * self.aspect_radio_height, (circle_y + 1.5) * self.aspect_radio_width))

                self.screen.blit(self.invisible_square, hitbox_r)
                self.hitbox_valid_moves.append([hitbox_r, legal_moves_touch_piece])

    def draw_press_activated(self):
        """
        Funcion encargada dibujar si press esta activado
        Encargado de realizarlo,Adrian
        """
        if self.press_activated is True:  # Cambiar
            mouse_pos = pygame.mouse.get_pos()
            self.screen.blit(self.piece_pressed.image,
                             (mouse_pos[0] - (48 * self.aspect_radio_height),
                              mouse_pos[1] - (48 * self.aspect_radio_width)))

    def draw_history_moves_san(self):
        """
        Funcion encargada de dibujar el historial de movimientos
        Encargado de realizarlo,Adrian
        """
        list_moves = self.table.get_history_moves_san()
        counter_san = 0
        start_san = 0
        max_moves = 11
        if len(list_moves) / 2 > max_moves:
            # start_san = len(list_moves) - (max_moves+self.history_count) * 2
            start_san = len(list_moves) - max_moves * 2
            shizuka = start_san / 2
            if shizuka - int(shizuka) == 0.5:
                counter_san = round((start_san / 2)) + 1
                if start_san % 2 == 1 and (start_san - 3) % 4 == 0:
                    counter_san -= 1
            else:
                counter_san = round(start_san / 2)

        j = 0
        for i in range(start_san, len(list_moves)):
            if i % 2 == 0:
                counter_san += 1
                actual_pos = (1150 * self.aspect_radio_height, (170 + (j * 50)) * self.aspect_radio_width)
                # self.screen.blit(self.circle, actual_pos)
                if i == len(list_moves) - 1:
                    actual_text_0 = self.font_move_san.render(f"{counter_san}.", True, (235, 235, 235))
                    actual_text = self.font_move_san.render(list_moves[i], True, (235, 235, 235))
                    actual_text_2 = self.font_move_san.render("", True, (235, 235, 235))
                else:
                    actual_text_0 = self.font_move_san.render(f"{counter_san}.", True, (235, 235, 235))
                    actual_text = self.font_move_san.render(list_moves[i], True, (235, 235, 235))
                    actual_text_2 = self.font_move_san.render(list_moves[i + 1], True, (235, 235, 235))

                self.screen.blit(actual_text_0, (actual_pos[0], actual_pos[1]))
                self.screen.blit(actual_text, (actual_pos[0] + 100, actual_pos[1]))
                self.screen.blit(actual_text_2, (actual_pos[0] + 300, actual_pos[1]))
                j += 1

    def check_ia_time(self):
        """
        Funcion encargada de verificar los tiempos.
        Encargado de realizarlo,Adrian
        """
        if self.ia_time is True:  # Cambiar
            if self.ia_time_2 is True:
                old_table = self.table.get_board().copy()
                calculate_time_ia = time.time()
                self.table.movement_calc()
                new_table = self.table.get_board()
                if old_table.turn:
                    self.white_player_time -= (time.time() - calculate_time_ia)
                else:
                    self.black_player_time -= (time.time() - calculate_time_ia)

                ai_move = self.table.two_board_to_piece_move(False, old_table, new_table)

                # Se carga el sonido correspondiente
                try:
                    if old_table.piece_at(chess.parse_square(ai_move[1])) is None:
                        self.sound_move_piece.play()
                    else:
                        self.sound_capture_piece.play()
                except:
                    self.sound_move_piece.play()

                self.table.append_history_actual_board()
                self.ia_time = False
                self.ia_time_2 = False
            else:
                self.ia_time_2 = True

    def check_status_game(self):
        """
        Funcion encargada de revisar el estado del juego
        Encargado de realizarlo,Adrian
        """
        if self.table.get_board().is_checkmate():
            # print("JAQUE MATE")
            print(self.table.get_board().result())
            if self.table.get_board().result() == "1-0":
                self.new_game = self.font.render("HA GANADO BLANCAS", False, (236, 236, 236))
            else:
                self.new_game = self.font.render("HA GANADO NEGRAS", False, (236, 236, 236))
            self.ia_time = False
            self.ia_time_2 = False
            self.history_activated = True

        if self.white_player_time <= 0:
            self.new_game = self.font.render("HA GANADO NEGRAS", False, (236, 236, 236))
            self.ia_time = False
            self.ia_time_2 = False
            self.history_activated = True
        if self.black_player_time <= 0:
            self.new_game = self.font.render("HA GANADO BLANCAS", False, (236, 236, 236))
            self.ia_time = False
            self.ia_time_2 = False
            self.history_activated = True

        if self.table.get_board().is_stalemate() or self.table.get_board().is_insufficient_material():
            # print("TABLAS")
            # print(self.table.get_board().result())
            self.new_game = self.font.render("TABLAS", False, (236, 236, 236))
            self.ia_time = False
            self.ia_time_2 = False
            self.history_activated = True

        # PROBANDO
        if self.table.get_board().is_fifty_moves():
            # print("fifty moves")
            self.new_game = self.font.render("TABLAS", False, (236, 236, 236))
            self.ia_time = False
            self.ia_time_2 = False
            self.history_activated = True
        if self.table.get_board().is_fivefold_repetition():
            # print("five_repitions")
            self.new_game = self.font.render("TABLAS", False, (236, 236, 236))
            self.ia_time = False
            self.ia_time_2 = False
            self.history_activated = True
        if self.table.get_board().is_seventyfive_moves():
            # print("seventifive moves")
            self.new_game = self.font.render("TABLAS", False, (236, 236, 236))
            self.ia_time = False
            self.ia_time_2 = False
            self.history_activated = True
        if self.table.get_board().is_repetition():
            # print("is repition")
            self.new_game = self.font.render("TABLAS", False, (236, 236, 236))
            self.ia_time = False
            self.ia_time_2 = False
            self.history_activated = True
