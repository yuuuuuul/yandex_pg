import random
import pygame
from memo import start_memo
import sys
import os
from pygame import mixer

size = width, height = 750, 750
screen = pygame.display.set_mode(size)
scheme = [[1, 2, 3],
          [4, 5, 6],
          [7, 8, 0]]
size_f = 90
x = width // 2 - size_f * 1.5 - 5
y = height // 2 - size_f * 1.5 - 5
clock = pygame.time.Clock()
FPS = 50


def generate(scheme, x, y, size_f):
    x_copy = float(str(x))
    for i in scheme:
        for j in i:
            if j != 0:
                screen.blit(tile_images[str(j)], (x, y))
            x += size_f + 5
        y += size_f + 5
        x = x_copy


def mix(scheme):
    i = 0
    while i != 5:
        moves = []
        if 0 not in scheme[2]:
            moves.append('down')
        if 0 not in scheme[0]:
            moves.append('up')
        if scheme[0][0] != 0 and scheme[1][0] != 0 and scheme[2][0] != 0:
            moves.append('left')
        if scheme[0][2] != 0 and scheme[1][2] != 0 and scheme[2][2] != 0:
            moves.append('right')
        move = random.choice(moves)
        if move == 'down':
            if 0 in scheme[0]:
                ind = scheme[0].index(0)
                scheme[0][ind] = scheme[1][ind]
                scheme[1][ind] = 0
            else:
                ind = scheme[1].index(0)
                scheme[1][ind] = scheme[2][ind]
                scheme[2][ind] = 0
        elif move == 'up':
            if 0 in scheme[1]:
                ind = scheme[1].index(0)
                scheme[1][ind] = scheme[0][ind]
                scheme[0][ind] = 0
            else:
                ind = scheme[2].index(0)
                scheme[2][ind] = scheme[1][ind]
                scheme[1][ind] = 0
        elif move == 'left':
            for x in range(3):
                if 0 in scheme[x]:
                    ind = scheme[x].index(0)
                    scheme[x][ind] = scheme[x][ind - 1]
                    scheme[x][ind - 1] = 0
                    break
        elif move == 'right':
            for x in range(3):
                if 0 in scheme[x]:
                    ind = scheme[x].index(0)
                    scheme[x][ind] = scheme[x][ind + 1]
                    scheme[x][ind + 1] = 0
                    break
        i += 1
    return scheme


def load_image_w_size(name, img_size, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
        if img_size is not None:
            image = pygame.transform.scale(image, img_size)
    return image


def terminate():
    pygame.quit()
    sys.exit()


tile_images = {
    '1': load_image_w_size('1.jpg', (90, 90)),
    '2': load_image_w_size('2.jpg', (90, 90)),
    '3': load_image_w_size('3.jpg', (90, 90)),
    '4': load_image_w_size('4.jpg', (90, 90)),
    '5': load_image_w_size('5.jpg', (90, 90)),
    '6': load_image_w_size('6.jpg', (90, 90)),
    '7': load_image_w_size('7.jpg', (90, 90)),
    '8': load_image_w_size('8.jpg', (90, 90)),
    '0': load_image_w_size('0.jpg', (90, 90))
}
tile_width = tile_height = 90

def move(scheme, pos, x, y, size_f):
    x_sch = -1
    y_sch = -1
    if x <= pos[0] <= x + size_f:
        x_sch = 0
    elif x + size_f + 5 <= pos[0] <= x + size_f * 2 + 5:
        x_sch = 1
    elif x + size_f * 2 + 5 * 2 <= pos[0] <= x + size_f * 3 + 5 * 2:
        x_sch = 2
    if y <= pos[1] <= y + size_f:
        y_sch = 0
    elif y + size_f + 5 <= pos[1] <= y + size_f * 2 + 5:
        y_sch = 1
    elif y + size_f * 2 + 5 * 2 <= pos[1] <= y + size_f * 3 + 5 * 2:
        y_sch = 2
    if x_sch == -1 or y_sch == -1:
        return scheme
    moves = []
    if y_sch - 1 != -1:
        moves.append('up')
    if y_sch + 1 != 3:
        moves.append('down')
    if x_sch - 1 != -1:
        moves.append('left')
    if x_sch + 1 != 3:
        moves.append('right')
    for move in moves:
        if move == 'up':
            if scheme[y_sch - 1][x_sch] == 0:
                scheme[y_sch - 1][x_sch] = scheme[y_sch][x_sch]
                scheme[y_sch][x_sch] = 0
                return scheme
        elif move == 'down':
            if scheme[y_sch + 1][x_sch] == 0:
                scheme[y_sch + 1][x_sch] = scheme[y_sch][x_sch]
                scheme[y_sch][x_sch] = 0
                return scheme
        elif move == 'left':
            if scheme[y_sch][x_sch - 1] == 0:
                scheme[y_sch][x_sch - 1] = scheme[y_sch][x_sch]
                scheme[y_sch][x_sch] = 0
                return scheme
        elif move == 'right':
            if scheme[y_sch][x_sch + 1] == 0:
                scheme[y_sch][x_sch + 1] = scheme[y_sch][x_sch]
                scheme[y_sch][x_sch] = 0
                return scheme
    return scheme


def start_pyatnashki(scheme):
    picked = False
    fon1 = pygame.transform.scale(load_image_w_size('fon_for_games.jpg', (750, 750)), (750, 750))
    running = True
    bt_x = width // 2 - 52.5
    bt_y = 80
    button = load_image_w_size('button_mix.bmp', None)
    is_on = False
    over = False
    pygame.mixer.init(44100, -16, 2, 2048)
    bow = pygame.mixer.Sound("data/bow.mp3")
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == 32:  # ПРОБЕЛ
                    start_memo()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if bt_x <= event.pos[0] <= bt_x + 100 and bt_y <= event.pos[1] <= bt_y + 37:
                    scheme = mix(scheme)
                    is_on = True
                else:
                    if is_on:
                        scheme = move(scheme, event.pos, x, y, size_f)
                        generate(scheme, x, y, size_f)
        fon1 = pygame.transform.scale(load_image_w_size('fon_for_games.jpg', (750, 700)), (750, 750))
        screen.blit(fon1, (0, 0))
        if not over:
            if is_on and scheme == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]:
                screen.blit(load_image_w_size('doge.jpg', (280, 280)), (x, y))
                bow.play(loops=0)
                over = True
        if not over:
            generate(scheme, x, y, size_f)
        screen.blit(button, (bt_x, bt_y))
        pygame.display.flip()
    clock.tick(FPS)
    terminate()

if __name__ == '__main__':
    start_pyatnashki(scheme)
