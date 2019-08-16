# -*- coding: utf-8 -*-

from os import path
import MeCab
from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
from collections import OrderedDict

current_dir = path.dirname(__file__)
text = open(path.join(current_dir, 'documents.txt'), 'r').read()
# text = open(path.join(current_dir, 'documents.txt'), 'r').read()
documents = text.split("|")

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


# 学習データとなる各文書
training_docs = []
for i, document in enumerate(documents):
    training_docs.append(TaggedDocument(words=words(document), tags=['doc' + str(i + 1)]))

# min_count=1:最低1回出現した単語を学習に使用
# dm=0: 学習モデル=DBOW
model = Doc2Vec(documents=training_docs, min_count=1, dm=0)

tags = OrderedDict() #辞書の繰り返し時による順番を保つ
tag_list = (('doc1', "記事A"), ('doc2', "記事B"), ('doc3', "記事C"), ('doc4', "記事D"), ('doc5', "記事E"), ('doc6', "記事F"))
dic = OrderedDict(tag_list)
tags.update(dic)

for k, v in tags.items():
    print("[" + v + "]")
    for items in model.docvecs.most_similar(k):
        print("\t" + tags[items[0]] + " : "+ str(items[1]))
