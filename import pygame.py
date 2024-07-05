
import pygame
import random
import sys

# Inicializar Pygame


# Definir constantes
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SHAPE_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0), (128, 0, 128), (0, 255, 255)]

# Definir formas de las piezas del Tetris
tetris_shapes = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3, 0],
     [0, 3, 3]],

    [[4, 0, 0],
     [4, 4, 4]],

    [[0, 0, 5],
     [5, 5, 5]],

    [[6, 6, 6, 6]],

    [[7, 7],
     [7, 7]]
]

# Clase para las piezas del Tetris
class TetrisPiece:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.shape = random.choice(tetris_shapes)
        self.color = SHAPE_COLORS[random.randint(0, len(SHAPE_COLORS) - 1)]
        self.rotation = 0

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)

    def get_rotated_shape(self):
        return self.shape[self.rotation]

# Función para crear un nuevo TetrisPiece
def new_piece():
    return TetrisPiece(5, 0)

# Función para dibujar una pieza en la pantalla
def draw_piece(piece, screen):
    shape = piece.get_rotated_shape()
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, piece.color, (piece.x * BLOCK_SIZE + x * BLOCK_SIZE, piece.y * BLOCK_SIZE + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, BLACK, (piece.x * BLOCK_SIZE + x * BLOCK_SIZE, piece.y * BLOCK_SIZE + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

# Función para mostrar el menú
def show_menu(screen):
    font = pygame.font.Font(None, 36)
    title_text = font.render("Tetris", True, WHITE)
    start_text = font.render("Presiona cualquier tecla para empezar", True, WHITE)

    screen.fill(BLACK)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

    pygame.display.flip()

    # Esperar hasta que el jugador presione una tecla para empezar
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                waiting = False

# Función principal del juego
def main():
    pygame.init()
    # Configurar la pantalla
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")

    # Mostrar el menú de inicio
    show_menu(screen)

    # Variables del juego
    piece = new_piece()
    clock = pygame.time.Clock()
    game_over = False

    # Loop principal del juego
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    piece.x -= 1
                elif event.key == pygame.K_RIGHT:
                    piece.x += 1
                elif event.key == pygame.K_DOWN:
                    piece.y += 1
                elif event.key == pygame.K_UP:
                    piece.rotate()

        # Dibujar el fondo
        screen.fill(BLACK)

        # Dibujar la pieza actual
        draw_piece(piece, screen)

        # Actualizar la pantalla
        pygame.display.flip()

        # Controlar la velocidad del juego
        clock.tick(5)

pygame.quit()
# Ejecutar el juego
if __name__ == "__main__":
    main()

sys.exit()