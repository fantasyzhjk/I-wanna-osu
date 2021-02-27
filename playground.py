import sys
import os
import pygame
from mutagen.mp3 import MP3
from config import Settings

delta = {
    pygame.K_UP: (0, -16),
    pygame.K_SPACE: (0, -16),
}

getindex = {1: 'normal', 2: 'soft', 3: 'drum'}

gravity = +1


def clip(val, min_val, max_val):
    return min(max(val, min_val), max_val)


class GenerateBarrages:
    def __init__(self, screen):
        self.screen = screen
        # print(self.screen.beatmap['HitObjects'])

    def update(self):
        if self.screen.timing < len(self.screen.beatmap['TimingPoints']):
            if self.screen.music_pos + Settings.offset > float(
                    self.screen.beatmap['TimingPoints'][
                        self.screen.timing]['time']):
                self.ctiming = self.screen.beatmap['TimingPoints'][
                    self.screen.timing]
                self.screen.kiai = int(self.ctiming['effects'])
                self.screen.timing += 1
        try:
            while self.screen.music_pos + Settings.offset > float(
                    self.screen.beatmap['HitObjects'][
                        self.screen.beat]['time']):
                cbeat = self.screen.beatmap['HitObjects'][self.screen.beat]
                # print(cbeat)
                # print(self.ctiming)
                try:
                    soundFile = os.path.join(
                        self.screen.song_path,
                        getindex[int(self.ctiming['sample_set'])] +
                        '-hitnormal.wav')
                    if not os.path.isfile(soundFile):
                        soundFile = './src/sounds/' + getindex[int(
                            self.ctiming['sample_set'])] + '-hitnormal.wav'
                    music = pygame.mixer.Sound(soundFile)
                    music.set_volume((int(self.ctiming['volume']) / 100) *
                                     Settings.volume * Settings.note_volume)
                    music.play()
                    if cbeat['time'] == self.ctiming['time']:
                        hitsound = int(cbeat['hitsound'])
                        if hitsound - 8 >= 0:
                            hitsound -= 8
                            sampleIndex = self.ctiming['sample_index']
                            if sampleIndex == '0' or sampleIndex == '1':
                                sampleIndex = ''
                            soundFile = os.path.join(
                                self.screen.song_path,
                                getindex[int(self.ctiming['sample_set'])] +
                                '-hit' + 'clap' + sampleIndex + '.wav')
                            if not os.path.isfile(soundFile):
                                soundFile = './src/sounds/' + getindex[int(
                                    self.ctiming['sample_set']
                                )] + '-hitclap.wav'
                            music = pygame.mixer.Sound(soundFile)
                            music.set_volume(
                                (int(self.ctiming['volume']) / 100) *
                                Settings.volume * Settings.note_volume)
                            music.play()
                        if hitsound - 4 >= 0:
                            hitsound -= 4
                            sampleIndex = self.ctiming['sample_index']
                            if sampleIndex == '0' or sampleIndex == '1':
                                sampleIndex = ''
                            soundFile = os.path.join(
                                self.screen.song_path,
                                getindex[int(self.ctiming['sample_set'])] +
                                '-hitfinish' + sampleIndex + '.wav')
                            if not os.path.isfile(soundFile):
                                soundFile = './src/sounds/' + getindex[int(
                                    self.ctiming['sample_set']
                                )] + '-hitfinish.wav'
                            music = pygame.mixer.Sound(soundFile)
                            music.set_volume(
                                (int(self.ctiming['volume']) / 100) *
                                Settings.volume * Settings.note_volume)
                            music.play()
                        if hitsound - 2 >= 0:
                            hitsound -= 2
                            sampleIndex = self.ctiming['sample_index']
                            if sampleIndex == '0' or sampleIndex == '1':
                                sampleIndex = ''
                            soundFile = os.path.join(
                                self.screen.song_path,
                                getindex[int(self.ctiming['sample_set'])] +
                                '-hit' + 'whistle' + sampleIndex + '.wav')
                            if not os.path.isfile(soundFile):
                                soundFile = './src/sounds/' + getindex[int(
                                    self.ctiming['sample_set']
                                )] + '-hitwhistle.wav'
                            music = pygame.mixer.Sound(soundFile)
                            music.set_volume(
                                (int(self.ctiming['volume']) / 100) *
                                Settings.volume * Settings.note_volume)
                            music.play()
                except AttributeError:
                    pass
                self.screen.beat += 1
                if int(cbeat['type']) == 6:
                    self.generateSquare1(x=int(cbeat['x']) * 2,
                                         y=int(cbeat['y']) * 1.3)
                elif int(cbeat['type']) == 5:
                    self.generateSquare(x=int(cbeat['x']) * 2,
                                        y=int(cbeat['y']) * 1.3)
                elif int(cbeat['type']) == 2:
                    if self.screen.kiai == 1:
                        self.genLight(x=int(cbeat['x']) * 2,
                                      y=int(cbeat['y']) * 1.3)
                    self.generateSquare2(x=int(cbeat['x']) * 2,
                                         y=int(cbeat['y']) * 1.3)
                elif int(cbeat['type']) > 10:
                    self.generateSquare1(x=int(cbeat['x']) * 2,
                                         y=int(cbeat['y']) * 1.3)
                else:
                    if self.screen.kiai == 1:
                        self.genLight(x=int(cbeat['x']) * 2,
                                      y=int(cbeat['y']) * 1.3)
                    self.generateBarrage(x=int(cbeat['x']) * 2,
                                         y=int(cbeat['y']) * 1.3)
        except IndexError:
            pass

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
        speed = [
            2.5 * self.screen.barrage_speed, 2.5 * self.screen.barrage_speed,
            5 * self.screen.barrage_speed
        ]
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
        self.image = pygame.image.frombuffer(self.screen.light_image,
                                             (184, 184), 'RGBA')
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
        self.screen = screen
        self.image = self.screen.barrage_image
        # self.image = pygame.Surface([14, 14])
        # self.image = self.image.convert()
        # self.image.fill((255, 23, 140))
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
            self.screen.points += int(200 * (self.screen.combo / 25))  # 算分
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


class ProgressBar(object):  # 歌曲进度条
    def __init__(self, screen):
        self.screen = screen
        self.max_w = 300
        self.bar_background = pygame.Surface([self.screen.width, 5]).convert()
        self.bar_background.fill((100, 100, 100))
        self.bar_background.set_alpha(100)
        # self.background = pygame.image.load("src/background.jpg")

    def draw(self):
        bar = pygame.Surface([
            ((self.screen.music_pos / (self.screen.audio.info.length * 1000)) *
             self.screen.width), 5
        ])
        bar = bar.convert()
        bar.fill((225, 225, 225))
        bar.set_alpha(100)
        self.screen.scene.blit(self.bar_background,
                               (0, self.screen.height - 5))
        self.screen.scene.blit(bar, (0, self.screen.height - 5))


class Score(object):
    def __init__(self, screen):
        self.screen = screen
        self.Font = pygame.font.Font(Settings.font, 60)
        # self.background = pygame.image.load("src/background.jpg")

    def draw(self):
        score = self.Font.render(str(format(self.screen.points, '0>8d')), True,
                                 (255, 255, 255))
        score_rect = score.get_rect()
        self.screen.scene.blit(
            score, (self.screen.width - score_rect.right - 20, -10))


class Combo(object):
    def __init__(self, screen):
        self.screen = screen
        self.combo = 0
        self.Font = pygame.font.Font(Settings.font, 60)
        # self.background = pygame.image.load("src/background.jpg")

    def draw(self):
        self.combo = self.screen.combo
        combo_text = self.Font.render(
            str(self.combo) + 'x', True, (255, 255, 255))
        self.screen.scene.blit(combo_text, (10, self.screen.height - 80))


class Time(object):
    def __init__(self, screen):
        self.screen = screen
        self.Font = pygame.font.Font(Settings.font, 30)
        # self.background = pygame.image.load("src/background.jpg")

    def draw(self):
        # time_delta = pygame.time.get_ticks() - self.screen.start_time
        mts = str(format(int(self.screen.music_pos / 60000), '0>2d'))
        sec = str(format(int(self.screen.music_pos / 1000 % 60), '0>2d'))
        ml = str(format(int(self.screen.music_pos % 1000), '0>2d'))[0:2]
        if mts != '00':
            time = self.Font.render(mts + ":" + sec + ":" + ml, True,
                                    (255, 255, 255))
        else:
            time = self.Font.render(sec + ":" + ml, True, (255, 255, 255))

        time_rect = time.get_rect()
        self.screen.scene.blit(time,
                               (self.screen.width - time_rect.right - 20, 50))


class GameBackground(object):
    def __init__(self, screen, img):
        self.screen = screen
        self.alphared = 0
        self.alphablack = 180
        # self.background = pygame.transform.scale(self.background, (self.screen.width, self.screen.height))
        try:
            self.background = img
            self.background = pygame.transform.smoothscale(
                self.background, (1024, 576))
        except FileNotFoundError:
            self.background = pygame.Surface(
                self.screen.scene.get_size()).convert()
            self.background.fill((0, 0, 0))
        self.backgroundback = pygame.Surface(
            self.screen.scene.get_size()).convert()
        self.backgroundback.fill((0, 0, 0))
        self.backgroundback.set_alpha(180)
        self.backgroundred = pygame.Surface(
            self.screen.scene.get_size()).convert()
        self.backgroundred.fill((240, 0, 0))

    def update(self):
        self.backgroundred.set_alpha(self.alphared)
        if self.alphared >= 0:
            self.alphared -= 5
        self.backgroundback.set_alpha(self.alphablack)
        if self.alphablack <= 175:
            self.alphablack += 1

    def draw(self):
        self.screen.scene.blit(self.background, (0, 96))
        self.screen.scene.blit(self.backgroundback, (0, 0))
        self.screen.scene.blit(self.backgroundred, (0, 0))


class Playground(object):
    def __init__(self, main, song, song_path):
        self.main = main
        (self.width, self.height) = (main.width, main.height)
        self.scene = main.scene
        self.song_path = song_path
        self.beatmap = song
        title = 'unknown'
        if 'artist_unicode' in self.beatmap[
                'Metadata'] and 'title_unicode' in self.beatmap['Metadata']:
            title = self.beatmap['Metadata'][
                'artist_unicode'] + ' - ' + self.beatmap['Metadata'][
                    'title_unicode'] + ' (' + self.beatmap['Metadata'][
                        'version'] + ')'
        else:
            title = self.beatmap['Metadata']['artist'] + ' - ' + self.beatmap[
                'Metadata']['title'] + ' (' + self.beatmap['Metadata'][
                    'version'] + ')'
        pygame.display.set_caption(title)
        self.light_image = pygame.image.tostring(
            pygame.image.load('./src/lighting.png').convert_alpha(), 'RGBA')
        self.barrage_image = pygame.transform.scale(
            pygame.image.load('./src/bullet.png').convert_alpha(), (24, 24))
        # self.start_time = pygame.time.get_ticks()
        self.player = Player(self)
        self.gb = GenerateBarrages(self)
        self.barrages = pygame.sprite.Group()
        self.lights = pygame.sprite.Group()
        self.barragesGrav = pygame.sprite.Group()
        try:
            backgroundimg = pygame.image.load(
                os.path.join(
                    self.song_path, self.beatmap['Events'][0]
                    ['Backgroundimg'].strip())).convert()
        except IndexError:
            backgroundimg = pygame.Surface((1024, 576)).convert()
            backgroundimg.fill((0, 0, 0))
        self.background = GameBackground(self, backgroundimg)
        if self.main.noFail is not True:
            self.healthBar = HealthBar(self)
        self.time = Time(self)
        self.progressbar = ProgressBar(self)
        self.score = Score(self)
        self.combot = Combo(self)
        self.beat = 0
        self.timing = 0
        self.kiai = 0
        self.esc_time = 0
        self.health = 100
        self.healthdiff = 60 * ((
            (float(self.beatmap['Difficulty']['h_p_drain_rate']) / 2) + 3) /
                                10)
        self.points = 0
        self.combo = 0
        self.max_combo = 0
        self.frame_time = 0
        self.jump_state = 2
        self.friction = 1
        self.barrage_speed = 1.5 * (
            (float(self.beatmap['Difficulty']['approach_rate']) + 1) / 10)
        self.miss = 0
        audioPath = os.path.join(
            song_path, self.beatmap['General']['audio_filename'].strip())
        pygame.mixer.music.load(audioPath)
        self.audio = MP3(audioPath)
        pygame.mixer.music.play()
        self.music_pos = pygame.mixer.music.get_pos()

    def draw(self):
        self.background.draw()
        self.player.draw()
        self.barragesGrav.draw(self.scene)
        self.barrages.draw(self.scene)
        self.lights.draw(self.scene)
        self.score.draw()
        self.combot.draw()
        self.time.draw()
        self.progressbar.draw()
        if self.main.noFail is not True:
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
            # print(self.beat, len(self.beatmap['HitObjects']))
            if self.combo > self.max_combo:
                self.max_combo = self.combo
            if self.combo > 30 and self.health < 100:
                self.health += 0.2
            if self.health <= 0:
                self.main.game_end = True
            if len(self.barrages) == 0 and len(
                    self.barragesGrav) == 0 and self.beat == len(
                        self.beatmap['HitObjects']):
                self.main.stat = 1
                if self.music_pos == -1:
                    self.main.game_end = True
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
                if self.main.stat == 1:
                    self.main.game_end = True
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
            if pygame.sprite.spritecollide(self.player, self.barrages, True):
                if self.main.noFail is not True:
                    if self.combo > 150:
                        self.health -= self.healthdiff * 1.3
                        self.background.alphared = 90
                    else:
                        self.health -= self.healthdiff
                        self.background.alphared = 90
                self.miss += 1
                self.combo = 0
            if pygame.sprite.spritecollide(self.player, self.barragesGrav,
                                           True):
                if self.main.noFail is not True:
                    if self.combo > 150:
                        self.health -= self.healthdiff * 1.3
                        self.background.alphared = 90
                    else:
                        self.health -= self.healthdiff
                        self.background.alphared = 90
                self.miss += 1
                self.combo = 0
