import pygame

pygame.init()

# Colores
Black, White, Green, Red, Blue, Yellow = (0, 0, 0), (255, 255, 255), (0, 255, 0), (255, 0, 0), (0, 0, 255), (
255, 255, 0)

screen = pygame.display.set_mode((378, 464))
pygame.display.set_caption("Treasure Hunt")
fuente = pygame.font.SysFont("Arial", 15)
image = pygame.image.load("fondo.jpeg")


def draw_circles(screen, color, positions, radius):
    for pos in positions:
        pygame.draw.circle(screen, color, pos, radius)


def background(image):
    screen.blit(pygame.transform.scale(image, (378, 464)), (0, 0))

    # Posiciones de los círculos
    azules = [(100, 100), (60, 200), (149, 276), (110, 350), (80, 230), (70, 400)]
    verdes = [(200, 200), (230, 148), (270, 300), (300, 55), (300, 360), (220, 100)]
    rojos = [(150, 110), (160, 90), (165, 130), (165, 140), (170, 150), (120, 155), (80, 160),
             (180, 175), (190, 180), (195, 185), (80, 200), (190, 160), (175, 360), (170, 350),
             (145, 440), (140, 430), (150, 420), (155, 410), (160, 370), (140, 450), (150, 150),
             (180, 300), (190, 290), (200, 280), (170, 270)]
    amarillos = [(100, 150), (110, 160), (120, 170), (130, 180), (140, 190), (150, 200), (160, 210),
                 (170, 220), (180, 230), (190, 240), (200, 230), (190, 250), (180, 260), (170, 270),
                 (160, 280), (150, 290), (160, 300), (170, 310), (180, 320), (190, 330), (200, 340),
                 (210, 350), (220, 360), (230, 370), (240, 380), (250, 390), (260, 400), (270, 410),
                 (220, 130), (230, 80), (250, 70), (200, 50), (200, 460), (220, 450), (220, 50),
                 (180, 400), (170, 400), (150, 400), (100, 250), (150, 300), (80, 150), (90, 160),
                 (120, 90), (250, 80), (275, 345), (270, 330), (272, 320), (270, 310), (260, 300),
                 (250, 290), (240, 280), (220, 260), (220, 280), (230, 290), (240, 300), (250, 310),
                 (260, 320), (270, 330), (280, 340), (120, 350), (130, 360), (140, 370), (150, 380),
                 (160, 390), (170, 400), (180, 410), (190, 420), (200, 430), (210, 440), (110, 100),
                 (120, 110), (130, 120), (140, 130), (150, 140)]

    # Dibujar círculos
    draw_circles(screen, Blue, azules, 5)
    draw_circles(screen, Green, verdes, 5)
    draw_circles(screen, Red, rojos, 4)
    draw_circles(screen, Yellow, amarillos, 4)


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill(White)
    background(image)
    pygame.display.update()

pygame.quit()