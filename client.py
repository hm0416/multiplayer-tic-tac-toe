import pygame
import os
import socket
import threading

# x_letter = pygame.image.load(os.path.join("imgs", 'x-tic.png'))
# o_letter = pygame.image.load(os.path.join("imgs", 'O-tic.png'))


def get_cells(x,y, grid):
    return grid[y][x]

def set_cells(val, x, y, grid):
    grid[y][x] = val

def get_mouse(x, y, player, grid, switch_player):
    if get_cells(x,y, grid) == 0:
        if player == 'X':
            set_cells('X', x, y, grid)
        elif player == 'O':
            set_cells('O', x, y, grid)
    else:
        switch_player = False

def create_thread(t):
    thread = threading.Thread(target = t)
    thread.daemon = True
    thread.start()

grid_lines = [  ((0,200), (600,200)),
                ((0,400), (600,400)),
                ((200,0), (200,600)),
                ((400,0), (400,600))
            ]

grid = [[0 for x in range(3)] for y in range(3)] #matrix

game_board = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Multiplayer Tic-Tac-Toe")
game_board.fill("white")

client_host = '127.0.0.1'
client_port = 65432

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((client_host, client_port))

def receive_data():
    while True:
        data = client_socket.recv(1024).decode() #length of string it can receive - 1KB
        print(data)

create_thread(receive_data)


is_game_running = True

player = 'X'

switch_player = True

while is_game_running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            is_game_running = False
        if e.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                screen_position = pygame.mouse.get_pos()
                x_cell, y_cell = screen_position[0] // 200, screen_position[1] //200
                # print(screen_position[0] // 200, screen_position[1] //200)
                get_mouse(x_cell, y_cell, player, grid, switch_player)
                data = '{}-{}'.format(x_cell, y_cell).encode()
                client_socket.send(data)
                if switch_player:
                    if player == 'X':
                        player = 'O'
                    else:
                        player = 'X'

                # for row in grid:
                #     print(row)

    game_board.fill((0,0,0))

    for line in grid_lines:
        pygame.draw.line(game_board, (200, 200, 200), line[0], line[1], 2)

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if get_cells(x, y, grid) == 'X':
                game_board.blit(pygame.image.load(os.path.join("imgs", 'x-tic.png')), (x*200, y*200))
            elif get_cells(x, y, grid) == 'O':
                game_board.blit(pygame.image.load(os.path.join("imgs", 'O-tic.png')), (x*200, y*200))


    pygame.display.flip()

