import pygame
import copy
import sys
import os


pygame.init()
hero_group = pygame.sprite.Group()
size = WIDTH, HEIGHT = 750, 750
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
fps = 7
a = True


def start_screen():
    intro_text = ["Правила игры:",
                  "Вам нужно добраться до красной клетки, не",
                  "задев зеленую жизнь",
                  "Для того, чтобы начать, нажмите любую кнопку",
                  "и затем пробел, когда появится поле.",
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
                terminate()
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
    image = pygame.transform.scale(image, (25, 25))
    #return image
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

def load_level(name):
    with open(name, 'r') as f:
        level_map = [[int(x) for x in line.split()] for line in f]
    return level_map

def print_text(message, x, y, font_color=(255, 0, 0), font_type="data/pobeda-bold1.ttf", font_size = 50):
    font_type = pygame.font.Font(font_type, font_size)
    text_coord = 50
    for text in message:
        string = font_type.render(text, True, font_color)
        intro_rect = string.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string, intro_rect)

class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = 30
        self.left = self.top = 0
        self.height = 30
        self.cell_size = 25
        global board
        board = load_level("data/level_one")
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
class Life(Board):
    def __init__(self, width, height):
        super().__init__(width, height)


    def next_moove(self):
        a = False
        cnt = 0
        for i in range(self.height):
            for j in range(self.width):
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
                        if cnt == 3 and self.board[i][j] == 0:
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
                        if cnt == 3 and self.board[i][j] == 0:
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
                        elif self.board[i][j] == 0 and cnt == 3:
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
                        if cnt == 3 and self.board[i][j] == 0:
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
                        if cnt == 3 and self.board[i][j] == 0:
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
                        elif self.board[i][j] == 0 and cnt == 3:
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
                    elif self.board[i][j] == 0 and cnt == 3:
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
                    elif self.board[i][j] == 0 and cnt == 3:
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
                    elif self.board[i][j] == 0 and cnt == 3:
                        self.board2[i][j] = 1
                    else:
                        self.board2[i][j] = 0
                    a = False
                cnt = 0
                self.board2[-1][-1] = 2
        board = copy.deepcopy(self.board2)


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
                    else:
                        pygame.draw.rect(screen, (255, 255, 255),
                                         (self.left + j * self.cell_size, self.top + i * self.cell_size, self.cell_size,
                                          self.cell_size), 0)
                    pygame.draw.rect(screen, (0, 0, 0),
                                     (self.left + j * self.cell_size, self.top + i * self.cell_size, self.cell_size,
                                      self.cell_size), 1)
        self.board = copy.deepcopy(self.board2)
        print(self.board2 == board)

    def on_click(self, cell):
        super().on_click(cell)
        self.board2 = self.board

cell_size = 25
hero_image = load_image("creature.png")

class Hero(pygame.sprite.Sprite, Life):
    def __init__(self):
        super().__init__(hero_group)
        self.image = hero_image
        self.rect = self.image.get_rect().move(0, 0)

    def move(self, key):
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
            print_text(text, x, y)
            for event in pygame.event.get():
                key = pygame.key.get_pressed()
                if event.type == pygame.QUIT or key[pygame.K_RETURN]:
                    paused = False
                    sys.exit()
                elif key[pygame.K_a]:
                    a = False
                    self.kill()
                    main()
            pygame.display.update()

    def check(self):
        if board[self.rect.y // cell_size][self.rect.x // cell_size] == 1:
            for i in board:
                print(i)
            print()
            self.pause(["Упс! Попробуйте еще!", "Enter - выход", "A - начать заново"], 100, 100)
        elif self.rect.x // cell_size == 29 and self.rect.y // cell_size == 29:
            self.pause(["Победа!", "Нажмите Enter для продолжения"], 100, 100)

def main():
    b = Life(30, 30)
    pygame.Surface(size)
    running = True
    hero = Hero()
    flag = False
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
                else:
                    hero.move(key)

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
    main()