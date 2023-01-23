import pygame
import copy
import sys
import os
from stones import load_image_w_size_stones, print_text_stones, change_color, pre_stones, stones_rules, ending, create_map
from stones import generate_level, what_to_do, moving, print_cards, check_what_card, check_card, start_stones

pygame.init()
hero_group = pygame.sprite.Group()
size = WIDTH, HEIGHT = 750, 750
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
fps = 7
a = True

def photo_screen(picture):
    fon = pygame.transform.scale(load_image(picture), (WIDTH, HEIGHT))
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

def start_screen():
    intro_text = ["Правила игры:",
                  "Вам нужно добраться до красной клетки, не",
                  "задев зеленую жизнь",
                  "Для того, чтобы начать, нажмите любую кнопку",
                  "и затем пробел, когда появится поле.",
                  "Удачи!"]

    fon = pygame.transform.scale(load_image('fon_for_games.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
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
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

def load_level(name):
    with open(name, 'r') as f:
        level_map = [[int(x) for x in line.split()] for line in f]
    return level_map

def print_text(message, font_color=(255, 0, 0), font_type="data/pobeda-bold1.ttf", font_size = 90):
    font_type = pygame.font.Font(font_type, font_size)
    text_coord = 50
    for text in message:
        string = font_type.render(text, True, font_color)
        intro_rect = string.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 20
        text_coord += intro_rect.height
        screen.blit(string, intro_rect)

class Board_life:
    # создание поля
    def __init__(self, width, height):
        self.width = 30
        self.left = self.top = 0
        self.height = 30
        self.cell_size = 25
        self.board = load_level("data/level_one")
        self.board2 = load_level("data/level_one")

    def get_click(self, mouse_pos):
        self.ans = []
        self.get_cell(mouse_pos)
        cell = self.ans
        if cell == []:
            cell = None
        self.on_click(cell)


    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        if self.left <= x <= self.left + self.width * self.cell_size and self.top <= y <= self.top + \
                self.cell_size * self.height:
            self.ans = (x - self.left) // self.cell_size + 1, (y - self.top) // self.cell_size + 1
        return self.ans

    def on_click(self, cell):
        if not (cell == None):
            x, y = cell
            x -= 1
            y -= 1
            self.board[y][x] = 1 - self.board[y][x]
class Life(Board_life):
    def __init__(self, width, height):
        super().__init__(width, height)


    def next_moove(self):
        a = False
        cnt = 0
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == 3:
                    self.board2[i][j] = 3
                else:
                    a = True
                    #ВЕРХНЯЯ ЛЕВАЯ КЛЕТКА
                    if i == 0: #or i == self.height - 1:
                        if j == 0:# or j == self.width - 1:
                            if self.board[i][j + 1] == 1:
                                cnt += 1
                            if self.board[i + 1][j] == 1:
                                cnt += 1
                            if self.board[i + 1][j + 1] == 1:
                                cnt += 1
                            if cnt == 3 and self.board[i][j] in [0, 4]:
                                self.board2[i][j] = 1
                            if cnt < 2:
                                self.board2[i][j] = 0
                            a = False
                        #ВЕРХНЯЯ ПРАВАЯ
                        elif j == self.width - 1 and a:
                            if self.board[i][j - 1] == 1:
                                cnt += 1
                            if self.board[i + 1][j] == 1:
                                cnt += 1
                            if self.board[i + 1][j - 1] == 1:
                                cnt += 1
                            if cnt == 3 and self.board[i][j] in [0, 4]:
                                self.board2[i][j] = 1
                            if cnt < 2:
                                self.board2[i][j] = 0
                            a = False
                        elif i == 0:
                            if self.board[i][j - 1] == 1:
                                cnt += 1
                            if self.board[i][j + 1] == 1:
                                cnt += 1
                            if self.board[i + 1][j - 1] == 1:
                                cnt += 1
                            if self.board[i + 1][j + 1] == 1:
                                cnt += 1
                            if self.board[i + 1][j] == 1:
                                cnt += 1
                            if (cnt == 3 or cnt == 2) and self.board[i][j] == 1:
                                self.board2[i][j] = 1
                            elif self.board[i][j] in [0, 4] and cnt == 3:
                                self.board2[i][j] = 1
                            else:
                                self.board2[i][j] = 0
                            a = False
                    #НИЖНЯЯ
                    elif i == self.height - 1 and a:
                        if j == 0:
                            #ЛЕВАЯ
                            if self.board[i - 1][j] == 1:
                                cnt += 1
                            if self.board[i - 1][j + 1] == 1:
                                cnt += 1
                            if self.board[i][j + 1] == 1:
                                cnt += 1
                            if cnt == 3 and self.board[i][j] in [0, 4]:
                                self.board2[i][j] = 1

                            if cnt < 2:
                                self.board2[i][j] = 0
                            a = False
                        #ПРАВАЯ
                        if j == self.width - 1 and a:
                            if self.board[i - 1][j] == 1:
                                cnt += 1
                            if self.board[i][j - 1] == 1:
                                cnt += 1
                            if self.board[i - 1][j - 1] == 1:
                                cnt += 1
                            if cnt == 3 and self.board[i][j] in [0, 4]:
                                self.board2[i][j] = 1
                            if cnt < 2:
                                self.board2[i][j] = 0
                            a = False
                        elif i == self.height - 1:
                            if self.board[i][j - 1] == 1:
                                cnt += 1
                            if self.board[i][j + 1] == 1:
                                cnt += 1
                            if self.board[i - 1][j - 1] == 1:
                                cnt += 1
                            if self.board[i - 1][j + 1] == 1:
                                cnt += 1
                            if self.board[i - 1][j] == 1:
                                cnt += 1
                            if (cnt == 3 or cnt == 2) and self.board[i][j] == 1:
                                self.board2[i][j] = 1
                            elif self.board[i][j] in [0, 4] and cnt == 3:
                                self.board2[i][j] = 1
                            else:
                                self.board2[i][j] = 0
                            a = False
                    elif j == 0 and a:
                        if self.board[i - 1][j] == 1:
                            cnt += 1
                        if self.board[i + 1][j] == 1:
                            cnt += 1
                        if self.board[i - 1][j + 1] == 1:
                            cnt += 1
                        if self.board[i + 1][j + 1] == 1:
                            cnt += 1
                        if self.board[i][j + 1] == 1:
                            cnt += 1
                        if (cnt == 3 or cnt == 2) and self.board[i][j] == 1:
                            self.board2[i][j] = 1
                        elif self.board[i][j] in [0, 4] and cnt == 3:
                            self.board2[i][j] = 1
                        else:
                            self.board2[i][j] = 0
                        a = False
                    if j == self.width - 1 and a:
                        if self.board[i - 1][j] == 1:
                            cnt += 1
                        if self.board[i + 1][j] == 1:
                            cnt += 1
                        if self.board[i - 1][j - 1] == 1:
                            cnt += 1
                        if self.board[i + 1][j - 1] == 1:
                            cnt += 1
                        if self.board[i][j - 1] == 1:
                            cnt += 1
                        if (cnt == 3 or cnt == 2) and self.board[i][j] == 1:
                            self.board2[i][j] = 1
                        elif self.board[i][j] in [0, 4] and cnt == 3:
                            self.board2[i][j] = 1
                        else:
                            self.board2[i][j] = 0
                        a = False
                    elif a:
                        if self.board[i][j - 1] == 1:
                            cnt += 1
                        if self.board[i][j + 1] == 1:
                            cnt += 1
                        if self.board[i - 1][j - 1] == 1:
                            cnt += 1
                        if self.board[i - 1][j + 1] == 1:
                            cnt += 1
                        if self.board[i - 1][j] == 1:
                            cnt += 1
                        if self.board[i + 1][j - 1] == 1:
                            cnt += 1
                        if self.board[i + 1][j + 1] == 1:
                            cnt += 1
                        if self.board[i + 1][j] == 1:
                            cnt += 1
                        if (cnt == 3 or cnt == 2) and self.board[i][j] == 1:
                            self.board2[i][j] = 1
                        elif self.board[i][j] in [0, 4] and cnt == 3:
                            self.board2[i][j] = 1
                        else:
                            self.board2[i][j] = 0
                        a = False
                    cnt = 0
                    self.board2[-1][-1] = 2


    def render(self):
        for i in range(self.height):
            for j in range(self.width):
                if i == self.height - 1 and j == self.width - 1:
                    pygame.draw.rect(screen, (255, 0, 0),
                                     (self.left + j * self.cell_size, self.top + i * self.cell_size, self.cell_size,
                                      self.cell_size), 0)
                else:
                    if self.board2[i][j] == 1:
                        pygame.draw.rect(screen, (0, 255, 0), (self.left + j * self.cell_size, self.top + i * self.cell_size, self.cell_size,
                                          self.cell_size), 0)
                    elif self.board2[i][j] == 3:
                        pygame.draw.rect(screen, (252, 199, 0), (self.left + j * self.cell_size, self.top + i * self.cell_size, self.cell_size,
                                          self.cell_size), 0)
                    else:
                        pygame.draw.rect(screen, (255, 255, 255),
                                         (self.left + j * self.cell_size, self.top + i * self.cell_size, self.cell_size,
                                          self.cell_size), 0)
                    pygame.draw.rect(screen, (0, 0, 0),
                                     (self.left + j * self.cell_size, self.top + i * self.cell_size, self.cell_size,
                                      self.cell_size), 1)
        self.board = copy.deepcopy(self.board2)
        board = copy.deepcopy(self.board2)


    def on_click(self, cell):
        super().on_click(cell)
        self.board2 = self.board

    def check(self, x, y):
        if self.board2[x][y] == 1 or self.board2[x][y] == 3 or self.board2[x][y] == 4:
            Hero.pause(hero, ["Упс! Попробуйте еще!", "A - начать заново"], 100, 100)
        elif x == 29 and y == 29:
            Hero.pause(hero, ["Победа!", "Нажмите Enter", "для продолжения"], 100, 100)

b = Life(30, 30)
cell_size = 25
hero_image = load_image("creature.jpg")

class Hero(pygame.sprite.Sprite, Life):
    def __init__(self):
        super().__init__(hero_group)
        self.image = hero_image
        self.rect = self.image.get_rect().move(0, 0)

    def move(self, key, start):
        if start == 1:
            if key[pygame.K_RIGHT] and self.rect.x + cell_size < size[0]:
                self.rect.x += cell_size
            elif key[pygame.K_LEFT] and self.rect.x - cell_size >= 0:
                self.rect.x -= cell_size
            if key[pygame.K_UP] and self.rect.y - cell_size >= 0:
                self.rect.y -= cell_size
            if key[pygame.K_DOWN] and self.rect.y + cell_size < size[1]:
                self.rect.y += cell_size

    def pause(self, text, x, y):
        paused = True
        while paused:
            print_text(text)
            for event in pygame.event.get():
                key = pygame.key.get_pressed()
                if event.type == pygame.QUIT or key[pygame.K_RETURN]:
                    stones = create_map()
                    start_stones(stones)

                    # вызвать вместо прекамней камни, а в камни в начале старта вставить фотоскрин,
                    # который СКОПИРОВАТЬ, А НЕ ИМПОРТИРОВАТЬ!!!!!!
                elif key[pygame.K_a]:
                    a = False
                    hero_group.remove(self)
                    for i in hero_group:
                        i.kill()
                    b2 = Life(20, 20)
                    hero2 = Hero()
                    start_life(b2, hero2)

            pygame.display.update()

    def check(self):
        Life.check(b, self.rect.y // cell_size, self.rect.x // cell_size)

hero = Hero()

def init():
    b = Life(30, 30)
    hero = Hero()
def start_life(b, hero):
    photo_screen('prelife_pic.jpg')
    start_screen()
    if a is False:
        init()
    pygame.Surface(size)
    running = True
    flag = False
    start = 0
    while running:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            key = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN: #ЛЕВАЯ КНОПКА МЫШИ
                if event.button == 1:
                    b.get_click(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == 32: #ПРОБЕЛ
                    flag = not flag
                    if start == 0:
                        start = 1
                    else:
                        start = 0
                else:
                    hero.move(key, start)

        if flag:
            b.next_moove()
        b.render()
        hero_group.draw(screen)
        hero.check()
        clock.tick(fps)
        pygame.display.flip()

if __name__ == "__main__":
    if a:
        start_screen()
    start_life(b, hero)
