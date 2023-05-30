import os
import sys
import time
import pygame
import chess
import chess.engine
import random

import chess.polyglot
import functools

import sqlite3


class Board:
    def __init__(self, board: str, parent, childs: list):
        self.board = chess.Board(f'{board}')
        self.board.__hash__ = chess.polyglot.zobrist_hash

        self.parent = parent
        self.childs = childs

    def evaluate_self(self, engine):
        info = engine.analyse(self.board, chess.engine.Limit(time=0.1))
        score = info["score"].relative.score(mate_score=100000)
        return score


class Ia:
    class Piece:
        def __init__(self, instance, screen):
            self.image = None
            self.type_piece = None
            self.hitbox_piece = None
            self.position = None
            self.instance = instance
            self.screen = screen

        def change_piece_image(self, piece_n):
            # global images_pieces, aspect_radio_width, aspect_radio_height
            self.type_piece = piece_n
            # 0.25 antigua interfaz
            self.image = pygame.transform.scale(self.instance.images_pieces[piece_n],
                                                ((self.instance.images_pieces[
                                                      piece_n].get_height() * 0.2425) * self.instance.aspect_radio_height,
                                                 self.instance.images_pieces[
                                                     piece_n].get_width() * 0.2425 * self.instance.aspect_radio_width))

        def hitbox_of_piece(self, position_piece):
            # global aspect_radio_width, aspect_radio_height
            hitbox_p = self.image.get_rect()
            hitbox_p.x = (self.instance.positions[position_piece][0]) * self.instance.aspect_radio_height
            hitbox_p.y = (self.instance.positions[position_piece][1]) * self.instance.aspect_radio_width
            return hitbox_p

        def blit_image(self, position_piece):
            # global positions, screen
            self.position = position_piece
            hitbox_p = self.hitbox_of_piece(position_piece)
            self.hitbox_piece = hitbox_p
            self.screen.blit(self.image, hitbox_p)

        def blit_image_move(self, pixel_position):
            # global screen
            self.screen.blit(self.image, pixel_position)

    def __init__(self, starting_FEN: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", depth=3, time=5, positions=None):

        info = pygame.display.Info()
        window_width = info.current_w
        window_height = info.current_h
        self.aspect_radio_width = window_width / 1920
        self.aspect_radio_height = window_height / 1080
        self.positions = positions
        # CAMBIAR
        names_pieces_images = ["alpha", "cardinal", "maestro", "merida"]
        bb = random.choice(names_pieces_images)
        self.images_pieces = {
            "P": pygame.transform.scale(pygame.image.load(f"assets/images/pieces/png_{bb}/wP.png").convert_alpha(),
                                        (400, 400)),
            "B": pygame.transform.scale(pygame.image.load(f"assets/images/pieces/png_{bb}/wB.png").convert_alpha(),
                                        (400, 400)),
            "N": pygame.transform.scale(pygame.image.load(f"assets/images/pieces/png_{bb}/wN.png").convert_alpha(),
                                        (400, 400)),
            "R": pygame.transform.scale(pygame.image.load(f"assets/images/pieces/png_{bb}/wR.png").convert_alpha(),
                                        (400, 400)),
            "Q": pygame.transform.scale(pygame.image.load(f"assets/images/pieces/png_{bb}/wQ.png").convert_alpha(),
                                        (400, 400)),
            "K": pygame.transform.scale(pygame.image.load(f"assets/images/pieces/png_{bb}/wK.png").convert_alpha(),
                                        (400, 400)),
            "p": pygame.transform.scale(pygame.image.load(f"assets/images/pieces/png_{bb}/bP.png").convert_alpha(),
                                        (400, 400)),
            "b": pygame.transform.scale(pygame.image.load(f"assets/images/pieces/png_{bb}/bB.png").convert_alpha(),
                                        (400, 400)),
            "n": pygame.transform.scale(pygame.image.load(f"assets/images/pieces/png_{bb}/bN.png").convert_alpha(),
                                        (400, 400)),
            "r": pygame.transform.scale(pygame.image.load(f"assets/images/pieces/png_{bb}/bR.png").convert_alpha(),
                                        (400, 400)),
            "q": pygame.transform.scale(pygame.image.load(f"assets/images/pieces/png_{bb}/bQ.png").convert_alpha(),
                                        (400, 400)),
            "k": pygame.transform.scale(pygame.image.load(f"assets/images/pieces/png_{bb}/bK.png").convert_alpha(),
                                        (400, 400)),
        }


        # ------------------------------------------------------------
        # Seleccion de ruta del engine en funcion del sistema operativo
        if sys.platform.startswith("linux"):  # could be "linux", "linux2", "linux3", ...
            assert os.path.exists(
                "stockfish_15.1_linux_x64/stockfish-ubuntu-20.04-x86-64"), "Archivo binario stockfish no encontrado"
            self.__engine_path = "stockfish_15.1_linux_x64/stockfish-ubuntu-20.04-x86-64"
        elif os.name == "nt":
            # Windows, Cygwin, etc. (either 32-bit or 64-bit)
            assert os.path.exists(
                "stockfish_15.1_win_x64_avx2/stockfish-windows-2022-x86-64-avx2.exe"), "Archivo binario stockfish no encontrado"
            self.__engine_path = "stockfish_15.1_win_x64_avx2/stockfish-windows-2022-x86-64-avx2.exe"
        else:
            # Windows, Cygwin, etc. (either 32-bit or 64-bit)
            assert os.path.exists(
                "stockfish_15.1_win_x64_avx2/stockfish-windows-2022-x86-64-avx2.exe"), "Archivo binario stockfish no encontrado"
            self.__engine_path = "stockfish_15.1_win_x64_avx2/stockfish-windows-2022-x86-64-avx2.exe"

        self.__board = chess.Board(starting_FEN)
        self.__board.__hash__ = chess.polyglot.zobrist_hash
        self.__depth = depth
        self.__max_time = time
        self.__history = []

        self.__history_moves_san = []
        self.data_base_activate = True
        self.conn = sqlite3.connect('repository/database_openings_chess.db')

    def get_history(self):
        return self.__history

    def get_history_moves_san(self):
        return self.__history_moves_san

    def append_history_actual_board(self):
        self.__history.append(self.__board.fen())

    def append_history_moves_san(self, doraemon):
        self.__history_moves_san.append(doraemon)

    def get_board(self):
        return self.__board

    def change_board(self, value_board):
        self.__board = value_board

    def change_board_FEN(self, value_board_fen):
        self.__board = chess.Board(value_board_fen)

    def recomend_move(self):
        engine = chess.engine.SimpleEngine.popen_uci(self.__engine_path)
        old_spice_2 = self.get_board_FEN()
        start_node = Board(board=self.__board.fen(), parent=None, childs=[])
        result = self.minmax(actual_node=start_node, depth=0, max_depth=1, start_time=time.time(),
                             max_time=5, engine=engine)

        move_ia_uci = self.two_board_to_piece_move(True, old_spice_2, result[1])
        engine.close()
        # Se devuelve el movimiento que haria la IA
        return move_ia_uci

    def access_data_base(self, movements_list):
        initial_moves = ["a3", "a4", "b3", "b4", "c3", "c4", "d3", "d4", "e3", "e4", "f3", "f4", "g3", "g4", "h3", "h4",
                         "Na3", "Nc3", "Nf3", "Nh3"]
        # Ya que el limite de jugadas de la base de datos es 20 lo limitamos con este if
        if len(movements_list) >= 20:
            return None

        # Si la maquina mueve primero elige un movimiento aleatorio
        elif len(movements_list) == 0:
            return random.choice(initial_moves)

        # Si el primer movimiento no esta en la lista significa que el tablero ha empezado en una posicion diferente
        elif movements_list[0] not in initial_moves:
            return None

        else:
            # Conexión a la base de datos
            conexion = sqlite3.connect('repository/database_openings_chess.db')
            cursor = conexion.cursor()

            # Consulta SQL para obtener los movimientos en la tabla correspondiente
            if movements_list[0] == "e4" or movements_list[0] == "d4":
                tabla = f"tabla_{movements_list[0]}_blitz"
            else:
                tabla = f"tabla_{movements_list[0]}"

            query = f"SELECT * FROM {tabla}"

            # Se ejecuta la consulta
            cursor.execute(query)

            # Creamos el str para hacer la consulta
            query_str = ''
            for i in range(1, len(movements_list) + 1):
                if i == len(movements_list):
                    query_str += f"COLUMN{i} = '{movements_list[i - 1]}'"
                else:
                    query_str += f"COLUMN{i} = '{movements_list[i - 1]}' AND "

            cursor.execute(f"SELECT COLUMN{len(movements_list) + 1} FROM {tabla} WHERE {query_str}")
            results = cursor.fetchall()

            # Cerraramos la conexión con la base de datos
            cursor.close()
            conexion.close()

            # Si se encontraron movimientos válidos se elige uno aleatoriamente
            if results:
                siguiente_movimiento = random.choice(results)
                return siguiente_movimiento[0]
            else:
                return None

    def movement_calc(self):
        """Esta funcion se encargara de realizar un movimiento solicitando primero a la base de datos, un posible movimiento
        y en caso de no haberlo llamara al algoritmo seleccionado encargado de calcular el movimiento optimo, abriendo y
        cerrando el motor cuando se deje de usar"""
        data_base_move = False
        if self.data_base_activate is True:
            actual_data_base_move = self.access_data_base(self.__history_moves_san)
            data_base_move = True

            if actual_data_base_move == "0" or actual_data_base_move == 0 or actual_data_base_move is None \
                    or actual_data_base_move == "NULL" or actual_data_base_move == "null":
                # QUITAR LOS == NULL
                data_base_move = False
            else:
                self.__history_moves_san.append(actual_data_base_move)
                try:
                    self.move_piece_san(actual_data_base_move)
                except:
                    data_base_move = False

        if data_base_move is False:
            self.data_base_activate = False
            engine = chess.engine.SimpleEngine.popen_uci(self.__engine_path)
            old_spice = self.get_board_FEN()
            start_node = Board(board=self.__board.fen(), parent=None, childs=[])
            result = self.minmax(actual_node=start_node, depth=0, max_depth=self.__depth, start_time=time.time(),
                                 max_time=self.__max_time, engine=engine)

            move_ia_uci = self.two_board_to_piece_move(True, old_spice, result[1])

            move_ia_san = self.uci_to_san(move_ia_uci[0] + move_ia_uci[1])

            try:
                self.move_piece_san(move_ia_san)
                self.__history_moves_san.append(move_ia_san)

            except:
                self.move_piece_san(move_ia_san + "=Q")
                self.__history_moves_san.append(move_ia_san + "=Q")

            # self.__board = chess.Board(result[1])

            engine.close()

    @functools.lru_cache()
    def minmax(self, actual_node: Board, depth, max_depth, start_time, max_time, engine, alpha=None,
               beta=None) -> tuple:
        # pygame.event.get()
        # Establecemos los valores iniciales para alpha y para beta
        if alpha is None:
            alpha = (float('-inf'), None)
        if beta is None:
            beta = (float('+inf'), None)

        # Se comprueba la condicion del tiempo
        if time.time() - start_time >= max_time or depth >= max_depth:
            o = actual_node.evaluate_self(engine), actual_node.board.fen()
            return o

        # Generamos los hijos del nodo(Esta parte esta en duda su optimizacion)
        self.gen_childs(actual_node)

        # Se comprueba que no hemos llegado al caso base, esto solo ocurrira en los finales de partidas
        if not actual_node.childs:
            return actual_node.evaluate_self(engine), actual_node.board.fen()

        # Modificamos y podamos en caso de necesitarlo
        for i in actual_node.childs:

            child = self.minmax(i, depth + 1, max_depth, start_time, max_time, engine, alpha, beta)
            if depth % 2 == 0:

                if child[0] < beta[0]:
                    beta = child

                # Poda beta
                if alpha[0] >= beta[0]:
                    return beta
            else:
                if child[0] > alpha[0]:
                    alpha = child

                # Poda alpha
                if alpha[0] >= beta[0]:
                    return alpha

        return beta if depth % 2 == 0 else alpha

    @functools.lru_cache()
    def gen_childs(self, board: Board):

        legal_moves = board.board.legal_moves
        for i in [move.xboard() for move in legal_moves]:
            temp_node = Board(board.board.fen(), board, [])
            temp_node.board.push(chess.Move.from_uci(i))
            board.childs.append(temp_node)

    def valid_moves(self, board: chess.Board):
        legal_moves = board.legal_moves
        moves = [move.xboard() for move in legal_moves]
        moves = [(move[:2], move[2:]) for move in moves]
        return moves

    def move_piece(self, origin: str, dest: str):
        try:
            self.__board.push(chess.Move.from_uci(f'{origin}{dest}'))
        except chess.InvalidMoveError:
            pass

    def move_piece_san(self, mov_san: str):
        try:
            self.__board.push_san(mov_san)
        except chess.InvalidMoveError:
            pass

    def uci_to_san(self, uci_move):
        return self.__board.san(chess.Move.from_uci(uci_move))

    def piece_movements(self, pos: str):
        square = chess.parse_square(pos)
        piece = self.__board.piece_at(square)
        if piece is not None:
            legal_moves = self.__board.legal_moves
            piece_moves = [move.xboard() for move in legal_moves if move.from_square == square]
            return piece_moves

    def get_board_FEN(self):
        return self.__board.fen()

    def two_board_to_piece_move(self, fen, board1, board2):
        # Cambiar de tablero FEN a sacar las de donde a donde a movido la pieza

        if fen is True:
            board1 = chess.Board(board1)
            board2 = chess.Board(board2)

        origin_p = None
        destiny_p = None
        for square in chess.SQUARES:
            piece1 = board1.piece_at(square)
            piece2 = board2.piece_at(square)
            if piece1 != piece2:
                if piece2 is None:
                    origin_p = chess.square_name(square)
                else:
                    destiny_p = chess.square_name(square)

        return origin_p, destiny_p


if __name__ == '__main__':

    ia = Ia(starting_FEN="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", depth=1, time=5)
    print("""
        
               _ ______ _____  _____  ______ ______
     /\       | |  ____|  __ \|  __ \|  ____|___  /
    /  \      | | |__  | |  | | |__) | |__     / / 
   / /\ \ _   | |  __| | |  | |  _  /|  __|   / /  
  / ____ \ |__| | |____| |__| | | \ \| |____ / /__ 
 /_/    \_\____/|______|_____/|_|  \_\______/_____|
                                                   
        """)

    while True:

        print(ia.get_board())
        move_o = str(input("o: "))
        move_d = str(input("d: "))
        ia.move_piece(move_o, move_d)
        print(ia.get_board())
        print("COMIENZA MIN MAX CON PODA")
        number_1 = time.time()
        ia.movement_calc()
        print(time.time() - number_1)

        if ia.get_board().is_checkmate():
            print(ia.get_board())
            break
