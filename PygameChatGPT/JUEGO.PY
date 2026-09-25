import pygame
import sys
import math

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Super Mario Python - Edición Definitiva")

# Reloj y FPS
clock = pygame.time.Clock()
FPS = 60

# Paleta de Colores
SKY_TOP = (80, 150, 255)
SKY_BOTTOM = (180, 220, 255)
PLAYER_RED = (220, 30, 30)
PLAYER_BLUE = (30, 90, 200)
SKIN_COLOR = (255, 210, 160)
GROUND_GREEN = (40, 150, 40)
GROUND_TOP = (70, 190, 70)
BRICK_BROWN = (150, 75, 0)
BRICK_DARK = (100, 50, 0)
GOLD = (255, 215, 0)
ENEMY_COLOR = (140, 50, 20)
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
RED_TEXT = (255, 60, 60)

# Fuentes
font = pygame.font.SysFont("Arial", 24, bold=True)
font_large = pygame.font.SysFont("Arial", 48, bold=True)

# Clase del Jugador (Mario detallado)
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 40
        self.height = 48
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Físicas
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5.5
        self.jump_force = -13
        self.gravity = 0.55
        self.on_ground = False
        self.jump_buffer = 0

    def update(self, platforms):
        if self.jump_buffer > 0:
            self.jump_buffer -= 1

        self.vel_y += self.gravity
        if self.vel_y > 13:
            self.vel_y = 13

        # Movimiento horizontal
        self.rect.x += self.vel_x
        self.handle_collision_x(platforms)

        # Movimiento vertical
        self.rect.y += self.vel_y
        self.on_ground = False
        self.handle_collision_y(platforms)

        if self.jump_buffer > 0 and self.on_ground:
            self.vel_y = self.jump_force
            self.on_ground = False
            self.jump_buffer = 0

        self.draw_player()

    def draw_player(self):
        self.image.fill((0, 0, 0, 0))
        # Overalls (Pantalón azul)
        pygame.draw.rect(self.image, PLAYER_BLUE, (8, 28, 24, 18), border_radius=3)
        # Camisa (Rojo)
        pygame.draw.rect(self.image, PLAYER_RED, (6, 14, 28, 16), border_radius=3)
        # Cara y ojos
        pygame.draw.rect(self.image, SKIN_COLOR, (14, 14, 20, 14), border_radius=2)
        pygame.draw.rect(self.image, BLACK, (24, 17, 3, 3)) # Ojo
        pygame.draw.rect(self.image, BLACK, (22, 22, 10, 3)) # Bigote
        # Gorra roja
        pygame.draw.rect(self.image, PLAYER_RED, (8, 6, 26, 10), border_radius=3)
        pygame.draw.rect(self.image, PLAYER_RED, (16, 4, 18, 4)) # Visera

    def handle_collision_x(self, platforms):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_x > 0:
                    self.rect.right = platform.rect.left
                elif self.vel_x < 0:
                    self.rect.left = platform.rect.right

    def handle_collision_y(self, platforms):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0

    def trigger_jump(self):
        self.jump_buffer = 12

# Clase para Enemigos (Goomba caminante)
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, min_x, max_x):
        super().__init__()
        self.width = 36
        self.height = 36
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.min_x = min_x
        self.max_x = max_x
        self.speed = 2
        self.direction = 1

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.x <= self.min_x or self.rect.x >= self.max_x:
            self.direction *= -1

        # Dibujar enemigo
        self.image.fill((0, 0, 0, 0))
        pygame.draw.ellipse(self.image, ENEMY_COLOR, (2, 8, 32, 26))
        pygame.draw.rect(self.image, (255, 200, 100), (8, 2, 20, 10), border_radius=5) # Cabeza
        pygame.draw.rect(self.image, WHITE, (10, 6, 5, 5))
        pygame.draw.rect(self.image, WHITE, (21, 6, 5, 5))
        pygame.draw.rect(self.image, BLACK, (12, 8, 2, 2))
        pygame.draw.rect(self.image, BLACK, (23, 8, 2, 2))

# Clase para Textos Flotantes (Efecto +100 puntos)
class FloatingText(pygame.sprite.Sprite):
    def __init__(self, x, y, text):
        super().__init__()
        self.image = font.render(text, True, GOLD)
        self.rect = self.image.get_rect(center=(x, y))
        self.timer = 30 # Dura 30 frames

    def update(self):
        self.rect.y -= 1
        self.timer -= 1
        if self.timer <= 0:
            self.kill()

# Plataformas
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, is_ground=False):
        super().__init__()
        self.image = pygame.Surface((width, height))
        if is_ground:
            self.image.fill(GROUND_GREEN)
            pygame.draw.rect(self.image, GROUND_TOP, (0, 0, width, 8))
        else:
            self.image.fill(BRICK_BROWN)
            pygame.draw.rect(self.image, BRICK_DARK, (0, 0, width, height), 3)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Monedas
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_y = y
        self.angle = 0
        self.image = pygame.Surface((24, 24), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.angle += 0.15
        self.rect.centery = self.original_y + math.sin(self.angle) * 5
        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(self.image, GOLD, (12, 12), 11)
        pygame.draw.circle(self.image, (255, 255, 180), (12, 12), 6)

# Meta (Bandera)
class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((35, 90), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        pygame.draw.rect(self.image, (180, 180, 180), (4, 0, 6, 90))
        pygame.draw.polygon(self.image, (220, 40, 40), [(10, 10), (35, 22), (10, 35)])

# Definición de 6 Niveles con enemigos y plataformas estratégicas
levels = [
    {
        "platforms": [(0, 550, 800, 50, True), (220, 440, 140, 22), (420, 330, 140, 22)],
        "coins": [(290, 390), (490, 280)],
        "enemies": [(440, 300, 420, 530)],
        "goal": (700, 460)
    },
    {
        "platforms": [(0, 550, 800, 50, True), (150, 440, 100, 22), (350, 350, 120, 22), (580, 260, 120, 22)],
        "coins": [(190, 390), (410, 300), (640, 210)],
        "enemies": [(370, 310, 350, 450), (600, 220, 580, 680)],
        "goal": (700, 170)
    },
    {
        "platforms": [(0, 550, 800, 50, True), (100, 430, 80, 22), (250, 320, 80, 22), (420, 220, 80, 22), (600, 320, 80, 22)],
        "coins": [(140, 380), (290, 270), (460, 170), (640, 270)],
        "enemies": [(260, 280, 250, 310), (610, 280, 600, 660)],
        "goal": (650, 230)
    },
    {
        "platforms": [(0, 550, 800, 50, True), (150, 450, 70, 22), (300, 370, 70, 22), (450, 290, 70, 22), (600, 200, 70, 22)],
        "coins": [(185, 400), (335, 320), (485, 240), (635, 150)],
        "enemies": [(160, 410, 150, 200), (460, 250, 450, 500)],
        "goal": (620, 110)
    },
    {
        "platforms": [(0, 550, 800, 50, True), (120, 430, 90, 22), (280, 340, 90, 22), (460, 250, 90, 22), (250, 160, 120, 22)],
        "coins": [(160, 380), (325, 290), (505, 200), (310, 110)],
        "enemies": [(290, 300, 280, 350), (270, 120, 250, 350)],
        "goal": (280, 70)
    },
    {
        "platforms": [(0, 550, 800, 50, True), (100, 440, 60, 22), (220, 360, 60, 22), (340, 280, 60, 22), (460, 200, 60, 22), (600, 130, 100, 22)],
        "coins": [(130, 390), (250, 310), (370, 230), (490, 150), (650, 80)],
        "enemies": [(230, 320, 220, 260), (470, 160, 460, 500)],
        "goal": (630, 40)
    }
]

current_level_index = 0
score = 0
lives = 3
game_state = "PLAYING" # PLAYING, GAMEOVER, WIN

def load_level(level_idx):
    global all_sprites, platforms, coins_group, enemies_group, goal, player, floating_texts
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    coins_group = pygame.sprite.Group()
    enemies_group = pygame.sprite.Group()
    floating_texts = pygame.sprite.Group()

    lvl_data = levels[level_idx]

    for p_data in lvl_data["platforms"]:
        p = Platform(p_data[0], p_data[1], p_data[2], p_data[3], is_ground=p_data[4] if len(p_data) > 4 else False)
        platforms.add(p)
        all_sprites.add(p)

    for c_pos in lvl_data["coins"]:
        c = Coin(c_pos[0], c_pos[1])
        coins_group.add(c)
        all_sprites.add(c)

    for e_data in lvl_data["enemies"]:
        e = Enemy(e_data[0], e_data[1], e_data[2], e_data[3])
        enemies_group.add(e)
        all_sprites.add(e)

    g_pos = lvl_data["goal"]
    goal = Goal(g_pos[0], g_pos[1])
    all_sprites.add(goal)

    player = Player(40, 480)
    all_sprites.add(player)

load_level(current_level_index)

def draw_background(surface):
    for y in range(SCREEN_HEIGHT):
        inter = y / SCREEN_HEIGHT
        r = int(SKY_TOP[0] * (1 - inter) + SKY_BOTTOM[0] * inter)
        g = int(SKY_TOP[1] * (1 - inter) + SKY_BOTTOM[1] * inter)
        b = int(SKY_TOP[2] * (1 - inter) + SKY_BOTTOM[2] * inter)
        pygame.draw.line(surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))
    
    # Nubes estéticas decorativas de fondo
    pygame.draw.circle(surface, (255, 255, 255, 180), (150, 100), 30)
    pygame.draw.circle(surface, (255, 255, 255, 180), (180, 90), 40)
    pygame.draw.circle(surface, (255, 255, 255, 180), (600, 140), 35)
    pygame.draw.circle(surface, (255, 255, 255, 180), (635, 130), 45)

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        
        elif event.type == pygame.KEYDOWN:
            if game_state == "PLAYING":
                if event.key == pygame.K_SPACE:
                    player.trigger_jump()
            elif game_state in ("GAMEOVER", "WIN"):
                if event.key == pygame.K_r: # Reiniciar juego completo
                    current_level_index = 0
                    score = 0
                    lives = 3
                    game_state = "PLAYING"
                    load_level(current_level_index)

    if game_state == "PLAYING":
        # Movimiento fluido
        keys = pygame.key.get_pressed()
        player.vel_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.vel_x = -player.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.vel_x = player.speed

        # Actualizar lógica
        player.update(platforms)
        coins_group.update()
        enemies_group.update()
        floating_texts.update()

        # Colisión con monedas
        collected_coins = pygame.sprite.spritecollide(player, coins_group, True)
        for coin in collected_coins:
            score += 100
            ft = FloatingText(coin.rect.centerx, coin.rect.centery, "+100")
            floating_texts.add(ft)

        # Colisión con enemigos (Pierde vida)
        if pygame.sprite.spritecollideany(player, enemies_group):
            lives -= 1
            if lives > 0:
                load_level(current_level_index) # Reiniciar nivel actual
            else:
                game_state = "GAMEOVER"

        # Colisión con la meta (Siguiente nivel)
        if player.rect.colliderect(goal.rect):
            current_level_index += 1
            if current_level_index < len(levels):
                load_level(current_level_index)
            else:
                game_state = "WIN"

    # Renderizado
    draw_background(screen)
    
    if game_state == "PLAYING":
        all_sprites.draw(screen)
        floating_texts.draw(screen)

        # UI de Puntuación, Vidas y Nivel
        score_text = font.render(f"PUNTOS: {score}", True, WHITE)
        lives_text = font.render(f"VIDAS: {'❤️ ' * lives}", True, WHITE)
        level_text = font.render(f"NIVEL: {current_level_index + 1}/{len(levels)}", True, WHITE)

        screen.blit(score_text, (20, 20))
        screen.blit(lives_text, (20, 50))
        screen.blit(level_text, (20, 80))

    elif game_state == "GAMEOVER":
        screen.fill((30, 10, 10))
        go_text = font_large.render("¡GAME OVER!", True, RED_TEXT)
        sub_text = font.render("Presiona 'R' para volver a intentar", True, WHITE)
        screen.blit(go_text, (SCREEN_WIDTH//2 - go_text.get_width()//2, SCREEN_HEIGHT//2 - 50))
        screen.blit(sub_text, (SCREEN_WIDTH//2 - sub_text.get_width()//2, SCREEN_HEIGHT//2 + 20))

    elif game_state == "WIN":
        screen.fill((10, 40, 10))
        win_text = font_large.render("¡HAS GANADO EL JUEGO!", True, GOLD)
        score_final = font.render(f"Puntuación Final: {score}", True, WHITE)
        sub_text = font.render("Presiona 'R' para jugar de nuevo", True, WHITE)
        screen.blit(win_text, (SCREEN_WIDTH//2 - win_text.get_width()//2, SCREEN_HEIGHT//2 - 60))
        screen.blit(score_final, (SCREEN_WIDTH//2 - score_final.get_width()//2, SCREEN_HEIGHT//2 - 10))
        screen.blit(sub_text, (SCREEN_WIDTH//2 - sub_text.get_width()//2, SCREEN_HEIGHT//2 + 40))

    pygame.display.flip()
    clock.tick(FPS)