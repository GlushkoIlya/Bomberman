import pygame
import random
import sys
from PyQt5.QtWidgets import QDesktopWidget, QApplication

# 1 - персонаж
# 0 - пустое поле
# -1 - железная стена
# 3 - враг
# [4, 0] - деревянная стена
# [4, 5] - +1 бомба (за стеной)
# [4, 6] - +1 диапазон взрыва (за стеной)
# [4, 7] - выход (за стеной) 
# 7 - выход
# 5 - +1 бомба
# 6 - +1 диапозон взрыва 


def ok(x, a, b, board,
       bomb=[]):  # направление, координаты, список точек куда можно, поле
    if not bomb:
        bomb = [bomb]
    if x == 1:  # right
        if board[a[0] + 1][a[1]] in b and [a[0] + 1, a[1]] not in bomb:
            return [a[0] + 1, a[1], x]
        else:
            return a + [x]
    elif x == 2:  # left
        if board[a[0] - 1][a[1]] in b and [a[0] - 1, a[1]] not in bomb:
            return [a[0] - 1, a[1], x]
        else:
            return a + [x]
    elif x == 4:  # down
        if board[a[0]][a[1] + 1] in b and [a[0], a[1] + 1] not in bomb:
            return [a[0], a[1] + 1, x]
        else:
            return a + [x]
    elif x == 3:  # up
        if board[a[0]][a[1] - 1] in b and [a[0], a[1] - 1] not in bomb:
            return [a[0], a[1] - 1, x]
        else:
            return a + [x]
    else:
        return a + [x]


class Map:
    # создание поля
    def __init__(self, width, height, bonus1=0, bonus2=0, life=3, time=0, top=10, left=10, cell_size=30, fpsall=30):  # высота, ширина
        self.boomarea = []
        self.points = 0
        self.time = time
        self.dethtime = 240
        self.life = life
        self.bonus1 = bonus1  # +1 бомба
        self.bonus2 = bonus2  # +1 к диапазону взрыва
        self.width = width
        self.height = height
        self.fps = 0
        self.board = [[0] * width for _ in range(height)]  # [x][y]
        self.gamecon = True
        for i in range(height):
            self.board[i][0] = -1
            self.board[i][-1] = -1
        for i in range(width):
            self.board[0][i] = -1
            self.board[-1][i] = -1
        x = 0
        for i in range(1, height - 1):
            if x == 0:
                pass
            else:
                y = 0
                for j in range(1, width - 1):
                    if y == 0:
                        pass
                    else:
                        self.board[i][j] = -1
                    y = (y + 1) % 2
            x = (x + 1) % 2
        f = [[1, 1], [1, 2], [2, 1]]
        for i in range(height * width // 5):  # стены для разбивания
            x = random.choice(range(height))
            y = random.choice(range(width))
            while self.board[x][y] != 0 or [x, y] in f:
                x = random.choice(range(height))
                y = random.choice(range(width))
            # print(x, y, f)
            if i == 0:
                self.board[x][y] = [4, 5]  # +1 бомба
            elif i == 2:
                self.board[x][y] = [4, 6]  # +1 диапазон взрыва
            elif i == 3:
                self.board[x][y] = [4, 7]  # выход
            else:
                self.board[x][y] = [4, 0]  # деревянная стена

        self.enemy = []
        for i in range(height * width // 19):  # враги
            x = random.choice(range(height))
            y = random.choice(range(width))
            while self.board[x][y] != 0 or [x, y] in f:
                x = random.choice(range(height))
                y = random.choice(range(width))
            self.board[x][y] = 3
            self.enemy.append([x, y, 0])
        self.enemycopy = self.enemy.copy()
        # print(len(self.enemy), height * width // 19)

        self.board[1][1] = 1  # персонаж
        self.pers = [1, 1, 4, 0]  # координаты персонажа

        self.bomb = False
        self.boom = False

        # значения по умолчанию
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.fpsall = fpsall

    # настройка внешнего вида
    def set_view(self, left, top, cell_size, fps=30):
        self.fpsall = fps
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        self.time += 1
        self.fps = (self.fps + 1) % self.fpsall
        a = self.board
        if self.board[self.pers[0]][self.pers[1]] != 1:
            self.pers[2] = 0
            self.pers[3] = self.cell_size
        if self.fps == 0:
            for i in range(len(self.enemy)):
                if self.enemy[i] and type(self.enemy[i]) != int:
                    g = [1, 2, 3, 4]
                    vll = False
                    for _ in range(4):
                        x = random.choice(g)
                        g = g[:x - 1] + g[x:]
                        if ok(x, [self.enemy[i][0], self.enemy[i][1]], [0, 1],
                              self.board) != \
                                [self.enemy[i][0], self.enemy[i][1]] + [x]:
                            vll = True
                            k = ok(x, [self.enemy[i][0], self.enemy[i][1]], [0, 1],
                              self.board)
                            for j in range(i):
                                if type(self.enemy[j]) == list:
                                    kk = ok(self.enemy[j][2], [self.enemy[j][0], self.enemy[j][1]], [0, 1], self.board)
                                    if [kk[0], kk[1]] == [k[0], k[1]]:
                                        vll = False
                                        # print(k, kk)
                            if vll:
                                self.enemy[i][2] = x
                                break
                    if not vll:
                        self.enemy[i][2] = 0
        if self.fps == self.fpsall - 1:
            for i in range(len(self.enemy)):
                if self.enemy[i] and type(self.enemy[i]) != int:
                    k = ok(self.enemy[i][2],
                           [self.enemy[i][0], self.enemy[i][1]], [0, 1],
                           self.board)
                    self.board[self.enemy[i][0]][self.enemy[i][1]] = 0
                    self.board[k[0]][k[1]] = 3
                    self.enemy[i] = k
        if self.boom:
            for b in range(len(self.boom)):
                if type(self.boom[b]) == int:
                    if self.fps == self.boom[b]:
                        w = [[self.bomb[b][0] + 1, self.bomb[b][1]],
                             [self.bomb[b][0] - 1, self.bomb[b][1]],
                             [self.bomb[b][0], self.bomb[b][1] + 1],
                             [self.bomb[b][0], self.bomb[b][1] - 1],
                             self.bomb[b]]
                        if self.bonus2 != 0:
                            for i in range(1, self.bonus2 + 2):
                                a = [[self.bomb[b][0] + i, self.bomb[b][1]],
                                     [self.bomb[b][0] - i, self.bomb[b][1]],
                                     [self.bomb[b][0], self.bomb[b][1] + i],
                                     [self.bomb[b][0], self.bomb[b][1] - i]]
                                w += a
                        g = [True, True, True, True]
                        for i in w:
                            if False not in g:
                                if self.board[i[0]][i[1]] == [4, 5]:
                                    self.boomarea.append([i[0], i[1], 0])
                                    self.board[i[0]][i[1]] = 5
                                elif self.board[i[0]][i[1]] == [4, 6]:
                                    self.boomarea.append([i[0], i[1], 0])
                                    self.board[i[0]][i[1]] = 6
                                elif self.board[i[0]][i[1]] == [4, 7]:
                                    self.boomarea.append([i[0], i[1], 0])
                                    self.board[i[0]][i[1]] = 7
                                elif self.board[i[0]][i[1]] not in [-1, 5, 6,
                                                                    7]:
                                    self.board[i[0]][i[1]] = 0
                                    self.boomarea.append([i[0], i[1], 0])
                                    for e in range(len(self.enemy)):
                                        if self.enemy[e] and type(self.enemy[e]) != int and self.enemy[e][
                                            0] == i[
                                            0] and self.enemy[e][1] == i[1]:
                                            self.enemy[e] = (self.fpsall + (self.fps - 1)) % self.fpsall
                                            # print(self.enemy[e])
                                            self.board[i[0]][i[1]] = 3
                                            self.points += 100
                                else:
                                    if i[0] != self.bomb[b][0]:
                                        if i[0] > self.bomb[b][0]:
                                            g[0] = False
                                        else:
                                            g[1] = False
                                    else:
                                        if i[1] > self.bomb[b][1]:
                                            g[2] = False
                                        else:
                                            g[3] = False
                            else:
                                if (i[0] > self.bomb[b][0] and g[0]) or (
                                        i[0] < self.bomb[b][0] and g[1]) or (
                                        i[1] > self.bomb[b][1] and g[2]) or (
                                        i[1] < self.bomb[b][1] and g[
                                    3]) or i == self.bomb[b]:
                                    if self.board[i[0]][i[1]] == [4, 5]:
                                        self.boomarea.append([i[0], i[1], 0])
                                        self.board[i[0]][i[1]] = 5
                                    elif self.board[i[0]][i[1]] == [4, 6]:
                                        self.boomarea.append([i[0], i[1], 0])
                                        self.board[i[0]][i[1]] = 6
                                    elif self.board[i[0]][i[1]] == [4, 7]:
                                        self.boomarea.append([i[0], i[1], 0])
                                        self.board[i[0]][i[1]] = 7
                                    elif self.board[i[0]][i[1]] not in [-1, 5,
                                                                        6, 7]:
                                        self.boomarea.append([i[0], i[1], 0])
                                        self.board[i[0]][i[1]] = 0
                                        for e in range(len(self.enemy)):
                                            if self.enemy[e] and type(self.enemy[e]) != int and self.enemy[e][
                                                0] == i[
                                                0] and self.enemy[e][1] == i[
                                                1]:
                                                self.enemy[e] = (self.fpsall + (self.fps - 1)) % self.fpsall
                                                # print(self.enemy[e])
                                                self.board[i[0]][i[1]] = 3
                                                self.points += 100
                                    else:
                                        if i[0] != self.bomb[b][0]:
                                            if i[0] > self.bomb[b][0]:
                                                g[0] = False
                                            else:
                                                g[1] = False
                                        else:
                                            if i[1] > self.bomb[b][1]:
                                                g[2] = False
                                            else:
                                                g[3] = False
                        self.bomb[b] = False
                        self.boom[b] = False
        if self.bomb:
            b = 0
            while False in self.bomb:
                if self.bomb[b]:
                    b += 1
                else:
                    del self.bomb[b]
                    del self.boom[b]

        if self.dethtime - (self.time - 1) // self.fpsall == 0:
            self.pers[2] = 0
            self.pers[3] = self.cell_size
        else:
            font = pygame.font.Font("18999.otf", self.cell_size // 10 * 9)
            text = font.render(
                'HP:' + str(self.life) + '  number of bombs: ' + str(
                    self.bonus1 + 1) + '  blast radius: ' + str(
                    self.bonus2 + 1) + '  time: ' + str(
                    self.dethtime - self.time // self.fpsall) + '  Points: ' + str(
                    self.points), 1,
                (250, 250, 250))
            screen.blit(text, (10, self.cell_size // 2))
        if self.pers[2] == 0 and self.pers[3] == 0:
            # print(self.pers)
            pass
        elif self.pers[2] == 0:
            self.board[self.pers[0]][self.pers[1]] = 1
        for i in range(len(self.enemy)):
            if type(self.enemy[i]) not in [bool, int]:
                self.enemycopy[i] = self.enemy[i]
        for i in range(len(a)):
            for j in range(len(a[i])):
                if self.gamecon:
                    if self.board[i][j] == 0:
                        pygame.draw.rect(screen, (200, 200, 200), (
                            self.top + i * self.cell_size,
                            self.left + j * self.cell_size, self.cell_size,
                            self.cell_size), 1)
                    elif self.board[i][j] == 1:
                        # pygame.draw.rect(screen, (80, 80, 255), (
                        # 	self.top + i * self.cell_size,
                        # 	self.left + j * self.cell_size, self.cell_size,
                        # 	self.cell_size))
                        pygame.draw.rect(screen, (200, 200, 200), (
                            self.top + i * self.cell_size,
                            self.left + j * self.cell_size, self.cell_size,
                            self.cell_size), 1)

                        # pygame.draw.circle(screen, (80, 80, 255), (
                        #     self.top + i * self.cell_size + self.cell_size // 2,
                        #     self.left + j * self.cell_size + self.cell_size // 2),
                        #                    self.cell_size // 2 - 2, self.cell_size // 7)
                        imgs = [['none.png', 'pers07.png', 'pers06.png', 'pers05.png', 'pers04.png', 'pers03.png', 'pers02.png', 'pers01.png', 'pers00.png'], ['pers10.png', 'pers11.png', 'pers12.png', 'pers11.png', 'pers10.png'], ['pers20.png', 'pers21.png', 'pers22.png', 'pers21.png', 'pers20.png'], ['pers30.png', 'pers31.png', 'pers32.png', 'pers31.png', 'pers30.png'], ['pers40.png', 'pers41.png', 'pers42.png', 'pers41.png', 'pers40.png']]
                        # hero_rect = hero.get_rect(center=(self.top + i * self.cell_size + self.cell_size // 2, self.left + j * self.cell_size + self.cell_size // 2))
                        if self.pers[3] == -1:
                            self.gamecon = False
                        else:
                            if self.pers[2] == 0:
                                # print(self.pers)
                                hero = pygame.image.load(
                                    imgs[self.pers[2]][self.pers[3] // (self.cell_size // 7)])
                                hero = pygame.transform.scale(hero, (
                                self.cell_size, self.cell_size))
                                hero_rect = hero.get_rect(center=(
                                    self.top +self.pers[0]* self.cell_size + self.cell_size // 2,
                                    self.left +self.pers[1]* self.cell_size + self.cell_size // 2))
                                if self.pers[3] == 0:
                                    self.pers[3] = -1
                            else:
                                hero = pygame.image.load(
                                    imgs[self.pers[2]][self.pers[3] // (self.cell_size // 4)])
                                hero = pygame.transform.scale(hero, (
                                self.cell_size, self.cell_size))
                            if self.pers[2] == 1:
                                if self.pers[3] == self.cell_size:
                                    # print(self.pers)
                                    self.pers[0] += 1
                                hero_rect = hero.get_rect(center=(
                                    self.top +self.pers[0]* self.cell_size + self.cell_size // 2 -
                                    self.pers[3],
                                    self.left +self.pers[1]* self.cell_size + self.cell_size // 2))
                            elif self.pers[2] == 2:
                                if self.pers[3] == self.cell_size:
                                    self.pers[0] -= 1
                                hero_rect = hero.get_rect(center=(
                                    self.top +self.pers[0]* self.cell_size + self.cell_size // 2 +
                                    self.pers[3],
                                    self.left +self.pers[1]* self.cell_size + self.cell_size // 2))
                            elif self.pers[2] == 3:
                                if self.pers[3] == self.cell_size:
                                    self.pers[1] -= 1
                                hero_rect = hero.get_rect(center=(
                                    self.top +self.pers[0]* self.cell_size + self.cell_size // 2,
                                    self.left +self.pers[1]* self.cell_size + self.cell_size // 2 +
                                    self.pers[3]))
                            elif self.pers[2] == 4:
                                if self.pers[3] == self.cell_size:
                                    self.pers[1] += 1
                                hero_rect = hero.get_rect(center=(
                                    self.top +self.pers[0]* self.cell_size + self.cell_size // 2,
                                    self.left +self.pers[1]* self.cell_size + self.cell_size // 2 -
                                    self.pers[3]))
                            self.board[i][j] = 0
                            self.board[self.pers[0]][self.pers[1]] = 1
                            screen.blit(hero, hero_rect)
                            if self.pers[3] >= self.cell_size // 4:
                                self.pers[3] -= self.cell_size // 4
                            elif 0 < self.pers[3] < self.cell_size // 4:
                                self.pers[3] -= 1
                    elif self.board[i][
                        j] == -1:
                        pygame.draw.rect(screen, (100, 100, 100), (
                            self.top + i * self.cell_size,
                            self.left + j * self.cell_size, self.cell_size,
                            self.cell_size))
                    elif self.board[i][j] == [4, 0] or self.board[i][j] == [4,
                                                                            5] or \
                            self.board[i][j] == [4, 6] or self.board[i][j] == [
                        4, 7]:
                        pygame.draw.rect(screen, (100, 70, 50), (
                            self.top + i * self.cell_size,
                            self.left + j * self.cell_size, self.cell_size,
                            self.cell_size))

                    elif self.board[i][j] == 5:
                        bonus1 = pygame.image.load("+1bomb.png").convert()
                        bonus1 = pygame.transform.scale(bonus1, (
                        self.cell_size, self.cell_size))
                        bonus1_rect = (
                            self.top + i * self.cell_size,
                            self.left + j * self.cell_size, self.cell_size,
                            self.cell_size)
                        screen.blit(bonus1, bonus1_rect)
                    elif self.board[i][j] == 6:
                        bonus2 = pygame.image.load("+1radius.png").convert()
                        bonus2 = pygame.transform.scale(bonus2, (self.cell_size, self.cell_size))
                        bonus2_rect = (
                            self.top + i * self.cell_size,
                            self.left + j * self.cell_size, self.cell_size,
                            self.cell_size)
                        screen.blit(bonus2, bonus2_rect)
                    elif self.board[i][j] == 7:
                        # pygame.draw.rect(screen, (0, 0, 200), (
                        #     self.top + i * self.cell_size,
                        #     self.left + j * self.cell_size, self.cell_size,
                        #     self.cell_size))
                        exit = pygame.image.load("door.png").convert()
                        exit = pygame.transform.scale(exit, (
                        self.cell_size, self.cell_size))
                        exit_rect = (
                            self.top + i * self.cell_size,
                            self.left + j * self.cell_size, self.cell_size,
                            self.cell_size)
                        screen.blit(exit, exit_rect)

                    elif self.board[i][j] == 3:
                        if self.fps != self.fpsall - 1:
                            ex = 0
                            ey = 0
                            for p in range(len(self.enemy)):
                                h = self.enemy[p]
                                bll = False
                                if h and type(h) != int:
                                    if h[0] == i and h[1] == j:
                                        if h[2] == 1:
                                            ex = 1
                                            ey = 0
                                        elif h[2] == 2:
                                            ex = -1
                                            ey = 0
                                        elif h[2] == 3:
                                            ex = 0
                                            ey = -1
                                        elif h[2] == 4:
                                            ex = 0
                                            ey = 1
                                        bll = True
                                        break
                            if not bll:
                                for p in range(len(self.enemy)):
                                    if type(self.enemy[p]) == int and self.enemycopy[p][0] == i and self.enemycopy[p][1] == j:
                                        if self.enemy[p] != self.fps:
                                            h = self.enemycopy[p]
                                            if h[0] == i and h[1] == j:
                                                if h[2] == 1:
                                                    ex = 1
                                                    ey = 0
                                                elif h[2] == 2:
                                                    ex = -1
                                                    ey = 0
                                                elif h[2] == 3:
                                                    ex = 0
                                                    ey = -1
                                                elif h[2] == 4:
                                                    ex = 0
                                                    ey = 1
                                            en = ["enemy06.png", "enemy05.png",
                                                  "enemy04.png", "enemy03.png",
                                                  "enemy02.png", "enemy01.png"]
                                            enemy = pygame.image.load(
                                                en[(self.fps // (
                                                            self.fpsall // 9) - 1) % 6])
                                            enemy = pygame.transform.scale(enemy, (
                                            self.cell_size, self.cell_size))
                                            enemy_rect = enemy.get_rect(center=(
                                                self.top + i * self.cell_size + self.cell_size // 2 + ex * (
                                            self.cell_size // self.fpsall * self.enemy[p]),
                                                self.left + j * self.cell_size + self.cell_size // 2 + ey * (
                                            self.cell_size // self.fpsall * self.enemy[p])))
                                            pygame.draw.rect(screen,
                                                             (200, 200, 200), (
                                                                 self.top + i * self.cell_size,
                                                                 self.left + j * self.cell_size,
                                                                 self.cell_size,
                                                                 self.cell_size),
                                                             1)
                                            screen.blit(enemy, enemy_rect)
                                        else:
                                            # print(self.enemy[p])
                                            self.board[i][j] = 0
                                            self.enemy[p] = False

                            if type(self.enemy[p]) not in [bool, int]:
                                en = ["enemy1.png", "enemy2.png", "enemy3.png"]
                                enemy = pygame.image.load(
                                    en[(self.fps // (self.fpsall // 9) - 1) % 3])
                                enemy = pygame.transform.scale(enemy, (self.cell_size, self.cell_size))
                                enemy_rect = enemy.get_rect(center=(
                                    self.top + self.enemy[p][0] * self.cell_size + self.cell_size // 2 + ex * (
                                            self.cell_size // self.fpsall * self.fps),
                                    self.left + h[1] * self.cell_size + self.cell_size // 2 + ey * (
                                            self.cell_size // self.fpsall * self.fps)))
                                pygame.draw.rect(screen, (200, 200, 200), (
                                    self.top + i * self.cell_size,
                                    self.left + j * self.cell_size, self.cell_size,
                                    self.cell_size), 1)
                                screen.blit(enemy, enemy_rect)
                        else:
                            ex = 0
                            ey = 0
                            for p in range(len(self.enemy)):
                                h = self.enemy[p]
                                bll = False
                                if h and type(h) != int:
                                    if h[0] == i and h[1] == j:
                                        if h[2] == 1:
                                            ex = 1
                                            ey = 0
                                        elif h[2] == 2:
                                            ex = -1
                                            ey = 0
                                        elif h[2] == 3:
                                            ex = 0
                                            ey = -1
                                        elif h[2] == 4:
                                            ex = 0
                                            ey = 1
                                        bll = True
                                        break
                            if not bll:
                                for p in range(len(self.enemy)):
                                    if type(self.enemy[p]) == int and \
                                            self.enemycopy[p] == [i, j]:
                                        if self.enemy[p] != self.fps:
                                            en = ["enemy06.png", "enemy05.png",
                                                  "enemy04.png", "enemy03.png",
                                                  "enemy02.png", "enemy01.png"]
                                            enemy = pygame.image.load(
                                                en[(self.fps // (
                                                        self.fpsall // 9) - 1) % 6])
                                            enemy = pygame.transform.scale(
                                                enemy, (
                                                    self.cell_size,
                                                    self.cell_size))
                                            enemy_rect = enemy.get_rect(
                                                center=(
                                                    self.top + i * self.cell_size + self.cell_size // 2,
                                                    self.left + j * self.cell_size + self.cell_size // 2))
                                            pygame.draw.rect(screen,
                                                             (200, 200, 200), (
                                                                 self.top + i * self.cell_size,
                                                                 self.left + j * self.cell_size,
                                                                 self.cell_size,
                                                                 self.cell_size),
                                                             1)
                                            screen.blit(enemy, enemy_rect)
                                        else:
                                            # print(self.enemy[p])
                                            self.board[i][j] = 0
                                            self.enemy[p] = False

                            if type(self.enemy[p]) not in [bool, int]:
                                en = ["enemy1.png", "enemy2.png", "enemy3.png"]
                                enemy = pygame.image.load(
                                    en[(self.fps // (
                                                self.fpsall // 9) - 1) % 3])
                                enemy = pygame.transform.scale(enemy, (
                                self.cell_size, self.cell_size))
                                enemy_rect = enemy.get_rect(center=(
                                    self.top + self.enemy[p][
                                        0] * self.cell_size + self.cell_size // 2,
                                    self.left + h[
                                        1] * self.cell_size + self.cell_size // 2))
                                pygame.draw.rect(screen, (200, 200, 200), (
                                    self.top + i * self.cell_size,
                                    self.left + j * self.cell_size,
                                    self.cell_size,
                                    self.cell_size), 1)
                                screen.blit(enemy, enemy_rect)
                else:
                    if self.life == 1:
                        pygame.quit()
                    else:
                        self.set_view(self.left, self.top, self.cell_size, self.fpsall)
                        self.__init__(self.width, self.height, self.bonus1, self.bonus2, self.life - 1, self.time, self.top, self.left, self.cell_size, self.fpsall)

        if self.gamecon:
            if self.bomb:
                for b in self.bomb:
                    if b:
                        pygame.draw.rect(screen, (200, 200, 200), (
                            self.top + b[0] * self.cell_size,
                            self.left + b[1] * self.cell_size, self.cell_size,
                            self.cell_size), 1)
                        bmb = ["bomb1.png", "bomb1.png", "bomb1.png", "bomb2.png", "bomb2.png", "bomb3.png"]
                        bomb = pygame.image.load(random.choice(bmb))
                        bomb = pygame.transform.scale(bomb, (self.cell_size, self.cell_size))
                        bomb_rect = bomb.get_rect(center=(
                            self.top + b[
                                0] * self.cell_size + self.cell_size // 2,
                            self.left + b[
                                1] * self.cell_size + self.cell_size // 2))
                        screen.blit(bomb, bomb_rect)

            if self.boomarea:
                i = 0
                for i in range(len(self.boomarea)):
                    # boom = pygame.image.load("boom.png")
                    # boom = pygame.transform.scale(boom, (self.cell_size, self.cell_size))
                    # boom.set_colorkey((255, 255, 255))
                    # boom_rect = boom.get_rect(center=((
                    #             self.top + self.boomarea[i][
                    #                 0] * self.cell_size + self.cell_size // 2,
                    #             self.left + self.boomarea[i][
                    #                 1] * self.cell_size + self.cell_size // 2)))
                    # screen.blit(boom, boom_rect)
                    # self.boomarea[i][2] += 1
                    # if self.boomarea[i][2] >= self.fpsall // 3:
                    #     self.boomarea[i] = False

                    bar = []
                    for j in self.boomarea:
                        bar.append([j[0], j[1]])
                    x = -1
                    if [self.boomarea[i][0] - 1, self.boomarea[i][1]] in bar and [self.boomarea[i][0] + 1, self.boomarea[i][1]] in bar and [self.boomarea[i][0], self.boomarea[i][1] - 1] in bar and [self.boomarea[i][0], self.boomarea[i][1] + 1] in bar:
                        x = 0
                    elif ([self.boomarea[i][0] + 1, self.boomarea[i][1]] in bar and [self.boomarea[i][0] - 1, self.boomarea[i][1]] in bar and [self.boomarea[i][0], self.boomarea[i][1] + 1] in bar) or ([self.boomarea[i][0] + 1, self.boomarea[i][1]] in bar and [self.boomarea[i][0] - 1, self.boomarea[i][1]] in bar and [self.boomarea[i][0], self.boomarea[i][1] - 1] in bar) or  ([self.boomarea[i][0], self.boomarea[i][1] + 1] in bar and [self.boomarea[i][0], self.boomarea[i][1] - 1] in bar and [self.boomarea[i][0] + 1, self.boomarea[i][1]] in bar) or ([self.boomarea[i][0], self.boomarea[i][1] + 1] in bar and [self.boomarea[i][0], self.boomarea[i][1] - 1] in bar and [self.boomarea[i][0] - 1, self.boomarea[i][1]] in bar):
                        x = 0
                    elif [self.boomarea[i][0] - 1, self.boomarea[i][1]] in bar and [self.boomarea[i][0], self.boomarea[i][1] + 1] in bar or [self.boomarea[i][0] + 1, self.boomarea[i][1]] in bar and [self.boomarea[i][0], self.boomarea[i][1] - 1] in bar or [self.boomarea[i][0] + 1, self.boomarea[i][1]] in bar and [self.boomarea[i][0], self.boomarea[i][1] + 1] in bar or [self.boomarea[i][0] - 1, self.boomarea[i][1]] in bar and [self.boomarea[i][0], self.boomarea[i][1] - 1] in bar:
                        x = 0
                    elif [self.boomarea[i][0] + 1, self.boomarea[i][1]] in bar and [self.boomarea[i][0] - 1, self.boomarea[i][1]] in bar:
                        x = 5
                    elif [self.boomarea[i][0], self.boomarea[i][1] + 1] in bar and [self.boomarea[i][0], self.boomarea[i][1] - 1] in bar:
                        x = 6
                    elif [self.boomarea[i][0] - 1, self.boomarea[i][1]] in bar:
                        x = 2
                    elif [self.boomarea[i][0] + 1, self.boomarea[i][1]] in bar:
                        x = 1
                    elif [self.boomarea[i][0], self.boomarea[i][1] + 1] in bar:
                        x = 3
                    elif [self.boomarea[i][0], self.boomarea[i][1] - 1] in bar:
                        x = 4
                    cd = self.boomarea[i][2] // (self.fpsall // 3 // 3) + 1
                    zero = pygame.image.load("center" + str(cd) + '.png')
                    one = pygame.image.load("end" + str(cd) + ".png")
                    two = pygame.transform.rotate(one, 180)
                    tree = pygame.transform.rotate(two, 90)
                    four = pygame.transform.rotate(two, -90)
                    five = pygame.image.load("middle" + str(cd) + ".png")
                    six = pygame.transform.rotate(five, 90)
                    dgr = [zero, one, two, tree, four, five, six]
                    boom = pygame.transform.scale(dgr[x],
                                                  (self.cell_size, self.cell_size))
                    boom_rect = boom.get_rect(center=((
                        self.top + self.boomarea[i][
                            0] * self.cell_size + self.cell_size // 2,
                        self.left + self.boomarea[i][
                            1] * self.cell_size + self.cell_size // 2)))
                    screen.blit(boom, boom_rect)
                    self.boomarea[i][2] += 1
                for i in range(len(self.boomarea)):
                    if self.boomarea[i][2] >= self.fpsall // 3:
                        self.boomarea[i] = False
                b = 0
                while False in self.boomarea:
                    if self.boomarea[b]:
                        b += 1
                    else:
                        del self.boomarea[b]

    def get_cell(self, pos):
        y = pos[0] - self.top
        x = pos[1] - self.left
        if 0 <= x <= self.width * self.cell_size and 0 <= y <= self.height * self.cell_size:
            for i in range(self.height):
                for j in range(self.width):
                    # print(x, y, i, j)
                    if j * self.cell_size <= x <= (
                            j + 1) * self.cell_size and i * self.cell_size <= y <= (
                            i + 1) * self.cell_size:
                        return [i, j]
        else:
            return None

    def keyd(self, key):
        a = self.pers.copy()
        kk = [[pygame.K_RIGHT, pygame.K_d, [a[0] + 1, a[1]], 1],
              [pygame.K_LEFT, pygame.K_a, [a[0] - 1, a[1]], 2],
              [pygame.K_UP, pygame.K_w, [a[0], a[1] - 1], 3],
              [pygame.K_DOWN, pygame.K_s, [a[0], a[1] + 1], 4]]
        if type(self.bomb) != list:
            bomb = [self.bomb]
        else:
            bomb = self.bomb.copy()
        if a[2] != 0 and a[3] == 0:
            for i in kk:
                if (key == i[0] or key == i[1]) and self.board[i[2][0]][
                    i[2][1]] in [0, 3, 5, 6, 7] and i[2] not in bomb:
                    if self.board[i[2][0]][i[2][1]] == 3:
                        self.pers[2] = 0
                        self.pers[3] = self.cell_size
                        print('THE END')
                    elif self.board[i[2][0]][i[2][1]] == 5:
                        self.bonus1 += 1
                        # self.board[a[0]][a[1]] = 0
                        # # self.pers = i[2]
                        # self.board[i[2][0]][i[2][1]] = 1
                        self.pers[3] = self.cell_size
                        self.pers[2] = i[3]
                    elif self.board[i[2][0]][i[2][1]] == 6:
                        self.bonus2 += 1
                        # self.board[a[0]][a[1]] = 0
                        # # self.pers = i[2]
                        # self.board[i[2][0]][i[2][1]] = 1
                        self.pers[3] = self.cell_size
                        self.pers[2] = i[3]
                    elif self.board[i[2][0]][i[2][1]] == 7:
                        if self.points > 500:
                            print('You win!')
                            self.gamecon = False
                    else:
                        # self.board[a[0]][a[1]] = 0
                        # # self.pers = i[2]
                        # self.board[i[2][0]][i[2][1]] = 1
                        self.pers[3] = self.cell_size
                        self.pers[2] = i[3]
        if key == pygame.K_SPACE:
            if self.bomb:
                if self.pers not in self.bomb:
                    if len(self.bomb) < self.bonus1 + 1:
                        self.bomb.append(a)
                        self.boom.append(self.fps)
            else:
                self.bomb = [a]
                self.boom = [self.fps]
        elif key == pygame.K_x:
            print('You left the game')
            self.pers[2] = 0
            self.pers[3] = self.cell_size


# menu
# app = QApplication(sys.argv)
# q = QDesktopWidget().availableGeometry()
# x = q.width() * q.height() // 42500
# print(q.width(), q.height(), x)
x = 29
fps = x # количество кадров в секунду
clock = pygame.time.Clock()
pygame.init()
size = width, height = 35 * x, 15 * x
board = Map(13, 35)
board.set_view(x * 2, 0, x, fps)
screen = pygame.display.set_mode(size)
screen.fill((150, 150, 150))
running = True
while running and board.gamecon:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            board.keyd(event.key)
    screen.fill((150, 150, 150))
    board.render()
    if board.gamecon:
        pygame.display.flip()
    clock.tick(fps)
# menu
