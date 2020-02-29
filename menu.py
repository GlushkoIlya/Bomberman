import pygame
import random
import sys
from PyQt5.QtWidgets import QDesktopWidget, QApplication
import game

# font = pygame.font.Font("18999.otf", self.cell_size // 10 * 7)
# text = font.render(
#     'HP:' + str(self.life) + '  number of bombs: ' + str(
#         self.bonus1 + 1) + '  blast radius: ' + str(
#         self.bonus2 + 1) + '  time: ' + str(
#         self.dethtime - self.time // self.fpsall) + '  Points: ' + str(
#         self.points), 1, (250, 250, 250))
# screen.blit(text, (10, self.cell_size // 2))


app = QApplication(sys.argv)
q = QDesktopWidget().availableGeometry()
x = q.width() * q.height() // 42500
fps = x
clock = pygame.time.Clock()
pygame.init()
size = width, height = 15 * x, 15 * x
screen1 = pygame.display.set_mode(size)
screen1.fill((150, 150, 150))

gx = 0
gy = 0
gfps = 0
vv = 0
bt = [[10 + 2 * x, 9 * x, 10 + 2 * x + 4 * x, 9 * x + x * 0.9],
      [10 + 2 * x, 10 * x, 10 + 2 * x + 4 * x, 10 * x + x * 0.9],
      [10 + 2 * x, 11 * x, 10 + 2 * x + 4 * x, 11 * x + x * 0.9]]


def get_cell(x, y, a):
    v = -1
    for i in range(len(a)):
        if a[i][0] <= x <= a[i][2] and a[i][1] <= y <= a[i][3]:
            v = i
    return v


# pygame.draw.rect(screen, (100, 70, 50), ())

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            h = [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7,
                 pygame.K_8, pygame.K_9, pygame.K_BACKSPACE]
            if event.key in h:
                k = h.index(event.key)
                if vv == 1 and (k == 10 or gx * 10 + k <= 50):
                    if k == 10:
                        gx = gx // 10
                    else:
                        gx = gx * 10 + k
                elif vv == 2 and (k == 10 or gy * 10 + k <= 30):
                    if k == 10:
                        gy = gy // 10
                    else:
                        gy = gy * 10 + k
                elif vv == 3 and (k == 10 or gfps * 10 + k <= 200):
                    if k == 10:
                        gfps = gfps // 10
                    else:
                        gfps = gfps * 10 + k
            elif event.key == pygame.K_TAB:
                vv = (vv + 1) % 3 + 1
            elif event.key == pygame.K_KP_ENTER:
                if len(bt) == 4:
                    game.start(gx, gy, gfps)
        if event.type == pygame.MOUSEBUTTONDOWN:
            d = get_cell(event.pos[0], event.pos[1], bt)
            if d != -1:
                vv = d + 1
            if d + 1 == 4:
                game.start(gx, gy, gfps)

    if gx != 0 and gy != 0 and gfps != 0 and len(bt) == 3:
        bt.append([5 * x + 2 * x, 10 * x, 5 * x + 2 * x + 4 * x, 10 * x + x * 0.9])
    elif gx == 0 or gy == 0 or gfps == 0 and len(bt) == 4:
        bt = [bt[0], bt[1], bt[2]]

    screen1.fill((150, 150, 150))
    logo = pygame.image.load("logo.png")
    logo = pygame.transform.scale(logo, (15 * x, 8 * x))
    screen1.blit(logo, (0, 0))

    if vv == 1:
        color = (250, 50, 50)
    else:
        color = (250, 250, 250)
    pygame.draw.rect(screen1, color, (5 + 2 * x, 9 * x + 2, 5 * x, round(x * 0.9)), 2)
    font = pygame.font.Font("18999.otf", x // 10 * 8)
    text = font.render("x: " + str(gx), 1, (100, 100, 100))
    screen1.blit(text, (2 * x + 10, 9 * x))

    if vv == 2:
        color = (250, 50, 50)
    else:
        color = (250, 250, 250)
    pygame.draw.rect(screen1, color, (5 + 2 * x, 10 * x + 2, 5 * x, round(x * 0.9)), 2)
    text = font.render("y: " + str(gy), 1, (100, 100, 100))
    screen1.blit(text, (2 * x + 10, 10 * x))

    if vv == 3:
        color = (250, 50, 50)
    else:
        color = (250, 250, 250)
    pygame.draw.rect(screen1, color, (5 + 2 * x, 11 * x + 2, 5 * x, round(x * 0.9)), 2)
    text = font.render("fps: " + str(gfps), 1, (100, 100, 100))
    screen1.blit(text, (2 * x + 10, 11 * x))

    if len(bt) > 3:
        pygame.draw.rect(screen1, (250, 250, 250), (5 * x + 4 * x, 10 * x + 2, 4 * x, round(x * 0.9)))
        text = font.render("START", 1, (100, 100, 100))
        screen1.blit(text, (5 * x + 4 * x + 10, 10 * x))

    pygame.display.flip()
    clock.tick(fps)
