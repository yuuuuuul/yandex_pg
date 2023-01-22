import pygame
import random
import sys
import os


pygame.init()
size = WIDTH, HEIGHT = 750, 750
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
fps = 50
stars_group = pygame.sprite.Group()
door_group = pygame.sprite.Group()
got_group = pygame.sprite.Group()
not_got_group = pygame.sprite.Group()
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
keys = {'eby':'ebu.jpg',
        'selfi':'selfi.jpg',
        'glasses':'glasses.jpg',
        'sun':'sun.jpg',
        'shit':'shit.jpg',
        'ly':'ly.jpg',
        'nice':'nice.jpg',
        'kaif':'kaif.jpg',
        'find':'find.jpg',
        'lang':'lang.jpg'}


def start_screen():
    intro_text = ["Правила игры:",
                  "Вам нужно собрать все пары.",
                  "При открытии новой картинки старая закрывается",
                  "Для того, чтобы начать, нажмите любую кнопку.",
                  "Кликайте на дверь мышкой, чтобы открыть её",
                  "Удачи!"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('red'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
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

class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [load_image("star.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(stars_group)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()


        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos
        GRAVITY = 0
        # гравитация будет одинаковой (значение константы)
        self.gravity = GRAVITY

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(0, 0, 750, 750):
            self.kill()

def create_particles(position):
    # количество создаваемых частиц
    particle_count = 20
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))

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
            #pygame.time.delay(1000)
            x, y = args[0].pos
            x_m = (x - 40) // 150
            y_m = (y - 10) // 150
            self.image = pygame.transform.scale(load_image(keys[desk[y_m][x_m]]), (150, 100))
            if len(now_opened) == 0:
                now_opened.add(self)
                now_opened_coords.add((y_m, x_m))
            if len(now_opened) != 0:
                noc2 = tuple(now_opened_coords)
                no2 = tuple(now_opened)
                if keys[desk[y_m][x_m]] == keys[desk[noc2[0][0]][noc2[0][1]]] and (y_m, x_m) != (noc2[0][0], noc2[0][1]):
                    got_group.add(no2[0])
                    got_group.add(self)
                    got_group.add(no2[0])
                    got_group.add(self)
                else:
                    now_opened.clear()
                    now_opened_coords.clear()
                    now_opened.add(self)

                    now_opened_coords.add((y_m, x_m))
            for i in door_group:
                if i not in got_group and i != self:
                    i.image = pygame.transform.scale(load_image("door.png"), (150, 100))




def main():
    start_screen()
    pygame.init()
    running = True
    board = Board()
    for i in range(20):
        Door(door_group)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            door_group.update(event)
        board.render(screen)
        screen.fill((255, 255, 255))
        door_group.draw(screen)
        got_group.draw(screen)
        #stars_group.draw(screen)

        #create_particles((300, 300))
        stars_group.update()
        clock.tick(fps)
        pygame.display.flip()

if __name__ == "__main__":
    main()
    stars_group.draw(screen)
    create_particles((300, 300))
    stars_group.update()