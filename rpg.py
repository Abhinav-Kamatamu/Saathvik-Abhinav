import pygame
from pygame.locals import *

pygame.init()
window = pygame.display.set_mode((600, 500))
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.pos = [x, y]
        self.images_up = [pygame.image.load('Character/Up/Up_1.png'),
                          pygame.image.load('Character/Up/Up_2.png'),
                          pygame.image.load('Character/Up/Up_1.png'),
                          pygame.image.load('Character/Up/Up_3.png')]
        self.images_down = [pygame.image.load('Character/Down/Down_1.png'),
                            pygame.image.load('Character/Down/Down_2.png'),
                            pygame.image.load('Character/Down/Down_3.png')]
        self.images_left = [pygame.image.load('Character/Left/Left_1.png'),
                            pygame.image.load('Character/Left/Left_2.png'),
                            pygame.image.load('Character/Left/Left_3.png')]
        self.images_right = [pygame.image.load('Character/Right/Right_1.png'),
                             pygame.image.load('Character/Right/Right_2.png'),
                             pygame.image.load('Character/Right/Right_3.png')]
        self.images_static = [pygame.image.load('Character/Up/Up_Rest.png'),
                              pygame.image.load('Character/Down/Down_Rest.png'),
                              pygame.image.load('Character/Left/Left_Rest.png'),
                              pygame.image.load('Character/Right/Right_Rest.png')]
        self.current_direction = 0
        self.current_image = 0
        self.motion = False
        self.image = self.images_static[self.current_direction]
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.pos[0], self.pos[1])
        self.movement = pygame.math.Vector2()
        self.speed = 5
        self.anim_speed = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
        keys = pygame.key.get_pressed()
        if keys[K_a]:
            print('hi')
            self.movement[0] = -1
            self.pos[0] += self.movement[0] * self.speed
            print(self.pos)
            self.current_direction = 2
            self.motion = True
            self.current_image = 0
        elif keys[K_d]:
            self.movement[0] = 1
            self.pos[0] += self.movement[0] * self.speed
            self.current_direction = 3
            self.motion = True
            self.current_image = 0
        elif keys[K_w]:
            self.movement[1] = -1
            self.pos[1] += self.movement[1] * self.speed
            self.current_direction = 0
            self.motion = True
            self.current_image = 0
        elif keys[K_s]:
            self.movement[1] = 1
            self.pos[1] += self.movement[1] * self.speed
            self.current_direction = 1
            self.motion = True
            self.current_image = 0
        else:
            self.motion = False

    def update(self):
        if not self.motion:
            self.image = self.images_static[self.current_direction]
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.pos[0], self.pos[1])
        if self.motion:
            if self.current_image > 3:
                self.current_image = 0

            if self.current_direction == 0:
                self.current_image += self.anim_speed
                self.image = self.images_up[int(self.current_image)]
                self.rect = self.image.get_rect()
                self.rect.topleft = (self.pos[0], self.pos[1])

            if self.current_direction == 1:
                self.current_image += self.anim_speed
                self.image = self.images_down[int(self.current_image)]
                self.rect = self.image.get_rect()
                self.rect.topleft = (self.pos[0], self.pos[1])

            if self.current_direction == 2:
                self.current_image += self.anim_speed
                self.image = self.images_left[int(self.current_image)]
                self.rect = self.image.get_rect()
                self.rect.topleft = (self.pos[0], self.pos[1])

            if self.current_direction == 3:
                self.current_image += self.anim_speed
                self.image = self.images_right[int(self.current_image)]
                self.rect = self.image.get_rect()
                self.rect.topleft = (self.pos[0], self.pos[1])


sprite_group = pygame.sprite.Group()
player = Player(100, 100)
sprite_group.add(player)
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    window.fill((0, 0, 0))
    player.move()
    sprite_group.update()
    sprite_group.draw(window)
    pygame.display.update()
    clock.tick(60)
