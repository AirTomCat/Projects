import pygame
import random

# --- Constants ---
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE

# --- Shapes and Colors ---
# Shape formats for the seven Tetriminos
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]],  # L
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]   # Z
]

# RGB color for each shape
SHAPE_COLORS = [
    (0, 255, 255),  # Cyan for I
    (255, 255, 0),  # Yellow for O
    (128, 0, 128),  # Purple for T
    (0, 0, 255),    # Blue for J
    (255, 165, 0),  # Orange for L
    (0, 255, 0),    # Green for S
    (255, 0, 0)     # Red for Z
]

# --- Main Game Classes ---

class Piece:
    """Represents a single Tetris piece (Tetrimino)."""
    def __init__(self, x, y, shape_index):
        self.x = x
        self.y = y
        self.shape_index = shape_index
        self.shape = SHAPES[shape_index]
        self.color = SHAPE_COLORS[shape_index]
        self.rotation = 0

    def rotate(self):
        """Rotates the piece's shape matrix 90 degrees clockwise."""
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

class Tetris:
    """The main class that orchestrates the Tetris game."""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.score = 0
        self.game_over = False
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()

    def new_piece(self):
        """Creates a new random piece at the top-center of the grid."""
        shape_index = random.randint(0, len(SHAPES) - 1)
        # Start new piece in the middle horizontally, just above the visible grid
        return Piece(self.width // 2 - len(SHAPES[shape_index][0]) // 2, 0, shape_index)

    def is_valid_position(self, piece, offset_x=0, offset_y=0):
        """Checks if the piece's position is valid (within bounds and not colliding)."""
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = piece.x + x + offset_x
                    new_y = piece.y + y + offset_y
                    # Check if outside grid boundaries
                    if new_x < 0 or new_x >= self.width or new_y >= self.height:
                        return False
                    # Check if colliding with an existing piece on the grid
                    if new_y >= 0 and self.grid[new_y][new_x]:
                        return False
        return True

    def lock_piece(self):
        """Locks the current piece onto the grid."""
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    grid_x = self.current_piece.x + x
                    grid_y = self.current_piece.y + y
                    # Use the shape index + 1 to store color info in the grid
                    self.grid[grid_y][grid_x] = self.current_piece.shape_index + 1
        
        # Clear lines and update score
        self.clear_lines()
        
        # Spawn the next piece
        self.current_piece = self.next_piece
        self.next_piece = self.new_piece()

        # Check for game over
        if not self.is_valid_position(self.current_piece):
            self.game_over = True

    def clear_lines(self):
        """Checks for and clears completed lines, updating the score."""
        lines_to_clear = []
        for y, row in enumerate(self.grid):
            if all(cell > 0 for cell in row):
                lines_to_clear.append(y)
        
        if lines_to_clear:
            # Simple scoring: 100 points per line
            self.score += len(lines_to_clear) * 100
            for y in lines_to_clear:
                # Remove the full row and add a new empty row at the top
                del self.grid[y]
                self.grid.insert(0, [0 for _ in range(self.width)])

    def move(self, dx, dy):
        """Moves the current piece if the new position is valid."""
        if self.is_valid_position(self.current_piece, offset_x=dx, offset_y=dy):
            self.current_piece.x += dx
            self.current_piece.y += dy
            return True
        return False

    def drop(self):
        """Moves the piece down one step, locking it if it hits the bottom."""
        if not self.move(0, 1):
            self.lock_piece()

    def rotate_piece(self):
        """Rotates the piece if the new orientation is valid."""
        original_shape = self.current_piece.shape
        self.current_piece.rotate()
        if not self.is_valid_position(self.current_piece):
            # If rotation is invalid, revert to original shape
            self.current_piece.shape = original_shape


# --- Drawing Functions ---

def draw_grid(surface, grid):
    """Draws the grid lines."""
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            pygame.draw.rect(surface, (50, 50, 50), (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_board(surface, grid):
    """Draws the locked pieces on the board."""
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell:
                # cell-1 because grid stores shape_index+1
                color = SHAPE_COLORS[cell - 1]
                pygame.draw.rect(surface, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(surface, (255, 255, 255), (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 2) # Border

def draw_piece(surface, piece):
    """Draws the currently falling piece."""
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(surface, piece.color, ((piece.x + x) * BLOCK_SIZE, (piece.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(surface, (255, 255, 255), ((piece.x + x) * BLOCK_SIZE, (piece.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 2) # Border

def draw_game_over(surface, score):
    """Displays the game over screen."""
    font = pygame.font.SysFont('Arial', 40, bold=True)
    text = font.render('GAME OVER', True, (255, 255, 255))
    surface.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    surface.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))


# --- Main Game Loop ---

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Code Tetris')
    clock = pygame.time.Clock()
    
    game = Tetris(GRID_WIDTH, GRID_HEIGHT)
    
    fall_time = 0
    fall_speed = 500  # Milliseconds per step down
    
    running = True
    while running:
        fall_time += clock.get_rawtime()
        clock.tick()
        
        # Automatic downward movement
        if fall_time >= fall_speed:
            fall_time = 0
            if not game.game_over:
                game.drop()
        
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN and not game.game_over:
                if event.key == pygame.K_LEFT:
                    game.move(-1, 0)
                if event.key == pygame.K_RIGHT:
                    game.move(1, 0)
                if event.key == pygame.K_DOWN:
                    game.drop()
                if event.key == pygame.K_UP:
                    game.rotate_piece()
        
        # Drawing
        screen.fill((0, 0, 0)) # Black background
        draw_grid(screen, game.grid)
        draw_board(screen, game.grid)
        if not game.game_over:
            draw_piece(screen, game.current_piece)
        else:
            draw_game_over(screen, game.score)
            
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
