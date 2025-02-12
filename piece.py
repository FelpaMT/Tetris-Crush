import pygame
import random
from config import CELL_SIZE, COLOR_LIST

# Definición de tetrominós https://es.m.wikipedia.org/wiki/Archivo:Piezas_Tetris_99.png.
TETROMINO_SHAPES = {
    "O": [(0, 0), (0, 1), (1, 0), (1, 1)],
    "I": [(0, 0), (1, 0), (2, 0), (3, 0)],
    "T": [(0, 1), (1, 0), (1, 1), (1, 2)],
    "S": [(0, 1), (0, 2), (1, 0), (1, 1)],
    "Z": [(0, 0), (0, 1), (1, 1), (1, 2)],
    "J": [(0, 0), (1, 0), (2, 0), (2, 1)],
    "L": [(0, 1), (1, 1), (2, 1), (2, 0)]
}

class Piece:
    def __init__(self, shape):

        self.shape = shape
        self.colors = [self.get_random_color() for _ in range(len(shape))]
        self.row = 0
        self.col = 3 

    def get_random_color(self):
        return random.choice(COLOR_LIST)

    def draw(self, surface):
        for idx, (r_offset, c_offset) in enumerate(self.shape):
            x = (self.col + c_offset) * CELL_SIZE
            y = (self.row + r_offset) * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, self.colors[idx], rect)
            pygame.draw.rect(surface, (0, 0, 0), rect, 1)  

    def move(self, drow, dcol):
        """Mueve la pieza en el tablero."""
        self.row += drow
        self.col += dcol

    def get_cells(self):
        return [((self.row + r_offset, self.col + c_offset), color) for (r_offset, c_offset), color in zip(self.shape, self.colors)]

    def rotate(self, board):
        """Rota la pieza si la nueva posición es válida."""
        if self.shape == TETROMINO_SHAPES["O"]:
            # Rotación de colores para la pieza 'O' cuadrado
            self.colors = [self.colors[2], self.colors[0], self.colors[3], self.colors[1]]
        else:
            rotated_shape = [(c, -r) for (r, c) in self.shape]

            # Verificar si la rotación es válida antes de aplicarla
            test_piece = Piece(rotated_shape)
            test_piece.row, test_piece.col = self.row, self.col  # Mantener la posición actual

            if board.is_valid_position(test_piece):
                self.shape = rotated_shape

    @staticmethod
    def get_random_piece():
        """Genera y retorna una nueva pieza aleatoria a partir de las formas definidas."""
        shape = random.choice(list(TETROMINO_SHAPES.values()))
        return Piece(shape)
