
import pygame

pygame.init() 

BOARD_COLS = 10
BOARD_ROWS = 18
CELL_SIZE = 30  
FONT = pygame.font.Font(None, 36)  

SCORE_CONTAINER_HEIGHT = 50  

# Colores del tablero (RGB)
WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
RED    = (255, 0, 0)
GREEN  = (0, 255, 0)
BLUE   = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
CYAN   = (0, 255, 255)   
ORANGE = (255, 165, 0)
GRAY = (100, 100, 100)   

# Lista de colores disponibles para las piezas
COLOR_LIST = [RED, GREEN, BLUE, YELLOW, PURPLE, CYAN, ORANGE]

# Dimensiones de la ventana
SCREEN_WIDTH = BOARD_COLS * CELL_SIZE
SCREEN_HEIGHT = BOARD_ROWS * CELL_SIZE + SCORE_CONTAINER_HEIGHT  # ajustar tablero completo



