import pygame

gravity = +0.6


def clip(val, min_val, max_val):
    return min(max(val, min_val), max_val)


class Player(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.direction = 0
        self.image = pygame.image.load('./src/player.png').convert_alpha()
        # self.image = pygame.Surface([25, 25])
        # self.image = self.image.convert()
        # self.image.fill((255, 255, 255))
        self.screen = screen
        self.rect = self.image.get_rect(x=screen.width * 0.5, y=screen.height)
        # self.rect.width, self.rect.height = 25, 25
        self.speed = [0.0, 0.0]
        self.width, self.height = screen.width, screen.height
        self.onGround = False
        self.friction = 1

    def flipPlayer(self):
        self.image = pygame.transform.flip(self.image, True, False)
        if self.direction == 0:
            self.direction = 1
        else:
            self.direction = 0

    def update(self):
        self.rect = self.rect.move(self.speed)
        if self.rect.left < 0 or self.rect.right > self.width:
            self.speed[0] = -self.speed[0] * 0.9
        if self.rect.top < 0 or self.rect.bottom > self.height:
            if self.speed[1] > 4:
                self.speed[1] = -self.speed[1] * 0.5
            else:
                self.speed[1] = 0
        if 0.1 > self.speed[0] > 0:
            self.speed[0] = 0
        if -0.1 < self.speed[0] < 0:
            self.speed[0] = 0
        if self.speed[1] == 0 or self.speed[1] == gravity:
            self.onGround = True
        else:
            self.onGround = False

        self.rect.left = clip(self.rect.left, 0, self.width)
        self.rect.right = clip(self.rect.right, 0, self.width)
        self.rect.top = clip(self.rect.top, 0, self.height)
        self.rect.bottom = clip(self.rect.bottom, 0, self.height)
        # print(self.speed)

    def move(self):
        self.speed[0] = self.speed[0] * 0.92
        key_down = pygame.key.get_pressed()
        if key_down[pygame.K_DOWN] or key_down[pygame.K_s]:
            self.speed[1] += 0.5
        if key_down[pygame.K_RIGHT] or key_down[pygame.K_d]:
            if self.direction == 1:
                self.flipPlayer()
            if key_down[pygame.K_LSHIFT]:
                self.speed[0] += 0.8
            else:
                self.speed[0] += 0.5
        if key_down[pygame.K_LEFT] or key_down[pygame.K_a]:
            if self.direction == 0:
                self.flipPlayer()
            if key_down[pygame.K_LSHIFT]:
                self.speed[0] -= 0.8
            else:
                self.speed[0] -= 0.5
        self.speed = [self.friction * s for s in self.speed]
        self.speed[1] += gravity
        pass

    def draw(self):
        self.screen.scene.blit(self.image, self.rect)
