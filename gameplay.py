import os
import sys
import pygame
import mutagen

from gameplay_ui import *
from player import *
from config import Settings

delta = {
    pygame.K_UP: (0, -12),
    pygame.K_SPACE: (0, -12),
    pygame.K_w: (0, -12),
}

getindex = {1: 'normal', 2: 'soft', 3: 'drum'}

gravity = +0.6


class GenerateBarrages:
    def __init__(self, screen):
        self.screen = screen
        # print(self.screen.beatmap['HitObjects'])

    def update(self):
        if self.screen.timing < len(self.screen.beatmap['TimingPoints']):
            if (self.screen.music_pos + Settings.offset) > float(
                    self.screen.beatmap['TimingPoints'][
                        self.screen.timing]['time']):
                self.ctiming = self.screen.beatmap['TimingPoints'][
                    self.screen.timing]
                # print(self.ctiming)
                self.screen.kiai = int(self.ctiming['effects'])
                self.screen.timing += 1
        try:
            while (self.screen.music_pos + Settings.offset) > float(
                    self.screen.beatmap['HitObjects'][
                        self.screen.beat]['time']):
                cbeat = self.screen.beatmap['HitObjects'][self.screen.beat]
                # print(cbeat)
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


class Playground(object):
    def __init__(self, main, song, song_path):
        self.main = main
        (self.width, self.height) = (main.width, main.height)
        self.scene = main.scene
        self.song_path = song_path
        self.beatmap = song

        # 铺面参数初始化
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
        try:
            backgroundimg = pygame.image.load(
                os.path.join(
                    self.song_path, self.beatmap['Events'][0]
                    ['Backgroundimg'].strip())).convert()
        except Exception:
            backgroundimg = pygame.Surface((1024, 576)).convert()
            backgroundimg.fill((0, 0, 0))
        self.beat = 0
        self.timing = 0
        self.kiai = 0
        self.esc_time = 0
        self.health = 100
        self.healthdiff = 60 * ((
            (float(self.beatmap['Difficulty']['h_p_drain_rate']) / 2) + 3) / 10)
        self.points = 0
        self.combo = 0
        self.max_combo = 0
        self.barrage_speed = 1.2 * (
            (float(self.beatmap['Difficulty']['approach_rate']) + 1) / 10)
        self.miss = 0
        self.godModeTime = 0        # miss后受伤无敌时间
        self.gameEnd = 0

        # 游戏数据初始化
        self.player = Player(self)
        self.gb = GenerateBarrages(self)
        self.barrages = pygame.sprite.Group()
        self.lights = pygame.sprite.Group()
        self.barragesGrav = pygame.sprite.Group()

        # UI初始化
        self.background = GameBackground(self, backgroundimg)
        self.redScreen = RedScreen(self)
        self.blackScreen = BlackScreen(self)
        self.time = Time(self)
        self.score = Score(self)
        self.combot = Combo(self)
        self.progressbar = ProgressBar(self)
        if self.main.noFail is not True:
            self.healthBar = HealthBar(self)

        # 播放音频开始游戏
        audioPath = os.path.join(
            song_path, self.beatmap['General']['audio_filename'].strip())
        pygame.mixer.music.load(audioPath)
        self.audio = mutagen.File(audioPath)
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
        # 最后显示红色蒙版
        self.redScreen.draw()
        self.blackScreen.draw()
        pygame.display.flip()

    def update(self):
        self.gb.update()
        self.player.update()
        self.barragesGrav.update()
        self.barrages.update()
        self.lights.update()
        self.background.update()
        self.redScreen.update()

    def run(self):
        if not self.gameEnd:
            self.music_pos = pygame.mixer.music.get_pos()
            if self.blackScreen.alpha > 0:
                self.blackScreen.alpha -= 8
                self.blackScreen.update()
            # print(self.music_pos)
            # print(self.beat, len(self.beatmap['HitObjects']))
            if self.combo > self.max_combo:
                self.max_combo = self.combo
            if self.combo > 30 and self.health < 100:
                self.health += 0.2
            if self.health <= 0:
                self.gameEnd = True
                # self.main.game_end = True
            if len(self.barrages) == 0 and len(
                    self.barragesGrav) == 0 and self.beat == len(
                        self.beatmap['HitObjects']):
                self.main.stat = 1
                if self.music_pos == -1:
                    self.gameEnd = True
                    # self.main.game_end = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    deltax, deltay = delta.get(event.key, (0, 0))
                    if 1 < self.jump_state <= 2:
                        self.jump_state -= 1
                        self.player.speed[1] = deltay
                        self.player.friction = 1
                elif event.type == pygame.KEYUP:
                    self.player.friction = 0.99
            if self.player.onGround:
                self.jump_state = 2
            key_down = pygame.key.get_pressed()

            if key_down[pygame.K_ESCAPE]:
                if self.main.stat == 1:
                    self.gameEnd = True
                    # self.main.game_end = True
                self.esc_time += 1
                self.redScreen.alphared += 7
                if self.esc_time > 60:
                    self.gameEnd = True
                    # self.main.game_end = True
                    self.main.stat = 2
            else:
                self.esc_time = 0
            for barrage in self.barragesGrav.sprites():
                barrage.speed = [0.98 * s for s in barrage.speed]
                barrage.speed[1] += 0.2  # 解除弹幕速度限制

            self.player.move()

            # 碰撞检测
            if pygame.sprite.spritecollide(self.player, self.barrages, True):
                if self.main.noFail is not True:
                    if self.godModeTime == 0:
                        self.godModeTime = 24
                        if self.combo > 150:
                            self.health -= self.healthdiff * 1.3
                            self.redScreen.alphared = 120
                        else:
                            self.health -= self.healthdiff
                            self.redScreen.alphared = 120
                self.miss += 1
                self.combo = 0
            if pygame.sprite.spritecollide(self.player, self.barragesGrav,
                                           True):
                if self.main.noFail is not True:
                    if self.godModeTime == 0:
                        self.godModeTime = 24
                        if self.combo > 150:
                            self.health -= self.healthdiff * 1.3
                            self.redScreen.alphared = 90
                        else:
                            self.health -= self.healthdiff
                            self.redScreen.alphared = 90
                self.miss += 1
                self.combo = 0

            if self.godModeTime > 0:
                self.godModeTime -= 1
                
            self.update()
            self.draw()
        else:
            if self.blackScreen.alpha >= 50:
                self.main.game_end = True
            else:
                self.blackScreen.alpha += 1
            self.blackScreen.update()
            self.blackScreen.draw()
            pygame.display.flip()