import pygame
from pygame.locals import*

pygame.init()
speed = 0.4
window = pygame.display.set_mode((1250, 650))
size = 25
x = 50
y = 50
clock = pygame.time.Clock()
recto = Rect(200, 500, 50, 50)


def move():
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

def player():
    global window, size, x, y, Player
    window.fill((255, 255, 255))
    Player = Rect(x, y, size, size)




# define a function for
# collision detection
'''
def crash():
global blockYPosition
if playerYPosition < (blockYPosition + pixel):

	if ((playerXPosition > blockXPosition
		and playerXPosition < (blockXPosition + pixel))
		or ((playerXPosition + pixel) > blockXPosition
		and (playerXPosition + pixel) < (blockXPosition + pixel))):

		blockYPosition = height + 1000
'''

while True:
    player()
    collide = pygame.Rect.colliderect(Player, recto)
    move()
    if collide:
        Player.bottom = recto.top
        #Player.top = recto.bottom
        #Player.right = recto.left
       # Player.left = recto.right
    pygame.draw.rect(window, (0, 0, 0), recto)
    pygame.draw.rect(window, (255, 0, 0), Player)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        speed = 1
    else:
        speed = 0.5
    x += (keys[pygame.K_d] - keys[pygame.K_a]) * speed
    y += (keys[pygame.K_s] - keys[pygame.K_w]) * speed
    pygame.display.update()



