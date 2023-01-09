import pygame
import copy
import sys
import os


pygame.init()
size = WIDTH, HEIGHT = 750, 750
screen = pygame.display.set_mode(size)
winner = None
group_one = pygame.sprite.Group()
group_two = pygame.sprite.Group()
group_three = pygame.sprite.Group()
camel_group = pygame.sprite.Group()
digits_group = pygame.sprite.Group()
cloud_group = pygame.sprite.Group()
all_stones = [group_one, group_two, group_three]
DIGITS = ['one.png', 'two.png', 'three.png']


def next_programm_moove():
    k1 = 10
    k2 = 10
    k3 = 10
    b = 0
    n = 0
    num = 0
    summ = 0
    if True:
        summ = k1 ^ k2 ^ k3
        if (k1 != 0 and k2 != 0 and k3 != 0):
            if k1 == k2 and k1 != k3:
                n = k3
                k3 = 0
                num = 3
            elif k1 == k3 and k2 != k1:
                n = k2
                num = 2
                k2 = 0
            elif k2 == k3 and k1 != k2:
                n = k1
                num = 1
                k1 = 0
            elif summ != 0:
                if k1 ^ k2 <= k3:
                    b = k3
                    k3 = k1 ^ k2
                    n = b - k3
                    num = 3
                elif k2 ^ k3 <= k1:
                    b = k1
                    k1 = k2 ^ k3
                    n = b - k1
                    num = 1
                elif k1 ^ k3 <= k2:
                    b = k2
                    k2 = k1 ^ k3
                    n = b - k2
                    num = 2
                else:
                    b = k1 - (summ - k1)
                    k1 = summ - k1
                    n = b
                    num = 1
            elif summ == 0:
                n = k1
                num = 1
                k1 -= n
        elif k1 != 0 and k2 != 0 and k3 == 0:
            if k2 == k1:
                k1 -= k2
                n = k2
                num = 1
            elif max(k1, k2) == k2:
                n = k2 - k1
                num = 2
                k2 = k1
            else:
                n = k1 - k2
                num = 1
                k1 = k2
        elif k1 != 0 and k2 == 0 and k3 != 0:
            if k1 == k3:
                k1 -= k3
                n = k3
                num = 1
            elif max(k1, k3) == k3:
                n = k3 - k1
                num = 3
                k3 = k1
            else:
                n = k1 - k3
                num = 1
                k1 = k3
        elif k1 == 0 and k2 != 0 and k3 != 0:
            if k2 == k3:
                k2 -= k3
                n = k3
                num = 2
            elif max(k2, k3) == k2:
                n = k2 - k3
                num = 2
                k2 = k3
            else:
                n = k3 - k2
                num = 3
                k3 = k2
        elif k1 == 0 and k2 == 0 and k3 != 0:
            n = k3
            k3 = 0
            num = 3
        elif k1 == 0 and k2 != 0 and k3 == 0:
            n = k2
            k2 = 0
            num = 2
        elif k1 != 0 and k2 == 0 and k3 == 0:
            n = k1
            k1 = 0
            num = 1
    if k1 == 0 and k2 == 0 and k3 == 0:
        winner = 'Computer'
    if 2 <= n <= 4:
        s = 'камня'
    elif n == 1:
        s = 'камень'
    else:
        s = 'камней'
    string = f'Я взял {n} {s} из {num} кучи'
    show_text(string, 24, x=520, y=530, font_color=(255, 255, 255), font_type="data/pobeda-bold1.ttf")
    rend(n, num)
    pygame.display.update()

def how_many_stones(number):
    show_text('Нажмите на кнопку с цифрой, сколько хотите взять', 24)
    count = len(all_stones[number - 1])
    print('here')
    for event in pygame.event.get():
        key = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:
            print('a')
            if event.key == 49:
                print('1')
                rend(1, number)
            if event.key == pygame.K_2:
                print('2')
                if count < 2:
                    show_text('слишком много', 24)
                    how_many_stones()
                else:
                    rend(2, number)
            if event.key == pygame.K_3:
                if count < 3:
                    show_text('слишком много', 24)
                    how_many_stones()
                else:
                    rend(3, number)
            if event.key == pygame.K_4:
                if count < 4:
                    show_text('слишком много', 24)
                    how_many_stones()
                else:
                    rend(4, number)
            if event.key == pygame.K_5:
                if count < 5:
                    show_text('слишком много', 24)
                    how_many_stones()
                else:
                    rend(5, number)
            if event.key == pygame.K_6:
                if count < 6:
                    show_text('слишком много', 24)
                    how_many_stones()
                else:
                    rend(6, number)
            if event.key == pygame.K_7:
                if count < 7:
                    show_text('слишком много', 24)
                    how_many_stones()
                else:
                    rend(7, number)
            if event.key == pygame.K_8:
                if count < 8:
                    show_text('слишком много', 24)
                    how_many_stones()
                else:
                    rend(8, number)
            if event.key == pygame.K_9:
                if count < 9:
                    show_text('слишком много', 24)
                    how_many_stones()
                else:
                    rend(9, number)

digit_coords = []
def next_user_moove():
    w = 150
    #print(group_three)
    pygame.draw.ellipse(screen, (255, 255, 255), (100, 100, 350, 200))
    show_text('Нажмите A, чтобы сделать ход', 24)
    #print(group_one, group_two, group_three)
    for event in pygame.event.get():
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            show_text('Нажмите на выбранную цифру', 24)
            for i in all_stones:
                if len(i) > 0:
                    digit = pygame.sprite.Sprite()
                    digit.image = pygame.transform.scale(load_image(DIGITS[all_stones.index(i)]), (50, 50))
                    digit.rect = digit.image.get_rect()
                    digit.rect.x = w
                    digit.rect.y = 300
                    digit_coords.append((digit.rect.x, digit.rect.y))
                    digits_group.add(digit)
                w += 150
                if all_stones.index(i) == 2:
                    break
            break
        digits_group.draw(screen)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            for i in digit_coords:
                if i[0] <= mx <= i[0] + 50 and i[1] <= my <= i[1] + 50:
                    number = digit_coords.index(i)
                    how_many_stones(number)
                    break


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    image = pygame.transform.scale(image, (500, 500))
    #return image
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

def set_fon():
    fon = pygame.transform.scale(load_image("fon_nim3.png"), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))


class Stones(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)

    def sprites_place(self, w, h, j):
        self.image = pygame.transform.scale(load_image("stone_for_nim3.png"), (40, 40))
        self.rect = self.image.get_rect()
        width = w
        height = h * j
        self.rect.x = width
        self.rect.y = 750 - height
        return self

class Camel(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.transform.scale(load_image("camel_for_nim3.png"), (250, 200))
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = 550

def show_text(message, font_size, x=150, y=190, font_color=(255, 0, 0), font_type="data/pobeda-bold1.ttf"):
    font_type = pygame.font.Font(font_type, font_size)
    text1 = font_type.render(message, True, font_color)
    screen.blit(text1, (x, y))
    pygame.draw.ellipse(screen, (255, 255, 255), (100, 100, 350, 200))

def rend(n, num):
    cnt = 0
    #print(n, num)
    group = all_stones[num - 1]
    length = len(group)
    for elem in group:
        if len(group) == length - n:
            break
        elem.kill()
            #print(group)
            #cnt += 1
    #print(len(group_three))
            #print('schetchik', cnt)
            #print('dlina', len(group))


    camel_group.draw(screen)
    group_one.draw(screen)
    group_two.draw(screen)
    group_three.draw(screen)
    pygame.display.update()


def main():
    count_of_turns = 0
    w = 150
    for i in all_stones:
        for j in range(9):
            i.add(Stones.sprites_place(pygame.sprite.Sprite(), w, 40, 10 - j))
        w += 150
    Camel(camel_group)
    while True:
        set_fon()
        pygame.draw.ellipse(screen, (255, 255, 255), (100, 100, 350, 200))
        for event in pygame.event.get():
            key = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == 32: #ПРОБЕЛ
                    while True:
                        next_programm_moove()
                        next_user_moove()
        group_one.draw(screen)
        group_two.draw(screen)
        group_three.draw(screen)
        camel_group.draw(screen)
        pygame.display.flip()




if __name__ == '__main__':
    main()