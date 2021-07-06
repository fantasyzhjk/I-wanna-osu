# import os
# import sys
import pygame
from config import Settings


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


class Frames(object):
    def __init__(self, screen):
        self.screen = screen
        self.Font = pygame.font.Font(Settings.font, 20)

    def draw(self):
        score = self.Font.render(str(int(self.screen.main.fps)), True, (255, 255, 255))
        score_rect = score.get_rect()
        self.screen.scene.blit(score, (self.screen.width - score_rect.right - 10, self.screen.height - 35))


class ProgressBar(object):  # 歌曲进度条
    def __init__(self, screen):
        self.screen = screen
        self.max_w = 300
        self.bar_background = pygame.Surface([self.screen.width, 5]).convert()
        self.bar_background.fill((100, 100, 100))
        self.bar_background.set_alpha(100)
        # self.background = pygame.image.load("src/background.jpg")

    def draw(self):
        bar = pygame.Surface([((self.screen.music_pos / (self.screen.audio.info.length * 1000)) * self.screen.width), 5])
        bar = bar.convert()
        bar.fill((225, 225, 225))
        bar.set_alpha(100)
        self.screen.scene.blit(self.bar_background, (0, self.screen.height - 5))
        self.screen.scene.blit(bar, (0, self.screen.height - 5))


class Score(object):
    def __init__(self, screen):
        self.screen = screen
        self.Font = pygame.font.Font(Settings.font, 60)
        # self.background = pygame.image.load("src/background.jpg")

    def draw(self):
        score = self.Font.render(str(format(self.screen.points, '0>8d')), True, (255, 255, 255))
        score_rect = score.get_rect()
        self.screen.scene.blit(score, (self.screen.width - score_rect.right - 20, -10))


class Combo(object):
    def __init__(self, screen):
        self.screen = screen
        self.combo = 0
        self.Font = pygame.font.Font(Settings.font, 60)
        # self.background = pygame.image.load("src/background.jpg")

    def draw(self):
        self.combo = self.screen.combo
        combo_text = self.Font.render(str(self.combo) + 'x', True, (255, 255, 255))
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
            time = self.Font.render(mts + ":" + sec + ":" + ml, True, (255, 255, 255))
        else:
            time = self.Font.render(sec + ":" + ml, True, (255, 255, 255))

        time_rect = time.get_rect()
        self.screen.scene.blit(time, (self.screen.width - time_rect.right - 20, 50))


class GameBackground(object):
    def __init__(self, screen, img):
        self.screen = screen
        self.alphablack = 180
        # self.background = pygame.transform.scale(self.background, (self.screen.width, self.screen.height))
        self.background = img
        self.background = pygame.transform.smoothscale(self.background, (1024, 576))
        self.backgroundback = pygame.Surface(self.screen.scene.get_size()).convert()
        self.backgroundback.fill((0, 0, 0))
        self.backgroundback.set_alpha(180)

    def update(self):
        self.backgroundback.set_alpha(self.alphablack)
        if self.alphablack <= 175:
            self.alphablack += 1

    def draw(self):
        self.screen.scene.blit(self.background, (0, 96))
        self.screen.scene.blit(self.backgroundback, (0, 0))


class RedScreen(object):
    def __init__(self, screen):
        self.screen = screen
        self.alphared = 0
        self.backgroundred = pygame.Surface(self.screen.scene.get_size()).convert()
        self.backgroundred.fill((240, 0, 0))

    def update(self):
        self.backgroundred.set_alpha(self.alphared)
        if self.alphared >= 0:
            self.alphared -= 5

    def draw(self):
        self.screen.scene.blit(self.backgroundred, (0, 0))


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
