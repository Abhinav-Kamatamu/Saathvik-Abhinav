import pygame
from pygame.locals import *

pygame.init()
window = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, group):
        super().__init__(group)
        self.top_limit = 0
        self.left_limit = 0
        self.bottom_limit = 500
        self.right_limit = 500

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
        self.speed = 3
        self.anim_speed = 0.1
        self.move_direction = pygame.math.Vector2()

    def move(self):
        self.move_direction = pygame.math.Vector2()
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
        keys = pygame.key.get_pressed()
        self.motion = False
        if keys[K_a] and self.rect.left > self.left_limit:
            self.move_direction.x = -1
            self.current_direction = 2
            self.motion = True
        if keys[K_d] and self.rect.right < self.right_limit:
            self.move_direction.x = 1
            self.current_direction = 3
            self.motion = True
        if keys[K_w] and self.rect.top > self.top_limit:
            self.move_direction.y = -1
            self.current_direction = 0
            self.motion = True
        if keys[K_s] and self.rect.bottom < self.bottom_limit:
            self.move_direction.y = 1
            self.current_direction = 1
            self.motion = True

        if self.move_direction.magnitude() != 0:
            self.move_direction = self.move_direction.normalize()

        self.pos += self.move_direction * self.speed

    def update(self):
        if not self.motion:
            self.image = self.images_static[self.current_direction]
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.pos[0], self.pos[1])

        if self.motion:

            if self.current_direction == 2:
                self.current_image += self.anim_speed
                if self.current_image >= 3:
                    self.current_image = 0
                self.image = self.images_left[int(self.current_image)]
                self.rect = self.image.get_rect()
                self.rect.topleft = (self.pos[0], self.pos[1])

            elif self.current_direction == 3:
                self.current_image += self.anim_speed
                if self.current_image >= 3:
                    self.current_image = 0
                self.image = self.images_right[int(self.current_image)]
                self.rect = self.image.get_rect()
                self.rect.topleft = (self.pos[0], self.pos[1])
            elif self.current_direction == 0:
                self.current_image += self.anim_speed
                if self.current_image >= 4:
                    self.current_image = 1
                self.image = self.images_up[int(self.current_image)]
                self.rect = self.image.get_rect()
                self.rect.topleft = (self.pos[0], self.pos[1])

            elif self.current_direction == 1:
                self.current_image += self.anim_speed
                if self.current_image >= 3:
                    self.current_image = 0
                self.image = self.images_down[int(self.current_image)]
                self.rect = self.image.get_rect()
                self.rect.topleft = (self.pos[0], self.pos[1])


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        self.display_surface = pygame.display.get_surface()
        self.camera_offset = pygame.math.Vector2()
        [self.half_w, self.half_h] = [self.display_surface.get_size()[0] // 2, self.display_surface.get_size()[1] // 2]

        self.ground_surface = pygame.image.load('TestMap.png').convert()
        self.ground_rect = self.ground_surface.get_rect(topleft=(0, 0))

    def centre_target_camera(self, target):
        self.camera_offset.x = target.rect.centerx - self.half_w
        self.camera_offset.y = target.rect.centery - self.half_h

    def custom_draw(self, target):
        self.centre_target_camera(target)
        self.display_surface.blit(self.ground_surface, self.ground_rect.topleft - self.camera_offset)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.camera_offset
            self.display_surface.blit(sprite.image, offset_pos)


camera_group = CameraGroup()
player = Player(234, 234, camera_group)
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    window.fill((0, 0, 0))
    player.move()
    camera_group.update()
    camera_group.custom_draw(player)
    pygame.display.update()
    clock.tick(60)
