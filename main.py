import pygame
import random


def ok(x, a, b,
       board):  # направление, координаты, список точек куда можно, поле
    if x == 1:  # right
        if board[a[0] + 1][a[1]] in b:
            return [a[0] + 1, a[1], x]
        else:
            return False
    elif x == 2:  # left
        if board[a[0] - 1][a[1]] in b:
            return [a[0] - 1, a[1], x]
        else:
            return False
    elif x == 3:  # down
        if board[a[0]][a[1] + 1] in b:
            return [a[0], a[1] + 1, x]
        else:
            return False
    elif x == 4:  # up
        if board[a[0]][a[1] - 1] in b:
            return [a[0], a[1] - 1, x]
        else:
            return False
    else:
    	return [a[0], a[1], x]


class Map:
    # создание поля
    def __init__(self, width, height):  # высота, ширина
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
            self.board[x][y] = [4, 0]

        self.enemy = []
        for i in range(height * width // 19):  # враги
            x = random.choice(range(height))
            y = random.choice(range(width))
            while self.board[x][y] != 0 or [x, y] in f:
                x = random.choice(range(height))
                y = random.choice(range(width))
            self.board[x][y] = 3
            self.enemy.append([x, y, 0])
        # print(len(self.enemy), height * width // 19)

        self.board[1][1] = 1  # персонаж
        self.pers = [1, 1]  # координаты персонажа

        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        self.fps = (self.fps + 1) % 30
        a = self.board
        if self.fps == 29:
            if self.pers.copy().append(1) in self.enemy or self.pers.copy().append(2) in self.enemy or self.pers.copy().append(3) in self.enemy or self.pers.copy().append(4) in self.enemy:
                pygame.quit()
            for i in range(len(self.enemy)):
                g = [1, 2, 3, 4]
                for _ in range(4):
                    x = random.choice(g)
                    g = g[:x - 1] + g[x:]
                    if ok(x, self.enemy[i], [0, 1], self.board):
                        k = ok(x, self.enemy[i], [0, 1], self.board)
                        self.board[self.enemy[i][0]][self.enemy[i][1]] = 0
                        self.board[k[0]][k[1]] = 3
                        self.enemy[i] = k
                        break

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
                        pygame.draw.circle(screen, (80, 80, 255), (
                            self.top + i * self.cell_size + self.cell_size // 2,
                            self.left + j * self.cell_size + self.cell_size // 2),
                                           self.cell_size // 2 - 2, 5)
                    elif self.board[i][j] == -1:
                        pygame.draw.rect(screen, (100, 100, 100), (
                            self.top + i * self.cell_size,
                            self.left + j * self.cell_size, self.cell_size,
                            self.cell_size))
                    elif self.board[i][j] == [4, 0]:
                        pygame.draw.rect(screen, (100, 70, 50), (
                            self.top + i * self.cell_size,
                            self.left + j * self.cell_size, self.cell_size,
                            self.cell_size))
                    elif self.board[i][j] == 3:
                        # pygame.draw.rect(screen, (200, 20, 20), (
                        # 	self.top + i * self.cell_size,
                        # 	self.left + j * self.cell_size, self.cell_size,
                        # 	self.cell_size))

                        ex = 0
                        ey = 0
                        for h in self.enemy:
                            if h[0] == i and h[1] == j:
                                if h[2] == 1:
                                    ex = 1
                                    ey = 0
                                elif h[2] == 2:
                                    ex = -1
                                    ey = 0
                                elif h[2] == 3:
                                    ex = 0
                                    ey = 1
                                elif h[2] == 4:
                                    ex = 0
                                    ey = -1
                                # if self.fps == 29:
                                #     k = ok(h[2], h, [0, 1], self.board)
                                #     # print(h[2], h, [0, 1], self.board)
                                #     self.board[h[0]][h[1]] = 0
                                #     self.board[k[0]][k[1]] = 3
                                #     self.enemy[u] = k

                        pygame.draw.rect(screen, (200, 200, 200), (
                            self.top + i * self.cell_size,
                            self.left + j * self.cell_size, self.cell_size,
                            self.cell_size), 1)
                        pygame.draw.circle(screen, (200, 20, 20), (
                            self.top + i * self.cell_size + self.cell_size // 2 + ex * (
                                        self.cell_size // 30 * self.fps),
                            self.left + j * self.cell_size + self.cell_size // 2 + ey * (
                                        self.cell_size // 30 * self.fps)),
                                           self.cell_size // 2 - 2, 5)
                else:
                    pygame.quit()

    def keyd(self, key):
        a = self.pers.copy()
        if key == pygame.K_RIGHT and (
                self.board[a[0] + 1][a[1]] == 0 or self.board[a[0] + 1][
            a[1]] == 3):
            if self.board[a[0] + 1][a[1]] == 3:
                self.gamecon = False
                print('THE END')
            else:
                self.board[a[0]][a[1]] = 0
                self.pers = [a[0] + 1, a[1]]
                self.board[a[0] + 1][a[1]] = 1
        elif key == pygame.K_LEFT and (
                self.board[a[0] - 1][a[1]] == 0 or self.board[a[0] - 1][
            a[1]] == 3):
            if self.board[a[0] - 1][a[1]] == 3:
                self.gamecon = False
                print('THE END')
            else:
                self.board[a[0]][a[1]] = 0
                self.pers = [a[0] - 1, a[1]]
                self.board[a[0] - 1][a[1]] = 1
        elif key == pygame.K_UP and (
                self.board[a[0]][a[1] - 1] == 0 or self.board[a[0]][
            a[1] - 1] == 3):
            if self.board[a[0]][a[1] - 1] == 3:
                self.gamecon = False
                print('THE END')
            else:
                self.board[a[0]][a[1]] = 0
                self.pers = [a[0], a[1] - 1]
                self.board[a[0]][a[1] - 1] = 1
        elif key == pygame.K_DOWN and (
                self.board[a[0]][a[1] + 1] == 0 or self.board[a[0]][
            a[1] + 1] == 3):
            if self.board[a[0]][a[1] + 1] == 3:
                self.gamecon = False
                print('THE END')
            else:
                self.board[a[0]][a[1]] = 0
                self.pers = [a[0], a[1] + 1]
                self.board[a[0]][a[1] + 1] = 1


fps = 30  # количество кадров в секунду
clock = pygame.time.Clock()
pygame.init()
size = width, height = 35 * 40, 14 * 40
board = Map(13, 35)
board.set_view(40, 0, 40)
screen = pygame.display.set_mode(size)
screen.fill((50, 200, 50))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            board.keyd(event.key)
    screen.fill((80, 160, 50))
    board.render()
    pygame.display.flip()
    clock.tick(fps)
