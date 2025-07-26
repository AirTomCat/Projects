# pacman_game.py

import pygame
import random

# --- Constants ---
SCREEN_WIDTH = 616
SCREEN_HEIGHT = 700
TILE_SIZE = 28
PLAYER_SPEED = 2
GHOST_SPEED = 2

# --- Colors ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PINK = (255, 182, 193)
CYAN = (0, 255, 255)
GHOST_VULNERABLE_COLOR = (100, 100, 255)

# --- Level Layout ---
# W = Wall, . = Dot, O = Power Pellet, P = Player, G = Ghost, E = Empty
level_layout = [
    "WWWWWWWWWWWWWWWWWWWWW",
    "W.........W.........W",
    "W.WWW.WWW.W.WWW.WWW.W",
    "WOWWW.WWW.W.WWW.WWWOW",
    "W.WWW.WWW.W.WWW.WWW.W",
    "W...................W",
    "W.WWW.W.WWWWW.W.WWW.W",
    "W.WWW.W.WWWWW.W.WWW.W",
    "W.....W...W...W.....W",
    "WWWWW.WWW W WWW.WWWWW",
    "EEW...W EGE W...WEE",
    "EEW.W.WWWWWWW.W.WEE",
    "WWWWW.W EEEEE W.WWWWW",
    "EEEEE.W EEEEE W.EEEEE",
    "WWWWW.W WWWWW W.WWWWW",
    "EEW...W EEEEE W...WEE",
    "EEW.W.WWWWWWW.W.WEE",
    "WWWWW.W W P W W.WWWWW",
    "W.........W.........W",
    "W.WWW.WWW.W.WWW.WWW.W",
    "WO..W..... .....W..OW",
    "WWW.W.W.WWWWW.W.W.WWW",
    "WWW.W.W.WWWWW.W.W.WWW",
    "W.....W...W...W.....W",
    "WWWWWWWWWWWWWWWWWWWWW",
]

# --- Classes ---
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([TILE_SIZE, TILE_SIZE])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(topleft=(x, y))

class Dot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([4, 4])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))

class PowerPellet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([12, 12], pygame.SRCALPHA)
        pygame.draw.circle(self.image, WHITE, (6, 6), 6)
        self.rect = self.image.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.base_image = pygame.Surface([TILE_SIZE, TILE_SIZE], pygame.SRCALPHA)
        pygame.draw.arc(self.base_image, YELLOW, self.base_image.get_rect(), 0.7, 2 * 3.14 - 0.7, TILE_SIZE // 2)
        pygame.draw.circle(self.base_image, BLACK, (TILE_SIZE // 2 + 3, TILE_SIZE // 2 - 8), 3)
        self.image = self.base_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.change_x, self.change_y = 0, 0
        self.direction = 'right'
        self.next_direction = None

    def update(self, walls):
        # Check for buffered direction change at intersections
        if self.rect.x % TILE_SIZE == 0 and self.rect.y % TILE_SIZE == 0:
            if self.next_direction:
                self.change_x, self.change_y = self.get_speed_from_direction(self.next_direction)
                # Check if new direction is valid
                self.rect.x += self.change_x
                self.rect.y += self.change_y
                if not pygame.sprite.spritecollide(self, walls, False):
                    self.direction = self.next_direction
                    self.rotate()
                else: # Invalid direction, revert
                    self.rect.x -= self.change_x
                    self.rect.y -= self.change_y
                    self.change_x, self.change_y = self.get_speed_from_direction(self.direction)

        # Movement and collision
        self.rect.x += self.change_x
        hit_list = pygame.sprite.spritecollide(self, walls, False)
        for wall in hit_list:
            if self.change_x > 0: self.rect.right = wall.rect.left
            else: self.rect.left = wall.rect.right
            self.change_x = 0

        self.rect.y += self.change_y
        hit_list = pygame.sprite.spritecollide(self, walls, False)
        for wall in hit_list:
            if self.change_y > 0: self.rect.bottom = wall.rect.top
            else: self.rect.top = wall.rect.bottom
            self.change_y = 0

    def rotate(self):
        center = self.rect.center
        if self.direction == 'right': self.image = self.base_image
        elif self.direction == 'left': self.image = pygame.transform.rotate(self.base_image, 180)
        elif self.direction == 'up': self.image = pygame.transform.rotate(self.base_image, 90)
        elif self.direction == 'down': self.image = pygame.transform.rotate(self.base_image, -90)
        self.rect = self.image.get_rect(center=center)

    def get_speed_from_direction(self, direction):
        if direction == 'left': return -PLAYER_SPEED, 0
        if direction == 'right': return PLAYER_SPEED, 0
        if direction == 'up': return 0, -PLAYER_SPEED
        if direction == 'down': return 0, PLAYER_SPEED
        return 0, 0

class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.normal_color = color
        self.image = self.create_ghost_image(self.normal_color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.directions = [(0, -GHOST_SPEED), (0, GHOST_SPEED), (-GHOST_SPEED, 0), (GHOST_SPEED, 0)]
        self.change_x, self.change_y = random.choice(self.directions)
        self.state = "normal"
        self.vulnerable_timer = 0
        self.spawn_point = (x, y)

    def create_ghost_image(self, color):
        image = pygame.Surface([TILE_SIZE, TILE_SIZE], pygame.SRCALPHA)
        # Body
        pygame.draw.circle(image, color, (TILE_SIZE // 2, TILE_SIZE // 2), TILE_SIZE // 2 - 2)
        # Eyes
        pygame.draw.circle(image, WHITE, (TILE_SIZE // 2 - 5, TILE_SIZE // 2 - 4), 4)
        pygame.draw.circle(image, WHITE, (TILE_SIZE // 2 + 5, TILE_SIZE // 2 - 4), 4)
        # Pupils
        pygame.draw.circle(image, BLACK, (TILE_SIZE // 2 - 5, TILE_SIZE // 2 - 4), 2)
        pygame.draw.circle(image, BLACK, (TILE_SIZE // 2 + 5, TILE_SIZE // 2 - 4), 2)
        return image
    
    def update(self, walls):
        if self.state == "vulnerable":
            self.vulnerable_timer -= 1
            if self.vulnerable_timer <= 0: self.respawn(False)
        
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        if pygame.sprite.spritecollide(self, walls, False) or random.randint(0, 50) == 0:
            self.rect.x -= self.change_x
            self.rect.y -= self.change_y
            self.change_x, self.change_y = random.choice(self.directions)

    def set_vulnerable(self):
        self.state = "vulnerable"
        self.image = self.create_ghost_image(GHOST_VULNERABLE_COLOR)
        self.vulnerable_timer = 300 # 5 seconds at 60 FPS

    def respawn(self, eaten=True):
        if eaten:
             self.rect.topleft = self.spawn_point
        self.state = "normal"
        self.image = self.create_ghost_image(self.normal_color)

# --- Game Class ---
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pac-Man")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 24, bold=True)
        self.reset_game()

    def reset_game(self):
        self.state = "start"
        self.score = 0
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.dots = pygame.sprite.Group()
        self.power_pellets = pygame.sprite.Group()
        self.ghosts = pygame.sprite.Group()
        self.create_level()

    def create_level(self):
        ghost_colors = [RED, PINK, GREEN, CYAN]
        for y, row in enumerate(level_layout):
            for x, char in enumerate(row):
                pos_x, pos_y = x * TILE_SIZE, y * TILE_SIZE
                if char == 'W': self.walls.add(Wall(pos_x, pos_y))
                elif char == '.': self.dots.add(Dot(pos_x, pos_y))
                elif char == 'O': self.power_pellets.add(PowerPellet(pos_x, pos_y))
                elif char == 'P': self.player = Player(pos_x, pos_y)
                elif char == 'G' and ghost_colors:
                    self.ghosts.add(Ghost(pos_x, pos_y, ghost_colors.pop(0)))
        self.all_sprites.add(self.walls, self.dots, self.power_pellets, self.ghosts, self.player)

    def run(self):
        while True:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(60)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); quit()
            if event.type == pygame.KEYDOWN:
                if self.state == "start":
                    self.state = "playing"
                elif self.state == "playing":
                    if event.key == pygame.K_LEFT: self.player.next_direction = 'left'
                    elif event.key == pygame.K_RIGHT: self.player.next_direction = 'right'
                    elif event.key == pygame.K_UP: self.player.next_direction = 'up'
                    elif event.key == pygame.K_DOWN: self.player.next_direction = 'down'
                elif self.state == "game_over" and event.key == pygame.K_r:
                    self.reset_game()
    
    def update(self):
        if self.state == "playing":
            self.player.update(self.walls)
            self.ghosts.update(self.walls)
            
            dots_hit = pygame.sprite.spritecollide(self.player, self.dots, True)
            self.score += len(dots_hit) * 10
            
            if pygame.sprite.spritecollide(self.player, self.power_pellets, True):
                self.score += 50
                for ghost in self.ghosts: ghost.set_vulnerable()

            ghosts_hit = pygame.sprite.spritecollide(self.player, self.ghosts, False)
            for ghost in ghosts_hit:
                if ghost.state == "vulnerable":
                    self.score += 200
                    ghost.respawn()
                else: self.state = "game_over"
            
            if not self.dots and not self.power_pellets:
                self.state = "game_over"

    def draw(self):
        self.screen.fill(BLACK)
        if self.state == "start": self.draw_text("PAC-MAN", self.font, WHITE, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50); self.draw_text("Press any key to start", self.font, WHITE, SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        elif self.state == "playing": self.all_sprites.draw(self.screen); self.draw_text(f"Score: {self.score}", self.font, WHITE, 80, 20)
        elif self.state == "game_over": self.all_sprites.draw(self.screen); self.draw_text("GAME OVER", self.font, RED, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50); self.draw_text("Press 'R' to Restart", self.font, WHITE, SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        pygame.display.flip()

    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

if __name__ == "__main__":
    game = Game()
    game.run()
