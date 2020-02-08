import pygame
import random
import sys
from PyQt5.QtWidgets import QDesktopWidget, QApplication
import game


app = QApplication(sys.argv)
q = QDesktopWidget().availableGeometry()
x = q.width() * q.height() // 42500
fps = x
# clock = pygame.time.Clock()
pygame.init()
size = width, height = 15 * x, 15 * x
screen1 = pygame.display.set_mode(size)
screen1.fill((150, 150, 150))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            print("hello")
            game
    screen1.fill((150, 150, 150))
    logo = pygame.image.load("logo.png")
    logo = pygame.transform.scale(logo, (15 * x, 8 * x))
    screen1.blit(logo, (0, 0))
    pygame.display.flip()
    # clock.tick(fps)