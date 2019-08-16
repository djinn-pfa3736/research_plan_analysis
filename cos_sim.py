# -*- coding: utf-8 -*-

from os import path
import numpy as np
import MeCab
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

current_dir = path.dirname(__file__)
input_text = open(path.join(current_dir, 'documents.txt'), 'r').read()
# input_text = open(path.join(current_dir, 'documents.txt'), 'r').read()
documents = input_text.split("|")

def words(text):
    """
        文章から単語を抽出
    """
    out_words = []
    tagger = MeCab.Tagger('-Ochasen')
    tagger.parse('')
    node = tagger.parseToNode(text)

    while node:
        word_type = node.feature.split(",")[0]
        if word_type in ["名詞"]:
            out_words.append(node.surface)
        node = node.next
    return out_words


def vecs_array(documents):
    """
    各文章における重み付け
    """
    docs = np.array(documents)
    vectorizer = TfidfVectorizer(
        analyzer=words,
        stop_words='|',
        min_df=1,
        token_pattern='(?u)\\b\\w+\\b' #文字列長が1の単語を処理対象に含める
    )
    vecs = vectorizer.fit_transform(docs)
    return vecs.toarray()

# Cos類似度
tag = ["記事A", "記事B", "記事C", "記事D", "記事E", "記事F"]
cs_array = cosine_similarity(vecs_array(documents), vecs_array(documents))

for i, cs_item in enumerate(cs_array):
    print("[" + tag[i] + "]")
    cs_dic = {}
    for j, cs in enumerate(cs_item):
        if round(cs - 1.0, 5) != 0: #同じ文書同士は省きます
            cs_dic[tag[j]] = cs
    for k, v in sorted(cs_dic.items(), key=lambda x:x[1], reverse=True):
        print("\t" + k + " : " + str(v))
