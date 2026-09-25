import pygame
import random
import math
import struct

# Inicialización de Pygame y del mezclador de audio
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=1)

# Configuración de la pantalla
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Invasión Espacial - Sistema de Mejoras")

# Colores (RGB)
BG_COLOR = (15, 15, 25)
PLAYER_COLOR = (0, 210, 255)
PLAYER_LASER_COLOR = (0, 255, 255)
SHIELD_COLOR = (77, 255, 136)
SLOW_COLOR = (255, 222, 77)
ENEMY_COLOR = (255, 50, 80)
ENEMY_LASER_COLOR = (255, 30, 30)
BOSS_COLOR = (180, 0, 255)
BOSS_LASER_COLOR = (255, 0, 100)
CARD_BG = (30, 35, 55)
CARD_BORDER = (0, 210, 255)
TEXT_COLOR = (255, 255, 255)
OVERLAY_COLOR = (0, 0, 0, 200)

# Reloj
clock = pygame.time.Clock()
FPS = 60

# Fuentes
font = pygame.font.SysFont("segoeui", 16)
font_bold = pygame.font.SysFont("segoeui", 18, bold=True)
font_large = pygame.font.SysFont("segoeui", 28, bold=True)

# Fondo de estrellas
stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1, 3)) for _ in range(60)]

# -------------------------------------------------------------
# Funciones para generar sonidos sintéticos
# -------------------------------------------------------------
def generate_sound(freq_func, duration=0.3, volume=0.3):
    sample_rate = 44100
    n_samples = int(sample_rate * duration)
    buf = bytearray()
    
    for i in range(n_samples):
        t = i / sample_rate
        freq = freq_func(t)
        value = int(32767 * volume * math.sin(2 * math.pi * freq * t))
        buf.extend(struct.pack('<h', value))
        
    return pygame.mixer.Sound(bytes(buf))

sound_game_over = generate_sound(lambda t: max(60, 350 - t * 700), duration=0.5, volume=0.4)
sound_powerup = generate_sound(lambda t: 400 + t * 1400, duration=0.2, volume=0.3)
sound_shield_break = generate_sound(lambda t: 300 - t * 500, duration=0.15, volume=0.3)
sound_enemy_laser = generate_sound(lambda t: 600 - t * 2000, duration=0.08, volume=0.15)
sound_player_laser = generate_sound(lambda t: 900 - t * 3000, duration=0.08, volume=0.2)
sound_explosion = generate_sound(lambda t: random.randint(100, 300), duration=0.12, volume=0.25)
sound_boss_hit = generate_sound(lambda t: 150 + random.randint(0, 100), duration=0.05, volume=0.2)
sound_player_hit = generate_sound(lambda t: 200 - t * 300, duration=0.2, volume=0.35)

# -------------------------------------------------------------
# Sistema de Partículas para Explosiones
# -------------------------------------------------------------
particles = []

def create_explosion(x, y, colors, count=25):
    for _ in range(count):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1.5, 6.0)
        vx = math.cos(angle) * speed
        vy = math.sin(angle) * speed
        size = random.randint(3, 7)
        color = random.choice(colors)
        lifetime = random.randint(20, 45)
        particles.append({
            "x": x, "y": y, "vx": vx, "vy": vy,
            "size": size, "color": color, "life": lifetime, "max_life": lifetime
        })

def update_and_draw_particles(surface):
    for p in particles[:]:
        p["x"] += p["vx"]
        p["y"] += p["vy"]
        p["life"] -= 1
        current_size = max(1, int(p["size"] * (p["life"] / p["max_life"])))

        if p["life"] <= 0:
            particles.remove(p)
        else:
            pygame.draw.circle(surface, p["color"], (int(p["x"]), int(p["y"])), current_size)

# -------------------------------------------------------------
# Catálogo de Mejoras
# -------------------------------------------------------------
ALL_UPGRADES = [
    {"id": "cadence", "title": "Cadencia de Tiro", "desc": "Reduce el tiempo de\nespera entre disparos."},
    {"id": "double_shot", "title": "Disparo Doble", "desc": "Dispara dos proyectiles\nparalelos a la vez."},
    {"id": "shield", "title": "Escudo Protector", "desc": "Activa un escudo que\nabsorbe un impacto."},
    {"id": "heal", "title": "Reparar Casco", "desc": "Recupera 1 vida de la\nnave (Máx 3)."},
    {"id": "speed", "title": "Súper Velocidad", "desc": "Aumenta la velocidad de\nmovimiento de la nave."}
]

def get_random_upgrades():
    return random.sample(ALL_UPGRADES, 3)

# -------------------------------------------------------------
# Funciones de Dibujo
# -------------------------------------------------------------
def draw_player_ship(surface, rect, color, has_shield, invulnerable_timer):
    if invulnerable_timer > 0 and (invulnerable_timer // 5) % 2 == 0:
        return

    x, y, w, h = rect.x, rect.y, rect.width, rect.height
    
    # Propulsor
    flame_h = random.randint(6, 12)
    pygame.draw.polygon(surface, (255, 150, 0), [
        (x + w * 0.35, y + h), (x + w * 0.65, y + h), (x + w * 0.5, y + h + flame_h)
    ])

    # Cuerpo
    points = [
        (x + w // 2, y), (x + w, y + h), (x + w * 0.75, y + h * 0.8),
        (x + w * 0.5, y + h * 0.9), (x + w * 0.25, y + h * 0.8), (x, y + h)
    ]
    pygame.draw.polygon(surface, color, points)
    
    # Cabina
    cockpit = [
        (x + w // 2, y + h * 0.25), (x + w * 0.65, y + h * 0.55), (x + w * 0.35, y + h * 0.55)
    ]
    pygame.draw.polygon(surface, (200, 240, 255), cockpit)

    if has_shield:
        pygame.draw.ellipse(surface, SHIELD_COLOR, (x - 6, y - 6, w + 12, h + 12), 2)

def draw_enemy_ship(surface, rect):
    x, y, w, h = rect.x, rect.y, rect.width, rect.height
    points = [
        (x, y), (x + w * 0.3, y + h * 0.3), (x + w // 2, y + h),
        (x + w * 0.7, y + h * 0.3), (x + w, y), (x + w * 0.5, y + h * 0.1)
    ]
    pygame.draw.polygon(surface, ENEMY_COLOR, points)
    pygame.draw.circle(surface, (255, 200, 200), (x + w // 2, y + int(h * 0.45)), max(2, int(w * 0.12)))

def draw_boss_ship(surface, boss):
    x, y, w, h = boss["rect"].x, boss["rect"].y, boss["rect"].width, boss["rect"].height

    left_wing = [(x, y + h * 0.2), (x + w * 0.25, y + h * 0.8), (x + w * 0.25, y)]
    right_wing = [(x + w, y + h * 0.2), (x + w * 0.75, y + h * 0.8), (x + w * 0.75, y)]
    pygame.draw.polygon(surface, (120, 0, 180), left_wing)
    pygame.draw.polygon(surface, (120, 0, 180), right_wing)

    body = [
        (x + w * 0.2, y), (x + w * 0.8, y), (x + w * 0.9, y + h * 0.6),
        (x + w * 0.5, y + h), (x + w * 0.1, y + h * 0.6)
    ]
    pygame.draw.polygon(surface, BOSS_COLOR, body)

    core_color = (255, 50, 150) if random.random() < 0.8 else (255, 255, 255)
    pygame.draw.circle(surface, core_color, (x + w // 2, y + int(h * 0.45)), 14)

    pygame.draw.rect(surface, (200, 200, 200), (x + w * 0.3 - 3, y + h * 0.8, 6, 12))
    pygame.draw.rect(surface, (200, 200, 200), (x + w * 0.7 - 3, y + h * 0.8, 6, 12))

def draw_player_lives_bar(surface, lives, max_lives):
    x, y = 15, 42
    bar_w, bar_h = 100, 10
    
    pygame.draw.rect(surface, (40, 40, 60), (x - 2, y - 2, bar_w + 4, bar_h + 4), border_radius=3)
    fill_color = PLAYER_COLOR if lives == 3 else ((255, 200, 0) if lives == 2 else (255, 50, 50))
    fill_w = int(bar_w * (lives / max_lives))
    if fill_w > 0:
        pygame.draw.rect(surface, fill_color, (x, y, fill_w, bar_h), border_radius=3)

    for i in range(max_lives):
        icon_x = x + i * 22
        icon_y = y + 16
        icon_color = PLAYER_COLOR if i < lives else (60, 60, 80)
        pts = [(icon_x + 6, icon_y), (icon_x + 12, icon_y + 12), (icon_x, icon_y + 12)]
        pygame.draw.polygon(surface, icon_color, pts)

def draw_boss_health_bar(surface, boss):
    bar_width = 260
    bar_height = 12
    x = (WIDTH - bar_width) // 2
    y = 45

    pygame.draw.rect(surface, (40, 40, 60), (x - 2, y - 2, bar_width + 4, bar_height + 4), border_radius=4)
    pygame.draw.rect(surface, (100, 20, 40), (x, y, bar_width, bar_height), border_radius=3)

    health_ratio = boss["hp"] / boss["max_hp"]
    fill_width = int(bar_width * health_ratio)
    if fill_width > 0:
        pygame.draw.rect(surface, (255, 0, 90), (x, y, fill_width, bar_height), border_radius=3)

    label = font.render("¡JEFE ESPACIAL!", True, (255, 180, 220))
    surface.blit(label, (WIDTH // 2 - label.get_width() // 2, y - 20))

def draw_upgrade_screen(surface, options):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill(OVERLAY_COLOR)
    surface.blit(overlay, (0, 0))

    title = font_large.render("¡MEJORA DISPONIBLE!", True, (255, 222, 77))
    subtitle = font.render("Presiona 1, 2 o 3 para elegir:", True, TEXT_COLOR)
    surface.blit(title, (WIDTH // 2 - title.get_width() // 2, 70))
    surface.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 110))

    card_w, card_h = 320, 110
    start_y = 160

    for idx, opt in enumerate(options):
        card_x = (WIDTH - card_w) // 2
        card_y = start_y + idx * 125

        # Tarjeta
        pygame.draw.rect(surface, CARD_BG, (card_x, card_y, card_w, card_h), border_radius=10)
        pygame.draw.rect(surface, CARD_BORDER, (card_x, card_y, card_w, card_h), width=2, border_radius=10)

        # Número de Opción
        num_txt = font_large.render(f"[{idx + 1}]", True, (255, 222, 77))
        surface.blit(num_txt, (card_x + 15, card_y + 15))

        # Título de Mejora
        opt_title = font_bold.render(opt["title"], True, TEXT_COLOR)
        surface.blit(opt_title, (card_x + 65, card_y + 15))

        # Descripción
        lines = opt["desc"].split("\n")
        for line_idx, line in enumerate(lines):
            desc_txt = font.render(line, True, (180, 190, 210))
            surface.blit(desc_txt, (card_x + 65, card_y + 42 + line_idx * 20))

# -------------------------------------------------------------
# Lógica del Juego
# -------------------------------------------------------------
def reset_game():
    player = pygame.Rect(WIDTH // 2 - 18, HEIGHT - 55, 36, 36)
    player_speed = 8
    player_lasers = []
    
    enemies = []
    enemy_lasers = []
    powerups = []
    
    enemy_speed = 2.5
    spawn_rate = 60
    frame_count = 0
    score = 0
    shoot_cooldown = 0
    max_cooldown = 18  # Cadencia inicial reducida (mayor tiempo entre disparos)
    double_shot = False
    game_over = False

    lives = 3
    max_lives = 3
    invulnerable_timer = 0

    has_shield = False
    slow_timer = 0
    particles.clear()

    boss = None
    next_boss_score = 1500

    # Estado de Mejoras
    selecting_upgrade = False
    current_upgrade_options = []
    next_upgrade_score = 1000

    return (player, player_speed, player_lasers, enemies, enemy_lasers, powerups, 
            enemy_speed, spawn_rate, frame_count, score, shoot_cooldown, max_cooldown, double_shot, 
            game_over, has_shield, slow_timer, boss, next_boss_score, lives, max_lives, invulnerable_timer,
            selecting_upgrade, current_upgrade_options, next_upgrade_score)

(player, player_speed, player_lasers, enemies, enemy_lasers, powerups, 
 enemy_speed, spawn_rate, frame_count, score, shoot_cooldown, max_cooldown, double_shot, 
 game_over, has_shield, slow_timer, boss, next_boss_score, lives, max_lives, invulnerable_timer,
 selecting_upgrade, current_upgrade_options, next_upgrade_score) = reset_game()

def hit_player():
    global has_shield, lives, invulnerable_timer, game_over
    if invulnerable_timer > 0:
        return

    if has_shield:
        has_shield = False
        sound_shield_break.play()
        create_explosion(player.x + player.width // 2, player.y + player.height // 2, [(77, 255, 136), (255, 255, 255)], count=15)
        invulnerable_timer = 40
    else:
        lives -= 1
        sound_player_hit.play()
        create_explosion(player.x + player.width // 2, player.y + player.height // 2, [(0, 210, 255), (255, 50, 50)], count=25)
        invulnerable_timer = 110

        if lives <= 0:
            game_over = True
            sound_game_over.play()

def apply_upgrade(upgrade_id):
    global max_cooldown, double_shot, has_shield, lives, player_speed
    sound_powerup.play()
    if upgrade_id == "cadence":
        max_cooldown = max(8, max_cooldown - 3)  # Límite mínimo ajustado a 8
    elif upgrade_id == "double_shot":
        double_shot = True
    elif upgrade_id == "shield":
        has_shield = True
    elif upgrade_id == "heal":
        lives = min(max_lives, lives + 1)
    elif upgrade_id == "speed":
        player_speed += 1.5

running = True
while running:
    # 1. Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if game_over and (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN):
                (player, player_speed, player_lasers, enemies, enemy_lasers, powerups, 
                 enemy_speed, spawn_rate, frame_count, score, shoot_cooldown, max_cooldown, double_shot, 
                 game_over, has_shield, slow_timer, boss, next_boss_score, lives, max_lives, invulnerable_timer,
                 selecting_upgrade, current_upgrade_options, next_upgrade_score) = reset_game()

            # Selección de Mejoras
            elif selecting_upgrade:
                chosen_idx = -1
                if event.key == pygame.K_1:
                    chosen_idx = 0
                elif event.key == pygame.K_2:
                    chosen_idx = 1
                elif event.key == pygame.K_3:
                    chosen_idx = 2

                if chosen_idx != -1 and chosen_idx < len(current_upgrade_options):
                    apply_upgrade(current_upgrade_options[chosen_idx]["id"])
                    selecting_upgrade = False

    if not game_over and not selecting_upgrade:
        # Check Trigger de Mejora (Cada 1000 pts)
        if score >= next_upgrade_score:
            selecting_upgrade = True
            current_upgrade_options = get_random_upgrades()
            next_upgrade_score += 1000

        # 2. Teclado
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player.left > 0:
            player.x -= player_speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player.right < WIDTH:
            player.x += player_speed

        # Disparo con Barra Espaciadora
        if shoot_cooldown > 0:
            shoot_cooldown -= 1

        if keys[pygame.K_SPACE] and shoot_cooldown == 0:
            if double_shot:
                l1 = pygame.Rect(player.x + 4, player.y - 12, 4, 14)
                l2 = pygame.Rect(player.x + player.width - 8, player.y - 12, 4, 14)
                player_lasers.extend([l1, l2])
            else:
                l1 = pygame.Rect(player.x + player.width // 2 - 2, player.y - 12, 4, 14)
                player_lasers.append(l1)
            sound_player_laser.play()
            shoot_cooldown = max_cooldown

        if invulnerable_timer > 0:
            invulnerable_timer -= 1

        # 3. Dificultad y Puntuación
        frame_count += 1
        score += 1

        if frame_count % 360 == 0:
            enemy_speed += 0.25
            if spawn_rate > 20:
                spawn_rate -= 1

        if slow_timer > 0:
            slow_timer -= 1

        current_speed = enemy_speed * 0.5 if slow_timer > 0 else enemy_speed

        # 4. Aparición del Jefe
        if score >= next_boss_score and boss is None:
            boss = {
                "rect": pygame.Rect(WIDTH // 2 - 50, -80, 100, 60),
                "hp": 30,
                "max_hp": 30,
                "dir": 1,
                "speed": 2.2,
                "target_y": 50,
                "shoot_cooldown": 0
            }

        # 5. Lógica del Jefe Final
        if boss:
            if boss["rect"].y < boss["target_y"]:
                boss["rect"].y += 2
            else:
                boss["rect"].x += boss["dir"] * boss["speed"]

                if boss["rect"].left <= 10:
                    boss["rect"].left = 10
                    boss["dir"] = 1
                elif boss["rect"].right >= WIDTH - 10:
                    boss["rect"].right = WIDTH - 10
                    boss["dir"] = -1

                boss["shoot_cooldown"] += 1
                if boss["shoot_cooldown"] >= 55:
                    boss["shoot_cooldown"] = 0
                    sound_enemy_laser.play()
                    l1 = pygame.Rect(boss["rect"].x + int(boss["rect"].width * 0.3) - 2, boss["rect"].y + boss["rect"].height, 5, 14)
                    l2 = pygame.Rect(boss["rect"].x + int(boss["rect"].width * 0.7) - 2, boss["rect"].y + boss["rect"].height, 5, 14)
                    enemy_lasers.extend([l1, l2])

        # 6. Generación de Naves Enemigas
        if boss is None and frame_count % max(18, int(spawn_rate)) == 0:
            enemy_w = random.randint(28, 48)
            enemy_x = random.randint(0, WIDTH - enemy_w)
            enemies.append(pygame.Rect(enemy_x, -35, enemy_w, 32))

        # 7. Generación de Power-Ups
        if frame_count % 220 == 0 and random.random() < 0.7:
            p_type = "shield" if random.random() < 0.5 else "slow"
            p_x = random.randint(10, WIDTH - 25)
            powerups.append({"rect": pygame.Rect(p_x, -20, 20, 20), "type": p_type})

        # 8. Mover Disparos del Jugador
        for laser in player_lasers[:]:
            laser.y -= 10

            if laser.y < -20:
                player_lasers.remove(laser)
                continue

            if boss and laser.colliderect(boss["rect"]):
                boss["hp"] -= 1
                sound_boss_hit.play()
                create_explosion(laser.x, laser.y, [(255, 0, 150), (255, 255, 255)], count=6)
                player_lasers.remove(laser)

                if boss["hp"] <= 0:
                    create_explosion(
                        boss["rect"].x + boss["rect"].width // 2, boss["rect"].y + boss["rect"].height // 2,
                        [(180, 0, 255), (255, 0, 100), (255, 255, 255), (255, 200, 0)], count=90
                    )
                    sound_explosion.play()
                    score += 500
                    next_boss_score += 1500
                    boss = None
                continue

            hit_enemy = False
            for enemy in enemies[:]:
                if laser.colliderect(enemy):
                    create_explosion(
                        enemy.x + enemy.width // 2, enemy.y + enemy.height // 2,
                        [(255, 50, 80), (255, 150, 0), (255, 220, 50)], count=20
                    )
                    enemies.remove(enemy)
                    hit_enemy = True
                    score += 50
                    sound_explosion.play()
                    break

            if hit_enemy and laser in player_lasers:
                player_lasers.remove(laser)

        # 9. Mover Power-Ups
        for p in powerups[:]:
            p["rect"].y += int(current_speed * 0.8)
            
            if player.colliderect(p["rect"]):
                sound_powerup.play()
                if p["type"] == "shield":
                    has_shield = True
                elif p["type"] == "slow":
                    slow_timer = 240
                powerups.remove(p)
            elif p["rect"].y > HEIGHT:
                powerups.remove(p)

        # 10. Mover Enemigos y Disparar
        laser_speed = current_speed + 2.5
        for enemy in enemies[:]:
            enemy.y += current_speed

            if enemy.y > 0 and enemy.y < HEIGHT - 120:
                if random.random() < 0.007:
                    e_laser = pygame.Rect(enemy.x + enemy.width // 2 - 2, enemy.y + enemy.height, 4, 12)
                    enemy_lasers.append(e_laser)
                    sound_enemy_laser.play()

            if player.colliderect(enemy):
                hit_player()
                enemies.remove(enemy)

            elif enemy.y > HEIGHT:
                enemies.remove(enemy)

        if boss and player.colliderect(boss["rect"]):
            hit_player()

        # 11. Mover Proyectiles Enemigos
        for laser in enemy_lasers[:]:
            laser.y += laser_speed

            if player.colliderect(laser):
                hit_player()
                enemy_lasers.remove(laser)

            elif laser.y > HEIGHT:
                enemy_lasers.remove(laser)

    # -------------------------------------------------------------
    # Renderizado
    # -------------------------------------------------------------
    screen.fill(BG_COLOR)

    # Estrellas de fondo
    for star_x, star_y, star_size in stars:
        pygame.draw.circle(screen, (180, 180, 220), (star_x, star_y), star_size)

    # Disparos Jugador
    for laser in player_lasers:
        pygame.draw.rect(screen, PLAYER_LASER_COLOR, laser)
        pygame.draw.rect(screen, (255, 255, 255), (laser.x + 1, laser.y + 1, 2, laser.height - 2))

    # Disparos Enemigos
    for laser in enemy_lasers:
        pygame.draw.rect(screen, BOSS_LASER_COLOR if boss else ENEMY_LASER_COLOR, laser)
        pygame.draw.rect(screen, (255, 200, 200), (laser.x + 1, laser.y + 1, 2, laser.height - 2))

    # Naves Enemigas
    for enemy in enemies:
        draw_enemy_ship(screen, enemy)

    # Jefe
    if boss:
        draw_boss_ship(screen, boss)
        draw_boss_health_bar(screen, boss)

    # Nave Jugador
    if not game_over:
        draw_player_ship(screen, player, PLAYER_COLOR, has_shield, invulnerable_timer)

    # Power-ups
    for p in powerups:
        color = SHIELD_COLOR if p["type"] == "shield" else SLOW_COLOR
        pygame.draw.ellipse(screen, color, p["rect"])
        pygame.draw.ellipse(screen, (255, 255, 255), p["rect"], 1)

    # Partículas de explosión
    update_and_draw_particles(screen)

    # Interfaz HUD
    score_text = font.render(f"Puntuación: {score}", True, TEXT_COLOR)
    screen.blit(score_text, (15, 15))
    draw_player_lives_bar(screen, lives, max_lives)

    hud_y = 80 if boss else 75
    if has_shield:
        shield_txt = font.render("ESCUDO ACTIVO", True, SHIELD_COLOR)
        screen.blit(shield_txt, (15, hud_y))
        hud_y += 25
    if slow_timer > 0:
        slow_txt = font.render(f"RALENTIZADO: {slow_timer // 60 + 1}s", True, SLOW_COLOR)
        screen.blit(slow_txt, (15, hud_y))

    # Pantalla de Selección de Mejoras
    if selecting_upgrade:
        draw_upgrade_screen(screen, current_upgrade_options)

    # Pantalla de Game Over
    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill(OVERLAY_COLOR)
        screen.blit(overlay, (0, 0))

        text_go = font_large.render("¡NAVE DESTRUIDA!", True, ENEMY_COLOR)
        text_final_score = font.render(f"Puntaje Final: {score}", True, TEXT_COLOR)
        text_restart = font.render("Presiona Enter para reiniciar", True, TEXT_COLOR)

        screen.blit(text_go, (WIDTH // 2 - text_go.get_width() // 2, HEIGHT // 2 - 40))
        screen.blit(text_final_score, (WIDTH // 2 - text_final_score.get_width() // 2, HEIGHT // 2 + 10))
        screen.blit(text_restart, (WIDTH // 2 - text_restart.get_width() // 2, HEIGHT // 2 + 50))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()