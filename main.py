import pygame
from board import Board
from piece import Piece
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, SCORE_CONTAINER_HEIGHT

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris Crush")
clock = pygame.time.Clock()

# Inicializar el tablero y la primera pieza
board = Board()
current_piece = Piece.get_random_piece()
game_over = False
score = 0

running = True
while running:
    screen.fill(BLACK)

    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_LEFT and board.is_valid_position(current_piece, delta_col=-1):
                current_piece.move(0, -1)
            elif event.key == pygame.K_RIGHT and board.is_valid_position(current_piece, delta_col=1):
                current_piece.move(0, 1)
            elif event.key == pygame.K_DOWN and board.is_valid_position(current_piece, delta_row=1):
                current_piece.move(1, 0)
            elif event.key == pygame.K_UP:
                current_piece.rotate(board)

    # Movimiento automático hacia abajo
    if not game_over:
        if board.is_valid_position(current_piece, delta_row=1):
            current_piece.move(1, 0)
        else:
            board.add_piece(current_piece)

            # Detectar secuencias eliminadas 
            sequences = board.detect_sequences()
            if sequences:
                board.remove_sequences(sequences)

            # Generar una nueva pieza
            new_piece = Piece.get_random_piece()
            if not board.is_valid_position(new_piece):
                game_over = True
            else:
                current_piece = new_piece

        board.update() 

    board.draw(screen)
    board.draw_score(screen)

    if not game_over:
        current_piece.draw(screen)

    #  Mostrar game over 
    if game_over:
        font = pygame.font.Font(None, 48)
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, (SCREEN_HEIGHT + SCORE_CONTAINER_HEIGHT) // 2))
        screen.blit(game_over_text, text_rect)

    #  Actualizar juego mientras avanza
    pygame.display.flip()
    clock.tick(5 + score // 100)  #aumenta la velocidad entre más alta la puntuación 

pygame.quit()

