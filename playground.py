import sys
import os
import pygame

delta = {
    pygame.K_UP: (0, -16),
    pygame.K_SPACE: (0, -16),
}

gravity = +1


def clip(val, min_val, max_val):
    return min(max(val, min_val), max_val)


class GenerateBarrages:
    def __init__(self, screen):
        self.screen = screen

    def update(self):
        self.screen.music_pos = pygame.mixer.music.get_pos()
        if self.screen.timing < len(self.screen.beatmap['TimingPoints']):
            if self.screen.music_pos > float(self.screen.beatmap['TimingPoints'][self.screen.timing]['time']):
                ctiming = self.screen.beatmap['TimingPoints'][self.screen.timing]
                self.screen.kiai = int(ctiming['effects'])
                self.screen.timing += 1
        if self.screen.beat < len(self.screen.beatmap['HitObjects']):
            if self.screen.music_pos > float(self.screen.beatmap['HitObjects'][self.screen.beat]['time']):
                cbeat = self.screen.beatmap['HitObjects'][self.screen.beat]
                print(cbeat)
                self.screen.beat += 1
                if int(cbeat['type']) == 6:
                    self.generateSquare1(x=int(cbeat['x']) * 2, y=int(cbeat['y']) * 1.3)
                elif int(cbeat['type']) == 5:
                    self.generateSquare(x=int(cbeat['x']) * 2, y=int(cbeat['y']) * 1.3)
                elif int(cbeat['type']) == 2:
                    if self.screen.kiai == 1:
                        self.genLight(x=int(cbeat['x']) * 2, y=int(cbeat['y']) * 1.3)
                    self.generateSquare2(x=int(cbeat['x']) * 2, y=int(cbeat['y']) * 1.3)
                elif int(cbeat['type']) > 10:
                    self.generateSquare1(x=int(cbeat['x']) * 2, y=int(cbeat['y']) * 1.3)
                else:
                    if self.screen.kiai == 1:
                        self.genLight(x=int(cbeat['x']) * 2, y=int(cbeat['y']) * 1.3)
                    self.generateBarrage(x=int(cbeat['x']) * 2, y=int(cbeat['y']) * 1.3)
        if self.screen.kiai == 1:
            self.set_background_alpha(120)

    def set_background_alpha(self, alpha):
        self.screen.background.alphablack = alpha

    def genLight(self, x, y):
        light = Light(self.screen, x=x, y=y)
        self.screen.lights.add(light)

    def generateBarrage(self, x, y):
        barrage = Barrage(self.screen, x=x, y=y)
        # barrage.speed[0] = random.randint(-20, 20)
        # barrage.speed[1] = random.randint(-20, 0)
        self.screen.barragesGrav.add(barrage)

    def generateSquare1(self, x, y):
        speed = [2.5 * self.screen.barrage_speed, 2.5 * self.screen.barrage_speed, 5 * self.screen.barrage_speed]
        barrage = Barrage(self.screen, x=x, y=y)
        barrage.speed[0] = speed[0]
        barrage.speed[1] = speed[1]
        self.screen.barrages.add(barrage)
        barrage = Barrage(self.screen, x=x, y=y)
        barrage.speed[0] = -speed[0]
        barrage.speed[1] = -speed[1]
        self.screen.barrages.add(barrage)
        barrage = Barrage(self.screen, x=x, y=y)
        barrage.speed[0] = -speed[0]
        barrage.speed[1] = speed[1]
        self.screen.barrages.add(barrage)
        barrage = Barrage(self.screen, x=x, y=y)
        barrage.speed[0] = speed[0]
        barrage.speed[1] = -speed[1]
        self.screen.barrages.add(barrage)
        barrage = Barrage(self.screen, x=x, y=y)
        barrage.speed[0] = 0
        barrage.speed[1] = speed[2]
        self.screen.barrages.add(barrage)
        barrage = Barrage(self.screen, x=x, y=y)
        barrage.speed[0] = speed[2]
        barrage.speed[1] = 0
        self.screen.barrages.add(barrage)
        barrage = Barrage(self.screen, x=x, y=y)
        barrage.speed[0] = 0
        barrage.speed[1] = -speed[2]
        self.screen.barrages.add(barrage)
        barrage = Barrage(self.screen, x=x, y=y)
        barrage.speed[0] = -speed[2]
        barrage.speed[1] = 0
        self.screen.barrages.add(barrage)
        pass

    def generateSquare2(self, x, y):
        speed = [5.5 * self.screen.barrage_speed]
        barrage = Barrage(self.screen, x=x, y=y)
        barrage.speed[0] = 0
        barrage.speed[1] = speed[0]
        self.screen.barrages.add(barrage)
        barrage = Barrage(self.screen, x=x, y=y)
        barrage.speed[0] = speed[0]
        barrage.speed[1] = 0
        self.screen.barrages.add(barrage)
        barrage = Barrage(self.screen, x=x, y=y)
        barrage.speed[0] = 0
        barrage.speed[1] = -speed[0]
        self.screen.barrages.add(barrage)
        barrage = Barrage(self.screen, x=x, y=y)
        barrage.speed[0] = -speed[0]
        barrage.speed[1] = 0
        self.screen.barrages.add(barrage)
        pass

    def generateSquare(self, x, y):
        speed = [5 * self.screen.barrage_speed, 5 * self.screen.barrage_speed]
        barrage = Barrage(self.screen, x=x, y=y)
        barrage.speed[0] = speed[0]
        barrage.speed[1] = speed[1]
        self.screen.barrages.add(barrage)
        barrage = Barrage(self.screen, x=x, y=y)
        barrage.speed[0] = -speed[0]
        barrage.speed[1] = -speed[1]
        self.screen.barrages.add(barrage)
        barrage = Barrage(self.screen, x=x, y=y)
        barrage.speed[0] = -speed[0]
        barrage.speed[1] = speed[1]
        self.screen.barrages.add(barrage)
        barrage = Barrage(self.screen, x=x, y=y)
        barrage.speed[0] = speed[0]
        barrage.speed[1] = -speed[1]
        self.screen.barrages.add(barrage)
        barrage = Barrage(self.screen, x=x, y=y)
        barrage.speed[0] = 0
        barrage.speed[1] = speed[1]
        self.screen.barrages.add(barrage)
        barrage = Barrage(self.screen, x=x, y=y)
        barrage.speed[0] = speed[0]
        barrage.speed[1] = 0
        self.screen.barrages.add(barrage)
        barrage = Barrage(self.screen, x=x, y=y)
        barrage.speed[0] = 0
        barrage.speed[1] = -speed[1]
        self.screen.barrages.add(barrage)
        barrage = Barrage(self.screen, x=x, y=y)
        barrage.speed[0] = -speed[0]
        barrage.speed[1] = 0
        self.screen.barrages.add(barrage)
        pass


class Light(pygame.sprite.Sprite):
    def __init__(self, screen, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.image = pygame.image.load('./src/lighting.png')
        self.rect = self.image.get_rect(x=x - 92, y=y - 92)
        self.alpha = 255

    def update(self):
        self.image.set_alpha(self.alpha)
        self.alpha -= 5
        if self.alpha <= 0:
            self.kill()

    def draw(self):
        self.screen.scene.blit(self.image, self.rect)


class Barrage(pygame.sprite.Sprite):
    def __init__(self, screen, x=0, y=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./src/bullet.png')
        self.image = pygame.transform.scale(self.image, (24, 24))
        # self.image = pygame.Surface([14, 14])
        # self.image = self.image.convert()
        # self.image.fill((255, 23, 140))
        self.screen = screen
        # self.rect = self.image.get_rect(x=random.randint(0, screen.width), y=random.randint(0, screen.height / 3))
        self.rect = self.image.get_rect(x=x, y=y)
        self.rect.width, self.rect.height = 12, 12
        self.speed = [0.0, 0.0]
        self.width, self.height = screen.width, screen.height

    def update(self):
        self.rect = self.rect.move(self.speed)

        if self.rect.top < 0:
            self.kill()

        if self.rect.left < 0 or self.rect.right > self.width or self.rect.bottom > self.height:
            self.screen.combo += 1
            self.screen.points += int(100 * (self.screen.combo / 25))  # 算分
            self.kill()
            if self.screen.health < 100:
                self.screen.health += 1

        self.rect.left = clip(self.rect.left, 0, self.width)
        self.rect.right = clip(self.rect.right, 0, self.width)
        self.rect.top = clip(self.rect.top, 0, self.height)
        self.rect.bottom = clip(self.rect.bottom, 0, self.height)

    def draw(self):
        self.screen.scene.blit(self.image, self.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.direction = 0
        self.image = pygame.image.load('./src/player.png')
        # self.image = pygame.Surface([25, 25])
        # self.image = self.image.convert()
        # self.image.fill((255, 255, 255))
        self.screen = screen
        self.rect = self.image.get_rect(x=screen.width * 0.5, y=screen.height)
        # self.rect.width, self.rect.height = 25, 25
        self.speed = [0.0, 0.0]
        self.width, self.height = screen.width, screen.height
        self.onGround = False

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
        if self.speed[1] == 0:
            self.onGround = True
        else:
            self.onGround = False

        self.rect.left = clip(self.rect.left, 0, self.width)
        self.rect.right = clip(self.rect.right, 0, self.width)
        self.rect.top = clip(self.rect.top, 0, self.height)
        self.rect.bottom = clip(self.rect.bottom, 0, self.height)
        # print(self.speed)

    def draw(self):
        self.screen.scene.blit(self.image, self.rect)


class HealthBar(object):
    def __init__(self, screen):
        self.screen = screen
        self.max_w = 300
        self.bar_background = pygame.Surface([310, 30]).convert()
        self.bar_background.fill((255, 255, 255))
        self.bar_background.set_alpha(200)
        # self.background = pygame.image.load("src/background.jpg")

    def draw(self, w):
        bar = pygame.Surface([max(min(w * 3, self.max_w), 0), 20])
        bar = bar.convert()
        bar.fill((240, 0, 0))
        self.screen.scene.blit(self.bar_background, (5, 5))
        self.screen.scene.blit(bar, (10, 10))


class Score(object):
    def __init__(self, screen):
        self.screen = screen
        self.Font = pygame.font.Font('./src/sarasa-mono-sc-regular.ttf', 60)
        # self.background = pygame.image.load("src/background.jpg")

    def draw(self):
        score = self.Font.render(str(format(self.screen.points, '0>8d')), True, (255, 255, 255))
        score_rect = score.get_rect()
        self.screen.scene.blit(score, (self.screen.width - score_rect.right - 20, -10))


class Combo(object):
    def __init__(self, screen):
        self.screen = screen
        self.combo = 0
        self.Font = pygame.font.Font('./src/sarasa-mono-sc-regular.ttf', 60)
        # self.background = pygame.image.load("src/background.jpg")

    def draw(self):
        if self.combo < self.screen.combo:
            self.combo = self.screen.combo
        elif self.combo > 1 and self.combo > self.screen.combo:
            self.combo -= 1
        combo_text = self.Font.render(str(self.combo) + 'x', True, (255, 255, 255))
        self.screen.scene.blit(combo_text, (10, self.screen.height - 80))


class Time(object):
    def __init__(self, screen):
        self.screen = screen
        self.Font = pygame.font.Font('./src/sarasa-mono-sc-regular.ttf', 30)
        # self.background = pygame.image.load("src/background.jpg")

    def draw(self):
        # time_delta = pygame.time.get_ticks() - self.screen.start_time
        mts = str(format(int(self.screen.music_pos / 60000), '0>2d'))
        sec = str(format(int(self.screen.music_pos / 1000 % 60), '0>2d'))
        ml = str(format(int(self.screen.music_pos % 1000), '0>2d'))[0:2]
        if mts != '00':
            time = self.Font.render(mts + ":" + sec + ":" + ml, True, (255, 255, 255))
        else:
            time = self.Font.render(sec + ":" + ml, True, (255, 255, 255))

        time_rect = time.get_rect()
        self.screen.scene.blit(time, (self.screen.width - time_rect.right - 20, 50))


class GameBackground(object):
    def __init__(self, screen, img):
        self.screen = screen
        self.background = pygame.image.load(img)
        self.alphared = 0
        self.alphablack = 180
        # self.background = pygame.transform.scale(self.background, (self.screen.width, self.screen.height))
        self.background = pygame.transform.scale(self.background, (1024, 600))
        self.backgroundback = pygame.Surface(self.screen.scene.get_size()).convert()
        self.backgroundback.fill((0, 0, 0))
        self.backgroundback.set_alpha(180)
        self.backgroundred = pygame.Surface(self.screen.scene.get_size()).convert()
        self.backgroundred.fill((240, 0, 0))

    def update(self):
        self.backgroundred.set_alpha(self.alphared)
        if self.alphared >= 0:
            self.alphared -= 5
        self.backgroundback.set_alpha(self.alphablack)
        if self.alphablack <= 175:
            self.alphablack += 1

    def draw(self):
        self.screen.scene.blit(self.background, (0, 84))
        self.screen.scene.blit(self.backgroundback, (0, 0))
        self.screen.scene.blit(self.backgroundred, (0, 0))


class Playground(object):
    def __init__(self, main, song, song_path):
        self.main = main
        (self.width, self.height) = (main.width, main.height)
        self.scene = main.scene
        self.beatmap = song
        pygame.mixer.music.load(os.path.join(song_path, self.beatmap['General']['audio_filename'].strip()))
        pygame.mixer.music.play()
        # self.start_time = pygame.time.get_ticks()
        self.music_pos = pygame.mixer.music.get_pos()
        self.player = Player(self)
        self.gb = GenerateBarrages(self)
        self.barrages = pygame.sprite.Group()
        self.lights = pygame.sprite.Group()
        self.barragesGrav = pygame.sprite.Group()
        self.background = GameBackground(self,
                                         os.path.join(song_path, self.beatmap['Events'][0]['Backgroundimg'].strip()))
        self.healthBar = HealthBar(self)
        self.time = Time(self)
        self.score = Score(self)
        self.combot = Combo(self)
        self.beat = 0
        self.timing = 0
        self.kiai = 0
        self.esc_time = 0
        self.health = 100
        self.points = 0
        self.combo = 0
        self.max_combo = 0
        self.frame_time = 0
        self.jump_state = 2
        self.friction = 1
        self.barrage_speed = 1.3

    def draw(self):
        self.background.draw()
        self.player.draw()
        self.barragesGrav.draw(self.scene)
        self.barrages.draw(self.scene)
        self.lights.draw(self.scene)
        self.score.draw()
        self.combot.draw()
        self.time.draw()
        self.healthBar.draw(self.health)
        pygame.display.update()

    def update(self):
        self.gb.update()
        self.player.update()
        self.barragesGrav.update()
        self.barrages.update()
        self.lights.update()
        self.background.update()

    def run(self):
        if True:
            self.music_pos = pygame.mixer.music.get_pos()
            # print(self.music_pos)
            if self.combo > self.max_combo:
                self.max_combo = self.combo
            if self.combo > 30 and self.health < 100:
                self.health += 0.2
            if self.health <= 0:
                self.main.game_end = True
            elif self.music_pos == -1:
                self.main.game_end = True
                self.main.stat = 1
            else:
                pygame.display.set_caption(
                    self.beatmap['Metadata']['artist_unicode'] + ' - ' + self.beatmap['Metadata'][
                        'title_unicode'] + ' (' + self.beatmap['Metadata']['version'] + ')')
            self.frame_time += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    deltax, deltay = delta.get(event.key, (0, 0))
                    if 1 < self.jump_state <= 2:
                        self.jump_state -= 1
                        self.player.speed[1] = deltay
                        self.friction = 1
                elif event.type == pygame.KEYUP:
                    self.friction = 0.99
            if self.player.onGround:
                self.jump_state = 2
            self.player.speed[0] = self.player.speed[0] * 0.92
            key_down = pygame.key.get_pressed()

            if key_down[pygame.K_ESCAPE]:
                self.esc_time += 1
                self.background.alphared += 7
                if self.esc_time > 60:
                    self.main.game_end = True
                    self.main.stat = 2
            else:
                self.esc_time = 0
            if key_down[pygame.K_DOWN]:
                self.player.speed[1] += 0.5
            if key_down[pygame.K_RIGHT]:
                if self.player.direction == 1:
                    self.player.flipPlayer()
                if key_down[pygame.K_LSHIFT]:
                    self.player.speed[0] += 1
                else:
                    self.player.speed[0] += 0.6
            if key_down[pygame.K_LEFT]:
                if self.player.direction == 0:
                    self.player.flipPlayer()
                if key_down[pygame.K_LSHIFT]:
                    self.player.speed[0] -= 1
                else:
                    self.player.speed[0] -= 0.6
            self.player.speed = [self.friction * s for s in self.player.speed]
            for barrage in self.barragesGrav.sprites():
                barrage.speed = [0.97 * s for s in barrage.speed]
                barrage.speed[1] += 0.3  # 解除弹幕速度限制

            self.player.speed[1] += gravity
            self.update()
            self.draw()
            # for barrage in self.barrages.sprites():
            #     pygame.sprite.collide_mask(self.player, barrage)
            #     barrage.kill()
            #     self.health -= 40
            #     self.combo = 0
            if pygame.sprite.spritecollide(self.player, self.barrages, True):
                if self.combo > 50:
                    self.health -= 60
                    self.background.alphared = 90
                else:
                    self.health -= 30
                    self.background.alphared = 120
                self.combo = 0
            if pygame.sprite.spritecollide(self.player, self.barragesGrav, True):
                if self.combo > 50:
                    self.health -= 60
                    self.background.alphared = 90
                else:
                    self.health -= 30
                    self.background.alphared = 120
                self.combo = 0
