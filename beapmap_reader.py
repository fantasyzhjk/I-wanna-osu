import os
import re

# 铺面参数类型
SECTION_TYPES = ['General', 'Editor', 'Metadata', 'Difficulty', 'Events', 'TimingPoints', 'Colours', 'HitObjects']

# 滑条类型
SLIDER_TYPES = ['C', 'L', 'P', 'B']


# 读取songs文件夹
def getSongs(songs_path):
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
                        print("正在读取 {}".format(song))
                    try:
                        songInfo = parse(song_path)
                        all_beatmaps[i].append(songInfo)
                    except Exception:
                        print("{} 读取失败".format(song))
    return all_beatmaps


def getSong(path):
    diffs = []
    diffs.append({'song_path': path})
    if os.path.isdir(path):
        for file in os.listdir(path):
            if file.endswith(".osu"):
                # song = file
                song_path = os.path.join(path, file)
                songInfo = parse(song_path)
                if songInfo:
                    diffs.append(songInfo)
    if len(diffs) == 1:
        return []
    return diffs


# 单文件解析
def parse(osu_beatmap_path: str):
    file = open(osu_beatmap_path, 'r+', encoding="utf8").readlines()
    current_sector = None
    beatmap_dict = {}
    for line in file:
        if line == '' or line == '\n':
            continue
        callback = check_for_header(line)
        if callback is not None:
            current_sector = callback
        if current_sector is not None:
            line = line.strip('\n')
            parse_line(line, current_sector, beatmap_dict)
    return beatmap_dict


def check_for_header(line: str):
    for section in SECTION_TYPES:
        if section in line:
            return section
    return None


# 解析铺面
def parse_hit_objects(line: str, sector: str, beatmap_dict: dict):
    item = line.split(',')
    point = {'x': item[0], 'y': item[1], 'time': item[2], 'type': item[3], 'hitsound': item[4]}
    if len(item) > 5:
        if not any(curve_type in item[5] for curve_type in SLIDER_TYPES):
            point['extras'] = item[5]
        else:
            try:
                ct_cp = item[5].split("|")
                point['curve_type'] = ct_cp[0]
                point['curve_points'] = tuple([{'x': params.split(':')[0], 'y': params.split(':')[1]} for params in ct_cp[1:]])
                point['slides'] = item[6]
                point['length'] = item[7]
                point['edge_sounds'] = item[8]
                point['edge_sets'] = item[9]
            except Exception:
                pass
    beatmap_dict[sector].append(point)


# 解析事件（背景图） todo：storyboard
def parse_events(line: str, sector: str, beatmap_dict: dict):
    item = line.split(',')
    if item[0] == '0' and item[1] == '0':
        point = {
            'Backgroundimg': item[2][1:-1],
        }
        beatmap_dict[sector].append(point)


# 解析timing结构
def parse_timing_objects(line: str, sector: str, beatmap_dict: dict):
    item = line.split(',')
    point = {'time': item[0], 'beat_length': item[1], 'meter': item[2], 'sample_set': item[3], 'sample_index': item[4], 'volume': item[5], 'uninherited': item[6], 'effects': item[7]}
    beatmap_dict[sector].append(point)


# 单行解析
def parse_line(line: str, current_sector: str, beatmap_dict: dict):
    if current_sector == "TimingPoints":
        if current_sector not in beatmap_dict:
            beatmap_dict[current_sector] = []
        if "," not in line:
            return
        parse_timing_objects(line, current_sector, beatmap_dict)
    elif current_sector == "HitObjects":
        if current_sector not in beatmap_dict:
            beatmap_dict[current_sector] = []
        if "," not in line:
            return
        parse_hit_objects(line, current_sector, beatmap_dict)
    elif current_sector == "Events":
        if current_sector not in beatmap_dict:
            beatmap_dict[current_sector] = []
        if "," not in line:
            return
        parse_events(line, current_sector, beatmap_dict)
    else:
        if current_sector not in beatmap_dict:
            beatmap_dict[current_sector] = {}
        if ":" not in line:
            return
        item = line.split(":")
        value = item[1].replace('\n', '')
        key = "_".join(re.sub(r"([A-Z])", r" \1", item[0]).lower().split())
        beatmap_dict[current_sector][key] = value
