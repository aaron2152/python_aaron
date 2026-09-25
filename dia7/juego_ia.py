import pygame
import random
import math

pygame.init()
pygame.font.init()

# --- CONFIGURACIÓN PANTALLA ---
ANCHO, ALTO = 600, 500
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Cross The Road - Pro Edition")
reloj = pygame.time.Clock()

# --- PALETA DE COLORES ---
COLOR_FONDO_TOP = (15, 23, 42)     # Azul oscuro elegante
COLOR_FONDO_BOT = (30, 41, 59)
COLOR_JUGADOR = (56, 189, 248)    # Azul Neón
COLOR_JUGADOR_GLOW = (14, 165, 233)
COLOR_META = (34, 197, 94)         # Verde Esmeralda
COLOR_OBSTACULO = (239, 68, 68)   # Rojo Neón
COLOR_TEXTO = (241, 245, 249)
COLOR_TARJETA = (15, 23, 42, 180) # Fondo semitransparente para UI

# --- FUENTES MEJORADAS ---
fuente_ui = pygame.font.SysFont("Trebuchet MS", 14, bold=True)
fuente_titulo = pygame.font.SysFont("Trebuchet MS", 40, bold=True)
fuente_sub = pygame.font.SysFont("Trebuchet MS", 18)

# --- JUGADOR ---
size = 14
pos_inicio_x = ANCHO // 2
pos_inicio_y = ALTO - 35
x, y = pos_inicio_x, pos_inicio_y
velocidad_jugador = 4.5

# --- ESTADOS DEL JUEGO ---
nivel = 1
max_niveles = 5
muertes = 0
tiempo_inicio = pygame.time.get_ticks()
meta_rect = pygame.Rect(ANCHO // 2 - 60, 0, 120, 35)

# --- SISTEMA DE PARTÍCULAS ---
particulas = []

def crear_particulas(px, py, color, cantidad=20):
    for _ in range(cantidad):
        particulas.append({
            "x": px, "y": py,
            "vx": random.uniform(-4, 4),
            "vy": random.uniform(-4, 4),
            "radius": random.uniform(2, 5),
            "life": 255,
            "color": color
        })

def actualizar_dibujar_particulas(surface):
    for p in particulas[:]:
        p["x"] += p["vx"]
        p["y"] += p["vy"]
        p["life"] -= 8
        if p["life"] <= 0:
            particulas.remove(p)
        else:
            color_alpha = p["color"]
            s = pygame.Surface((p["radius"] * 2, p["radius"] * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*color_alpha, int(p["life"])), (p["radius"], p["radius"]), p["radius"])
            surface.blit(s, (p["x"] - p["radius"], p["y"] - p["radius"]))

# --- FUNCIONES DE DIBUJO ESTÉTICO DE TEXTO ---
def dibujar_badge(superficie, texto, x, y, color_texto, color_fondo=(30, 41, 59)):
    """Dibuja una etiqueta o badge redondeada con sombra suave."""
    render = fuente_ui.render(texto, True, color_texto)
    padding_x, padding_y = 12, 6
    w, h = render.get_width() + padding_x * 2, render.get_height() + padding_y * 2
    
    # Superficie con transparencia
    badge = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(badge, (*color_fondo, 220), (0, 0, w, h), border_radius=12)
    pygame.draw.rect(badge, (255, 255, 255, 30), (0, 0, w, h), width=1, border_radius=12)
    
    superficie.blit(badge, (x, y))
    superficie.blit(render, (x + padding_x, y + padding_y))

def dibujar_texto_con_sombra(superficie, texto, fuente, color, pos_center):
    """Renderiza texto con sombra proyectada para mayor legibilidad."""
    sombra = fuente.render(texto, True, (0, 0, 0))
    render = fuente.render(texto, True, color)
    
    cx, cy = pos_center
    rect_sombra = sombra.get_rect(center=(cx + 2, cy + 2))
    rect_render = render.get_rect(center=(cx, cy))
    
    superficie.blit(sombra, rect_sombra)
    superficie.blit(render, rect_render)

# --- GENERADOR DE OBSTÁCULOS ---
def crear_obstaculos(nivel_actual):
    obstaculos = []
    filas_y = [80, 140, 200, 260, 320, 380]
    
    for i, pos_y in enumerate(filas_y):
        ancho_obs = random.randint(70, 150)
        pos_x = random.randint(0, max(0, ANCHO - ancho_obs))
        direccion = 1 if i % 2 == 0 else -1
        vel_obs = (random.uniform(2.5, 4.0) + (nivel_actual * 0.6)) * direccion
        
        rect = pygame.Rect(pos_x, pos_y, ancho_obs, 22)
        obstaculos.append({"rect": rect, "vel": vel_obs})
        
    return obstaculos

def colision_circulo_rect(cx, cy, r, rect):
    closest_x = max(rect.left, min(cx, rect.right))
    closest_y = max(rect.top, min(cy, rect.bottom))
    dist_x = cx - closest_x
    dist_y = cy - closest_y
    return (dist_x**2 + dist_y**2) < (r**2)

obstaculos = crear_obstaculos(nivel)
juego_terminado = False
segundos_transcurridos = 0

# --- BUCLE PRINCIPAL ---
corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        if evento.type == pygame.KEYDOWN and juego_terminado:
            if evento.key == pygame.K_SPACE:
                nivel = 1
                muertes = 0
                tiempo_inicio = pygame.time.get_ticks()
                x, y = pos_inicio_x, pos_inicio_y
                obstaculos = crear_obstaculos(nivel)
                juego_terminado = False

    if not juego_terminado:
        # Movimiento del jugador
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_RIGHT] and x < ANCHO - size:
            x += velocidad_jugador
        if teclas[pygame.K_LEFT] and x > size:
            x -= velocidad_jugador
        if teclas[pygame.K_UP] and y > size:
            y -= velocidad_jugador
        if teclas[pygame.K_DOWN] and y < ALTO - size:
            y += velocidad_jugador

        # Movimiento de obstáculos
        for obs in obstaculos:
            obs["rect"].x += obs["vel"]
            if obs["rect"].right >= ANCHO or obs["rect"].left <= 0:
                obs["vel"] *= -1

        # Colisiones
        for obs in obstaculos:
            if colision_circulo_rect(x, y, size, obs["rect"]):
                crear_particulas(x, y, COLOR_OBSTACULO, 30)
                muertes += 1
                x, y = pos_inicio_x, pos_inicio_y

        # Victoria de nivel
        if colision_circulo_rect(x, y, size, meta_rect):
            crear_particulas(x, y, COLOR_META, 40)
            if nivel < max_niveles:
                nivel += 1
                x, y = pos_inicio_x, pos_inicio_y
                obstaculos = crear_obstaculos(nivel)
            else:
                juego_terminado = True

    # --- RENDERIZADO ---
    # Fondo con degradado
    for row in range(ALTO):
        r = COLOR_FONDO_TOP[0] + (COLOR_FONDO_BOT[0] - COLOR_FONDO_TOP[0]) * row // ALTO
        g = COLOR_FONDO_TOP[1] + (COLOR_FONDO_BOT[1] - COLOR_FONDO_TOP[1]) * row // ALTO
        b = COLOR_FONDO_TOP[2] + (COLOR_FONDO_BOT[2] - COLOR_FONDO_TOP[2]) * row // ALTO
        pygame.draw.line(ventana, (r, g, b), (0, row), (ANCHO, row))

    # Zona de Inicio y Meta
    pygame.draw.rect(ventana, (255, 255, 255, 10), (0, ALTO - 60, ANCHO, 60))
    pygame.draw.rect(ventana, COLOR_META, meta_rect, border_bottom_left_radius=12, border_bottom_right_radius=12)

    # Obstáculos con bordes redondeados
    for obs in obstaculos:
        pygame.draw.rect(ventana, COLOR_OBSTACULO, obs["rect"], border_radius=6)

    # Jugador con efecto de brillo (Glow)
    pygame.draw.circle(ventana, COLOR_JUGADOR_GLOW, (int(x), int(y)), size + 3)
    pygame.draw.circle(ventana, COLOR_JUGADOR, (int(x), int(y)), size)

    # Renderizado de partículas
    actualizar_dibujar_particulas(ventana)

    # --- INTERFAZ DE USUARIO (UI ESTÉTICA) ---
    if not juego_terminado:
        segundos_transcurridos = (pygame.time.get_ticks() - tiempo_inicio) // 1000

    # Badges modernos en la parte inferior
    dibujar_badge(ventana, f"NIVEL  {nivel}/{max_niveles}", 20, ALTO - 42, COLOR_JUGADOR)
    dibujar_badge(ventana, f"FALLOS  {muertes}", ANCHO // 2 - 45, ALTO - 42, COLOR_OBSTACULO)
    dibujar_badge(ventana, f"TIEMPO  {segundos_transcurridos}s", ANCHO - 125, ALTO - 42, COLOR_META)

    # Pantalla de Victoria Elegante
    if juego_terminado:
        overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        overlay.fill((15, 23, 42, 220))
        ventana.blit(overlay, (0, 0))
        
        # Tarjeta central con bordes suavizados
        tarjeta = pygame.Rect(ANCHO // 2 - 200, ALTO // 2 - 110, 400, 220)
        pygame.draw.rect(ventana, (30, 41, 59), tarjeta, border_radius=16)
        pygame.draw.rect(ventana, COLOR_META, tarjeta, width=2, border_radius=16)

        dibujar_texto_con_sombra(ventana, "¡VICTORIA!", fuente_titulo, COLOR_META, (ANCHO // 2, ALTO // 2 - 60))
        dibujar_texto_con_sombra(ventana, f"Tiempo: {segundos_transcurridos}s  |  Fallos: {muertes}", fuente_sub, COLOR_TEXTO, (ANCHO // 2, ALTO // 2 - 5))
        dibujar_badge(ventana, "PRESIONA ESPACIO PARA REINICIAR", ANCHO // 2 - 130, ALTO // 2 + 40, COLOR_JUGADOR, (15, 23, 42))

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()