import pygame
import random
import math
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
SIZE = 400
GRID = 20
CELL = SIZE // GRID
FPS = 60
BASE_MOVE_DELAY = 150  # milliseconds per step
MIN_MOVE_DELAY = 60
SPEEDUP_RATE = 2  # ms faster per food eaten

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 160, 0)
RED = (255, 50, 50)
YELLOW = (255, 255, 0)
PURPLE = (160, 50, 200)
GOLD = (255, 215, 0)

# High score file
HIGHSCORE_FILE = "snake_highscore.txt"

def load_highscore():
    if os.path.exists(HIGHSCORE_FILE):
        try:
            with open(HIGHSCORE_FILE, 'r') as f:
                return int(f.read())
        except:
            return 0
    return 0

def save_highscore(score):
    with open(HIGHSCORE_FILE, 'w') as f:
        f.write(str(score))

# Simple sound generation (beeps)
def generate_sound(freq, duration=0.1, volume=0.5):
    sample_rate = 22050
    n_samples = int(sample_rate * duration)
    buf = bytearray()
    for i in range(n_samples):
        t = i / sample_rate
        envelope = 1.0 - (i / n_samples)
        val = int(volume * 127 * envelope * math.sin(2 * math.pi * freq * t))
        buf.append(val + 128)
    return pygame.mixer.Sound(buffer=bytes(buf))

# Create sounds
try:
    eat_sound = generate_sound(600, 0.08, 0.4)
    bonus_sound = generate_sound(900, 0.15, 0.5)
    poison_sound = generate_sound(200, 0.3, 0.6)
    death_sound = generate_sound(150, 0.4, 0.7)
    powerup_sound = generate_sound(1000, 0.2, 0.5)
except:
    eat_sound = bonus_sound = poison_sound = death_sound = powerup_sound = None

# Particle class for effects
class Particle:
    def __init__(self, x, y, vx, vy, radius, color, lifetime=20):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.color = color
        self.lifetime = lifetime
        self.age = 0

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.age += 1
        return self.age < self.lifetime

    def draw(self, surface):
        alpha = 1.0 - (self.age / self.lifetime)
        if alpha < 0: alpha = 0
        r, g, b = self.color
        color = (int(r * alpha), int(g * alpha), int(b * alpha))
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), max(1, int(self.radius * alpha)))

class Snake:
    def __init__(self):
        # Initial snake positions (grid coordinates)
        self.body = [(5, 5), (4, 5), (3, 5)]
        self.direction = (1, 0)       # current direction
        self.pending_dir = (1, 0)     # next direction after queue
        self.grow = False
        self.shield = False
        self.shield_timer = 0

    def change_direction(self, new_dir):
        # Prevent reversing directly
        if (new_dir[0] != -self.direction[0] or new_dir[1] != -self.direction[1]):
            self.pending_dir = new_dir

    def update(self):
        self.direction = self.pending_dir
        head = self.body[0]
        new_head = ((head[0] + self.direction[0]) % GRID,
                    (head[1] + self.direction[1]) % GRID)
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
        # Shield timer
        if self.shield_timer > 0:
            self.shield_timer -= 1
            if self.shield_timer == 0:
                self.shield = False

    def collides_self(self):
        return self.body[0] in self.body[1:]

    def draw(self, surface, t=0):
        # t is interpolation factor 0-1 for smooth movement
        for i, (sx, sy) in enumerate(self.body):
            # Calculate smooth position: interpolate between previous and current grid position
            # For simplicity, we'll keep grid-aligned but with rounded corners
            x = sx * CELL
            y = sy * CELL
            if i == 0:
                color = GREEN
            else:
                color = DARK_GREEN
            # Draw rounded rectangle for each segment
            rect = pygame.Rect(x + 1, y + 1, CELL - 2, CELL - 2)
            pygame.draw.rect(surface, color, rect, border_radius=6)
            # Draw shield bubble on head
            if i == 0 and self.shield:
                pygame.draw.circle(surface, (100, 200, 255),
                                   (x + CELL//2, y + CELL//2), CELL//2 + 4, 2)

        # Draw eyes on head
        head_x, head_y = self.body[0]
        hx = head_x * CELL + CELL // 2
        hy = head_y * CELL + CELL // 2
        eye_size = 3
        if self.direction == (1, 0):    # right
            eye1 = (hx + 3, hy - 4)
            eye2 = (hx + 3, hy + 4)
        elif self.direction == (-1, 0): # left
            eye1 = (hx - 3, hy - 4)
            eye2 = (hx - 3, hy + 4)
        elif self.direction == (0, -1): # up
            eye1 = (hx - 4, hy - 3)
            eye2 = (hx + 4, hy - 3)
        else:                           # down
            eye1 = (hx - 4, hy + 3)
            eye2 = (hx + 4, hy + 3)
        pygame.draw.circle(surface, WHITE, eye1, eye_size)
        pygame.draw.circle(surface, WHITE, eye2, eye_size)
        pygame.draw.circle(surface, BLACK, eye1, 1)
        pygame.draw.circle(surface, BLACK, eye2, 1)

class Food:
    def __init__(self, snake_body):
        self.type = 'normal'
        self.pos = self.place(snake_body)
        self.lifetime = 0  # for bonus/poison expiry

    def place(self, snake_body):
        while True:
            pos = (random.randint(0, GRID - 1), random.randint(0, GRID - 1))
            if pos not in snake_body:
                return pos

    def update(self):
        self.lifetime += 1
        # Bonus and poison foods expire after some time
        if self.type != 'normal' and self.lifetime > 100:
            return False  # expired
        return True

    def draw(self, surface):
        x, y = self.pos
        rect = pygame.Rect(x * CELL + 2, y * CELL + 2, CELL - 4, CELL - 4)
        if self.type == 'normal':
            pygame.draw.rect(surface, RED, rect, border_radius=4)
        elif self.type == 'bonus':
            # Gold star-like
            pygame.draw.circle(surface, GOLD, (x * CELL + CELL//2, y * CELL + CELL//2), CELL//2 - 2)
            pygame.draw.circle(surface, WHITE, (x * CELL + CELL//2 - 2, y * CELL + CELL//2 - 2), 2)
        elif self.type == 'poison':
            pygame.draw.circle(surface, PURPLE, (x * CELL + CELL//2, y * CELL + CELL//2), CELL//2 - 2)
            pygame.draw.line(surface, WHITE, (x * CELL + 3, y * CELL + 3), (x * CELL + CELL - 3, y * CELL + CELL - 3), 2)
            pygame.draw.line(surface, WHITE, (x * CELL + 3, y * CELL + CELL - 3), (x * CELL + CELL - 3, y * CELL + 3), 2)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SIZE, SIZE))
        pygame.display.set_caption("Advanced Snake")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 28)
        self.big_font = pygame.font.Font(None, 48)
        self.state = 'menu'  # 'menu', 'playing', 'gameover'
        self.reset()
        self.highscore = load_highscore()
        self.particles = []
        self.move_delay = BASE_MOVE_DELAY
        self.last_move_time = 0
        self.shake = 0

    def reset(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.score = 0
        self.particles = []
        self.move_delay = BASE_MOVE_DELAY
        self.shake = 0
        self.food_timer = 0
        self.powerup_timer = 0

    def place_food(self):
        # 70% normal, 20% bonus, 10% poison
        r = random.random()
        if r < 0.7:
            self.food = Food(self.snake.body)
            self.food.type = 'normal'
        elif r < 0.9:
            self.food = Food(self.snake.body)
            self.food.type = 'bonus'
        else:
            self.food = Food(self.snake.body)
            self.food.type = 'poison'

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.snake.change_direction((1, 0))
                elif event.key == pygame.K_SPACE:
                    if self.state == 'menu':
                        self.state = 'playing'
                        self.reset()
                    elif self.state == 'gameover':
                        self.state = 'menu'
                    elif self.state == 'playing' and self.snake.shield:
                        # Maybe activate shield? but we'll keep simple
                        pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == 'menu':
                    self.state = 'playing'
                    self.reset()
                elif self.state == 'gameover':
                    self.state = 'menu'
                elif self.state == 'playing':
                    # Mouse click to change direction relative to head
                    tx, ty = event.pos
                    head = self.snake.body[0]
                    hx, hy = head[0] * CELL + CELL // 2, head[1] * CELL + CELL // 2
                    dx, dy = tx - hx, ty - hy
                    if abs(dx) > abs(dy):
                        want = (1, 0) if dx > 0 else (-1, 0)
                    else:
                        want = (0, 1) if dy > 0 else (0, -1)
                    self.snake.change_direction(want)
        return True

    def update(self):
        if self.state != 'playing':
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time >= self.move_delay:
            self.last_move_time = current_time
            self.snake.update()

            # Check self collision
            if self.snake.collides_self():
                self.game_over()
                return

            # Check food collision
            head = self.snake.body[0]
            if head == self.food.pos:
                if self.food.type == 'normal':
                    self.score += 10
                    self.snake.grow = True
                    if eat_sound: eat_sound.play()
                    self.spawn_particles(self.food.pos, (255, 100, 100), 10)
                elif self.food.type == 'bonus':
                    self.score += 30
                    self.snake.grow = True
                    # Bonus also gives temporary speed boost? We'll just reduce move delay permanently
                    self.move_delay = max(MIN_MOVE_DELAY, self.move_delay - SPEEDUP_RATE)
                    if bonus_sound: bonus_sound.play()
                    self.spawn_particles(self.food.pos, GOLD, 20)
                elif self.food.type == 'poison':
                    self.score -= 20
                    self.snake.grow = False
                    # Poison also reverses direction? We'll just shrink if possible
                    if len(self.snake.body) > 1:
                        self.snake.body.pop()
                    if poison_sound: poison_sound.play()
                    self.spawn_particles(self.food.pos, PURPLE, 15)
                    self.shake = 10
                # Place new food
                self.place_food()

            # Move particles
            self.particles = [p for p in self.particles if p.update()]

            # Decrease shake
            if self.shake > 0:
                self.shake -= 1

            # Increase speed as score grows
            self.move_delay = max(MIN_MOVE_DELAY, BASE_MOVE_DELAY - (self.score // 10) * SPEEDUP_RATE)

    def game_over(self):
        self.state = 'gameover'
        if self.score > self.highscore:
            self.highscore = self.score
            save_highscore(self.highscore)
        if death_sound: death_sound.play()
        self.shake = 20
        self.spawn_particles(self.snake.body[0], RED, 30)

    def spawn_particles(self, grid_pos, color, count):
        x, y = grid_pos
        px = x * CELL + CELL // 2
        py = y * CELL + CELL // 2
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 4)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            self.particles.append(Particle(px, py, vx, vy, random.randint(2, 4), color, random.randint(15, 30)))

    def draw(self):
        # Background with gradient
        for y in range(SIZE):
            ratio = y / SIZE
            r = int(20 + (40 - 20) * ratio)
            g = int(20 + (60 - 20) * ratio)
            b = int(30 + (50 - 30) * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SIZE, y))

        # Draw grid lines (subtle)
        for i in range(GRID + 1):
            pygame.draw.line(self.screen, (40, 40, 40), (i * CELL, 0), (i * CELL, SIZE))
            pygame.draw.line(self.screen, (40, 40, 40), (0, i * CELL), (SIZE, i * CELL))

        # Draw food
        self.food.draw(self.screen)

        # Draw particles
        for p in self.particles:
            p.draw(self.screen)

        # Draw snake
        self.snake.draw(self.screen)

        # HUD
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 5))
        high_text = self.font.render(f'High: {self.highscore}', True, (200, 200, 200))
        self.screen.blit(high_text, (SIZE - 80, 5))

        # Shield indicator
        if self.snake.shield:
            shield_text = self.font.render('Shield!', True, (100, 200, 255))
            self.screen.blit(shield_text, (SIZE // 2 - 20, 5))

        # Screen shake: shift entire scene (simple approximation)
        if self.shake > 0:
            offset_x = random.randint(-3, 3)
            offset_y = random.randint(-3, 3)
            # We redraw the scene with an offset by blitting onto itself with offset? Not easy.
            # Instead, we'll just draw a red flash overlay for feedback.
            overlay = pygame.Surface((SIZE, SIZE), pygame.SRCALPHA)
            overlay.fill((255, 0, 0, min(50, self.shake * 2)))
            self.screen.blit(overlay, (0, 0))

        # Menu / Game Over overlays
        if self.state == 'menu':
            overlay = pygame.Surface((SIZE, SIZE), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))
            title = self.big_font.render('Snake!', True, GREEN)
            self.screen.blit(title, title.get_rect(center=(SIZE // 2, SIZE // 2 - 30)))
            instruct = self.font.render('Press SPACE or Click to Start', True, WHITE)
            self.screen.blit(instruct, instruct.get_rect(center=(SIZE // 2, SIZE // 2 + 20)))
        elif self.state == 'gameover':
            overlay = pygame.Surface((SIZE, SIZE), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            self.screen.blit(overlay, (0, 0))
            go_text = self.big_font.render('Game Over!', True, YELLOW)
            self.screen.blit(go_text, go_text.get_rect(center=(SIZE // 2, SIZE // 2 - 30)))
            score_text = self.font.render(f'Score: {self.score}', True, WHITE)
            self.screen.blit(score_text, score_text.get_rect(center=(SIZE // 2, SIZE // 2 + 10)))
            restart = self.font.render('Click or SPACE to Continue', True, (200, 200, 200))
            self.screen.blit(restart, restart.get_rect(center=(SIZE // 2, SIZE // 2 + 40)))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            if not running:
                break
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
