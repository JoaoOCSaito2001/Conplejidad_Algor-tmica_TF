import random
import time
import sys
import pygame
import os
import math
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk, ImageFilter
from heapq import heappop, heappush

# Colores
Black, White, Green, Red, Blue, Yellow = (0, 0, 0), (255, 255, 255), (0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0)

# Posiciones de los círculos
azules = [(100, 100), (60, 200), (149, 276), (110, 350), (80, 230), (70, 400)]
verdes = [(200, 200), (230, 148), (270, 300), (300, 55), (300, 360), (220, 100)]
rojos = [(150, 110), (160, 90), (165, 130), (165, 140), (170, 150), (120, 155), (80, 160),
         (180, 175), (190, 180), (195, 185), (80, 200), (190, 160), (175, 360), (170, 350),
         (145, 440), (140, 430), (150, 420), (155, 410), (160, 370), (140, 450), (150, 150),
         (180, 300), (190, 290), (200, 280), (170, 270)]
amarillos = [(110, 170), (120, 190), (140, 180), (160, 210), (180, 230),
             (200, 220), (240, 250), (200, 260), (160, 280), (180, 290),
             (170, 300), (190, 310), (200, 320), (210, 330), (220, 340),
             (200, 350), (270, 340), (240, 360), (320, 370), (340, 380),
             (250, 390), (260, 400), (270, 410), (220, 130), (250, 70),
             (270, 80), (240, 100), (220, 50), (230, 120), (250, 450)]

# Inicialización de Pygame
pygame.init()
screen = pygame.display.set_mode((378, 464))
pygame.display.set_caption("Treasure Hunt")
fuente = pygame.font.SysFont("Arial", 20)
background_image = pygame.image.load("fondo.jpeg")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.image.load("player.png").convert()
            self.image.set_colorkey(White)
        except FileNotFoundError:
            print(f"The file 'player.png' was not found in the directory: {os.getcwd()}")
            sys.exit()
        self.rect = self.image.get_rect()

def draw_circles(screen, color, positions, radius):
    for pos in positions:
        pygame.draw.circle(screen, color, pos, radius)

def draw_background(image):
    screen.blit(pygame.transform.scale(image, (378, 464)), (0, 0))
    draw_circles(screen, Blue, azules, 5)
    draw_circles(screen, Green, verdes, 5)
    draw_circles(screen, Red, rojos, 4)
    draw_circles(screen, Yellow, amarillos, 4)

def draw_text(screen, text, font, color, position):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

def check_collision(rect, positions):
    for pos in positions:
        if rect.collidepoint(pos):
            return pos  # Devolver la posición del punto amarillo colisionado
    return None  # Devolver None si no hay colisión

def initialize_player_position(player, positions):
    initial_position = random.choice(positions)
    player.rect.topleft = initial_position

def format_time(milliseconds):
    minutes = int(milliseconds / 60000)
    seconds = int((milliseconds % 60000) / 1000)
    millis = int(milliseconds % 1000)
    return f"{minutes:02}:{seconds:02}:{millis:03}"

def calculate_distance(point1, point2):
    return math.hypot(point2[0] - point1[0], point2[1] - point1[1])

def create_graph(points):
    graph = {}
    for i, point1 in enumerate(points):
        graph[i] = []
        for j, point2 in enumerate(points):
            if i != j:
                distance = calculate_distance(point1, point2)
                graph[i].append((distance, j))
    return graph

def dijkstra(graph, start_node):
    heap = [(0, start_node)]
    distances = {node: float('inf') for node in graph}
    distances[start_node] = 0
    while heap:
        current_distance, current_node = heappop(heap)
        if current_distance > distances[current_node]:
            continue
        for distance, neighbor in graph[current_node]:
            distance += current_distance
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heappush(heap, (distance, neighbor))
    return distances

def find_best_path(start_pos, yellow_points, green_points, total_time):
    points = [start_pos] + yellow_points + green_points
    graph = create_graph(points)
    start_index = 0
    yellow_indices = range(1, len(yellow_points) + 1)
    green_indices = range(len(yellow_points) + 1, len(points))

    # Finding the shortest path that maximizes yellow points collected before reaching green point
    best_path = []
    max_yellows = 0

    for green_index in green_indices:
        distances = dijkstra(graph, start_index)
        if distances[green_index] <= total_time:
            path = []
            current_node = green_index
            time_left = total_time - distances[green_index]
            yellows_collected = 0
            while current_node != start_index:
                path.append(current_node)
                neighbors = [(dist, node) for dist, node in graph[current_node] if distances[node] + dist <= time_left]
                if not neighbors:
                    break
                next_node = min(neighbors)[1]
                time_left -= distances[next_node]
                current_node = next_node
                if current_node in yellow_indices:
                    yellows_collected += 1
            path.append(start_index)
            if yellows_collected > max_yellows:
                max_yellows = yellows_collected
                best_path = path[::-1]

    return [points[i] for i in best_path]

# Definimos la función para el minijuego
def run_minigame():
    # Creamos una nueva ventana de tkinter
    minigame_window = tk.Tk()
    minigame_window.title("Minijuego")
    minigame_window.geometry("500x600")  # Establecemos el tamaño de la ventana

    # Cargamos la imagen del minijuego y la convertimos a un formato compatible
    pil_image = Image.open("back-minigame.jpeg")
    pil_image = pil_image.resize((500, 600), resample=Image.BILINEAR)  # Redimensionamos la imagen con antialiasing
    minigame_image = ImageTk.PhotoImage(pil_image)

    # Mostramos la imagen de fondo en la ventana de tkinter
    label = tk.Label(minigame_window, image=minigame_image)
    label.image = minigame_image  # Mantenemos una referencia para evitar que la imagen sea recolectada por el recolector de basura
    label.pack()

    # Función para colocar las minas
    def place_mines():
        mines = 13
        min_image = Image.open("mina.jpeg")  # Cargar la imagen de la mina
        min_image = min_image.resize((20, 20))  # Redimensionar la imagen de la mina según sea necesario

        for _ in range(mines):
            x = random.randint(20, 470)  # Posiciones aleatorias dentro del rango de la ventana
            y = random.randint(100, 500)  # Ajustado para evitar cortes
            min_label = tk.Label(minigame_window)  # Etiqueta para la mina
            min_label.image = ImageTk.PhotoImage(
                min_image)  # Convertir la imagen de la mina a un formato compatible con tkinter
            min_label.configure(image=min_label.image)  # Configurar la imagen de la etiqueta
            min_label.place(x=x, y=y)  # Colocar la mina en la posición generada

    # Llamamos a la función para colocar las minas
    place_mines()

    # Función para cerrar la ventana del minijuego
    def close_minigame(event):
        minigame_window.destroy()

    # Cerramos la ventana del minijuego al hacer clic
    minigame_window.bind("<Button-1>", close_minigame)

    # Mantenemos la ventana abierta hasta que se cierre
    minigame_window.mainloop()


# Configuración del jugador
player = Player()
all_sprites_list = pygame.sprite.Group(player)
initialize_player_position(player, azules)
start_position = player.rect.topleft
pos_player_final = random.choice(verdes)

# Configuración del temporizador
start_time = random.randint(90, 120) * 1000  # convertir a milisegundos
start_ticks = pygame.time.get_ticks()

# Calculando el camino óptimo
optimal_path = find_best_path(start_position, amarillos, verdes, start_time)

run = True
clock = pygame.time.Clock()
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill(White)
    draw_background(background_image)
    all_sprites_list.draw(screen)

    # Calculando el tiempo restante
    elapsed_ticks = pygame.time.get_ticks() - start_ticks
    time_left = max(0, start_time - elapsed_ticks)

    # Mostrando el temporizador en cuenta regresiva en la esquina superior izquierda
    formatted_time = format_time(time_left)
    draw_text(screen, f"Tiempo: {formatted_time}", fuente, Black, (10, 10))

    # Mover el jugador a lo largo del camino óptimo
    if optimal_path:
        next_pos = optimal_path.pop(0)
        player.rect.topleft = next_pos

    pygame.display.update()

    if time_left <= 0:
        # Fin del juego por tiempo agotado
        screen.fill(White)
        game_over_image = pygame.image.load("game_over.png")
        screen.blit(pygame.transform.scale(game_over_image, (378, 464)), (0, 0))
        pygame.display.update()
        time.sleep(3)
        run = False

    # Manejo de colisiones con los puntos amarillos
    collision_point = check_collision(player.rect, amarillos)
    if collision_point:
        amarillos.remove(collision_point)  # Eliminar el punto amarillo colisionado para evitar múltiples colisiones
        run_minigame()  # Ejecutar el minijuego cuando se colisiona con un punto amarillo

    if player.rect.topleft == pos_player_final:
        run = False

    clock.tick(60)  # Control de la velocidad del juego

pygame.quit()
