import pygame
import os
from mutagen.mp3 import MP3
import beapmap_reader

dic = r'C:\Users\Administrator\Desktop\osu\Songs\beatmap-637499191593362925-audio/'
getindex = {1: 'normal', 2: 'soft', 3: 'drum'}

beatmap = beapmap_reader.parse(dic + 'a_hisa -  (OwopwqowO) [213].osu')
timing = 0
beat = 0
# 标识是否退出循环
exitFlag = False
# 设置画面刷新的帧率，即1s内刷新几次
FPS = 30
# 初始化pygame
pygame.init()
# 设置窗口标题
pygame.display.set_caption("pygame音频播放教程")
# 设置窗口大小
surface = pygame.display.set_mode((1000, 500), pygame.RESIZABLE)
# 设置icon
paused = False
# 获取游戏时钟
clock = pygame.time.Clock()
music1Path = dic + 'audio.mp3'
music2Path = r'C:\Users\Administrator\Desktop\osu\Songs\beatmap-637499191593362925-audio/audio.mp3'
# 初始化音频模块
pygame.mixer.init()
# 加载音频文件
pygame.mixer.music.load(music1Path)
# 排队多个音频,依次播放
pygame.mixer.music.queue(music2Path)
# 指定播放位置,相对于当前位置，移动多少秒
# pygame.mixer.music.set_pos(5)
# 设置音量，0.0~1.0
pygame.mixer.music.set_volume(0.5)
# 开始播放
pygame.mixer.music.play(0)
# 加载mp3配置信息
audio1 = MP3(music1Path)
# 获取MP3音频文件的长度
length = audio1.info.length
print('len=', length)
# 图片缩放为指定宽高

newRect = None
dirtyList = []
while not exitFlag:
    clock.tick(FPS)
    music_pos = pygame.mixer.music.get_pos()
    if timing < len(beatmap['TimingPoints']):
        if music_pos > float(beatmap['TimingPoints'][timing]['time']):
            ctiming = beatmap['TimingPoints'][timing]
            timing += 1
            # print(ctiming)
    try:
        while music_pos > float(beatmap['HitObjects'][beat]['time']):
            clock.tick(FPS)
            cbeat = beatmap['HitObjects'][beat]
            soundFile = dic + getindex[int(
                ctiming['sample_set'])] + '-hitnormal.wav'
            if not os.path.isfile(soundFile):
                soundFile = './src/sounds/' + getindex[int(
                    ctiming['sample_set'])] + '-hitnormal.wav'
            music = pygame.mixer.Sound(soundFile)
            music.set_volume((int(ctiming['volume']) / 100) * 0.5 * 0.7)
            music.play()
            if cbeat['time'] == ctiming['time']:
                hitsound = int(cbeat['hitsound'])
                if hitsound - 8 >= 0:
                    hitsound -= 8
                    sampleIndex = ctiming['sample_index']
                    if sampleIndex == '0' or sampleIndex == '1':
                        sampleIndex = ''
                    soundFile = dic + getindex[int(
                        ctiming['sample_set']
                    )] + '-hit' + 'clap' + sampleIndex + '.wav'
                    if not os.path.isfile(soundFile):
                        soundFile = './src/sounds/' + getindex[int(
                            ctiming['sample_set'])] + '-hitclap.wav'
                    music = pygame.mixer.Sound(soundFile)
                    music.set_volume(
                        (int(ctiming['volume']) / 100) * 0.5 * 0.7)
                    music.play()
                if hitsound - 4 >= 0:
                    hitsound -= 4
                    sampleIndex = ctiming['sample_index']
                    if sampleIndex == '0' or sampleIndex == '1':
                        sampleIndex = ''
                    soundFile = dic + getindex[int(
                        ctiming['sample_set']
                    )] + '-hitfinish' + sampleIndex + '.wav'
                    if not os.path.isfile(soundFile):
                        soundFile = './src/sounds/' + getindex[int(
                            ctiming['sample_set'])] + '-hitfinish.wav'
                    music = pygame.mixer.Sound(soundFile)
                    music.set_volume(
                        (int(ctiming['volume']) / 100) * 0.5 * 0.7)
                    music.play()
                if hitsound - 2 >= 0:
                    hitsound -= 2
                    sampleIndex = ctiming['sample_index']
                    if sampleIndex == '0' or sampleIndex == '1':
                        sampleIndex = ''
                    soundFile = dic + getindex[int(
                        ctiming['sample_set']
                    )] + '-hit' + 'whistle' + sampleIndex + '.wav'
                    if not os.path.isfile(soundFile):
                        soundFile = './src/sounds/' + getindex[int(
                            ctiming['sample_set'])] + '-hitwhistle.wav'
                    music = pygame.mixer.Sound(soundFile)
                    music.set_volume(
                        (int(ctiming['volume']) / 100) * 0.5 * 0.7)
                    music.play()
            beat += 1
    except IndexError:
        pass
    dirtyList.clear()
    for event in pygame.event.get():
        # 点击关闭
        if event.type == pygame.QUIT:
            exitFlag = True
        elif event.type == pygame.KEYDOWN:
            # 按下空格键
            if event.key == pygame.K_SPACE:
                if paused:
                    if pygame.mixer.get_init():
                        paused = False
                        # 恢复
                        pygame.mixer.music.unpause()
                else:
                    if pygame.mixer.get_init():
                        paused = True
                        # 暂停
                        pygame.mixer.music.pause()
            # 按下ESC键
            elif event.key == pygame.K_ESCAPE:
                if pygame.mixer.get_init():
                    # 设置音频几毫秒之后慢慢消失
                    pygame.mixer.music.fadeout(500)
            # 按下R键
            elif event.key == pygame.K_r:
                if pygame.mixer.get_init():
                    # 重新开始播放
                    pygame.mixer.music.play(0)
            # 按下E键
            elif event.key == pygame.K_e:
                if pygame.mixer.get_init():
                    # 释放资源退出
                    pygame.mixer.music.unload()
                    pygame.mixer.quit()

    # 擦除脏区域
    if newRect:
        fillRect = surface.fill((0, 0, 0), newRect)
        dirtyList.append(fillRect)
    if pygame.mixer.get_init():  # 音频退出之后就会提示没初始化
        pass
    pygame.display.update(dirtyList)

if __name__ == '__main__':
    pass
