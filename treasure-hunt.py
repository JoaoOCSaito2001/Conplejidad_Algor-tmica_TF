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
    pil_image = pil_image.resize((500, 600), resample=Image.Resampling.LANCZOS)  # Redimensionamos la imagen con antialiasing
    minigame_image = ImageTk.PhotoImage(pil_image)

    # Mostramos la imagen de fondo en la ventana de tkinter
    background_label = tk.Label(minigame_window, image=minigame_image)
    background_label.image = minigame_image  # Mantenemos una referencia para evitar que la imagen sea recolectada por el recolector de basura
    background_label.place(x=0, y=0)

    # Cargamos la imagen del anzuelo
    hook_image = Image.open("anzuelo.jpeg")
    hook_image = hook_image.resize((40, 40), Image.Resampling.LANCZOS)  # Ajustamos el tamaño según sea necesario
    hook_photo = ImageTk.PhotoImage(hook_image)

    # Variables para el anzuelo
    hook_x = 250
    hook_y = 50
    hook_speed = 2

    # Etiqueta para el anzuelo
    hook_label = tk.Label(minigame_window, image=hook_photo, bg='white')
    hook_label.image = hook_photo
    hook_label.place(x=hook_x, y=hook_y)

    # Cargamos la imagen del tesoro
    treasure_image = Image.open("tesoro.png")
    treasure_image = treasure_image.resize((40, 40), Image.Resampling.LANCZOS)  # Ajustamos el tamaño según sea necesario
    treasure_photo = ImageTk.PhotoImage(treasure_image)

    # Variables para el tesoro
    treasure_x = random.randint(20, 460)
    treasure_y = 560  # Cerca de la parte inferior de la ventana

    # Etiqueta para el tesoro
    treasure_label = tk.Label(minigame_window, image=treasure_photo, bg='white')
    treasure_label.image = treasure_photo
    treasure_label.place(x=treasure_x, y=treasure_y)

    # Lista para almacenar las posiciones de las minas
    mines_positions = []

    # Función para mover el anzuelo
    def move_hook(event):
        nonlocal hook_x
        if event.keysym == "Left":
            hook_x -= 10
        elif event.keysym == "Right":
            hook_x += 10
        hook_label.place(x=hook_x, y=hook_y)

    # Función para actualizar la posición del anzuelo
    def update_hook():
        nonlocal hook_y, after_id
        hook_y += hook_speed
        hook_label.place(x=hook_x, y=hook_y)
        
        # Verificar colisión con el tesoro
        if (hook_x < treasure_x + 40 and hook_x + 40 > treasure_x and
            hook_y < treasure_y + 40 and hook_y + 40 > treasure_y):
            minigame_window.destroy()  # Cerrar la ventana del minijuego

        # Verificar colisión con las minas
        for mine_x, mine_y in mines_positions:
            if (hook_x < mine_x + 20 and hook_x + 40 > mine_x and
                hook_y < mine_y + 20 and hook_y + 40 > mine_y):
                minigame_window.destroy()  # Cerrar la ventana del minijuego al colisionar con una mina
                return

        if hook_y < 600 - hook_image.height:
            after_id = minigame_window.after(50, update_hook)

    # Llamamos a la función para colocar las minas
    def place_mines():
        mines = 13
        min_image = Image.open("mina.jpeg")  # Cargar la imagen de la mina
        min_image = min_image.resize((20, 20), Image.Resampling.LANCZOS)  # Redimensionar la imagen de la mina según sea necesario

        for _ in range(mines):
            x = random.randint(20, 470)  # Posiciones aleatorias dentro del rango de la ventana
            y = random.randint(100, 500)  # Ajustado para evitar cortes
            mines_positions.append((x, y))  # Almacenar la posición de la mina
            min_label = tk.Label(minigame_window, image=ImageTk.PhotoImage(min_image))  # Etiqueta para la mina
            min_label.image = ImageTk.PhotoImage(min_image)  # Convertir la imagen de la mina a un formato compatible con tkinter
            min_label.configure(image=min_label.image)  # Configurar la imagen de la etiqueta
            min_label.place(x=x, y=y)  # Colocar la mina en la posición generada

    # Llamamos a la función para colocar las minas
    place_mines()

    # Vincular las teclas de dirección al movimiento del anzuelo
    minigame_window.bind("<Left>", move_hook)
    minigame_window.bind("<Right>", move_hook)

    # Iniciar la actualización del anzuelo
    after_id = minigame_window.after(50, update_hook)

    # Función para cerrar la ventana del minijuego
    def close_minigame(event):
        nonlocal after_id
        minigame_window.after_cancel(after_id)  # Cancelar el temporizador after
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

# Variable para la animación
animation_steps = 50  # Número de pasos para la animación entre puntos
current_step = 0
current_segment = 0

def interpolate(start_pos, end_pos, step, total_steps):
    x = start_pos[0] + (end_pos[0] - start_pos[0]) * step / total_steps
    y = start_pos[1] + (end_pos[1] - start_pos[1]) * step / total_steps
    return (x, y)

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

    # Mover el jugador a lo largo del camino óptimo con animación
    if current_segment < len(optimal_path) - 1:
        start_pos = optimal_path[current_segment]
        end_pos = optimal_path[current_segment + 1]
        player.rect.topleft = interpolate(start_pos, end_pos, current_step, animation_steps)
        current_step += 1
        if current_step >= animation_steps:
            current_step = 0
            current_segment += 1

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
