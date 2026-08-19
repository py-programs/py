import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
DARK_BLUE = (0, 0, 128)
LIGHT_BLUE = (100, 200, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders - Infinite Levels")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemy_bombs = pygame.sprite.Group()
coins_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
explosions = pygame.sprite.Group()

class Star:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.speed = random.uniform(0.5, 2.0)
        self.size = random.randint(1, 3)
        self.brightness = random.randint(100, 255)

    def update(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.y = 0
            self.x = random.randint(0, SCREEN_WIDTH)

    def draw(self, surface):
        color = (self.brightness, self.brightness, self.brightness)
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.size)

stars = [Star() for _ in range(150)]

def draw_background(surface):
    surface.fill(BLACK)
    for star in stars:
        star.update()
        star.draw(surface)

def draw_player_ship():
    surf = pygame.Surface((50, 40), pygame.SRCALPHA)
    pygame.draw.polygon(surf, CYAN, [(25, 0), (50, 40), (0, 40)])
    pygame.draw.polygon(surf, WHITE, [(25, 5), (32, 25), (18, 25)])
    pygame.draw.polygon(surf, DARK_BLUE, [(10, 20), (25, 30), (0, 40), (0, 35)])
    pygame.draw.polygon(surf, DARK_BLUE, [(40, 20), (25, 30), (50, 40), (50, 35)])
    pygame.draw.rect(surf, ORANGE, (20, 35, 10, 5))
    return surf

def draw_enemy_ship(enemy_type):
    if enemy_type == 'basic':
        surf = pygame.Surface((35, 35), pygame.SRCALPHA)
        pygame.draw.polygon(surf, GREEN, [(17, 0), (35, 35), (0, 35)])
        pygame.draw.polygon(surf, (0, 200, 0), [(10, 10), (25, 10), (17, 25)])
        pygame.draw.circle(surf, WHITE, (12, 12), 3)
        pygame.draw.circle(surf, WHITE, (23, 12), 3)
        pygame.draw.circle(surf, BLACK, (12, 12), 1)
        pygame.draw.circle(surf, BLACK, (23, 12), 1)
        return surf
    elif enemy_type == 'fast':
        surf = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.polygon(surf, YELLOW, [(15, 0), (30, 30), (15, 20), (0, 30)])
        pygame.draw.polygon(surf, (255, 200, 0), [(10, 15), (20, 15), (15, 30)])
        pygame.draw.circle(surf, WHITE, (10, 10), 3)
        pygame.draw.circle(surf, WHITE, (20, 10), 3)
        pygame.draw.circle(surf, BLACK, (10, 10), 1)
        pygame.draw.circle(surf, BLACK, (20, 10), 1)
        return surf
    elif enemy_type == 'tank':
        surf = pygame.Surface((45, 45), pygame.SRCALPHA)
        pygame.draw.polygon(surf, MAGENTA, [(22, 0), (45, 45), (0, 45)])
        pygame.draw.rect(surf, (200, 0, 200), (10, 20, 25, 10))
        pygame.draw.circle(surf, WHITE, (15, 15), 4)
        pygame.draw.circle(surf, WHITE, (30, 15), 4)
        pygame.draw.circle(surf, BLACK, (15, 15), 2)
        pygame.draw.circle(surf, BLACK, (30, 15), 2)
        return surf
    else:
        return draw_enemy_ship('basic')

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = draw_player_ship()
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 20
        self.speed = 5
        self.health = 100
        self.max_health = 100
        self.fire_rate = 200
        self.last_shot = 0
        self.bullet_damage = 10
        self.bullet_speed = -12
        self.bullet_count = 1
        self.coins = 0
        self.score = 0
        self.dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.shield_active = False
        self.shield_end_time = 0
        self.shield_cooldown_end_time = 0
        self.shield_duration = 3000
        self.shield_cooldown = 5000

    def reset_for_new_game(self):
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 20
        self.health = self.max_health
        self.score = 0
        self.last_shot = 0
        self.shield_active = False
        self.shield_end_time = 0
        self.shield_cooldown_end_time = 0

    def level_up(self):
        self.max_health += 100
        self.health = self.max_health

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed

        now = pygame.time.get_ticks()
        if not self.shield_active and now >= self.shield_cooldown_end_time:
            self.shield_active = True
            self.shield_end_time = now + self.shield_duration
        if self.shield_active and now >= self.shield_end_time:
            self.shield_active = False
            self.shield_cooldown_end_time = now + self.shield_cooldown

        self.shoot()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot >= self.fire_rate:
            self.last_shot = now
            spread = 5
            total_width = (self.bullet_count - 1) * spread
            start_x = self.rect.centerx - total_width // 2
            for i in range(self.bullet_count):
                laser = Laser(start_x + i * spread, self.rect.top, self.bullet_damage, self.bullet_speed)
                all_sprites.add(laser)
                player_bullets.add(laser)

    def take_damage(self, amount):
        if not self.shield_active:
            self.health -= amount
            if self.health <= 0:
                self.health = 0
                self.kill()

    def draw_health_bar(self, surface):
        bar_width = 200
        bar_height = 20
        x = 10
        y = 10
        fill = (self.health / self.max_health) * bar_width
        outline_rect = pygame.Rect(x, y, bar_width, bar_height)
        fill_rect = pygame.Rect(x, y, fill, bar_height)
        pygame.draw.rect(surface, RED, fill_rect)
        pygame.draw.rect(surface, WHITE, outline_rect, 2)
        health_text = small_font.render(f"HP: {self.health}/{self.max_health}", True, WHITE)
        surface.blit(health_text, (x, y + bar_height + 5))

    def draw_shield(self, surface):
        if self.shield_active:
            shield_surf = pygame.Surface((100, 100), pygame.SRCALPHA)
            pygame.draw.circle(shield_surf, (0, 255, 255, 128), (50, 50), 45)
            pygame.draw.circle(shield_surf, (0, 255, 255, 255), (50, 50), 45, 3)
            surface.blit(shield_surf, (self.rect.centerx - 50, self.rect.centery - 50))

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, speed):
        super().__init__()
        self.image = pygame.Surface((4, 12), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (255, 255, 255), (1, 0, 2, 12))
        pygame.draw.rect(self.image, (0, 255, 255), (0, 2, 4, 8))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.damage = damage
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

class EnemyBomb(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = pygame.Surface((6, 12), pygame.SRCALPHA)
        pygame.draw.circle(self.image, ORANGE, (3, 6), 3)
        pygame.draw.circle(self.image, (255, 100, 0), (3, 3), 2)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((12, 12), pygame.SRCALPHA)
        pygame.draw.circle(self.image, YELLOW, (6, 6), 5)
        pygame.draw.circle(self.image, (255, 255, 200), (4, 4), 2)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 2
        self.value = 1

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size=20):
        super().__init__()
        self.image = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        self.start_time = pygame.time.get_ticks()
        self.duration = 300
        self.size = size

    def update(self):
        elapsed = pygame.time.get_ticks() - self.start_time
        if elapsed >= self.duration:
            self.kill()
            return
        progress = elapsed / self.duration
        radius = int(self.size * (0.5 + progress * 0.5))
        alpha = int(255 * (1 - progress))
        self.image.fill((0,0,0,0))
        pygame.draw.circle(self.image, (255, 200, 0, alpha), (self.size, self.size), radius)
        pygame.draw.circle(self.image, (255, 100, 0, alpha//2), (self.size, self.size), max(0, radius-2))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type='basic', level=1):
        super().__init__()
        self.enemy_type = enemy_type
        self.level = level
        self.image = draw_enemy_ship(enemy_type)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1
        self.move_down_counter = 0

        if enemy_type == 'basic':
            self.health = 20 + level * 2
            self.speed_x = 1 + level * 0.2
            self.points = 100
            self.coin_drop_chance = 0.3
            self.bomb_chance = 0.005
            self.bomb_speed = 3
        elif enemy_type == 'fast':
            self.health = 10 + level * 2
            self.speed_x = 2 + level * 0.3
            self.points = 150
            self.coin_drop_chance = 0.4
            self.bomb_chance = 0.003
            self.bomb_speed = 4
        elif enemy_type == 'tank':
            self.health = 40 + level * 5
            self.speed_x = 0.5 + level * 0.1
            self.points = 300
            self.coin_drop_chance = 0.8
            self.bomb_chance = 0.01
            self.bomb_speed = 2
        else:
            self.health = 20 + level * 2
            self.speed_x = 1 + level * 0.2
            self.points = 100
            self.coin_drop_chance = 0.3
            self.bomb_chance = 0.005
            self.bomb_speed = 3

    def update(self):
        if random.random() < self.bomb_chance:
            self.drop_bomb()

    def drop_bomb(self):
        bomb = EnemyBomb(self.rect.centerx, self.rect.bottom, self.bomb_speed)
        all_sprites.add(bomb)
        enemy_bombs.add(bomb)

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
            if random.random() < self.coin_drop_chance:
                coin = Coin(self.rect.centerx, self.rect.centery)
                all_sprites.add(coin)
                coins_group.add(coin)
            return self.points
        return 0

class EnemyManager:
    def __init__(self):
        self.move_down_amount = 10
        self.move_timer = 0
        self.move_delay = 500

    def update(self):
        if not enemies:
            return
        self.move_timer += clock.get_time()
        if self.move_timer >= self.move_delay:
            self.move_timer = 0
            move_down = False
            for enemy in enemies:
                if enemy.rect.right >= SCREEN_WIDTH and enemy.direction == 1:
                    move_down = True
                    break
                if enemy.rect.left <= 0 and enemy.direction == -1:
                    move_down = True
                    break
            if move_down:
                for enemy in enemies:
                    enemy.rect.y += self.move_down_amount
                    enemy.direction *= -1
            else:
                for enemy in enemies:
                    enemy.rect.x += enemy.speed_x * enemy.direction

def create_enemies(level):
    enemies.empty()
    for sprite in enemies:
        sprite.kill()
    rows = min(3 + level // 2, 7)
    cols = 8
    spacing_x = 70
    spacing_y = 55
    start_x = (SCREEN_WIDTH - (cols - 1) * spacing_x) // 2
    start_y = 50

    type_weights = {
        'basic': max(0.5, 1.0 - level * 0.05),
        'fast': min(0.3, level * 0.05),
        'tank': min(0.3, level * 0.1)
    }
    total_weight = sum(type_weights.values())
    for key in type_weights:
        type_weights[key] /= total_weight

    for row in range(rows):
        for col in range(cols):
            r = random.random()
            if r < type_weights['basic']:
                enemy_type = 'basic'
            elif r < type_weights['basic'] + type_weights['fast']:
                enemy_type = 'fast'
            else:
                enemy_type = 'tank'
            x = start_x + col * spacing_x
            y = start_y + row * spacing_y
            enemy = Enemy(x, y, enemy_type, level)
            all_sprites.add(enemy)
            enemies.add(enemy)

def show_lobby():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return 'play'
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        draw_background(screen)
        title = font.render("SPACE INVADERS", True, CYAN)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 150))
        start_text = font.render("Press ENTER to Start", True, WHITE)
        screen.blit(start_text, (SCREEN_WIDTH//2 - start_text.get_width()//2, 300))
        quit_text = font.render("Press Q to Quit", True, RED)
        screen.blit(quit_text, (SCREEN_WIDTH//2 - quit_text.get_width()//2, 350))
        pygame.display.flip()
        clock.tick(FPS)

def game_over_screen(player):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False
                    return 'lobby'
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        draw_background(screen)
        game_over_text = font.render("GAME OVER", True, RED)
        score_text = font.render(f"Score: {player.score}", True, WHITE)
        coins_text = font.render(f"Coins collected: {player.coins}", True, YELLOW)
        restart_text = small_font.render("Press ENTER to return to lobby, ESC to quit", True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, 200))
        screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 250))
        screen.blit(coins_text, (SCREEN_WIDTH//2 - coins_text.get_width()//2, 290))
        screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, 350))
        pygame.display.flip()
        clock.tick(FPS)

def main():
    player = Player()
    player_group.add(player)
    all_sprites.add(player)
    game_state = 'lobby'
    level = 1
    enemy_manager = None
    paused = False

    while True:
        if game_state == 'lobby':
            action = show_lobby()
            if action == 'play':
                player.reset_for_new_game()
                player_group.empty()
                player_group.add(player)
                all_sprites.empty()
                all_sprites.add(player)
                enemies.empty()
                player_bullets.empty()
                enemy_bombs.empty()
                coins_group.empty()
                explosions.empty()
                level = 1
                enemy_manager = EnemyManager()
                create_enemies(level)
                game_state = 'playing'

        elif game_state == 'playing':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player.shoot()
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_p:
                        paused = not paused
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if player.rect.collidepoint(event.pos):
                            player.dragging = True
                            player.drag_offset_x = player.rect.x - event.pos[0]
                            player.drag_offset_y = player.rect.y - event.pos[1]
                        else:
                            player.shoot()
                if event.type == pygame.MOUSEMOTION:
                    if player.dragging:
                        new_x = event.pos[0] + player.drag_offset_x
                        new_y = event.pos[1] + player.drag_offset_y
                        player.rect.x = max(0, min(new_x, SCREEN_WIDTH - player.rect.width))
                        player.rect.y = max(0, min(new_y, SCREEN_HEIGHT - player.rect.height))
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        player.dragging = False

            if not paused:
                player.update()
                enemy_manager.update()
                enemies.update()
                player_bullets.update()
                enemy_bombs.update()
                coins_group.update()
                explosions.update()

                hits = pygame.sprite.groupcollide(enemies, player_bullets, False, True)
                for enemy, bullets in hits.items():
                    for bullet in bullets:
                        expl = Explosion(bullet.rect.centerx, bullet.rect.centery, size=15)
                        all_sprites.add(expl)
                        explosions.add(expl)
                        points = enemy.take_damage(bullet.damage)
                        if points > 0:
                            player.score += points
                            big_expl = Explosion(enemy.rect.centerx, enemy.rect.centery, size=30)
                            all_sprites.add(big_expl)
                            explosions.add(big_expl)

                bomb_hits = pygame.sprite.spritecollide(player, enemy_bombs, True)
                if bomb_hits:
                    player.take_damage(10 * len(bomb_hits))

                coin_hits = pygame.sprite.spritecollide(player, coins_group, True)
                for coin in coin_hits:
                    player.coins += coin.value

                if not enemies:
                    level += 1
                    player.level_up()  # Heal to full and increase max HP by 100
                    create_enemies(level)
                    enemy_manager = EnemyManager()

                if player.health <= 0:
                    game_state = 'game_over'

            draw_background(screen)
            all_sprites.draw(screen)
            player.draw_shield(screen)
            player.draw_health_bar(screen)
            score_text = small_font.render(f"Score: {player.score}", True, WHITE)
            coins_text = small_font.render(f"Coins: {player.coins}", True, YELLOW)
            level_text = small_font.render(f"Level: {level}", True, CYAN)
            screen.blit(score_text, (SCREEN_WIDTH - 150, 10))
            screen.blit(coins_text, (SCREEN_WIDTH - 150, 40))
            screen.blit(level_text, (SCREEN_WIDTH - 150, 70))
            if paused:
                pause_text = font.render("PAUSED - Press P to resume", True, WHITE)
                screen.blit(pause_text, (SCREEN_WIDTH//2 - pause_text.get_width()//2, SCREEN_HEIGHT//2))
            pygame.display.flip()
            clock.tick(FPS)

        elif game_state == 'game_over':
            result = game_over_screen(player)
            if result == 'lobby':
                game_state = 'lobby'

if __name__ == "__main__":
    main()
