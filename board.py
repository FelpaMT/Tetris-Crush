import pygame
from config import BOARD_COLS, BOARD_ROWS, CELL_SIZE, SCREEN_WIDTH, WHITE, BLACK, FONT, GREEN, GRAY, SCORE_CONTAINER_HEIGHT


class Board:
    def __init__(self):
        self.grid = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
        self.score = 0  
        self.width = BOARD_COLS * CELL_SIZE
        self.height = BOARD_ROWS * CELL_SIZE

    def draw(self, surface):
        surface.fill(BLACK)
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                rect = pygame.Rect(col * CELL_SIZE, SCORE_CONTAINER_HEIGHT + row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if self.grid[row][col]:
                    pygame.draw.rect(surface, self.grid[row][col], rect)
                else:
                    pygame.draw.rect(surface, WHITE, rect, 1)  

    def draw_score(self, surface):
        pygame.draw.rect(surface, GRAY, (0, 0, SCREEN_WIDTH, SCORE_CONTAINER_HEIGHT))  # 🔹 Fondo gris para la puntuación

        font = pygame.font.Font(None, 36) 

        score_text = font.render(f"Puntuación {self.score}", True, WHITE)
    
        text_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCORE_CONTAINER_HEIGHT // 2))
        surface.blit(score_text, text_rect)

    def add_piece(self, piece):
        
        for (row, col), color in piece.get_cells():
            if 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLS:
                self.grid[row][col] = color

    def is_valid_position(self, piece, delta_row=0, delta_col=0):
        
        for (row, col), _ in piece.get_cells():
            new_row = row + delta_row
            new_col = col + delta_col
            if new_row < 0 or new_row >= BOARD_ROWS or new_col < 0 or new_col >= BOARD_COLS:
                return False
            if self.grid[new_row][new_col]:
                return False
        return True

    def check_game_over(self):
        
        return any(cell is not None for cell in self.grid[0])

    def detect_sequences(self):
        
        sequences = []

        # Horizontales
        for row in range(BOARD_ROWS):
            col = 0
            while col < BOARD_COLS:
                if self.grid[row][col] is not None:
                    current_color = self.grid[row][col]
                    start_col = col
                    while col < BOARD_COLS and self.grid[row][col] == current_color:
                        col += 1
                    length = col - start_col
                    if length >= 3:
                        sequences.append({
                            'orientation': 'horizontal',
                            'row': row,
                            'start_col': start_col,
                            'length': length,
                            'color': current_color
                        })
                else:
                    col += 1

        # Verticales
        for col in range(BOARD_COLS):
            row = 0
            while row < BOARD_ROWS:
                if self.grid[row][col] is not None:
                    current_color = self.grid[row][col]
                    start_row = row
                    while row < BOARD_ROWS and self.grid[row][col] == current_color:
                        row += 1
                    length = row - start_row
                    if length >= 3:
                        sequences.append({
                            'orientation': 'vertical',
                            'col': col,
                            'start_row': start_row,
                            'length': length,
                            'color': current_color
                        })
                else:
                    row += 1

        return sequences

    def remove_sequences(self, sequences):

        if not sequences:
            return

        to_remove = set()
        remove_rows = set()
        remove_cols = set()
        remove_color = None
        score_increment = 0

        for seq in sequences:
            if seq['length'] == 3:
                score_increment += 10  
                for i in range(3):
                    if seq['orientation'] == 'horizontal':
                        to_remove.add((seq['row'], seq['start_col'] + i))
                    else:
                        to_remove.add((seq['start_row'] + i, seq['col']))

            elif seq['length'] == 4:
                score_increment += 20  
                if seq['orientation'] == 'horizontal':
                    remove_rows.add(seq['row'])
                else:
                    remove_cols.add(seq['col'])

            elif seq['length'] == 5:
                score_increment += 30  
                remove_color = seq['color']

            elif seq['length'] >= 6:
                self.grid = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
                self.score += 100  
                return 

        for row, col in to_remove:
            self.grid[row][col] = None

        # Eliminar filas completas
        for row in remove_rows:
            for col in range(BOARD_COLS):
                self.grid[row][col] = None

        # Eliminar columnas completas
        for col in remove_cols:
            for row in range(BOARD_ROWS):
                self.grid[row][col] = None

        # Eliminar todas las celdas de un color específico
        if remove_color:
            for row in range(BOARD_ROWS):
                for col in range(BOARD_COLS):
                    if self.grid[row][col] == remove_color:
                        self.grid[row][col] = None

        self.score += score_increment  
        self.apply_gravity()

    def apply_gravity(self):
        
        for col in range(BOARD_COLS):
            nueva_columna = [None] * BOARD_ROWS
            index = BOARD_ROWS - 1

            for row in range(BOARD_ROWS - 1, -1, -1):
                if self.grid[row][col] is not None:
                    nueva_columna[index] = self.grid[row][col]
                    index -= 1

            for row in range(BOARD_ROWS):
                self.grid[row][col] = nueva_columna[row]

    def update(self):
        sequences = self.detect_sequences()
        if sequences:
            self.remove_sequences(sequences)

