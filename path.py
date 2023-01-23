from memo import load_image, Board_memo, Door, start_memo, start_screen
from life import start_screen, load_image, load_level, Board_life, Life, Hero, init, start_life, b, hero
from pyatnashki import generate, mix, start_pyatnashki, load_image_w_size, move, terminate
from stones import load_image_w_size_stones, print_text_stones, change_color, pre_stones, stones_rules, ending, create_map
from stones import generate_level, what_to_do, moving, print_cards, check_what_card, check_card, start_stones

import pygame
import sys
import random
import os


pygame.init()
size = WIDTH, HEIGHT = 750, 750
width, height = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
fps = 50
scheme = [[1, 2, 3],
          [4, 5, 6],
          [7, 8, 0]]
size_f = 60
x = width // 2 - size_f * 1.5 - 5
y = height // 2 - size_f * 1.5 - 5
door_group = pygame.sprite.Group()
got_group = pygame.sprite.Group()
now_opened = set()
now_opened_coords = set()
d1 = ['kaif', 'find', 'find', 'lang']
d2 = ['ly', 'shit', 'ebu', 'sun']
d3 = ['nice', 'selfi', 'kaif', 'lang']
d4 = ['glasses', 'shit', 'sun', 'nice']
d5 = ['selfi', 'ebu', 'ly', 'glasses']

random.shuffle(d1)
random.shuffle(d2)
random.shuffle(d3)
random.shuffle(d4)
random.shuffle(d5)

desk = [d1, d2, d3, d4, d5]
set_of_coords = set()
set_now_opened = []
set_check = set()
keys = {'ebu':'ebu.jpg',
        'selfi':'selfi.jpg',
        'glasses':'glasses.jpg',
        'sun':'sun.jpg',
        'shit':'shit.jpg',
        'ly':'ly.jpg',
        'nice':'nice.jpg',
        'kaif':'kaif.jpg',
        'find':'find.jpg',
        'lang':'lang.jpg'}


def load_image_path(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def photo_screen(picture):
    fon = pygame.transform.scale(load_image_path(picture), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(fps)


def main():
    photo_screen('greeting_pic.jpg')
    photo_screen('prepyat_pic.png')
    start_pyatnashki(scheme)
    #start_memo()
    #photo_screen('prelife_pic.jpg')
    #start_life(b, hero)
    #photo_screen('pre_kamni.jpg')
    #start_stones()




if __name__ == '__main__':
    main()



