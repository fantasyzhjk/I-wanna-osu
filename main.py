import sys
from threading import Thread

import pygame

import menu
import gameplay as pg
from config import Settings


class Main(object):
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('I wanna osu')
        pygame.mixer.music.set_volume(Settings.volume * Settings.music_volume)
        icon = pygame.image.load('./src/player.png')
        pygame.display.set_icon(icon)  # 可以填img
        size = (self.width, self.height) = (Settings.window_width,
                                            Settings.window_height)
        self.scene = pygame.display.set_mode(
            size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        self.clock_tick = Settings.clock_tick
        self.intro = True
        self.game_end = False
        self.stat = 0
        self.noFail = False
        # 加载铺面
        # self.loadingScreen = menu.LoadingScreen(self)
        # loadingS = Thread(target=self.loadingScreen.run)
        # loadingS.setDaemon(True)  # 必须在t.start()之前设置
        # loadingS.start()
        
        # all_beatmaps = beapmap_reader.getSongs(Settings.songs_path)
        # loadingS.join()
        self.menu = menu.Menu(self)

    def loop(self):
        self.menu.blackScreen.alpha = 255
        self.menu.gameStart = False
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
                        if self.noFail is not True:
                            pygame.display.set_caption('I wanna osu')
                        else:
                            pygame.display.set_caption('[NOFAIL] I wanna osu')
                        self.game_end = False
                        self.intro = True
                        self.stat = 0
                        self.loop()
                if self.stat == 0:
                    pygame.mixer.music.fadeout(500)
                    faildtext = myFont.render(
                        "You Failed! Score:" + str(self.playground.points),
                        True, (255, 255, 255))
                    max_combo = otherFont.render(
                        "MaxCombo:" + str(self.playground.max_combo), True,
                        (255, 255, 255))
                    faildtext1 = otherFont.render("Press Esc to Menu", True,
                                                  (255, 255, 255))
                    backgroundback = pygame.Surface(
                        self.scene.get_size()).convert()
                    backgroundback.fill((0, 0, 0))
                    backgroundback.set_alpha(200)
                    self.scene.blit(backgroundback, (0, 0))
                    self.scene.blit(faildtext, (50, 50))
                    self.scene.blit(max_combo, (130, 130))
                    self.scene.blit(faildtext1, (150, 180))
                    pygame.display.flip()
                elif self.stat == 1:
                    wintext = myFont.render(
                        "You Win! Score:" + str(self.playground.points), True,
                        (255, 255, 255))
                    max_combo = otherFont.render(
                        "MaxCombo:" + str(self.playground.max_combo), True,
                        (255, 255, 255))
                    wintext1 = otherFont.render("Press Esc to Menu", True,
                                                (255, 255, 255))
                    backgroundback = pygame.Surface(
                        self.scene.get_size()).convert()
                    backgroundback.fill((0, 0, 0))
                    backgroundback.set_alpha(200)
                    self.scene.blit(backgroundback, (0, 0))
                    self.scene.blit(wintext, (50, 50))
                    self.scene.blit(max_combo, (130, 130))
                    self.scene.blit(wintext1, (150, 180))
                    pygame.display.flip()
                elif self.stat == 2:
                    pygame.mixer.music.fadeout(200)
                    if self.noFail is not True:
                        pygame.display.set_caption('I wanna osu')
                    else:
                        pygame.display.set_caption('[NOFAIL] I wanna osu')
                    self.game_end = False
                    self.intro = True
                    self.stat = 0
                    self.loop()
                self.clock.tick(self.clock_tick)
            else:
                try:
                    self.start_game()
                except Exception as e:
                    print(e)
                    self.intro = True
                    if self.noFail is not True:
                        pygame.display.set_caption('I wanna osu')
                    else:
                        pygame.display.set_caption('[NOFAIL] I wanna osu')
                    self.loop()

    def start_game(self):
        self.playground = pg.Playground(self, self.menu.beatmap_diff, self.menu.song_path)
        while not self.game_end:
            self.playground.run()
            self.clock.tick(self.clock_tick)
        # pygame.time.wait(15)


if __name__ == '__main__':
    app = Main()
    app.loop()
