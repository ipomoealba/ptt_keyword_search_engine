# -*- coding: utf-8 -*-
import re
import os
import numpy as np

def sort_dict_data(data):
    return OrderedDict((datetime.strftime(k, '%d-%m-%Y'), v)
                       for k, v in sorted(data.iteritems()))


def chinese_comma_split(text):
    """Return Text List
    Split Chinese Sentence By all commas and white Space, Including Full-shaped characters
    """
    return re.split("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+", text)

print(os.getcwd())
negative_words = None
positive_words = None
# print()
with open("./dict/ntusd/ntusd-negative.txt", 'r') as f:
    negative_words = np.array(f.read().split("\n"))
with open("./dict/ntusd/ntusd-positive.txt", 'r') as f:
    positive_words = np.array(f.read().split("\n"))


def cal_sentiment(article, keywords, cal_class="all", first_score=5, second_score=3, third_score=1, normalize=True):
    """Return Socre of Sentiment
    Calculate Score in three level

    cal_class:
        all: return positive score - negetive score
        p: return positive score
        n: return abs(negative score)
    level1: the sentence has the keyword
    level2: the sentence before or after the keywords
    """

    p_score = 0
    n_score = 0
    sentences = chinese_comma_split(article)
    keyword_appear = []
    for _, sentence in enumerate(sentences):
        if keywords in sentence:
            keyword_appear.append(_)
    for positive_word, negative_word in zip(positive_words, negative_words):
        tmp_sentences = sentences[:]

        for kp in keyword_appear:
            if positive_word in tmp_sentences[kp]:
                p_score += first_score
                tmp_sentences[kp] = ""
            if negative_word in tmp_sentences[kp]:
                n_score -= first_score
                tmp_sentences[kp] = ""
            if (kp - 1 > 0 and kp - 1 not in keyword_appear) or (
                    kp + 1 < len(keyword_appear) and kp + 1 not in keyword_appear):
                p_contorller = []
                n_contorller = []
                if positive_word in tmp_sentences[kp + 1]:
                    p_score += second_score
                    tmp_sentences[kp] = ""
                    p_contorller.append(kp + 1)
                if positive_word in tmp_sentences[kp - 1]:
                    p_score += second_score
                    tmp_sentences[kp] = ""
                    p_contorller.append(kp - 1)
                if negative_word in tmp_sentences[kp + 1]:
                    n_score -= second_score
                    tmp_sentences[kp] = ""
                    n_contorller.append(kp + 1)
                if negative_word in tmp_sentences[kp - 1]:
                    n_score -= second_score
                    tmp_sentences[kp] = ""
                    n_contorller.append(kp - 1)
                for p, n in zip(p_contorller, n_contorller):
                    kp[p] = ""
                    kp[n] = ""
        for s in tmp_sentences:
            if positive_word in s:
                p_score += third_score
            if negative_word in s:
                n_score -= third_score
    score = 0
    if cal_class == "p":
        score = p_score
    elif cal_class == "n":
        score = abs(n_score)
    else:
        score = p_score + n_score
    if normalize:
        return score / len(sentences)
    else:
        return score
