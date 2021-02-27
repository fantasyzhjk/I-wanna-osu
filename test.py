import beapmap_reader

bm = beapmap_reader.parse(
    'C:\\Users\\Administrator\\Desktop\\osu\\Songs\\beatmap-637499191593362925-audio\\a_hisa -  (OwopwqowO) [213].osu'
)
# print(bm)
for bti in bm['HitObjects']:
    print(bti)
for bti in bm['TimingPoints']:
    print(bti)

# 0 normal
# 2 whistle
# 4 finish
# 8 clap
# 6 10 12 14

# sample_set
# 1 Normal
# 2 Soft
# 3 Drum
