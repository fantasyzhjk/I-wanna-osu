import os
import beapmap_reader
import pygame
import sys
from main import Colours


class Background(object):
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.Surface(self.screen.scene.get_size()).convert()
        self.background.fill((0, 0, 0))
        self.backgroundback = pygame.Surface(self.screen.scene.get_size()).convert()
        self.backgroundback.fill((0, 0, 0))

    def draw(self):
        self.screen.scene.blit(self.backgroundback, (0, 0))
        self.screen.scene.blit(self.background, (0, 84))


class Menu:
    def __init__(self, main):
        (self.width, self.height) = (main.width, main.height)
        self.main = main
        self.scene = main.scene
        self.all_beatmaps = self.getSongs()
        self.background = Background(self)
        self.song = 0
        self.song_diff = 0
        self.myFont = pygame.font.Font('./src/sarasa-mono-sc-regular.ttf', 45)
        self.otherFont = pygame.font.Font('./src/sarasa-mono-sc-regular.ttf', 25)
        self.smallFont = pygame.font.Font('./src/sarasa-mono-sc-regular.ttf', 20)
        self.up_text = self.otherFont.render("△", True, Colours.white)
        self.down_text = self.otherFont.render("▽", True, Colours.white)
        title = 'Safetyisland'
        self.SurfaceFont = self.myFont.render(title, True, Colours.white)
        version = 'You have no Beatmaps'
        self.SurfaceFont2 = self.otherFont.render(version, True, Colours.white)
        if self.all_beatmaps:
            self.setSong()

    def getSongs(self):
        songs_path = "./Songs"
        osu_songs = os.listdir(songs_path)
        all_beatmaps = []
        lastBeatmap = ''
        i = -1
        for song in osu_songs:
            path = os.path.join(songs_path, song)
            if os.path.isdir(path):
                for file in os.listdir(path):
                    if file.endswith(".osu"):
                        song_path = os.path.join(path, file)
                        if song != lastBeatmap:
                            i += 1
                            lastBeatmap = song
                            all_beatmaps.append([])
                            all_beatmaps[i].append({'song_path': path})
                            print("Reading {}".format(song))
                        try:
                            songInfo = beapmap_reader.parse(song_path)
                            all_beatmaps[i].append(songInfo)
                        except:
                            print("Could not read {}".format(song))
        return all_beatmaps

    def setSong(self):
        self.beatmap = self.all_beatmaps[self.song]
        self.setDiff()
        self.song_path = self.beatmap[0]['song_path']
        img_file = os.path.join(self.song_path, self.beatmapdiff['Events'][0]['Backgroundimg'].strip())
        backgroundimg = pygame.image.load(img_file)
        backgroundimg = pygame.transform.scale(backgroundimg, (1024, 600))
        self.background.background = backgroundimg
        pygame.mixer.music.load(os.path.join(self.song_path, self.beatmapdiff['General']['audio_filename'].strip()))
        pygame.mixer.music.play()
        title = self.beatmapdiff['Metadata']['artist_unicode'] + ' - ' + self.beatmapdiff['Metadata']['title_unicode']
        self.SurfaceFont = self.myFont.render(title, True, Colours.white)

    def setDiff(self):
        self.beatmapdiff = self.beatmap[self.song_diff + 1]
        version = "(" + self.beatmapdiff['Metadata']['version'] + ') - Press Space to Start'
        self.SurfaceFont2 = self.otherFont.render(version, True, Colours.white)

    def draw(self):
        self.scene.blit(self.SurfaceFont2, (30, self.height - 60))
        self.scene.blit(self.SurfaceFont, (30, 15))
        self.scene.blit(self.up_text, (self.width - 100, self.height - 70))
        self.scene.blit(self.down_text, (self.width - 100, self.height - 50))
        pygame.display.flip()
        self.background.draw()

    def run(self):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
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

                if event.key == pygame.K_SPACE:
                    self.main.intro = False

        self.draw()
