# 文章で使用されている単語の特徴ベクトルの平均を算出
def avg_feature_vector(sentence, model, num_features):
    words = mecab.parse(sentence).replace(' \n', '').split() # mecabの分かち書きでは最後に改行(\n)が出力されてしまうため、除去
    feature_vec = np.zeros((num_features,), dtype="float32") # 特徴ベクトルの入れ物を初期化
    for word in words:
        feature_vec = np.add(feature_vec, model[word])
    if len(words) > 0:
        feature_vec = np.divide(feature_vec, len(words))
    return feature_vec

# ２つの文章の類似度を算出
def sentence_similarity(sentence_1, sentence_2):
    # 今回使うWord2Vecのモデルは300次元の特徴ベクトルで生成されているので、num_featuresも300に指定
    num_features=300
    sentence_1_avg_vector = avg_feature_vector(sentence_1, word2vec_model, num_features)
    sentence_2_avg_vector = avg_feature_vector(sentence_2, word2vec_model, num_features)
    # １からベクトル間の距離を引いてあげることで、コサイン類似度を計算
    return 1 - spatial.distance.cosine(sentence_1_avg_vector, sentence_2_avg_vector)
