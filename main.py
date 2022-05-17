import os
import sys
import pygame
import sqlite3


def load_image(name, colorkey=None):
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
    return image


con = sqlite3.connect("db/buttons.sqlite")
cur = con.cursor()
cur.execute(f"UPDATE buttons SET True_or_False = ''")
con.commit()
pygame.init()
screen_size = (990, 600)
screen = pygame.display.set_mode(screen_size)
FPS = 15
clock = pygame.time.Clock()
level = 1


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    game = True
    screen.fill(pygame.Color(37, 9, 54))
    while game:
        pygame.display.update()
        clock.tick(60)
        try:
            new_level = open('levels/' + str(level) + '.txt', "r", encoding="UTF-8")
        except FileNotFoundError:
            print('игра закончена')
            break
        y = 20
        player_image = load_image(str(level) + '.png')
        car_rect = player_image.get_rect(center=(450, 300))
        screen.blit(player_image, car_rect)
        for line in new_level:
            if 'кнопка' not in line:
                font = pygame.font.Font(None, 25)
                message = font.render(line[0:-1], True, pygame.Color(255, 255, 255))
                screen.blit(message, (10, y))
                y += 20
            else:
                button = Button(480, 60)
                line = line.split(' ')
                if 'кнопка1' == line[0]:
                    del line[0]
                    button.draw(10, 520, ' '.join(line)[0:-1], next_level_true, 25, 15, 20)
                if 'кнопка2' == line[0]:
                    del line[0]
                    button.draw(500, 520, ' '.join(line)[0:-1], next_level_false, 25, 15, 20)
                if 'кнопка3' == line[0]:
                    button = Button(280, 60)
                    del line[0]
                    button.draw(700, 520, ' '.join(line)[0:-1], next_level, 25, 15, 20)
        con = sqlite3.connect("db/buttons.sqlite")
        cur = con.cursor()
        result = cur.execute("SELECT * FROM buttons WHERE True_or_False = 'False'").fetchall()
        if len(result) > 2:
            print('ты умер')
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass
        pygame.display.flip()
        clock.tick(FPS)


def next_level():
    global level
    level += 1


def next_level_true():
    global level
    screen.fill(pygame.Color(37, 9, 54))
    con = sqlite3.connect("db/buttons.sqlite")
    cur = con.cursor()
    cur.execute(f"UPDATE buttons SET True_or_False = 'True' WHERE id = {level}")
    con.commit()
    level += 1


def next_level_false():
    global level
    con = sqlite3.connect("db/buttons.sqlite")
    cur = con.cursor()
    cur.execute(f"UPDATE buttons SET True_or_False = 'False' WHERE id = {level}")
    con.commit()
    level += 1
    screen.fill(pygame.Color(37, 9, 54))


'''button.draw(280, 320, '  картон ', None, 35, 15, 100)
player_image = load_image('test.png')
    car_rect = player_image.get_rect(center=(450, 300))
    screen.blit(player_image, car_rect)
    button = Button(400, 60)
'''

class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_color = (1, 61, 117)
        self.active_color = (0, 76, 163)
        self.border_color = (0, 28, 130)

    def draw(self, x, y, message, action, size, text_offset_x, text_offset_y):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            if click[0] == 1 and action is not None:
                action()
            pygame.draw.rect(screen, self.border_color, (x, y, self.width, self.height))
            pygame.draw.rect(screen, self.active_color, (x + 5, y + 5, self.width - 10, self.height - 10))

        else:
            pygame.draw.rect(screen, self.border_color, (x, y, self.width, self.height))
            pygame.draw.rect(screen, self.inactive_color, (x + 5, y + 5, self.width - 10, self.height - 10))

        font = pygame.font.Font(None, size)
        message = font.render(message, True, pygame.Color(255, 255, 255))
        screen.blit(message, (x + text_offset_x, y + text_offset_y))


start_screen()
pygame.quit()
