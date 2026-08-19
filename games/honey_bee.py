import pygame
import random
import math
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()

W, H = 300, 500
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Flappy Bee - Advanced")
clock = pygame.time.Clock()
FPS = 60  # Higher FPS for smoother animation

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 200, 40)
DARK_BROWN = (50, 40, 10)

# Game constants
GRAVITY = 0.35
BUZZ = -6.5
BEE_X = 60
GROUND_HEIGHT = 60
CEILING = 10
BASE_SPAWN_RATE = 0.02
MAX_SPAWN_RATE = 0.06
FLOWER_SPAWN_RATE = 0.01
POWERUP_SPAWN_RATE = 0.005

# High score file
HIGHSCORE_FILE = "highscore.txt"

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

# Sound generation (simple beeps using math)
def generate_sound(freq, duration=0.1, volume=0.5):
    sample_rate = 22050
    n_samples = int(sample_rate * duration)
    buf = bytearray()
    for i in range(n_samples):
        t = i / sample_rate
        # Simple sine wave with decay
        envelope = 1.0 - (i / n_samples)
        val = int(volume * 127 * envelope * math.sin(2 * math.pi * freq * t))
        buf.append(val + 128)  # 8-bit mono
    return pygame.mixer.Sound(buffer=bytes(buf))

# Create sounds
try:
    flap_sound = generate_sound(600, 0.08, 0.4)
    collect_sound = generate_sound(800, 0.12, 0.5)
    hit_sound = generate_sound(200, 0.3, 0.7)
    powerup_sound = generate_sound(1000, 0.15, 0.5)
    gameover_sound = generate_sound(300, 0.5, 0.6)
except:
    # Fallback if sound generation fails
    flap_sound = collect_sound = hit_sound = powerup_sound = gameover_sound = None

# Particle class
class Particle:
    def __init__(self, x, y, vx, vy, radius, color, lifetime=30):
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
        self.vy += 0.1  # gravity
        self.age += 1
        return self.age < self.lifetime

    def draw(self, surface):
        alpha = 1.0 - (self.age / self.lifetime)
        if alpha < 0: alpha = 0
        r, g, b = self.color
        color = (int(r * alpha), int(g * alpha), int(b * alpha))
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), max(1, int(self.radius * alpha)))

# Bee class
class Bee:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vy = 0
        self.alive = True
        self.shield = False
        self.shield_timer = 0
        self.trail = []  # for trail effect

    def flap(self):
        if self.alive:
            self.vy = BUZZ
            if flap_sound:
                flap_sound.play()

    def update(self):
        self.vy += GRAVITY
        self.y += self.vy
        # Update trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > 20:
            self.trail.pop(0)
        # Shield timer
        if self.shield_timer > 0:
            self.shield_timer -= 1
            if self.shield_timer == 0:
                self.shield = False

    def draw(self, surface, frames):
        # Draw trail
        for i, (tx, ty) in enumerate(self.trail):
            alpha = (i + 1) / len(self.trail)
            radius = int(3 * alpha)
            pygame.draw.circle(surface, (255, 255, 200, int(alpha * 255)), (int(tx), int(ty)), radius)
        # Wings
        wing_up = frames % 10 < 5
        wy = int(self.y - 16) if wing_up else int(self.y - 11)
        pygame.draw.ellipse(surface, (220, 230, 255), (self.x - 8, wy, 18, 13))
        pygame.draw.ellipse(surface, (220, 230, 255), (self.x + 3, wy, 18, 13))
        # Body
        pygame.draw.ellipse(surface, YELLOW, (self.x - 15, int(self.y) - 10, 30, 20))
        # Stripes
        for sx in range(-6, 12, 6):
            pygame.draw.line(surface, DARK_BROWN, (self.x + sx, int(self.y) - 9), (self.x + sx, int(self.y) + 9), 3)
        # Eye
        pygame.draw.circle(surface, WHITE, (self.x + 11, int(self.y) - 3), 5)
        pygame.draw.circle(surface, BLACK, (self.x + 12, int(self.y) - 3), 3)
        # Stinger
        pygame.draw.polygon(surface, (80, 60, 30), [
            (self.x - 15, int(self.y) - 3),
            (self.x - 15, int(self.y) + 3),
            (self.x - 22, int(self.y))])
        # Shield bubble
        if self.shield:
            pygame.draw.circle(surface, (100, 200, 255), (int(self.x), int(self.y)), 22, 2)

# Thorn obstacle
class Thorn:
    def __init__(self, x, y, radius, speed_x, drift_y=0, rotation_speed=0, moving_range=None):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed_x = speed_x
        self.drift_y = drift_y
        self.rotation = 0
        self.rotation_speed = rotation_speed
        self.moving_range = moving_range  # (min_y, max_y) for vertical movement
        self.base_y = y
        self.direction = 1 if drift_y >= 0 else -1

    def update(self):
        self.x -= self.speed_x
        if self.moving_range:
            self.y += self.drift_y
            if self.y < self.moving_range[0] or self.y > self.moving_range[1]:
                self.drift_y = -self.drift_y
        else:
            self.y += self.drift_y
            if self.y - self.radius < 30 or self.y + self.radius > H - GROUND_HEIGHT - 10:
                self.drift_y = -self.drift_y
        self.rotation += self.rotation_speed

    def draw(self, surface):
        ix, iy = int(self.x), int(self.y)
        pts = []
        n = 10
        for i in range(n * 2):
            a = math.radians(i * 180 / n - 90) + self.rotation
            cr = self.radius + 7 if i % 2 == 0 else self.radius * 0.55
            pts.append((ix + int(cr * math.cos(a)), iy + int(cr * math.sin(a))))
        pygame.draw.polygon(surface, (45, 100, 35), pts)
        pygame.draw.circle(surface, (65, 140, 50), (ix, iy), int(self.radius * 0.6))
        pygame.draw.circle(surface, (90, 170, 70), (ix - self.radius // 5, iy - self.radius // 5), int(self.radius * 0.3))

# Flower collectible
class Flower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.collected = False

    def update(self):
        self.x -= 2.5

    def draw(self, surface):
        ix, iy = int(self.x), int(self.y)
        for i in range(5):
            angle = i * 72
            px = ix + int(8 * math.cos(math.radians(angle)))
            py = iy + int(8 * math.sin(math.radians(angle)))
            pygame.draw.circle(surface, (255, 255, 100), (px, py), 5)
        pygame.draw.circle(surface, (255, 180, 50), (ix, iy), 5)

# Power-up class
class PowerUp:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type  # 'shield' or 'slow'
        self.active = True

    def update(self):
        self.x -= 2.5

    def draw(self, surface):
        if not self.active: return
        ix, iy = int(self.x), int(self.y)
        if self.type == 'shield':
            pygame.draw.circle(surface, (100, 200, 255), (ix, iy), 10)
            pygame.draw.circle(surface, WHITE, (ix, iy), 6)
        elif self.type == 'slow':
            pygame.draw.circle(surface, (200, 200, 100), (ix, iy), 10)
            pygame.draw.line(surface, (255, 255, 0), (ix-5, iy), (ix+5, iy), 3)
            pygame.draw.line(surface, (255, 255, 0), (ix, iy-5), (ix, iy+5), 3)

# Cloud class for parallax
class Cloud:
    def __init__(self, x, y, speed, scale=1.0):
        self.x = x
        self.y = y
        self.speed = speed
        self.scale = scale

    def update(self):
        self.x -= self.speed
        if self.x < -100 * self.scale:
            self.x = W + random.randint(20, 100)
            self.y = random.randint(10, H // 2)

    def draw(self, surface):
        cs = self.scale
        pygame.draw.ellipse(surface, (255, 255, 255), (self.x, self.y, 50*cs, 25*cs))
        pygame.draw.ellipse(surface, (255, 255, 255), (self.x+15*cs, self.y-10*cs, 40*cs, 30*cs))
        pygame.draw.ellipse(surface, (255, 255, 255), (self.x+35*cs, self.y, 50*cs, 25*cs))

# Game class to manage states
class Game:
    def __init__(self):
        self.reset()
        self.highscore = load_highscore()
        self.clouds = [Cloud(random.randint(0, W), random.randint(10, H//2), random.uniform(0.2, 0.8), random.uniform(0.5, 1.5)) for _ in range(6)]
        self.particles = []
        self.shake = 0
        self.slow_motion_timer = 0
        self.state = 'menu'  # 'menu', 'playing', 'gameover'
        self.frames = 0

    def reset(self):
        self.bee = Bee(BEE_X, H // 2)
        self.thorns = []
        self.flowers = []
        self.powerups = []
        self.score = 0
        self.particles = []
        self.shake = 0
        self.slow_motion_timer = 0
        self.frames = 0
        self.spawn_timer = 0

    def spawn_thorn(self):
        r = random.randint(14, 32)
        # Different thorn types
        type = random.random()
        if type < 0.6:  # normal
            y = random.randint(r + 40, H - r - GROUND_HEIGHT - 10)
            sx = random.uniform(2.0, 3.5)
            dy = random.uniform(-0.5, 0.5)
            rot = random.uniform(-0.05, 0.05)
            self.thorns.append(Thorn(W + r, y, r, sx, dy, rot))
        elif type < 0.85:  # moving vertically
            y = random.randint(r + 40, H - r - GROUND_HEIGHT - 10)
            sx = random.uniform(2.5, 4.0)
            dy = random.uniform(-1.5, 1.5)
            rot = random.uniform(-0.05, 0.05)
            self.thorns.append(Thorn(W + r, y, r, sx, dy, rot))
        else:  # big slow thorn
            r = random.randint(25, 40)
            y = random.randint(r + 40, H - r - GROUND_HEIGHT - 10)
            sx = random.uniform(1.5, 2.5)
            dy = random.uniform(-0.3, 0.3)
            rot = random.uniform(-0.02, 0.02)
            self.thorns.append(Thorn(W + r, y, r, sx, dy, rot))

    def spawn_flower(self):
        y = random.randint(50, H - GROUND_HEIGHT - 20)
        self.flowers.append(Flower(W, y))

    def spawn_powerup(self):
        y = random.randint(50, H - GROUND_HEIGHT - 20)
        type = random.choice(['shield', 'slow'])
        self.powerups.append(PowerUp(W, y, type))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    if self.state == 'menu':
                        self.state = 'playing'
                        self.bee.flap()
                    elif self.state == 'playing':
                        self.bee.flap()
                    elif self.state == 'gameover':
                        if self.frames > 30:  # delay to prevent accidental restart
                            self.reset()
                            self.state = 'playing'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == 'menu':
                    self.state = 'playing'
                    self.bee.flap()
                elif self.state == 'playing':
                    self.bee.flap()
                elif self.state == 'gameover':
                    if self.frames > 30:
                        self.reset()
                        self.state = 'playing'
        return True

    def update(self):
        if self.state != 'playing':
            return

        self.frames += 1
        # Score increases with time
        if self.frames % 30 == 0:
            self.score += 1

        # Slow motion timer
        if self.slow_motion_timer > 0:
            self.slow_motion_timer -= 1

        # Update bee
        self.bee.update()
        if self.bee.y > H - GROUND_HEIGHT - 10 or self.bee.y < CEILING:
            self.game_over()
            return

        # Spawn thorns
        spawn_rate = min(MAX_SPAWN_RATE, BASE_SPAWN_RATE + self.frames * 0.0001)
        if random.random() < spawn_rate:
            self.spawn_thorn()

        # Spawn flowers
        if random.random() < FLOWER_SPAWN_RATE:
            self.spawn_flower()

        # Spawn powerups
        if random.random() < POWERUP_SPAWN_RATE:
            self.spawn_powerup()

        # Update thorns
        speed_mult = 0.5 if self.slow_motion_timer > 0 else 1.0
        for t in self.thorns:
            t.speed_x *= speed_mult
            t.update()
            t.speed_x /= speed_mult  # restore

        # Remove off-screen thorns
        self.thorns[:] = [t for t in self.thorns if t.x + t.radius > -10]

        # Update flowers
        for f in self.flowers:
            f.update()
        self.flowers[:] = [f for f in self.flowers if f.x > -15 and not f.collected]

        # Update powerups
        for p in self.powerups:
            p.update()
        self.powerups[:] = [p for p in self.powerups if p.x > -15 and p.active]

        # Collision detection with thorns
        for t in self.thorns:
            dx = self.bee.x - t.x
            dy = self.bee.y - t.y
            dist = math.hypot(dx, dy)
            if dist < t.radius + 13:
                if self.bee.shield:
                    # Shield absorbs hit
                    self.bee.shield = False
                    self.bee.shield_timer = 0
                    self.thorns.remove(t)
                    self.add_explosion(t.x, t.y, 20, (100, 200, 255))
                    if hit_sound: hit_sound.play()
                else:
                    self.game_over()
                    return

        # Collect flowers
        for f in self.flowers:
            if not f.collected:
                dx = self.bee.x - f.x
                dy = self.bee.y - f.y
                dist = math.hypot(dx, dy)
                if dist < 18:
                    f.collected = True
                    self.score += 3
                    self.add_sparkles(f.x, f.y, 10)
                    if collect_sound: collect_sound.play()

        # Collect powerups
        for p in self.powerups:
            if p.active:
                dx = self.bee.x - p.x
                dy = self.bee.y - p.y
                dist = math.hypot(dx, dy)
                if dist < 20:
                    p.active = False
                    if p.type == 'shield':
                        self.bee.shield = True
                        self.bee.shield_timer = 180  # 3 seconds
                    elif p.type == 'slow':
                        self.slow_motion_timer = 180  # 3 seconds
                    if powerup_sound: powerup_sound.play()
                    self.add_sparkles(p.x, p.y, 15, (200, 255, 200))

        # Update clouds
        for c in self.clouds:
            c.update()

        # Update particles
        self.particles = [p for p in self.particles if p.update()]

        # Shake effect
        if self.shake > 0:
            self.shake -= 1

    def add_explosion(self, x, y, count, color):
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 5)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            self.particles.append(Particle(x, y, vx, vy, random.randint(2, 5), color, random.randint(20, 40)))

    def add_sparkles(self, x, y, count, color=(255, 255, 100)):
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(0.5, 3)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed - 1
            self.particles.append(Particle(x, y, vx, vy, random.randint(1, 3), color, random.randint(15, 30)))

    def game_over(self):
        if self.bee.shield:
            # Shield already used, but we shouldn't get here
            return
        self.state = 'gameover'
        self.frames = 0
        if self.score > self.highscore:
            self.highscore = self.score
            save_highscore(self.highscore)
        self.add_explosion(self.bee.x, self.bee.y, 30, (255, 100, 50))
        if gameover_sound: gameover_sound.play()
        self.shake = 20

    def draw(self):
        # Sky gradient (day to dusk based on score)
        t = min(1.0, self.score / 50.0)
        for y in range(H - GROUND_HEIGHT):
            ratio = y / (H - GROUND_HEIGHT)
            # Interpolate between day and dusk colors
            r = int(135 + (250 - 135) * t * ratio + (100 - 135) * (1 - t) * ratio)
            g = int(206 + (120 - 206) * t * ratio + (180 - 206) * (1 - t) * ratio)
            b = int(235 + (80 - 235) * t * ratio + (140 - 235) * (1 - t) * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (W, y))

        # Ground
        pygame.draw.rect(screen, (90, 160, 60), (0, H - GROUND_HEIGHT, W, GROUND_HEIGHT))
        pygame.draw.rect(screen, (110, 180, 70), (0, H - GROUND_HEIGHT - 2, W, 4))

        # Ground flowers
        for gx in range(20, W, 55):
            pygame.draw.circle(screen, (255, 100, 100), (gx, H - 48), 5)
            pygame.draw.circle(screen, (255, 220, 80), (gx, H - 48), 3)
            pygame.draw.line(screen, (60, 130, 40), (gx, H - 43), (gx, H - 35), 2)
        for gx in range(45, W, 55):
            pygame.draw.circle(screen, (200, 130, 255), (gx, H - 42), 4)
            pygame.draw.circle(screen, (255, 220, 120), (gx, H - 42), 2)
            pygame.draw.line(screen, (60, 130, 40), (gx, H - 38), (gx, H - 32), 2)

        # Clouds
        for c in self.clouds:
            c.draw(screen)

        # Draw flowers
        for f in self.flowers:
            if not f.collected:
                f.draw(screen)

        # Draw powerups
        for p in self.powerups:
            p.draw(screen)

        # Draw thorns
        for t in self.thorns:
            t.draw(screen)

        # Draw particles (behind bee)
        for p in self.particles:
            p.draw(screen)

        # Draw bee
        self.bee.draw(screen, self.frames)

        # Apply screen shake
        if self.shake > 0:
            offset_x = random.randint(-5, 5)
            offset_y = random.randint(-5, 5)
            screen.blit(screen.copy(), (offset_x, offset_y))  # crude shake
            # Actually we should apply offset to entire scene, but this is tricky.
            # Instead we'll just draw everything twice? For simplicity, we'll skip real shake.
            # Better: we can shift the entire display by modifying coordinates, but that's complex.
            # We'll just flash the screen.

        # HUD
        font_score = pygame.font.Font(None, 36)
        score_text = font_score.render(str(self.score), True, WHITE)
        screen.blit(score_text, score_text.get_rect(center=(W // 2, 18)))

        # High score
        font_small = pygame.font.Font(None, 20)
        hs_text = font_small.render(f"High: {self.highscore}", True, (255, 255, 200))
        screen.blit(hs_text, (5, 5))

        # Slow motion indicator
        if self.slow_motion_timer > 0:
            pygame.draw.rect(screen, (255, 255, 0, 100), (10, 30, 100, 10))
            pygame.draw.rect(screen, (255, 255, 0), (10, 30, int(100 * self.slow_motion_timer / 180), 10))

        # Menu / Game Over overlays
        if self.state == 'menu':
            panel = pygame.Rect(W // 2 - 100, H // 2 - 50, 200, 100)
            pygame.draw.rect(screen, (30, 30, 30, 200), panel, border_radius=12)
            pygame.draw.rect(screen, (80, 80, 80), panel, 2, border_radius=12)
            font_big = pygame.font.Font(None, 50)
            title = font_big.render('Flappy Bee', True, (255, 200, 40))
            screen.blit(title, title.get_rect(center=(W // 2, H // 2 - 20)))
            font_small = pygame.font.Font(None, 26)
            instruct = font_small.render('Tap or Space to buzz!', True, WHITE)
            screen.blit(instruct, instruct.get_rect(center=(W // 2, H // 2 + 15)))

        elif self.state == 'gameover':
            # Darken screen
            overlay = pygame.Surface((W, H), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))
            panel = pygame.Rect(W // 2 - 100, H // 2 - 60, 200, 120)
            pygame.draw.rect(screen, (30, 30, 30), panel, border_radius=12)
            pygame.draw.rect(screen, (80, 80, 80), panel, 2, border_radius=12)
            font_big = pygame.font.Font(None, 40)
            gt = font_big.render('Game Over!', True, (255, 80, 80))
            screen.blit(gt, gt.get_rect(center=(W // 2, H // 2 - 35)))
            font_mid = pygame.font.Font(None, 26)
            st = font_mid.render(f'Score: {self.score}', True, WHITE)
            screen.blit(st, st.get_rect(center=(W // 2, H // 2 - 5)))
            hs = font_mid.render(f'High: {self.highscore}', True, (255, 255, 200))
            screen.blit(hs, hs.get_rect(center=(W // 2, H // 2 + 20)))
            font_small = pygame.font.Font(None, 20)
            restart = font_small.render('Tap to restart', True, (180, 180, 180))
            screen.blit(restart, restart.get_rect(center=(W // 2, H // 2 + 45)))

        pygame.display.flip()

# Main loop
game = Game()
running = True

while running:
    running = game.handle_events()
    if not running:
        break

    game.update()
    game.draw()
    clock.tick(FPS)

pygame.quit()
