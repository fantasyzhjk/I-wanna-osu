import sys
import getopt
import os
import pygame

import menu
import gameplay as pg
from config import Settings, Colours
from player import *

delta = {
    pygame.K_UP: (0, -12),
    pygame.K_SPACE: (0, -12),
    pygame.K_w: (0, -12),
}


class Background(object):
    def __init__(self, screen):
        self.screen = screen
        self.backgroundback = pygame.Surface(self.screen.scene.get_size()).convert()
        self.backgroundback.fill((0, 0, 0))

    def draw(self):
        self.screen.scene.blit(self.backgroundback, (0, 0))


class Intro:
    def __init__(self, main):
        (self.width, self.height) = (main.width, main.height)
        self.main = main
        self.scene = main.scene
        self.background = Background(self)
        self.player = Player(self)
        self.clock = pygame.time.Clock()
        self.myFont = pygame.font.Font(Settings.font, 45)
        self.myFont2 = pygame.font.Font(Settings.font, 25)
        self.SurfaceFont = self.myFont.render("I wanna osu", True, Colours.white)
        self.SurfaceFont2 = self.myFont2.render("Press ENTER or SPACE to continue", True, Colours.white)

    def draw(self):
        self.background.draw()
        self.scene.blit(self.SurfaceFont, (350, 320))
        self.scene.blit(self.SurfaceFont2, (270, 380))
        self.player.draw()
        pygame.display.flip()

    def run(self):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    self.main.isIntro = False
                deltax, deltay = delta.get(event.key, (0, 0))
                self.player.speed[1] = deltay
                self.player.friction = 1
            elif event.type == pygame.KEYUP:
                self.player.friction = 0.99
        self.player.move()
        self.player.update()
        self.draw()


class Main(object):
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('I wanna osu')
        pygame.mixer.music.set_volume(Settings.volume * Settings.music_volume)
        icon = pygame.image.load('./src/player.png')
        pygame.display.set_icon(icon)  # 可以填img
        size = (self.width, self.height) = (Settings.window_width, Settings.window_height)
        self.scene = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        self.clock_tick = Settings.clock_tick
        self.isIntro = True
        self.isMenu = True
        self.game_end = False
        self.stat = 0
        self.fps = 0
        self.show_fps = False
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
        intro = Intro(self)
        while self.isIntro:
            intro.run()
            self.clock.tick(self.clock_tick)
            pass
        if self.menu.osu_songs:  # 预加载铺面
            self.menu.setSong()
        while self.isMenu:
            self.menu.run()
            self.fps = self.clock.get_fps()
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
                        self.isMenu = True
                        self.stat = 0
                        self.loop()
                if self.stat == 0:
                    pygame.mixer.music.fadeout(500)
                    faildtext = myFont.render("You Failed! Score:" + str(self.playground.points), True, (255, 255, 255))
                    max_combo = otherFont.render("MaxCombo:" + str(self.playground.max_combo), True, (255, 255, 255))
                    faildtext1 = otherFont.render("Press Esc to Menu", True, (255, 255, 255))
                    backgroundback = pygame.Surface(self.scene.get_size()).convert()
                    backgroundback.fill((0, 0, 0))
                    backgroundback.set_alpha(200)
                    self.scene.blit(backgroundback, (0, 0))
                    self.scene.blit(faildtext, (50, 50))
                    self.scene.blit(max_combo, (130, 130))
                    self.scene.blit(faildtext1, (150, 180))
                    pygame.display.flip()
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
                    pygame.display.flip()
                elif self.stat == 2:
                    pygame.mixer.music.fadeout(200)
                    if self.noFail is not True:
                        pygame.display.set_caption('I wanna osu')
                    else:
                        pygame.display.set_caption('[NOFAIL] I wanna osu')
                    self.game_end = False
                    self.isMenu = True
                    self.stat = 0
                    self.loop()
                self.clock.tick(self.clock_tick)
            else:
                try:
                    self.start_game()
                except Exception as e:
                    print(e)
                    self.isMenu = True
                    if self.noFail is not True:
                        pygame.display.set_caption('I wanna osu')
                    else:
                        pygame.display.set_caption('[NOFAIL] I wanna osu')
                    self.loop()

    def start_game(self):
        self.playground = pg.Playground(self, self.menu.beatmap_diff, self.menu.song_path)
        while not self.game_end:
            self.playground.run()
            self.fps = self.clock.get_fps()
            self.clock.tick(self.clock_tick)
        # pygame.time.wait(15)hhv


if __name__ == '__main__':
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "hp:", ["songpath="])
    except getopt.GetoptError:
        print('main.py -p <songPath>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -p <songPath>')
            sys.exit()
        elif opt in ("-p", "--songpath"):
            path = arg.strip()
            if os.path.isdir(path):
                Settings.songs_path = path
            else:
                print('无效的歌曲文件夹，将使用默认文件夹')
    app = Main()
    app.loop()
