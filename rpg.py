import pygame
from pygame.locals import *

pygame.init()
speed = 0.4
window = pygame.display.set_mode((1250, 650))
size = 25
x = 50
y = 50
clock = pygame.time.Clock()
recto = Rect(200, 500, 50, 50)


def quit_window():
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()


class Player:
    def __init__(self, x, y, sizex, sizey):
        self.player = None
        self.position = (x, y)
        self.size = (sizex, sizey)
        self.colour = (255, 0, 0)

    def draw(self):
        pygame.draw.rect(window, self.colour, [self.position[0], self.position[1], self.size[0], self.size[1]])
    def move(self, obstacle_list):
        if not self.collision(obstacle_list):
            keys = pygame.key.get_pressed()
            self.position[0] += (keys[pygame.K_d] - keys[pygame.K_a]) * speed
            self.position[1] += (keys[pygame.K_s] - keys[pygame.K_w]) * speed

    def collision(self, obstacle_list):
        for i in obstacle_list:
            if pygame.Rect.collidedict(self.player, i):
                return True
            else:
                return False
class Obstacle:
    def __init__(self, x, y, sizex, sizey):
        self.position = (x, y)
        self.size = (sizex, sizey)
        self.colour = (0, 0, 40)
    def draw(self):
        pygame.draw.rect(window, self.colour, [self.position[0], self.position[1], self.size[0], self.size[1]])



#
#
# while True:
#     player()
#     collide = pygame.Rect.colliderect(Player, recto)
#     move()
#     if collide:
#         Player.bottom = recto.top
#         # Player.top = recto.bottom
#         # Player.right = recto.left
#     # Player.left = recto.right
#     pygame.draw.rect(window, (0, 0, 0), recto)
#     pygame.draw.rect(window, (255, 0, 0), Player)
#     keys = pygame.key.get_pressed()
#     if keys[pygame.K_SPACE]:
#         speed = 1
#     else:
#         speed = 0.5
#     x += (keys[pygame.K_d] - keys[pygame.K_a]) * speed
#     y += (keys[pygame.K_s] - keys[pygame.K_w]) * speed
#     pygame.display.update()
