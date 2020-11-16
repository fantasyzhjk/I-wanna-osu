import pygame
import playground as pg
import menu
import sys
from config import *


class Main(object):
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Safetyisland')
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)
        icon = pygame.image.load('./src/player.png')
        pygame.display.set_icon(icon)  # 可以填img
        size = (self.width, self.height) = (Settings.window_width, Settings.window_height)
        self.scene = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        self.clock_tick = Settings.clock_tick
        self.intro = True
        self.stat = 0
        self.game_end = False
        self.menu = menu.Menu(self)

    def loop(self):
        while self.intro:
            self.menu.run()
            self.clock.tick(self.clock_tick)
            pass

        while True:
            myFont = pygame.font.Font(Settings.font, 55)
            otherFont = pygame.font.Font(Settings.font, 30)
            if self.game_end:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        pygame.display.set_caption('Safetyisland')
                        self.game_end = False
                        self.intro = True
                        self.stat = 0
                        self.loop()
                if self.stat == 0:
                    pygame.mixer.music.fadeout(500)
                    faildtext = myFont.render("You Failed! Score:" + str(self.playground.points), True,
                                              (255, 255, 255))
                    max_combo = otherFont.render("MaxCombo:" + str(self.playground.max_combo), True, (255, 255, 255))
                    faildtext1 = otherFont.render("Press Esc to Menu", True, (255, 255, 255))
                    backgroundback = pygame.Surface(self.scene.get_size()).convert()
                    backgroundback.fill((0, 0, 0))
                    backgroundback.set_alpha(200)
                    self.scene.blit(backgroundback, (0, 0))
                    self.scene.blit(faildtext, (50, 50))
                    self.scene.blit(max_combo, (130, 130))
                    self.scene.blit(faildtext1, (150, 180))
                    pygame.display.update()
                elif self.stat == 1:
                    wintext = myFont.render("You Win! Score:" + str(self.playground.points), True, (255, 255, 255))
                    max_combo = otherFont.render("MaxCombo:" + str(self.playground.max_combo), True, (255, 255, 255))
                    wintext1 = otherFont.render("Press Esc to Menu", True, (255, 255, 255))
                    backgroundback = pygame.Surface(self.scene.get_size()).convert()
                    backgroundback.fill((0, 0, 0))
                    backgroundback.set_alpha(200)
                    self.scene.blit(backgroundback, (0, 0))
                    self.scene.blit(wintext, (50, 50))
                    self.scene.blit(max_combo, (130, 130))
                    self.scene.blit(wintext1, (150, 180))
                    pygame.display.update()
                elif self.stat == 2:
                    pygame.mixer.music.fadeout(200)
                    self.game_end = False
                    self.intro = True
                    self.stat = 0
                    self.loop()
                self.clock.tick(self.clock_tick)
            else:
                self.start_game()

    def start_game(self):
        song = self.menu.beatmap_diff
        song_path = self.menu.song_path
        self.playground = pg.Playground(self, song, song_path)
        while not self.game_end:
            self.playground.run()
            self.clock.tick(self.clock_tick)

        # pygame.time.wait(15)


if __name__ == '__main__':
    app = Main()
    app.loop()
