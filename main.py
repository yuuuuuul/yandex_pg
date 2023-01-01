import pygame
import copy

class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = 30
        self.height = 30
        self.board = [[0] * width for i in range(height)]
        # значения по умолчанию
        self.left = 20
        self.top = 20
        self.cell_size = 30
        self.pal = {0: (0, 0, 0),
                    1: (255, 255, 255)}
        self.cnt = 0
        self.r = [1, 2]
    def render(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, (255, 255, 255),
                                (self.left + j * self.cell_size, self.top + i * self.cell_size, self.cell_size, self.cell_size), 1)
                if self.board[i][j] == 1:
                    pygame.draw.ellipse(screen, (255, 0, 0), (self.left + j * self.cell_size + 3,
                                        self.top + i * self.cell_size + 3, self.cell_size - 6, self.cell_size - 6), 2)
                if self.board[i][j] == 2:
                    pygame.draw.line(screen, (0, 0, 255),
                                    (self.left + j * self.cell_size + 3, self.top + i * self.cell_size + 3),
                                    (self.left + (j + 1) * self.cell_size - 3, self.top + (i + 1) * self.cell_size - 3), 2)
                    pygame.draw.line(screen, (0, 0, 255),
                                     (self.left + (j + 1) * self.cell_size - 3, self.top + i * self.cell_size + 3),
                                     (self.left + j * self.cell_size + 3, self.top + (i + 1) * self.cell_size - 3), 2)

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
        self.left = self.top = 15
        self.cell_size = 15
        self.board2 = [[0] * width for i in range(height)]

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


    def render(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.board2[i][j] == 1:
                    pygame.draw.rect(screen, (0, 255, 0), (self.left + j * self.cell_size, self.top + i * self.cell_size, self.cell_size,
                                      self.cell_size), 0)
                else:
                    pygame.draw.rect(screen, (0, 0, 0),
                                     (self.left + j * self.cell_size, self.top + i * self.cell_size, self.cell_size,
                                      self.cell_size), 0)
                pygame.draw.rect(screen, (255, 255, 255),
                                 (self.left + j * self.cell_size, self.top + i * self.cell_size, self.cell_size,
                                  self.cell_size), 1)
        self.board = copy.deepcopy(self.board2)


    def get_click(self, mouse_pos):
        super().get_click(mouse_pos)


    def get_cell(self, mouse_pos):
        super().get_cell(mouse_pos)

    def on_click(self, cell):
        super().on_click(cell)
        self.board2 = self.board



if __name__ == '__main__':
    size = 500, 500
    board = Life(30, 30)
    screen = pygame.display.set_mode(size)
    pygame.Surface(size)
    running = True
    fps = 2
    flag = False
    clock = pygame.time.Clock()
    while running:
        count = 0
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN: #ЛЕВАЯ КНОПКА МЫШИ
                if event.button == 1:
                    board.get_click(event.pos)
                elif event.button == 1:
                    flag = not flag
   #             board.next_moove()
            if event.type == pygame.KEYDOWN:
                if event.key == 32: #ПРОБЕЛ
                    flag = not flag
            if event.type == pygame.MOUSEWHEEL:
                fps += event.y * 2
        if flag:
            board.next_moove()
            clock.tick(fps) * 0.5
        screen.fill((0, 0, 0))
        board.render()
        pygame.display.flip()