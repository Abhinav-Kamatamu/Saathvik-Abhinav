import pygame
from pygame.locals import *

pygame.init()
window = pygame.display.set_mode((800, 600))
scaling = 3  # dont set above 10. --> cuz computer will CRASH BADLY!!!
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
        self.zoom = scale
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

        self.speed = 3 * self.zoom
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
        if keys[K_w] and self.rect.top > self.top_limit:
            self.move_direction.y = -1
            self.current_direction = 0
            self.motion = True
        elif keys[K_s] and self.rect.bottom < self.bottom_limit:
            self.move_direction.y = 1
            self.current_direction = 1
            self.motion = True
        if keys[K_SPACE]:
            self.speed = 5 * self.zoom
        else:
            self.speed = 3 * self.zoom

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


class Game:
    def __init__(self):
        self.game_mode = 'menu'
        self.screens = [self.menuScreen]
        self.is_fade = False
        self.fade_value = 0
        self.un_fade = False
        self.fade_screens = []
        self.fade_speed = 10

    def menuScreen(self):
        window.fill((0, 0, 0))
        self.menu_image = pygame.image.load('Menu.png')
        self.play_button_image = pygame.image.load('Play_button.png')
        self.play_rect = self.play_button_image.get_rect(topleft=(350, 300))
        self.image_2 = pygame.image.load('Play_button.png')
        self.image2_rect = self.play_button_image.get_rect(topleft=(350, 400))
        window.blit(self.menu_image, (0, 0))
        window.blit(self.play_button_image, self.play_rect)
        window.blit(self.image_2, self.image2_rect)

    def if_clicked(self, pos):
        if self.play_rect.collidepoint(pos):
            self.fade_screens = [self.menuScreen, self.mainGame]
            self.is_fade = True

    def initiateMainGame(self):
        self.camera_group = CameraGroup(scaling, backgroud_size)
        self.obstacle_group = pygame.sprite.Group()

        self.Obstacle1 = StaticInvisibleObstacle((0, 50 * scaling), (400 * scaling, 50 * scaling),
                                                 [self.obstacle_group, self.camera_group])
        self.Obstacle2 = StaticInvisibleObstacle((250 * scaling, 100 * scaling), (150 * scaling, 200 * scaling),
                                                 [self.obstacle_group, self.camera_group])
        self.Obstacle3 = StaticInvisibleObstacle((50 * scaling, 150 * scaling), (150 * scaling, 150 * scaling),
                                                 [self.obstacle_group, self.camera_group])
        self.Obstacle4 = StaticInvisibleObstacle((0, 350 * scaling), (200 * scaling, 150 * scaling),
                                                 [self.obstacle_group, self.camera_group])
        self.Obstacle5 = StaticInvisibleObstacle((450 * scaling, 0), (50 * scaling, 500 * scaling),
                                                 [self.obstacle_group, self.camera_group])
        self.Obstacle6 = StaticInvisibleObstacle((250 * scaling, 350 * scaling), (150 * scaling, 150 * scaling),
                                                 [self.obstacle_group, self.camera_group])
        self.player = Player(218 * scaling, 218 * scaling, self.camera_group, self.obstacle_group, scaling,
                             backgroud_size)

    def fade(self):
        if not self.un_fade:
            self.fade_screens[0]()
            self.block_surf = pygame.Surface((800, 600))
            self.block_surf.fill((0, 0, 0))
            self.block_surf.set_alpha(self.fade_value)
            window.blit(self.block_surf, (0, 0))
            self.fade_value += self.fade_speed
            if self.fade_value >= 256:
                self.fade_value = 255
                self.un_fade = True
            pygame.display.update()
        else:
            self.fade_screens[1]()
            self.block_surf = pygame.Surface((800, 600))
            self.block_surf.fill((0, 0, 0))
            self.block_surf.set_alpha(self.fade_value)
            window.blit(self.block_surf, (0, 0))
            self.fade_value -= self.fade_speed
            if self.fade_value < 0:
                self.fade_value = 0
                self.un_fade = False
                self.screens = [self.fade_screens[1]]
                self.fade_screens = []
                self.is_fade = False
                self.game_mode = "main_game"

    def mainGame(self):
        window.fill((0, 0, 0))
        self.camera_group.update()
        self.camera_group.custom_draw(self.player)

    def run(self):
        for i in self.screens:
            i()


game = Game()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == MOUSEBUTTONDOWN and game.game_mode == 'menu':
            game.initiateMainGame()
            game.if_clicked(event.pos)
    game.run()
    if game.is_fade:
        game.fade()
    pygame.display.update()
    clock.tick(60)
