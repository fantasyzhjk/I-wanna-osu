import re

SECTION_TYPES = [
    'General',
    'Editor',
    'Metadata',
    'Difficulty',
    'Events',
    'TimingPoints',
    'Colours',
    'HitObjects'
]
SLIDER_TYPES = ['C', 'L', 'P', 'B']


def check_for_header(line: str):
    for section in SECTION_TYPES:
        if section in line:
            return section
    return None


def parse_hit_objects(line: str, sector: str, beatmap_dict: dict):
    item = line.split(',')
    point = {
        'x': item[0],
        'y': item[1],
        'time': item[2],
        'type': item[3],
        'hitsound': item[4]
    }
    if len(item) > 5:
        if not any(curve_type in item[5] for curve_type in SLIDER_TYPES):
            point['extras'] = item[5]
        else:
            try:
                ct_cp = item[5].split("|")
                point['curve_type'] = ct_cp[0]
                point['curve_points'] = tuple(
                    [{'x': params.split(':')[0], 'y': params.split(':')[1]} for params in ct_cp[1:]])
                point['slides'] = item[6]
                point['length'] = item[7]
                point['edge_sounds'] = item[8]
                point['edge_sets'] = item[9]
            except:
                pass
    beatmap_dict[sector].append(point)


def parse_events(line: str, sector: str, beatmap_dict: dict):
    item = line.split(',')
    if item[0] == '0' and item[1] == '0':
        point = {
            'Backgroundimg': item[2][1:-1],
        }
        beatmap_dict[sector].append(point)


def parse_timing_objects(line: str, sector: str, beatmap_dict: dict):
    item = line.split(',')
    point = {
        'time': item[0],
        'beat_length': item[1],
        'meter': item[2],
        'sample_set': item[3],
        'sample_index': item[4],
        'volume': item[5],
        'uninherited': item[6],
        'effects': item[7]
    }
    beatmap_dict[sector].append(point)


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


def parse(osu_beatmap_path: str):
    try:
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
                parse_line(line, current_sector, beatmap_dict)
        return beatmap_dict
    except:
        return None
