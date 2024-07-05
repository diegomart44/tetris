from collections import OrderedDict
import random

from pygame import Rect
import pygame
import sys
import random
import numpy as np

# Dimensiones de la ventana
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 601
CELL_SIZE = 30
GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // CELL_SIZE

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)

# Tetrominos
tetrominos = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 0, 1]],  # L
    [[1, 1, 1], [1, 0, 0]]   # J
]

# Función principal del juego
def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Tetris')

    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)

        draw_text(screen, 'Tetris', font, WHITE, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4))

        draw_button(screen, 'Play', font, GREEN, RED, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2), 120, 50)
        draw_button(screen, 'Exit', font, RED, GREEN, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100), 120, 50)

        pygame.display.update()
        clock.tick(30)

# Función para dibujar texto en la pantalla
def draw_text(surface, text, font, color, pos):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=pos)
    surface.blit(text_surface, text_rect)

# Función para dibujar botones
def draw_button(surface, text, font, color, hover_color, pos, width, height):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    button_rect = pygame.Rect(pos[0] - width // 2, pos[1] - height // 2, width, height)

    if button_rect.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(surface, hover_color, button_rect)
        if pygame.mouse.get_pressed()[0]:
            if text == 'Play':
                # Llamar a la función para iniciar el juego
                run_game()
            elif text == 'Exit':
                pygame.quit()
                sys.exit()
    else:
        pygame.draw.rect(surface, color, button_rect)

    draw_text(surface, text, font, BLACK, pos)

# Función principal del juego de Tetris
def run_game():
    # Código del juego de Tetris aquí
    pass
def remove_empty_columns(arr, _x_offset=0, _keep_counting=True):
    """
    Elimine las columnas vacías de arr (es decir, las que están llenas de ceros). 
    El valor devuelto es (new_arr, x_offset), donde x_offset es cómo Es necesario
    aumentar mucho la coordenada x para mantener la posición original del bloque.
    """
    for colid, col in enumerate(arr.T):
        if col.max() == 0:
            if _keep_counting:
                _x_offset += 1
            # Quite la columna actual e inténta de nuevo.
            arr, _x_offset = remove_empty_columns(
                np.delete(arr, colid, 1), _x_offset, _keep_counting)
            break
        else:
            _keep_counting = False
    return arr, _x_offset


class BottomReached(Exception):
    pass


class TopReached(Exception):
    pass


class Block(pygame.sprite.Sprite):
    
    @staticmethod
    def collide(block, group):
        """
        Comprueba si el bloque especificado colisiona con algún otro bloque en el grupo.
        """
        for other_block in group:
            # Ignore el bloque actual que siempre chocará consigo mismo.
            if block == other_block:
                continue
            if pygame.sprite.collide_mask(block, other_block) is not None:
                return True
        return False
    
    def __init__(self):
        super().__init__()
        # Consigue un color aleatorio.
        self.color = random.choice((
            (200, 200, 200),
            (215, 133, 133),
            (30, 145, 255),
            (0, 170, 0),
            (180, 0, 140),
            (200, 200, 0)
        ))
        self.current = True
        self.struct = np.array(self.struct)
        # Rotación aleatoria inicial y volteo.
        if random.randint(0, 1):
            self.struct = np.rot90(self.struct)
        if random.randint(0, 1):
            # Voltea en el eje X.
            self.struct = np.flip(self.struct, 0)
        self._draw()
    
    def _draw(self, x=4, y=0):
        width = len(self.struct[0]) * CELL_SIZE
        height = len(self.struct) * CELL_SIZE
        self.image = pygame.surface.Surface([width, height])
        self.image.set_colorkey((0, 0, 0))
        # Posición y tamaño.
        self.rect = Rect(0, 0, width, height)
        self.x = x
        self.y = y
        for y, row in enumerate(self.struct):
            for x, col in enumerate(row):
                if col:
                    pygame.draw.rect(
                        self.image,
                        self.color,
                        Rect(x*CELL_SIZE + 1, y*CELL_SIZE + 1,
                             CELL_SIZE - 2, CELL_SIZE - 2)
                    )
        self._create_mask()
    
    def redraw(self):
        self._draw(self.x, self.y)
    
    def _create_mask(self):
        """
    Cree el atributo mask a partir de la superficie principal.
    La máscara es necesaria para comprobar las colisiones. 
    A esto se le debe llamar después de crear o actualizar la superficie.
        """
        self.mask = pygame.mask.from_surface(self.image)
    
    def initial_draw(self):
        raise NotImplementedError
    
    @property
    def group(self):
        return self.groups()[0]
    
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value
        self.rect.left = value*CELL_SIZE
    
    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value):
        self._y = value
        self.rect.top = value*CELL_SIZE
    
    def move_left(self, group):
        self.x -= 1
        # Compruebamos si hemos llegado al margen izquierdo.
        if self.x < 0 or Block.collide(self, group):
            self.x += 1
    
    def move_right(self, group):
        self.x += 1
        # Comprobar si hemos llegado al margen derecho o hemos chocado con otro
        # Bloquear.
        if self.rect.right > GRID_WIDTH or Block.collide(self, group):
            # Reversión.
            self.x -= 1
    
    def move_down(self, group):
        self.y += 1
        # Compruebe si el bloque llegó al fondo o chocó con 
        #  otro.
        if self.rect.bottom > GRID_HEIGHT or Block.collide(self, group):
            # Volver a la posición anterior.
            self.y -= 1
            self.current = False
            raise BottomReached
    
    def rotate(self, group):
        self.image = pygame.transform.rotate(self.image, 90)
        # Una vez rotado necesitamos actualizar el tamaño y la posición.
        self.rect.width = self.image.get_width()
        self.rect.height = self.image.get_height()
        self._create_mask()
        #Compruebe que la nueva posición no supere los límites ni colisione
        # con otros bloques y ajústelo si es necesario.
        while self.rect.right > GRID_WIDTH:
            self.x -= 1
        while self.rect.left < 0:
            self.x += 1
        while self.rect.bottom > GRID_HEIGHT:
            self.y -= 1
        while True:
            if not Block.collide(self, group):
                break
            self.y -= 1
        self.struct = np.rot90(self.struct)
    
    def update(self):
        if self.current:
            self.move_down()


class SquareBlock(Block):
    struct = (
        (1, 1),
        (1, 1)
    )


class TBlock(Block):
    struct = (
        (1, 1, 1),
        (0, 1, 0)
    )


class LineBlock(Block):
    struct = (
        (1,),
        (1,),
        (1,),
        (1,)
    )


class LBlock(Block):
    struct = (
        (1, 1),
        (1, 0),
        (1, 0),
    )


class ZBlock(Block):
    struct = (
        (0, 1),
        (1, 1),
        (1, 0),
    )


class BlocksGroup(pygame.sprite.OrderedUpdates):
    
    @staticmethod
    def get_random_block():
        return random.choice(
            (SquareBlock, TBlock, LineBlock, LBlock, ZBlock))()
    
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self._reset_grid()
        self._ignore_next_stop = False
        self.score = 0
        self.next_block = None
        # Realmente no se mueve, solo para inicializar el atributo.
        self.stop_moving_current_block()
        #El primer bloque.
        self._create_new_block()
    
    def _check_line_completion(self):
        """
       Revisa cada línea de la cuadrícula y elimina las que están completos.
        """
        # Empieza a comprobarlo desde abajo.
        for i, row in enumerate(self.grid[::-1]):
            if all(row):
                self.score += 5
                # Obtener los bloques afectados por la eliminación de la línea y eliminar duplicados.
                affected_blocks = list(
                    OrderedDict.fromkeys(self.grid[-1 - i]))
                
                for block, y_offset in affected_blocks:
                    # Retire las fichas de bloque que pertenecen a la línea completada.
                    block.struct = np.delete(block.struct, y_offset, 0)
                    if block.struct.any():
                        # Una vez eliminado, comprobamos si tenemos columnas vacías ya que deben eliminarse.
                        block.struct, x_offset = \
                            remove_empty_columns(block.struct)
                        #Compensar el espacio que se ha ido con las columnas para 
                        # Mantener la posición original del bloque.
                        block.x += x_offset
                     # Forzar actualización.
                        block.redraw()
                    else:
                        # Si la estructura está vacía, entonces el bloque desaparece.
                        self.remove(block)
                # En lugar de comprobar qué bloques hay que mover 
                # Una vez que se completó una línea, solo intente mover todas las # ellos.
                for block in self:
                    #Excepto el bloque actual.
                    if block.current:
                        continue
                    # Tire hacia abajo de cada bloque hasta que llegue al
                    #  # toca fondo o choca con otro bloque.
                    while True:
                        try:
                            block.move_down(self)
                        except BottomReached:
                            break
                
                self.update_grid()
                # Ya que hemos actualizado la cuadrícula, ahora el contador i 
                # ya no es válido, así que vuelva a llamar a la función
                # para comprobar si hay otras líneas completadas en el archivo 
                # nueva cuadrícula.
                self._check_line_completion()
                break
    
    def _reset_grid(self):
        self.grid = [[0 for _ in range(10)] for _ in range(20)]
    
    def _create_new_block(self):
        new_block = self.next_block or BlocksGroup.get_random_block()
        if Block.collide(new_block, self):
            raise TopReached
        self.add(new_block)
        self.next_block = BlocksGroup.get_random_block()
        self.update_grid()
        self._check_line_completion()
    
    def update_grid(self):
        self._reset_grid()
        for block in self:
            for y_offset, row in enumerate(block.struct):
                for x_offset, digit in enumerate(row):
                    # Evitar la sustitución de bloques anteriores.
                    if digit == 0:
                        continue
                    rowid = block.y + y_offset
                    colid = block.x + x_offset
                    self.grid[rowid][colid] = (block, y_offset)
    
    @property
    def current_block(self):
        return self.sprites()[-1]
    
    def update_current_block(self):
        try:
            self.current_block.move_down(self)
        except BottomReached:
            self.stop_moving_current_block()
            self._create_new_block()
        else:
            self.update_grid()
    
    def move_current_block(self):
        # Primero comprueba si hay algo que mover.
        if self._current_block_movement_heading is None:
            return
        action = {
            pygame.K_DOWN: self.current_block.move_down,
            pygame.K_LEFT: self.current_block.move_left,
            pygame.K_RIGHT: self.current_block.move_right
        }
        try:
            # Cada función requiere el grupo como primer argumento
         # para comprobar cualquier posible colisión.
            action[self._current_block_movement_heading](self)
        except BottomReached:
            self.stop_moving_current_block()
            self._create_new_block()
        else:
            self.update_grid()
    
    def start_moving_current_block(self, key):
        if self._current_block_movement_heading is not None:
            self._ignore_next_stop = True
        self._current_block_movement_heading = key
    
    def stop_moving_current_block(self):
        if self._ignore_next_stop:
            self._ignore_next_stop = False
        else:
            self._current_block_movement_heading = None
    
    def rotate_current_block(self):
        #Evite la rotación de SquareBlocks.
        if not isinstance(self.current_block, SquareBlock):
            self.current_block.rotate(self)
            self.update_grid()


def draw_grid(background):
    """Dibuja la cuadrícula de fondo."""
    grid_color = 10, 10, 10 # color de la cuadricula de fondo
    # Líneas verticales.
    for i in range(11):
        x = CELL_SIZE * i
        pygame.draw.line(
            background, grid_color, (x, 0), (x, GRID_HEIGHT)
        )
    # Lineas horizontales.
    for i in range(41):
        y = CELL_SIZE * i
        pygame.draw.line(
            background, grid_color, (0, y), (GRID_WIDTH, y)
        )


def draw_centered_surface(screen, surface, y):
    screen.blit(surface, (400 - surface.get_width()/2, y)) # posicion del puntaje


def main():
    pygame.init()
    pygame.display.set_caption("Tetris con PyGame")
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    run = True
    paused = False
    game_over = False
    background = pygame.Surface(screen.get_size())
    bgcolor = (100, 100, 100)
    background.fill(bgcolor)
    draw_grid(background)
    background = background.convert()
    
    try:
        font = pygame.font.Font("C:/Juego/Roboto-Regular.ttf", 20) # Es un archivo de fuente de letra el 
        # 20 indica el tamaño de letra
    except OSError:
        # Si el archivo de fuente no está disponible, se utilizará el valor predeterminado.
        pass
    next_block_text = font.render(
        "Siguiente figura:", True, (255, 255, 255), bgcolor)
    score_msg_text = font.render(
        "Puntaje:", True, (255, 255, 255), bgcolor)
    game_over_text = font.render(
        "¡Juego terminado!", True, (255, 220, 0), bgcolor)
    
    # Constantes de eventos.
    MOVEMENT_KEYS = pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN
    EVENT_UPDATE_CURRENT_BLOCK = pygame.USEREVENT + 1
    EVENT_MOVE_CURRENT_BLOCK = pygame.USEREVENT + 2
    pygame.time.set_timer(EVENT_UPDATE_CURRENT_BLOCK, 2000)
    pygame.time.set_timer(EVENT_MOVE_CURRENT_BLOCK, 100)
    
    blocks = BlocksGroup()
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            elif event.type == pygame.KEYUP:
                if not paused and not game_over:
                    if event.key in MOVEMENT_KEYS:
                        blocks.stop_moving_current_block()
                    elif event.key == pygame.K_UP:
                        blocks.rotate_current_block()
                if event.key == pygame.K_p:
                    paused = not paused
            
            #Deja de mover bloques si el juego ha terminado o está en pausa.
            if game_over or paused:
                continue
            
            if event.type == pygame.KEYDOWN:
                if event.key in MOVEMENT_KEYS:
                    blocks.start_moving_current_block(event.key)
            
            try:
                if event.type == EVENT_UPDATE_CURRENT_BLOCK:
                    blocks.update_current_block()
                elif event.type == EVENT_MOVE_CURRENT_BLOCK:
                    blocks.move_current_block()
            except TopReached:
                game_over = True
        
        # Dibuja el fondo y la cuadrícula.
        screen.blit(background, (0, 0))
        # Blocks.
        blocks.draw(screen)
        # Barra lateral con información miscelánea.
        draw_centered_surface(screen, next_block_text, 70)
        draw_centered_surface(screen, blocks.next_block.image, 100)
        draw_centered_surface(screen, score_msg_text, 240)
        score_text = font.render(
            str(blocks.score), True, (255, 255, 255), bgcolor)
        draw_centered_surface(screen, score_text, 270)
        if game_over:
            draw_centered_surface(screen, game_over_text, 360)
        # Update.
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == '_main_':
    main()