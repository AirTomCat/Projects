import pygame
import random
import sys

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# --- Game Classes ---

class Player(pygame.sprite.Sprite):
    """Represents the player's spaceship."""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 40), pygame.SRCALPHA)
        # Draw a simple triangular ship
        pygame.draw.polygon(self.image, GREEN, [(25, 0), (0, 35), (50, 35)])
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.speed_x = 0
        self.shoot_delay = 250  # milliseconds
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        """Update player position and handle shooting."""
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -8
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 8
        
        self.rect.x += self.speed_x
        # Keep player on the screen
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        """Create a bullet if shoot delay has passed."""
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            player_bullets.add(bullet)


class Enemy(pygame.sprite.Sprite):
    """Represents a single enemy alien."""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 30), pygame.SRCALPHA)
        # Draw a simple U-shaped enemy
        pygame.draw.rect(self.image, RED, (0, 0, 40, 20))
        pygame.draw.rect(self.image, RED, (5, 20, 10, 10))
        pygame.draw.rect(self.image, RED, (25, 20, 10, 10))
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        """Enemies are updated as a group, so individual update is minimal."""
        pass # The main loop will control enemy group movement.


class Bullet(pygame.sprite.Sprite):
    """Represents a bullet fired by the player."""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 15))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_y = -10

    def update(self):
        """Move the bullet up the screen."""
        self.rect.y += self.speed_y
        # Kill the bullet if it goes off-screen
        if self.rect.bottom < 0:
            self.kill()

# --- Helper Functions ---

def draw_text(surface, text, size, x, y):
    """Draws text on the screen."""
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(midtop=(x, y))
    surface.blit(text_surface, text_rect)

def draw_lives(surface, x, y, lives, img):
    """Draws player lives indicators."""
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 35 * i
        img_rect.y = y
        surface.blit(img, img_rect)

def create_enemy_wave():
    """Creates a grid of new enemies."""
    for row in range(5):
        for col in range(10):
            enemy = Enemy(100 + col * 60, 50 + row * 45)
            all_sprites.add(enemy)
            enemies.add(enemy)

# --- Game Initialization ---
pygame.init()
pygame.mixer.init() # For sound, if you add it later
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Galaga")
clock = pygame.time.Clock()

# Generate a static starry background
star_field = []
for _ in range(150):
    x = random.randrange(0, SCREEN_WIDTH)
    y = random.randrange(0, SCREEN_HEIGHT)
    star_field.append((x, y))

# --- Sprite Groups ---
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()

# --- Game Objects ---
player = Player()
all_sprites.add(player)
create_enemy_wave()

# --- Game Variables ---
score = 0
player_lives = 3
enemy_group_speed = 2
enemy_move_direction = 1  # 1 for right, -1 for left
enemy_drop_distance = 15

# --- Main Game Loop ---
running = True
game_over = False
while running:
    # Keep loop running at the right speed
    clock.tick(FPS)

    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                player.shoot()
            if event.key == pygame.K_r and game_over:
                # Restart the game
                all_sprites.empty()
                enemies.empty()
                player_bullets.empty()
                player = Player()
                all_sprites.add(player)
                create_enemy_wave()
                score = 0
                player_lives = 3
                game_over = False


    if not game_over:
        # --- Update ---
        all_sprites.update()

        # --- Enemy Group Movement ---
        move_down = False
        for enemy in enemies:
            enemy.rect.x += enemy_group_speed * enemy_move_direction
            if enemy.rect.right >= SCREEN_WIDTH or enemy.rect.left <= 0:
                move_down = True
        
        if move_down:
            enemy_move_direction *= -1
            for enemy in enemies:
                enemy.rect.y += enemy_drop_distance
        
        # --- Collision Detection ---
        # Player bullets hitting enemies
        hits = pygame.sprite.groupcollide(enemies, player_bullets, True, True)
        for hit in hits:
            score += 100
        
        # Enemies hitting the player
        hits = pygame.sprite.spritecollide(player, enemies, True) # True to kill enemy on hit
        if hits:
            player_lives -= 1
            if player_lives <= 0:
                game_over = True
        
        # Check if wave is cleared
        if not enemies:
            create_enemy_wave()
            # Optionally increase difficulty
            enemy_group_speed += 0.5


    # --- Drawing ---
    screen.fill(BLACK)
    # Draw stars
    for star in star_field:
        pygame.draw.circle(screen, WHITE, star, 1)
        
    all_sprites.draw(screen)

    # Draw Score and Lives
    draw_text(screen, f"SCORE: {score}", 24, SCREEN_WIDTH // 2, 10)
    draw_lives(screen, SCREEN_WIDTH - 120, 10, player_lives, pygame.transform.scale(player.image, (25, 20)))

    if game_over:
        draw_text(screen, "GAME OVER", 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50)
        draw_text(screen, "Press 'R' to Restart", 22, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20)

    # *After* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
sys.exit()
