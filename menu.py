import os
import pygame
import sys
from config import Settings, Colours


class Background(object):
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.Surface(
            self.screen.scene.get_size()).convert()
        self.background.fill((0, 0, 0))
        self.backgroundback = pygame.Surface(
            self.screen.scene.get_size()).convert()
        self.backgroundback.fill((0, 0, 0))

    def draw(self):
        self.screen.scene.blit(self.backgroundback, (0, 0))
        self.screen.scene.blit(self.background, (0, 96))


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
    def __init__(self, main, all_beatmaps):
        (self.width, self.height) = (main.width, main.height)
        self.main = main
        self.scene = main.scene
        self.beatmap = []
        self.beatmap_diff = {}
        self.song_path = ''
        self.all_beatmaps = all_beatmaps
        self.background = Background(self)
        self.song = 0
        self.song_diff = 0
        self.myFont = pygame.font.Font(Settings.font, 45)
        self.otherFont = pygame.font.Font(Settings.font, 25)
        self.smallFont = pygame.font.Font(Settings.font, 20)
        self.up_text = self.otherFont.render("△", True, Colours.white)
        self.down_text = self.otherFont.render("▽", True, Colours.white)
        title = 'Safetyisland'
        self.SurfaceFont = self.myFont.render(title, True, Colours.white)
        self.SurfaceFont_Y = 15
        version = 'You have no Beatmaps'
        self.SurfaceFont2 = self.otherFont.render(version, True, Colours.white)
        if self.all_beatmaps:
            self.setSong()

    def setSong(self):
        self.beatmap = self.all_beatmaps[self.song]
        self.song_path = self.beatmap[0]['song_path']
        self.setDiff()
        pygame.mixer.music.load(
            os.path.join(
                self.song_path,
                self.beatmap_diff['General']['audio_filename'].strip()))
        pygame.mixer.music.play()
        title = self.beatmap_diff['Metadata'][
            'artist'] + ' - ' + self.beatmap_diff['Metadata']['title']
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

    def setDiff(self):
        self.beatmap_diff = self.beatmap[self.song_diff + 1]
        try:
            img_file = os.path.join(
                self.song_path,
                self.beatmap_diff['Events'][0]['Backgroundimg'].strip())
            backgroundimg = pygame.image.load(img_file).convert()
            backgroundimg = pygame.transform.smoothscale(
                backgroundimg, (1024, 576))
            self.background.background = backgroundimg
            version = "(" + self.beatmap_diff['Metadata'][
                'version'] + ') - Press Space to Start'
            self.SurfaceFont2 = self.otherFont.render(version, True, Colours.white)
        except KeyError:
            self.song_diff += 1
            self.setDiff()
        except FileNotFoundError:
            backgroundback = pygame.Surface(self.scene.get_size()).convert()
            backgroundback.fill((0, 0, 0))
            self.background.background = backgroundback

    def draw(self):
        self.scene.blit(self.SurfaceFont2, (30, self.height - 65))
        self.scene.blit(self.SurfaceFont, (30, self.SurfaceFont_Y))
        self.scene.blit(self.up_text, (self.width - 80, self.height - 75))
        self.scene.blit(self.down_text, (self.width - 80, self.height - 55))
        pygame.display.flip()
        self.background.draw()

    def run(self):
        for event in pygame.event.get():
            if (event.type
                    == pygame.QUIT) or (event.type == pygame.KEYDOWN
                                        and event.key == pygame.K_ESCAPE):
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if self.song > 0:
                        self.song -= 1
                        self.song_diff = 0
                        self.setSong()
                if event.key == pygame.K_RIGHT:
                    if self.song < len(self.all_beatmaps) - 1:
                        self.song += 1
                        self.song_diff = 0
                        self.setSong()
                if event.key == pygame.K_DOWN:
                    if self.song_diff < len(self.beatmap) - 2:
                        self.song_diff += 1
                        self.setDiff()
                if event.key == pygame.K_UP:
                    if self.song_diff > 0:
                        self.song_diff -= 1
                        self.setDiff()

                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    self.main.intro = False

        self.draw()
