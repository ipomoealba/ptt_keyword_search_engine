# -*- coding: utf-8 -*-
# @Author: ipomoealba
# @Date:   2016-09-23 01:26:53
# @Last Modified by:   ipomoealba
import jieba
import operator
import re

# load Dict
jieba.load_userdict(
    r'/Users/ipomoealba/Code/ptt_gossiping_analysis_project/pttWebSite/GossipingPage/jieba_dict/dict.txt')


class Counter():
    @staticmethod
    def countFrequence(data, hash):
        data = re.sub("[A-Za-z0-9\[\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%]", "", data)
        tt = jieba.cut(data, cut_all=True)
        # hash = {}
        for item in tt:
            if item in hash and len(item) > 1:
                hash[item] += 1
            else:
                hash[item] = 1

        return sorted(hash.items(), key=operator.itemgetter(1), reverse=True)
