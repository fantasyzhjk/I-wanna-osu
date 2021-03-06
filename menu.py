import os
import sys
import beapmap_reader
import pygame
from random import randint
# import time

from config import Settings, Colours


class Frames(object):
    def __init__(self, screen):
        self.screen = screen
        self.Font = pygame.font.Font(Settings.font, 20)

    def draw(self):
        score = self.Font.render(str(int(self.screen.main.fps)), True, (255, 255, 255))
        score_rect = score.get_rect()
        self.screen.scene.blit(score, (self.screen.width - score_rect.right - 10, self.screen.height - 35))


class Background(object):
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.Surface(self.screen.scene.get_size()).convert()
        self.background.fill((0, 0, 0))
        self.backgroundback = pygame.Surface(self.screen.scene.get_size()).convert()
        self.backgroundback.fill((0, 0, 0))

    def draw(self):
        self.screen.scene.blit(self.backgroundback, (0, 0))
        self.screen.scene.blit(self.background, (0, 96))


class BlackScreen(object):
    def __init__(self, screen):
        self.screen = screen
        self.alpha = 255
        self.backgroundred = pygame.Surface(self.screen.scene.get_size()).convert()
        self.backgroundred.fill((0, 0, 0))

    def update(self):
        self.backgroundred.set_alpha(self.alpha)

    def draw(self):
        self.screen.scene.blit(self.backgroundred, (0, 0))


class LoadingScreen:
    def __init__(self, main):
        (self.width, self.height) = (main.width, main.height)
        self.main = main
        self.scene = main.scene
        self.background = Background(self)
        self.clock = pygame.time.Clock()
        self.myFont = pygame.font.Font(Settings.font, 45)
        self.SurfaceFont = self.myFont.render("Loading....", True, Colours.white)

    def draw(self):
        self.scene.blit(self.SurfaceFont, (30, 15))
        pygame.display.flip()
        self.background.draw()

    def run(self):
        self.draw()
        self.clock.tick(Settings.clock_tick)


class Menu:
    def __init__(self, main):
        (self.width, self.height) = (main.width, main.height)
        self.main = main
        self.scene = main.scene
        self.beatmap = []
        self.beatmap_diff = {}
        self.song_path = ''
        self.gameStart = False  # 是否开始游戏
        self.osu_songs = os.listdir(Settings.songs_path)
        self.all_beatmaps = []
        self.background = Background(self)
        self.blackScreen = BlackScreen(self)
        if self.main.show_fps:
            self.fps = Frames(self)
        self.selState = 0
        self.selPressTime = {pygame.K_RIGHT: 0, pygame.K_LEFT: 0}
        self.last_song = 0
        self.song = 0
        self.song_diff = 0
        self.myFont = pygame.font.Font(Settings.font, 45)
        self.otherFont = pygame.font.Font(Settings.font, 25)
        self.smallFont = pygame.font.Font(Settings.font, 20)
        self.up_text = self.otherFont.render("△", True, Colours.white)
        self.down_text = self.otherFont.render("▽", True, Colours.white)
        title = 'I wanna osu'
        self.SurfaceFont = self.myFont.render(title, True, Colours.white)
        self.SurfaceFont_Y = 15
        version = 'You have no Beatmaps'
        self.SurfaceFont2 = self.otherFont.render(version, True, Colours.white)

    def load_beatmap(self):
        print("正在读取 {}".format(self.osu_songs[self.song]))
        path = os.path.join(Settings.songs_path, self.osu_songs[self.song])
        try:
            self.beatmap = beapmap_reader.getSong(path)
        except Exception as e:
            print(e)
            del self.osu_songs[self.song]

    def setSong(self):
        if not self.osu_songs:
            return
        self.load_beatmap()
        if self.beatmap == []:
            print("{} 读取失败".format(self.osu_songs[self.song]))
            del self.osu_songs[self.song]
            self.load_beatmap()
        try:
            self.song_path = self.beatmap[0]['song_path']
            self.setDiff()
            pygame.mixer.music.load(os.path.join(self.song_path, self.beatmap_diff['General']['audio_filename'].strip()))
            pygame.mixer.music.play()
            title = self.beatmap_diff['Metadata']['artist'] + ' - ' + self.beatmap_diff['Metadata']['title']
            if 42 >= len(title) > 36:
                self.myFont = pygame.font.Font(Settings.font, 38)
                self.SurfaceFont_Y = 20
            elif 55 >= len(title) > 42:
                self.myFont = pygame.font.Font(Settings.font, 31)
                self.SurfaceFont_Y = 25
            elif len(title) > 55:
                self.myFont = pygame.font.Font(Settings.font, 24)
                self.SurfaceFont_Y = 30
            else:
                self.myFont = pygame.font.Font(Settings.font, 45)
                self.SurfaceFont_Y = 15
            self.SurfaceFont = self.myFont.render(title, True, Colours.white)
        except pygame.error as e:
            print(e)
            print(self.osu_songs[self.song])
            del self.osu_songs[self.song]
            self.setSong()

    def setDiff(self):
        self.beatmap_diff = self.beatmap[self.song_diff + 1]
        try:
            version = self.beatmap_diff['Metadata']['version']
            self.SurfaceFont2 = self.otherFont.render("(" + str(version) + ') - Press Space to Start', True, Colours.white)
            try:
                img_file = os.path.join(self.song_path, self.beatmap_diff['Events'][0]['Backgroundimg'].strip())
                backgroundimg = pygame.image.load(img_file).convert()
                backgroundimg = pygame.transform.smoothscale(backgroundimg, (1024, 576))
            except IndexError:
                backgroundimg = pygame.Surface((1024, 576)).convert()
                backgroundimg.fill((0, 0, 0))
            self.background.background = backgroundimg
        except KeyError:
            self.song_diff += 1
            self.setDiff()
        except TypeError as e:
            print("ERROR: ", e)
            print(self.osu_songs[self.song])
            del self.osu_songs[self.song]
            self.setSong()
        except FileNotFoundError as e:
            print("background image not found: ", e)
            backgroundback = pygame.Surface(self.scene.get_size()).convert()
            backgroundback.fill((0, 0, 0))
            self.background.background = backgroundback

    def draw(self):
        self.background.draw()
        self.scene.blit(self.SurfaceFont2, (30, self.height - 65))
        self.scene.blit(self.SurfaceFont, (30, self.SurfaceFont_Y))
        self.scene.blit(self.up_text, (self.width - 80, self.height - 75))
        self.scene.blit(self.down_text, (self.width - 80, self.height - 55))
        self.blackScreen.draw()
        if self.main.show_fps:
            self.fps.draw()
        pygame.display.flip()

    def run(self):
        if not self.gameStart:
            if self.blackScreen.alpha > 0:
                self.blackScreen.alpha -= 5
                self.blackScreen.update()
            for event in pygame.event.get():
                if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                    if self.main.noFail is True:
                        self.main.noFail = False
                        pygame.display.set_caption('I wanna osu')
                    else:
                        self.main.noFail = True
                        pygame.display.set_caption('[NOFAIL] I wanna osu')
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F1:
                        if self.main.show_fps:
                            self.main.show_fps = False
                            del self.fps
                        else:
                            self.main.show_fps = True
                            self.fps = Frames(self)
                    if event.key == pygame.K_F3 and self.song != self.last_song:
                        self.song = self.last_song
                        self.song_diff = 0
                        self.setSong()
                    if event.key == pygame.K_F2:
                        song = self.song
                        while song == self.song:
                            self.song = randint(0, len(self.osu_songs) - 1)
                        self.last_song = song
                        self.song_diff = 0
                        self.setSong()
                    if event.key == pygame.K_LEFT:
                        if self.song > 0:
                            self.song -= 1
                        else:
                            self.song = len(self.osu_songs) - 1
                        self.song_diff = 0
                        self.setSong()
                    if event.key == pygame.K_RIGHT:
                        if self.song < len(self.osu_songs) - 1:
                            self.song += 1
                        else:
                            self.song = 0
                        self.song_diff = 0
                        self.setSong()
                    if event.key == pygame.K_DOWN:
                        if self.beatmap != []:
                            if self.song_diff < len(self.beatmap) - 2:
                                self.song_diff += 1
                                self.setDiff()
                    if event.key == pygame.K_UP:
                        if self.song_diff > 0:
                            self.song_diff -= 1
                            self.setDiff()

                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        # self.main.intro = False
                        self.gameStart = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.selPressTime[pygame.K_LEFT] = 0
                    if event.key == pygame.K_RIGHT:
                        self.selPressTime[pygame.K_RIGHT] = 0

            key_down = pygame.key.get_pressed()
            if key_down[pygame.K_LEFT]:
                if self.selPressTime[pygame.K_LEFT] > 32:
                    if self.song > 0:
                        self.song -= 1
                    else:
                        self.song = len(self.osu_songs) - 1
                    self.song_diff = 0
                    self.setSong()
                self.selPressTime[pygame.K_LEFT] += 1
            if key_down[pygame.K_RIGHT]:
                if self.selPressTime[pygame.K_RIGHT] > 32:
                    if self.song < len(self.osu_songs) - 1:
                        self.song += 1
                    else:
                        self.song = 0
                    self.song_diff = 0
                    self.setSong()
                self.selPressTime[pygame.K_RIGHT] += 1
            self.draw()
        else:
            if self.blackScreen.alpha >= 30:
                self.main.isMenu = False
            else:
                self.blackScreen.alpha += 1
            self.blackScreen.update()
            self.blackScreen.draw()
            pygame.display.flip()
