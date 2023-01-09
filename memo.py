import pygame
import copy
import sys
import os


pygame.init()
size = WIDTH, HEIGHT = 750, 750
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
door_group = pygame.sprite.Group()
got_group = pygame.sprite.Group()
not_got_group = pygame.sprite.Group()
now_opened = []
fps = 7
desk = [['пин', 'тигр', 'тигр', 'копатыч'],
      ['ежик', 'карыч', 'лосяш', 'крош'],
      ['нюша', 'совунья', 'пин', 'копатыч'],
      ['бараш', 'карыч', 'крош', 'нюша'],
      ['совунья', 'лосяш', 'ежик', 'бараш']]
set_of_coords = set()
set_now_opened = []
set_check = set()
keys = {'пин':'pin.png',
        'тигр':'tig.png',
        'копатыч':'kop.png',
        'ежик':'ezhik.png',
        'нюша':'nusha.png',
        'совунья':'sov.png',
        'крош':'krosh.png',
        'лосяш':'los.png',
        'бараш':'barash.png',
        'карыч':'kar.png'}
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

def maximize(x):
    return x + 30
class Board:
    def __init__(self):
        self.width = 4
        self.height = 5
        #self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 40
        self.top = 10
        self.cell_size = 150

    def render(self, screen):
        j = 0
        k = 0
        for i in door_group:
            if j % 4 == 0 and j != 0:
                j = 0
                k += 1
            i.rect.x = self.left + self.cell_size * j + 20
            i.rect.y = self.top + self.cell_size * k + 10
            j += 1
        door_group.draw(screen)

class Door(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("door.png"), (150, 100))

    def __init__(self, group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно !!!
        super().__init__(group)
        self.top = self.left = 10
        self.image = Door.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.cnt = 0
        self.now = ''
        self.m = 0

    def check(self, coords):
        if coords not in set_of_coords and len(set_of_coords) != 0:
            return 2
        else:
            set_of_coords.append(coords)
            return 1

    def m_max(self, z):
        if z == '+':
            self.m += 1
        else:
            self.m = 0
        return self.m

    def update(self, *args):
        j = 0
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            print(set_of_coords, 'before')
            #pygame.time.delay(1000)
            x, y = args[0].pos
            x_m = (x - 40) // 150
            y_m = (y - 10) // 150
            print(set_of_coords, 'middle')
            self.image = pygame.transform.scale(load_image(keys[desk[y_m][x_m]]), (150, 100))
            if self.m == 0:
                now_opened.append(self)
                set_of_coords.add((y_m, x_m))
            print(set_of_coords, 'main')
            if len(set_of_coords) == 2:
                list_of_coords = list(set_of_coords)
                if keys[desk[list_of_coords[0][0]][list_of_coords[0][1]]] == keys[desk[list_of_coords[1][0]][list_of_coords[1][1]]]:
                    print('yes')
                    for i in set(now_opened):
                        got_group.add(i)
                    self.m_max('+')

                else:
                    print('not')
                    self.m_max('-')
                    for i in door_group:
                        if i not in got_group:
                            i.image = pygame.transform.scale(load_image('door.png'), (150, 100))
                print(got_group)
                set_of_coords.clear()
                now_opened.clear()

















def main():
    pygame.init()
    running = True

    board = Board()
    for i in range(20):
        Door(door_group)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        board.render(screen)
        screen.fill((255, 255, 255))
        door_group.draw(screen)
        got_group.draw(screen)
        door_group.update(event)
        pygame.display.flip()
        #clock.tick(fps)

if __name__ == "__main__":
    main()