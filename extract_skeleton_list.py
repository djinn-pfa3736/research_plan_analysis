import sys
import csv
import re
import MeCab

import pdb

mecab = MeCab.Tagger("/usr/lib/mecab/dic")

with open("./dataset/H30_kagaku.csv") as f:
    reader = csv.reader(f)
    data = [row for row in reader]
# row_count = int(sys.argv[1])
# parse_results = mecab.parse(data[row_count][9])

for i in range(1, len(data)):

    parse_results = mecab.parse(data[i][9])

    noun = []
    conj = []
    keywords = []
    skeleton = []
    noun_count = 0
    for res in parse_results.split('\n'):
        cols = res.split('\t')
        if(1 < len(cols)):
            parts = cols[1].split(',')
            if(parts[0].startswith('名詞')):
                noun.append(cols[0])
                noun_count += 1
            elif(parts[0].startswith('接続詞')):
                conj.append(cols[0])
                skeleton.append(noun_count)
                skeleton.append(cols[0])
                noun_count = 0
            if(parts[0].startswith('名詞') or parts[0].startswith('接続詞')):
                keywords.append(cols[0])
    skeleton.append(noun_count)
    # print(data[i][0] + "\t" + str(skeleton) + "\t" + data[i][12] + "\t" + data[i][13])
    print(data[i][0] + "\t" + str(skeleton))
    # pdb.set_trace()
