import random
import time
import sys
import pygame
import os
import math
import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk, ImageFilter
from heapq import heappop, heappush
from threading import Thread

# Colores
Black, White, Green, Red, Blue, Yellow = (0, 0, 0), (255, 255, 255), (0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0)

# Posiciones de los círculos
azules = [(100, 100),(60, 200), (149, 276), (110, 350), (80, 230), (70, 400)]
verdes = [(200, 200),(230, 148), (270, 300), (300, 55), (300, 360), (220, 100)]
rojos = [ (150, 110),(160, 90),(165, 130),(165, 140),(170, 150),(120, 155),(80, 160),
         (180, 175),(190, 180),(195, 185),(80, 200),(190, 160),(175, 360),(170, 350),
         (145, 440),(140, 430),(150, 420),(155, 410),(160, 370),(140, 450), (150, 150),
         (180, 300),(190, 290),(200, 280),(170, 270),(144, 161),(173, 298),(165, 209),
         (125, 60),(110, 355),(178, 223),(141, 118),(154, 383),(198, 169),(108, 278),
         (193, 255),(186, 66),(112, 344),(161, 129), (173, 294),(176, 109),(129, 253),
         (136, 323),(144, 163),(148, 67),(153, 320),(148, 348),(140, 143),(199, 156),
         (196, 385),(194, 299),(160, 240),(106, 238),(169, 189),(130, 214),(113, 318),
         (118, 108),(179, 149),(195, 199),(132, 210),(131, 116),(107, 251),(135, 391),
         (115, 219),(152, 382),(184, 140),(163, 328),(149, 114),(113, 316),(147, 252),
         (179, 383),(142, 392),(108, 232),(177, 207),(192, 262),(140, 346),(152, 53),
         (149, 167),(178, 312), (110, 310),(186, 235),(197, 277),(143, 157),(122, 176),
         (184, 141),(176, 322),(144, 71),(171, 392),(198, 257),(172, 139),(169, 339),
         (116, 330),(174, 379),(198, 96),(149, 253),(116, 246),(157, 149),(160, 330),
         (191, 369),(178, 134),(188, 308),(191, 75),(152, 289),(166, 173), (136, 375),
         (166, 131), (123, 105), (103, 264), (115, 264), (135, 141), (182, 261), (199, 68),
         (114, 68),(163, 351), (158, 113), (185, 317), (189, 117), (122, 100), (198, 335),
         (118, 188), (116, 183), (180, 375),(140, 204), (115, 297), (151, 177), (166, 312),
         (124, 150), (126, 354), (191, 117), (153, 134), (151, 388),(125, 349), (193, 320),
         (174, 188), (170, 117), (199, 47), (174, 241), (143, 384), (172, 321), (192, 325),
         (196, 61), (112, 300), (164, 121), (117, 314), (131, 141), (170, 96), (115, 107),
         (126, 174), (130, 198), (138, 296), (128, 393), (146, 204), (144, 330), (142, 130),
         (147, 186), (118, 380), (185, 392), (159, 66), (105, 239), (102, 150), (166, 101),
         (174, 109), (147, 66), (193, 56), (143, 396), (115, 175), (110, 382), (141, 328),
         (197, 250), (120, 365), (102, 81), (172, 201), (199, 384), (186, 254), (130, 359),
         (166, 263), (130, 234), (163, 110), (168, 157), (118, 221), (165, 308), (186, 269),
         (136, 45), (152, 302), (186, 68), (199, 210), (196, 373), (181, 92), (142, 259), (160, 177),
         (174, 320), (169, 388), (123, 168), (132, 192), (137, 401), (194, 296), (163, 240), (130, 254),
         (104, 151), (169, 310), (197, 74), (142, 387), (186, 226), (139, 351), (119, 123), (152, 236),
         (166, 325), (133, 136), (199, 122), (110, 142), (154, 389), (170, 149), (142, 50), (113, 263),
         (199, 123), (178, 374), (164, 182), (113, 277), (135, 174), (181, 228), (175, 77), (120, 326),
         (191, 190), (182, 395), (160, 301), (129, 250), (114, 220), (118, 301), (195, 322), (138, 303),
         (153, 97), (176, 52), (163, 126), (195, 130), (147, 201), (186, 318), (102, 174), (169, 331),
         (179, 107), (126, 300), (106, 47), (190, 141), (158, 70), (148, 309), (187, 209), (151, 390),
         (101, 258), (144, 247), (133, 252), (103, 118), (137, 266), (142, 314), (109, 263), (155, 85),
         (193, 285), (166, 216), (173, 333), (143, 158), (159, 296), (130, 238), (196, 280), (172, 134),
         (116, 285), (174, 371), (104, 122), (187, 225), (188, 374), (190, 377), (158, 229), (147, 260),
         (169, 319), (196, 259), (185, 88), (198, 187), (159, 383), (170, 339), (150, 188), (162, 314),
         (148, 395), (105, 200), (171, 260), (124, 277), (138, 172), (115, 312), (118, 99), (179, 314),
         (195, 197), (132, 215), (131, 119), (107, 247), (135, 394), (114, 225), (152, 375), (184, 132),
         (163, 325), (148, 109), (113, 322), (147, 257), (179, 391), (142, 394), (108, 228), (177, 204),
         (192, 261), (140, 349), (152, 55), (149, 161), (178, 315), (110, 312), (186, 238), (197, 272),
         (143, 152), (122, 178), (184, 145), (176, 326), (144, 69), (171, 390), (198, 254), (172, 137),
         (169, 341), (116, 332), (174, 377), (198, 94), (149, 251), (116, 244), (157, 147), (160, 324),
         (191, 363), (178, 132), (188, 301), (191, 71), (152, 287), (169, 353), (179, 61), (126, 254),
         (110, 307), (173, 371), (199, 102), (171, 224), (126, 324), (149, 174), (189, 393), (184, 57),
         (112, 212), (132, 249), (102, 143), (176, 166), (173, 310), (103, 178), (137, 330), (142, 268),
         (109, 266), (155, 99), (145, 105), (131, 302), (147, 90), (174, 52), (182, 217), (190, 234),
         (158, 208), (181, 315), (107, 165), (139, 387), (158, 267), (175, 334), (177, 164), (116, 233),
         (119, 395),(121, 328), (175, 313), (134, 159), (122, 258),(111, 293)]

amarillos = [(110, 170),(120, 190),(140, 180),(160, 210),(180, 230),(200, 220),(240, 250),
             (200, 260),(160, 280),(180, 290),(170, 300),(190, 310),(200, 320),(210, 330),
             (220, 340),(200, 350),(270, 340),(240, 360),(320, 370),(340, 380),(250, 390),
             (260, 400),(270, 410),(220, 130),(250, 70),(270, 80),(240, 100),(220, 50),
             (230, 120),(250, 450),(150, 110),(160, 90),(165, 130),(165, 140),(170, 150),
             (120, 155),(80, 160),(180, 175),(190, 180),(195, 185),(80, 200),(190, 160),
             (175, 360),(170, 350),(145, 440),(140, 430),(150, 420),(155, 410),(160, 370),
             (140, 450),(150, 150),(180, 300),(190, 290),(200, 280),(170, 270),(144, 161),
             (173, 298),(165, 209),(125, 60),(110, 355),(178, 223),(141, 118),(154, 383),
             (198, 169),(108, 278),(193, 255),(186, 66),(112, 344),(161, 129), (173, 294),
             (176, 109),(129, 253),(136, 323),(144, 163),(148, 67),(153, 320),(148, 348),
             (140, 143),(199, 156),(196, 385),(194, 299),(160, 240),(106, 238),(169, 189),
             (130, 214),(113, 318),(118, 108),(179, 149),(195, 199),(132, 210),(131, 116),
             (107, 251),(135, 391),(115, 219),(152, 382),(184, 140),(163, 328),(149, 114),
             (113, 316),(147, 252),(179, 383),(142, 392),(108, 232),(177, 207),(192, 262),
             (140, 346),(152, 53),(149, 167),(178, 312), (110, 310),(186, 235),(197, 277),
             (143, 157),(122, 176),(184, 141),(176, 322),(144, 71),(171, 392),(198, 257),
             (172, 139),(169, 339),(116, 330),(174, 379),(198, 96),(149, 253),(116, 246),
             (157, 149),(160, 330),(191, 369),(178, 134),(188, 308),(191, 75),(152, 289),
             (166, 173), (136, 375),(166, 131), (123, 105), (103, 264), (115, 264), (135, 141),
             (182, 261), (199, 68),(114, 68),(163, 351), (158, 113), (185, 317), (189, 117),
             (122, 100), (198, 335),(118, 188), (116, 183), (180, 375),(140, 204), (115, 297),
             (151, 177), (166, 312),(124, 150), (126, 354), (191, 117), (153, 134), (151, 388),
             (125, 349), (193, 320),(174, 188), (170, 117), (199, 47), (174, 241), (143, 384),
             (172, 321), (192, 325),(196, 61), (112, 300), (164, 121), (117, 314), (131, 141),
             (170, 96), (115, 107),(126, 174), (130, 198), (138, 296), (128, 393), (146, 204),
             (144, 330), (142, 130),(147, 186), (118, 380), (185, 392), (159, 66), (105, 239),
             (102, 150), (166, 101),(174, 109), (147, 66), (193, 56), (143, 396), (115, 175),
             (110, 382), (141, 328),(197, 250), (120, 365), (102, 81), (172, 201), (199, 384),
             (186, 254), (130, 359),(166, 263), (130, 234), (163, 110), (168, 157), (118, 221),
             (165, 308), (186, 269),(136, 45), (152, 302), (186, 68), (199, 210),(196, 373),
             (181, 92), (142, 259), (160, 177),(174, 320), (169, 388), (123, 168),(132, 192),
             (137, 401), (194, 296), (163, 240), (130, 254),(104, 151), (169, 310),(197, 74),
             (142, 387), (186, 226), (139, 351), (119, 123), (152, 236),(166, 325),(133, 136),
             (199, 122), (110, 142), (154, 389), (170, 149), (142, 50), (113, 263),(199, 123),
             (178, 374), (164, 182), (113, 277), (135, 174), (181, 228), (175, 77), (120, 326),
             (191, 190), (182, 395), (160, 301), (129, 250), (114, 220), (118, 301), (195, 322),
             (138, 303),(153, 97), (176, 52), (163, 126), (195, 130), (147, 201), (186, 318), (102, 174),
             (169, 331),(179, 107), (126, 300), (106, 47), (190, 141), (158, 70), (148, 309),
             (187, 209),(151, 390),(101, 258), (144, 247), (133, 252), (103, 118), (137, 266), (142, 314),
             (109, 263), (155, 85),(193, 285), (166, 216), (173, 333), (143, 158), (159, 296), (130, 238),
             (196, 280), (172, 134),(116, 285), (174, 371), (104, 122), (187, 225), (188, 374),
             (190, 377), (158, 229), (147, 260),(169, 319), (196, 259), (185, 88), (198, 187),(159, 383),
             (170, 339), (150, 188), (162, 314),(148, 395), (105, 200), (171, 260), (124, 277),
             (138, 172), (115, 312), (118, 99), (179, 314),(195, 197), (132, 215), (131, 119), (107, 247),
             (135, 394), (114, 225), (152, 375), (184, 132),(163, 325), (148, 109), (113, 322), (147, 257),
             (179, 391), (142, 394), (108, 228), (177, 204),(192, 261), (140, 349), (152, 55), (149, 161),
             (178, 315), (110, 312), (186, 238), (197, 272),(143, 152), (122, 178), (184, 145), (176, 326),
             (144, 69), (171, 390), (198, 254), (172, 137),(169, 341), (116, 332), (174, 377), (198, 94),
             (149, 251), (116, 244), (157, 147), (160, 324),(190, 362), (177, 132), (187, 300), (190, 70),
             (151, 286), (168, 352), (178, 60), (125, 255),(111, 306), (172, 370), (198, 103), (172, 225),
             (125, 325), (148, 173), (188, 392), (185, 56),(111, 211), (131, 248), (101, 142), (175, 165),
             (172, 311), (102, 177), (136, 331), (141, 267),(108, 265), (154, 98), (144, 104), (130, 301), 
             (148, 92), (173, 51), (181, 218), (191, 233),(159, 209), (180, 314), (108, 166), (140, 388),
             (159, 268), (174, 335), (176, 165), (115, 232),(118, 394),(120, 327), (176, 312), (135, 158),
             (123, 259),(110, 294)]

# Inicialización de Pygame
pygame.init()
screen = pygame.display.set_mode((378, 464))
pygame.display.set_caption("Treasure Hunt")
fuente = pygame.font.SysFont("Arial", 20)
background_image = pygame.image.load("fondo.jpeg")
coin_image = pygame.image.load("moneda.png")

# Monedas del jugador
monedas = 0

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

def show_coins(screen, coin_image, coin_count, font, position):
    screen.blit(pygame.transform.scale(coin_image, (25, 25)), position)
    draw_text(screen, f"{coin_count}", font, Black, (position[0] + 30, position[1]))

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
    global monedas  # Acceder a la variable global de monedas
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
            global monedas
            monedas += 50
            minigame_window.destroy()  # Cerrar la ventana del minijuego

        # Verificar colisión con las minas
        for mine_x, mine_y in mines_positions:
            if (hook_x < mine_x + 20 and hook_x + 40 > mine_x and
                hook_y < mine_y + 20 and hook_y + 40 > mine_y):
                if monedas > 0:
                    monedas = max(monedas - 25, 0)  # Asegurar que las monedas no bajen de 0
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

    # Mantenemos la ventana abierta hasta que se cierre
    minigame_window.mainloop()

# Función para mostrar la pantalla de fin del juego
def show_game_over_screen(screen, monedas):
    game_over_image = pygame.image.load("game_over.png")
    screen.blit(pygame.transform.scale(game_over_image, (378, 464)), (0, 0))
    pygame.display.update()
    
    # Mostrar la cantidad de monedas y un botón de reinicio en una nueva ventana de Tkinter
    root = tk.Tk()
    root.title("Game Over")
    root.geometry("300x200")

    # Mostrar la cantidad de monedas
    label = tk.Label(root, text=f"Monedas obtenidas: {monedas}", font=("Arial", 16))
    label.pack(pady=20)

    # Botón para reiniciar el juego
    def restart_game():
        root.destroy()
        main()  # Llamar a la función principal para reiniciar el juego

    restart_button = tk.Button(root, text="Reiniciar", font=("Arial", 14), command=restart_game)
    restart_button.pack(pady=20)

    root.mainloop()

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
animation_steps = 350  # Número de pasos para la animación entre puntos
current_step = 0
current_segment = 0

# Bandera para controlar el estado del minijuego
is_minigame_running = False

def interpolate(start_pos, end_pos, step, total_steps):
    x = start_pos[0] + (end_pos[0] - start_pos[0]) * step / total_steps
    y = start_pos[1] + (end_pos[1] - start_pos[1]) * step / total_steps
    return (x, y)

def run_minigame_in_thread():
    global is_minigame_running
    is_minigame_running = True
    thread = Thread(target=run_minigame)
    thread.start()
    thread.join()
    is_minigame_running = False

def main():
    global monedas, run, current_step, current_segment, is_minigame_running, start_ticks
    monedas = 0
    run = True
    current_step = 0
    current_segment = 0
    is_minigame_running = False
    start_ticks = pygame.time.get_ticks()
    player.rect.topleft = start_position
    initialize_player_position(player, azules)

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

        # Mostrando la cantidad de monedas en la esquina superior derecha
        show_coins(screen, coin_image, monedas, fuente, (300, 10))

        # Mover el jugador a lo largo del camino óptimo con animación
        if not is_minigame_running and current_segment < len(optimal_path) - 1:
            start_pos = optimal_path[current_segment]
            end_pos = optimal_path[current_segment + 1]
            player.rect.topleft = interpolate(start_pos, end_pos, current_step, animation_steps)
            current_step += 1

            # Manejo de colisiones con los puntos amarillos
            collision_point = check_collision(player.rect, amarillos)
            if collision_point:
                amarillos.remove(collision_point)  # Eliminar el punto amarillo colisionado para evitar múltiples colisiones
                run_minigame_in_thread()  # Ejecutar el minijuego en un hilo separado

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
            show_game_over_screen(screen, monedas)
            run = False

        if player.rect.topleft == pos_player_final:
            show_game_over_screen(screen, monedas)
            run = False

        clock.tick(60)  # Control de la velocidad del juego

    pygame.quit()

if __name__ == "__main__":
    main()
