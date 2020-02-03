import pygame
import random


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        a = []
        for i in range(height):
            v = []
            for j in range(width):
                v.append(random.choice([0, 1]))
            a.append(v)
        self.board = a.copy()
        # self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, top, left, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        a = self.board
        if self.board.count([0] * self.width) == self.height or self.board.count([1] * self.width) == self.height:
            print('THE END')
            pygame.quit()
        for i in range(len(a)):
            for j in range(len(a[i])):
                if self.board[i][j] == 0:
                    pygame.draw.rect(screen, (255, 255, 255), (
                        self.top + i * self.cell_size, self.left + j * self.cell_size, self.cell_size,
                        self.cell_size), 1)
                    pygame.draw.circle(screen, (50, 255, 50), (self.top + i * self.cell_size + self.cell_size // 2,
                                       self.left + j * self.cell_size + self.cell_size // 2),
                                       self.cell_size // 2 - 2, 2)
                else:
                    pygame.draw.rect(screen, (255, 255, 255), (
                        self.top + i * self.cell_size, self.left + j * self.cell_size, self.cell_size,
                        self.cell_size), 1)
                    pygame.draw.circle(screen, (255, 50, 50), (self.top + i * self.cell_size + self.cell_size // 2,
                                                                 self.left + j * self.cell_size + self.cell_size // 2),
                                       self.cell_size // 2 - 2, 2)

    def get_cell(self, mouse_pos):
        y = mouse_pos[0] - self.top
        x = mouse_pos[1] - self.left
        if 0 <= x <= self.width * self.cell_size and 0 <= y <= self.height * self.cell_size:
            for i in range(self.height):
                for j in range(self.width):
                    # print(x, y, i, j)
                    if j * self.cell_size <= x <= (j + 1) * self.cell_size and i * self.cell_size <= y <= (i + 1) * self.cell_size:
                        return [i, j]
        else:
            return None

    def on_click(self, cell_coords):
        if cell_coords is not None:
            for i in range(self.height):
                self.board[i][cell_coords[1]] = self.board[cell_coords[0]][cell_coords[1]]
            for i in range(self.width):
                self.board[cell_coords[0]][i] = self.board[cell_coords[0]][cell_coords[1]]

    def get_click(self, mouse_pos):
        self.on_click(self.get_cell(mouse_pos))


pygame.init()
n = 10
v = 500
size = width, height = v, v
board = Board(n, n)
board.set_view(0, 0, v // n)
screen = pygame.display.set_mode(size)
screen.fill((0, 0, 0))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)
    screen.fill((0, 0, 0))
    board.render()
    pygame.display.flip()