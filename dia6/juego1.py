import pygame

pygame.init()
ancho = 600
alto = 400
ventana = pygame.display.set_mode((ancho,alto))
reloj = pygame.time.Clock()

x,y = 300, 200
velocidad = 5
size = 20
corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_RIGHT]:
        if x < ancho - size:
            x = x + velocidad
    elif teclas[pygame.K_LEFT]:
        if x > size:
            x = x - velocidad
    elif teclas[pygame.K_UP]:
        if y > size:
            y = y - velocidad
    elif teclas[pygame.K_DOWN]:
        if y < alto -size:
            y = y + velocidad

    ventana.fill((255,255,255))
    pygame.draw.circle(ventana, (30,60,200), (x,y),size)
    pygame.display.flip()
    reloj.tick(60)

pygame.quit()