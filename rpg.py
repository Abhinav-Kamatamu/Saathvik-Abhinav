import pygame
from pygame.locals import *

pygame.init()
window = pygame.display.set_mode((800, 600))
scaling = 3
backgroud_size = pygame.image.load('TestMap.png').get_size()
clock = pygame.time.Clock()


class StaticInvisibleObstacle(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups):
        super().__init__(groups)
        self.image = pygame.Surface(size)
        self.image.set_alpha(0)
        self.rect = self.image.get_rect(topleft=pos)
        self.old_rect = self.rect.copy()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, group, obstacles, scale, backgroundsize):
        super().__init__(group)  # This is to make it such that the player is a sprite and belongs to a group

        self.new_scale = (32 * scale, 32 * scale)
        self.pos = pygame.math.Vector2(x, y)
        self.images_up = [pygame.transform.scale(pygame.image.load('Character/Up/Up_1.png'), self.new_scale),
                          pygame.transform.scale(pygame.image.load('Character/Up/Up_2.png'), self.new_scale),
                          pygame.transform.scale(pygame.image.load('Character/Up/Up_3.png'), self.new_scale)]
        self.images_down = [pygame.transform.scale(pygame.image.load('Character/Down/Down_1.png'), self.new_scale),
                            pygame.transform.scale(pygame.image.load('Character/Down/Down_2.png'), self.new_scale),
                            pygame.transform.scale(pygame.image.load('Character/Down/Down_3.png'), self.new_scale)]
        self.images_left = [pygame.transform.scale(pygame.image.load('Character/Left/Left_1.png'), self.new_scale),
                            pygame.transform.scale(pygame.image.load('Character/Left/Left_2.png'), self.new_scale),
                            pygame.transform.scale(pygame.image.load('Character/Left/Left_3.png'), self.new_scale)]
        self.images_right = [pygame.transform.scale(pygame.image.load('Character/Right/Right_1.png'), self.new_scale),
                             pygame.transform.scale(pygame.image.load('Character/Right/Right_2.png'), self.new_scale),
                             pygame.transform.scale(pygame.image.load('Character/Right/Right_3.png'), self.new_scale)]
        self.images_static = [pygame.transform.scale(pygame.image.load('Character/Up/Up_Rest.png'), self.new_scale),
                              pygame.transform.scale(pygame.image.load('Character/Down/Down_Rest.png'), self.new_scale),
                              pygame.transform.scale(pygame.image.load('Character/Left/Left_Rest.png'), self.new_scale),
                              pygame.transform.scale(pygame.image.load('Character/Right/Right_Rest.png'),
                                                     self.new_scale)]

        self.current_direction = 0
        self.current_image = 0
        self.motion = False
        # Defining player movement limits
        self.top_limit = pygame.display.get_window_size()[1] // 2 - (self.new_scale[1] // 2) + 2
        self.left_limit = pygame.display.get_window_size()[0] // 2 - (self.new_scale[0] // 2) + 2
        self.bottom_limit = backgroundsize[1] * scale - pygame.display.get_window_size()[1] // 2 + (
                self.new_scale[1] // 2) - 2
        self.right_limit = backgroundsize[0] * scale - pygame.display.get_window_size()[0] // 2 + (
                self.new_scale[0] // 2) - 2

        self.image = self.images_static[self.current_direction]
        self.rect = self.image.get_rect(topleft=self.pos)

        self.obstacles = obstacles

        self.speed = 3
        self.anim_speed = 0.1
        self.move_direction = pygame.math.Vector2()
        self.old_rect = self.rect.copy()

    def collision(self, direction):
        collision_sprites = pygame.sprite.spritecollide(self, self.obstacles, False)
        if collision_sprites:
            if direction == 'horizontal':
                for sprite in collision_sprites:
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                        self.pos.x = self.rect.x
                    elif self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                        self.pos.x = self.rect.x
            elif direction == 'vertical':
                for sprite in collision_sprites:
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                        self.pos.y = self.rect.y
                    elif self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.pos.y = self.rect.y

    def input(self):
        self.move_direction = pygame.math.Vector2()
        self.motion = False

        keys = pygame.key.get_pressed()

        if keys[K_a] and self.rect.left > self.left_limit:
            self.move_direction.x = -1
            self.current_direction = 2
            self.motion = True
        elif keys[K_d] and self.rect.right < self.right_limit:
            self.move_direction.x = 1
            self.current_direction = 3
            self.motion = True
            print(self.right_limit, '\n', self.rect.right)
        if keys[K_w] and self.rect.top > self.top_limit:
            self.move_direction.y = -1
            self.current_direction = 0
            self.motion = True
        elif keys[K_s] and self.rect.bottom < self.bottom_limit:
            self.move_direction.y = 1
            self.current_direction = 1
            self.motion = True
        if keys[K_SPACE]:
            self.speed = 5
        else:
            self.speed = 3

    def update(self):
        self.old_rect = self.rect.copy()
        self.input()
        if self.move_direction.magnitude() != 0:
            self.move_direction = self.move_direction.normalize()

        self.pos.x += self.move_direction.x * self.speed
        self.rect.x = self.pos.x
        self.collision('horizontal')

        self.pos.y += self.move_direction.y * self.speed
        self.rect.y = self.pos.y
        self.collision('vertical')

        # display images for each direction
        if not self.motion:
            self.image = self.images_static[self.current_direction]
            self.rect = self.image.get_rect(topleft=self.pos)
        if self.motion:

            if self.current_direction == 2:
                self.current_image += self.anim_speed
                if self.current_image >= 3:
                    self.current_image = 0
                self.image = self.images_left[int(self.current_image)]
                self.rect = self.image.get_rect(topleft=self.pos)

            elif self.current_direction == 3:
                self.current_image += self.anim_speed
                if self.current_image >= 3:
                    self.current_image = 0
                self.image = self.images_right[int(self.current_image)]
                self.rect = self.image.get_rect(topleft=self.pos)
            elif self.current_direction == 0:
                self.current_image += self.anim_speed
                if self.current_image >= 3:
                    self.current_image = 0
                self.image = self.images_up[int(self.current_image)]
                self.rect = self.image.get_rect(topleft=self.pos)

            elif self.current_direction == 1:
                self.current_image += self.anim_speed
                if self.current_image >= 3:
                    self.current_image = 0
                self.image = self.images_down[int(self.current_image)]
                self.rect = self.image.get_rect(topleft=self.pos)


class CameraGroup(pygame.sprite.Group):
    def __init__(self, scale, image_size):
        super().__init__()

        self.display_surface = pygame.display.get_surface()
        self.camera_offset = pygame.math.Vector2()
        [self.half_w, self.half_h] = [self.display_surface.get_size()[0] // 2, self.display_surface.get_size()[1] // 2]

        self.ground_surface = pygame.transform.scale(pygame.image.load('TestMap.png').convert(),
                                                     (image_size[0] * scale, image_size[0] * scale))
        self.ground_rect = self.ground_surface.get_rect(topleft=(0, 0))

    def centre_target_camera(self, target):
        self.camera_offset.x = target.rect.centerx - self.half_w
        self.camera_offset.y = target.rect.centery - self.half_h

    def custom_draw(self, target):
        self.centre_target_camera(target)
        self.display_surface.blit(self.ground_surface, self.ground_rect.topleft - self.camera_offset)

        for sprite in sorted(self.sprites(), key=lambda sprites: sprites.rect.centery):
            offset_pos = sprite.rect.topleft - self.camera_offset
            self.display_surface.blit(sprite.image, offset_pos)


camera_group = CameraGroup(scaling, backgroud_size)
obstacle_group = pygame.sprite.Group()

Obstacle1 = StaticInvisibleObstacle((0, 50 * scaling), (400 * scaling, 50 * scaling), [obstacle_group, camera_group])
Obstacle2 = StaticInvisibleObstacle((250 * scaling, 100 * scaling), (150 * scaling, 200 * scaling),
                                    [obstacle_group, camera_group])
Obstacle3 = StaticInvisibleObstacle((50 * scaling, 150 * scaling), (150 * scaling, 150 * scaling),
                                    [obstacle_group, camera_group])
Obstacle4 = StaticInvisibleObstacle((0, 350 * scaling), (200 * scaling, 150 * scaling), [obstacle_group, camera_group])
Obstacle5 = StaticInvisibleObstacle((450 * scaling, 0), (50 * scaling, 500 * scaling), [obstacle_group, camera_group])
Obstacle6 = StaticInvisibleObstacle((250 * scaling, 350 * scaling), (150 * scaling, 150 * scaling),
                                    [obstacle_group, camera_group])

player = Player(218 * scaling, 218 * scaling, camera_group, obstacle_group, scaling, backgroud_size)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    window.fill((0, 0, 0))
    camera_group.update()
    camera_group.custom_draw(player)
    pygame.display.update()
    clock.tick(60)