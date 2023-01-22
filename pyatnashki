import random
import pygame
import sys
import os


pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
FPS = 50
DEFAULT_IMAGE_SIZE = (50, 50)
scheme = [[1, 2, 3],
          [4, 5, 6],
          [7, 8, 0]]
size_f = 60
x = width // 2 - size_f * 1.5 - 5
y = height // 2 - size_f * 1.5 - 5


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
    while i != 50:
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


def load_image(name, img_size, colorkey=None):
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
    '1': load_image('1.jpg', (60, 60)),
    '2': load_image('2.jpg', (60, 60)),
    '3': load_image('3.jpg', (60, 60)),
    '4': load_image('4.jpg', (60, 60)),
    '5': load_image('5.jpg', (60, 60)),
    '6': load_image('6.jpg', (60, 60)),
    '7': load_image('7.jpg', (60, 60)),
    '8': load_image('8.jpg', (60, 60)),
    '0': load_image('0.jpg', (60, 60))
}
tile_width = tile_height = 50


def print_text(text):
    font = pygame.font.Font(None, 30)
    text_coord = 80
    for line in text:
        string_rendered = font.render(line, 1, pygame.Color('brown'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.right = 100
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


def start_screen():
    fon = pygame.transform.scale(load_image('rules.jpg', (500, 500)), (500, 500))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


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


if __name__ == '__main__':
    picked = False
    fon1 = pygame.transform.scale(load_image('fon_pt.jpg', (500, 500)), (500, 500))
    start_screen()
    print_text('Восьмнашки')
    running = True
    bt_x = width // 2 - 52.5
    bt_y = 80
    button = load_image('button_mix.bmp', None)
    is_on = False
    over = False
    bow = pygame.mixer.Sound("data/bow.mp3")
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                if bt_x <= event.pos[0] <= bt_x + 100 and bt_y <= event.pos[1] <= bt_y + 37:
                    scheme = mix(scheme)
                    is_on = True
                else:
                    if is_on:
                        scheme = move(scheme, event.pos, x, y, size_f)
                        generate(scheme, x, y, size_f)
        fon1 = pygame.transform.scale(load_image('fon_pt.jpg', (500, 500)), (500, 500))
        screen.blit(fon1, (0, 0))
        if not over:
            if is_on and scheme == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]:
                screen.blit(load_image('doge.jpg', (190, 190)), (x, y))
                bow.play(loops=0)
                over = True
        if not over:
            generate(scheme, x, y, size_f)
        if over:
            screen.blit(load_image('doge.jpg', (190, 190)), (x, y))
        screen.blit(button, (bt_x, bt_y))
        pygame.display.flip()
    clock.tick(FPS)
    terminate()
