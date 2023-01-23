import random
import time

import pygame
import sys
import os

pygame.init()
size = width, height = 750, 750
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
FPS = 50
DEFAULT_IMAGE_SIZE = (50, 50)
size_stone = 90
x_for_st = width // 2 - size_stone * 1.5 - 5
y_for_st = height // 2 - size_stone * 1.5 - 50
t_size = 120, 160


def load_image_w_size_stones(name, img_size, colorkey=None):
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


def print_text_stones(cards_left, fine, new_game=False, won=False):
    intro_text = [f'    осталось собрать {cards_left} карт',
                  f'    штраф: {fine}']
    if new_game or fine == 6:
        intro_text = ['    упс, не вышло, попробуйте снова']
        fine = 0
    if won or cards_left == 0:
        intro_text = ['    ВЫ ВЫИГРАЛИ!!!']
    font = pygame.font.Font(None, 30)
    text_coord = 20
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.right = 100
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    return fine


tile_images = {
    'orange': load_image_w_size_stones('orange.png', (90, 90)),
    'green': load_image_w_size_stones('green.png', (90, 90)),
    'red': load_image_w_size_stones('red.png', (90, 90)),
    'black': load_image_w_size_stones('black.png', (90, 90)),
    'blue': load_image_w_size_stones('blue.png', (90, 90)),
    'white': load_image_w_size_stones('white.png', (90, 90)),
    'violet': load_image_w_size_stones('violet.png', (90, 90)),
    'yellow': load_image_w_size_stones('yellow.png', (90, 90))
}
tile_width = tile_height = 90


def change_color(color):
    if color == 'yellow':
        return 'black'
    if color == 'black':
        return 'yellow'
    if color == 'orange':
        return 'red'
    if color == 'red':
        return 'orange'
    if color == 'violet':
        return 'blue'
    if color == 'blue':
        return 'violet'
    if color == 'white':
        return 'green'
    if color == 'green':
        return 'white'


def terminate():
    pygame.quit()
    sys.exit()


def pre_stones():
    fon = pygame.transform.scale(load_image_w_size_stones('pre_kamni.png', (750, 750)), (750, 750))
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


def stones_rules():
    fon = pygame.transform.scale(load_image_w_size_stones('rules_stones.jpg', (750, 750)), (750, 750))
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


def ending():
    fon = pygame.transform.scale(load_image_w_size_stones('end_pic.jpg', (750, 750)), (750, 750))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                terminate()
        pygame.display.flip()
        clock.tick(FPS)



def create_map():
    stones = []
    stones.append(random.choice(['yellow', 'black']))
    for i in range(2):
        stones.append(random.choice(['orange', 'red']))
    for i in range(3):
        stones.append(random.choice(['violet', 'blue']))
        stones.append(random.choice(['white', 'green']))
    random.shuffle(stones)
    stones = [[stones[0], stones[1], stones[2]],
              [stones[3], stones[4], stones[5]],
              [stones[6], stones[7], stones[8]]]
    return stones


def generate_level(stones, x, y, size_f):
    x_copy = float(str(x))
    for i in stones:
        for j in i:
            if j != 0:
                screen.blit(tile_images[str(j)], (x, y))
            x += size_f + 5
        y += size_f + 5
        x = x_copy


def what_to_do(pos):
    x = pos[0]
    y = pos[1]
    if 235 <= x <= 515 and 190 <= y <= 470:
        return 'moving'
    if 750 - 20 - 120 <= x <= 750 - 20 and 20 <= y <= 20 + 80:
        return 'start_game'
    if 750 - 20 - 120 <= x <= 750 - 20 and 20 + 80 + 10 <= y <= 20 + 80 + 10 + 80:
        return 'turn_over'
    if 550 <= y <= 710:
        return 'cards'
    return 'moving'


def moving(x, y, pos, picked, stones, picked_stone, moving_allowed):
    x_st = -1
    y_st = -1
    if x <= pos[0] <= x + size_stone:
        x_st = 0
    elif x + size_stone + 5 <= pos[0] <= x + size_stone * 2 + 5:
        x_st = 1
    elif x + size_stone * 2 + 5 * 2 <= pos[0] <= x + size_stone * 3 + 5 * 2:
        x_st = 2
    if y <= pos[1] <= y + size_stone:
        y_st = 0
    elif y + size_stone + 5 <= pos[1] <= y + size_stone * 2 + 5:
        y_st = 1
    elif y + size_stone * 2 + 5 * 2 <= pos[1] <= y + size_stone * 3 + 5 * 2:
        y_st = 2
    if x_st != -1 and y_st != -1:
        if not picked:
            picked_stone = x_st, y_st
            picked = True
            return picked, stones, picked_stone, True
        else:
            if (x_st == picked_stone[0] and abs(y_st - picked_stone[1]) == 1) or \
                    (y_st == picked_stone[1] and abs(x_st - picked_stone[0]) == 1):
                stones[y_st][x_st], stones[picked_stone[1]][picked_stone[0]] = \
                    stones[picked_stone[1]][picked_stone[0]], stones[y_st][x_st]
                moving_allowed = False
                picked = False
                return picked, stones, picked_stone, False
            elif x_st == picked_stone[0] and y_st == picked_stone[1]:
                stones[y_st][x_st] = change_color(stones[y_st][x_st])
                picked = False
                moving_allowed = False
                return picked, stones, picked_stone, False
            picked = False
            return picked, stones, picked_stone, True
    else:
        picked = False
        return picked, stones, picked_stone, True


d = 'black'
w = 'white'
y = 'yellow'
b = 'blue'
g = 'green'
r = 'red'
v = 'violet'
o = 'orange'

tile_cards = {
    '1_1': [load_image_w_size_stones('1_1.jpg', t_size), 'two', v + v],
    '1_2': [load_image_w_size_stones('1_2.jpg', t_size), 'two', w + g],
    '1_3': [load_image_w_size_stones('1_3.jpg', t_size), 'two', w + o],
    '1_4': [load_image_w_size_stones('1_4.jpg', t_size), 'all',
            [[None, None, None], [None, o, None], [None, None, None]]],
    '1_5': [load_image_w_size_stones('1_5.jpg', t_size), 'all',
            [[None, None, None], [None, r, None], [None, None, None]]],
    '1_6': [load_image_w_size_stones('1_6.jpg', t_size), 'two', b + r],
    '1_7': [load_image_w_size_stones('1_7.jpg', t_size), 'two', o + g],
    '1_8': [load_image_w_size_stones('1_8.jpg', t_size), 'two', r + v],
    '1_9': [load_image_w_size_stones('1_9.jpg', t_size), 'two', g + g],
    '1_10': [load_image_w_size_stones('1_10.jpg', t_size), 'two', g+ w],
    '2_1': [load_image_w_size_stones('2_1.jpg', t_size), 'three', [None, None, y]],
    '2_2': [load_image_w_size_stones('2_2.jpg', t_size), 'two', o + o],
    '2_3': [load_image_w_size_stones('2_3.jpg', t_size), 'three', [d, None, None]],
    '2_4': [load_image_w_size_stones('2_4.jpg', t_size), 'three', [None, v, r]],
    '2_5': [load_image_w_size_stones('2_5.jpg', t_size), 'all',
            [[y, None, None], [None, None, None], [None, None, None]]],
    '2_6': [load_image_w_size_stones('2_6.jpg', t_size), 'all',
            [[None, None, w], [None, None, None], [w, None, None]]],
    '2_7': [load_image_w_size_stones('2_7.jpg', t_size), 'two', b + d],
    '2_8': [load_image_w_size_stones('2_8.jpg', t_size), 'three', [o, b, None]],
    '3_1': [load_image_w_size_stones('3_1.jpg', t_size), 'three', [w, w, w]],
    '3_2': [load_image_w_size_stones('3_2.jpg', t_size), 'three', [g, o, b]],
    '3_3': [load_image_w_size_stones('3_3.jpg', t_size), 'three', [r, None, r]],
    '3_4': [load_image_w_size_stones('3_4.jpg', t_size), 'all',
            [[b, None, b], [None, None, None], [None, b, None]]],
    '3_5': [load_image_w_size_stones('3_5.jpg', t_size), 'all',
            [[None, w, None], [None, None, None], [w, None, w]]],
    '5_1': [load_image_w_size_stones('5_1.jpg', t_size), 'all',
            [[d, None, None], [None, o, None], [None, None, o]]],
    '5_2': [load_image_w_size_stones('5_2.jpg', t_size), 'all',
            [[None, y, None], [None, None, None], [r, None, r]]],
    '5_3': [load_image_w_size_stones('5_3.jpg', t_size), 'all',
            [[None, w, None], [v, None, v], [None, d, None]]]
}


def print_cards(cards_in_game):
    x = 95
    y = 550
    for card in cards_in_game:
        screen.blit(tile_cards[card][0], (x, y))
        x += 140


def check_what_card(pos, cards_in_game):
    if 95 <= pos[0] <= 215 and len(cards_in_game) > 0:
        return cards_in_game[0]
    if 235 <= pos[0] <= 355 and len(cards_in_game) > 1:
        return cards_in_game[1]
    if 375 <= pos[0] <= 495 and len(cards_in_game) > 2:
        return cards_in_game[2]
    if 515 <= pos[0] <= 635 and len(cards_in_game) > 3:
        return cards_in_game[3]
    return None


def check_card(picked_card, stones):
    if tile_cards[picked_card][1] == 'two':
        for i in stones:
            a = ''.join(i)
            if tile_cards[picked_card][2] in a:
                return True
    elif tile_cards[picked_card][1] == 'three':
        kt = tile_cards[picked_card][2]
        for i in stones:
            j = []
            for k in i:
                j.append(k)
            for el in range(3):
                if kt[el] is None:
                    j[el] = None
            if j == kt:
                return True
    elif tile_cards[picked_card][1] == 'all':
        kt = tile_cards[picked_card][2]
        st = []
        for i in stones:
            j = []
            for k in i:
                j.append(k)
            ktt = kt[stones.index(i)]
            for el in range(3):
                if ktt[el] is None:
                    j[el] = None
            st.append(j)
        if st == kt:
            return True
    return False


def start_stones(stones):
    fine = 0
    cards_left = 16
    picked = False
    pre_stones()
    button_take = load_image_w_size_stones('take.bmp', None)
    button_start = load_image_w_size_stones('start_game.bmp', None)
    button_check = load_image_w_size_stones('proverit.bmp', None)
    button_give = load_image_w_size_stones('otdat.bmp', None)
    stones_rules()
    running = True
    picked_stone = None
    game_is_on = False
    fine = print_text_stones(cards_left, fine)
    opt_1 = ['1_1', '1_2', '1_3', '1_4', '1_5', '1_6', '1_7', '1_8', '1_9', '1_10']
    opt_2 = ['2_1', '2_2', '2_3', '2_4', '2_5', '2_6', '2_7', '2_8']
    opt_3 = ['3_1', '3_2', '3_3', '3_4', '3_5']
    opt_5 = ['5_1', '5_2', '5_3']
    random.shuffle(opt_1)
    random.shuffle(opt_2)
    random.shuffle(opt_3)
    random.shuffle(opt_5)
    is_turn = True
    cards_in_col = []
    cards_in_col += opt_1[:8] + opt_2[:4] + opt_3[:3] + opt_5[:1]
    random.shuffle(cards_in_col)
    solved = 0
    cards_in_game = []
    moving_allowed = False
    picked_card = None
    won = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                action = what_to_do(event.pos)
                if action == 'moving' and game_is_on and moving_allowed:
                    picked, stones, picked_stone, moving_allowed = moving(x_for_st, y_for_st, event.pos,
                                                                          picked, stones, picked_stone, moving_allowed)
                    if picked_stone:
                        pass
                elif action == 'start_game':
                    fine = 0
                    game_is_on = True
                    cards_in_col = []
                    cards_in_col += opt_1[:8] + opt_2[:4] + opt_3[:3] + opt_5[:1]
                    random.shuffle(cards_in_col)
                    if len(cards_in_col) >= 4:
                        cards_in_game = cards_in_col[:4]
                    else:
                        cards_in_game = cards_in_col[:]
                    for i in range(4):
                        cards_in_col.pop(0)
                    is_turn = True
                    solved = 0
                    cards_left = 16
                    won = False
                elif action == 'turn_over':
                    is_turn = False
                    if solved == 0:
                        fine += 1
                    solved = 0
                    moving_allowed = False
                    if len(cards_in_col) >= 4:
                        while len(cards_in_game) != 4:
                            cards_in_game.append(cards_in_col[0])
                            cards_in_col.pop(0)
                    else:
                        if len(cards_in_col) + len(cards_in_game) < 4:
                            for i in range(len(cards_in_game)):
                                cards_in_col.append(cards_in_game.pop(0))
                            for i in range(len(cards_in_col)):
                                cards_in_game.append(cards_in_col.pop(0))
                    picked_card = None
                elif action == 'cards' and game_is_on:
                    picked, stones, picked_stone, moving_allowed = moving(x_for_st, y_for_st, event.pos, picked,
                                                                          stones, picked_stone, moving_allowed)
                    picked_card = check_what_card(event.pos, cards_in_game)
                    if picked_card:
                        screen.blit(button_give, (750 / 2 - 150, 450))
                        screen.blit(button_check, (750 / 2 + 150, 450))
                if 750 - 150 <= event.pos[0] <= 750 - 150 + 120 and 750 - 300 <= event.pos[1] <= 750 - 300 + 80:
                    moving_allowed = True
                    cards_in_col.append(picked_card)
                    cards_in_game.remove(picked_card)
                    picked_card = None
                if 30 <= event.pos[0] <= 30 + 120 and 750 - 300 <= event.pos[1] <= 750 - 300 + 80:
                    if check_card(picked_card, stones):
                        cards_left -= 1
                        cards_in_game.remove(picked_card)
                        solved += 1
                        picked_card = None
                    else:
                        picked_card = None
                if 700 <= event.pos[0] <= 750 and 700 <= event.pos[1] <= 750:
                    won = True
        fon = pygame.transform.scale(load_image_w_size_stones('fon_st.jpg', (750, 750)), (750, 750))
        screen.blit(fon, (0, 0))
        if game_is_on:
            print_cards(cards_in_game)
        generate_level(stones, x_for_st, y_for_st, size_stone)
        if fine == 6:
            game_is_on = False
            print_text_stones(cards_left, fine, new_game=True)
        if picked:
            pygame.draw.rect(screen, 'brown', (x_for_st + (size_stone + 5) * picked_stone[0],
                                               y_for_st + (size_stone + 5) * picked_stone[1], size_stone, size_stone),
                             3)
        screen.blit(button_start, (750 - 20 - 120, 20))
        screen.blit(button_take, (750 - 20 - 120, 20 + 80 + 10))
        screen.blit(load_image_w_size_stones('pamyatka.png', 120, 160), (50, 275))
        print_text_stones(cards_left, fine)
        if picked_card:
            screen.blit(button_give, (750 - 150, 750 - 300))
            screen.blit(button_check, (30, 750 - 300))
            pygame.draw.rect(screen, 'brown', (x_for_st + (120 + 20) * (cards_in_game.index(picked_card) - 1),
                                               550, 120, 160), 3)
        if cards_left == 0:
            won = True
        if won:
            ending()
        pygame.display.flip()
    clock.tick(FPS)
    terminate()


if __name__ == '__main__':
    stones = create_map()
    start_stones(stones)
