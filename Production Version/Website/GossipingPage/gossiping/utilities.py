# -*- coding: utf-8 -*-

def sort_dict_data(data):
    return OrderedDict((datetime.strftime(k, '%d-%m-%Y'), v)
                       for k, v in sorted(data.iteritems()))

import pickle
import base64
import datetime
import ast
import operator

from collections import defaultdict
from .dict import stopwords

class Tracking_concept_drift:
    def __init__(self, data=None, stopwords=stopwords):
        self.data = data
        self.start_date = data[0].ptime  if data else None
        self.end_date = data[len(data)-1].ptime if data else None
        self.stopwords = stopwords

    def pickle_encoder_with_base64(self, data):
        pickledList = pickle.dumps(data)
        pickled_encode = base64.b64encode(pickledList)
        return pickled_encode.decode("utf-8")

    def pickle_decoder_with_base64(self, data):
        return pickle.loads(base64.b64decode(data))

    def cal_time_weight(self, current_date):
        date_interval = (self.end_date - self.start_date).days
        date_differ = (current_date - self.start_date).days
        return (date_interval - date_differ) + 1

    def cal_concept_drift_score_date_list(self, interval=5):
        data = self.data
        # interval = 5
        concept_drift_score_date_list = []
        date_list = []
        margin = datetime.timedelta(days=interval)

        content_concept_drift_score_dict = defaultdict(int)
        comment_concept_drift_score_dict = defaultdict(int)

        previos_date = None

        for row in data:
            current_date = row.ptime
            if previos_date is None:
                previos_date = self.start_date

            if previos_date <= current_date < previos_date + margin:

                time_weight = self.cal_time_weight(row.ptime)
                content_keywords = ast.literal_eval(row.content_keywords)
                for ck in content_keywords:
                    ck[0] = ck[0].replace(" ", "")
                    if ck[0] not in self.stopwords and len(ck[0]) > 1:
                        content_concept_drift_score_dict[ck[0]
                                                        ] += ck[1] * time_weight

                comment_keywords = ast.literal_eval(row.comment_keywords)
                for cm in comment_keywords:
                    if cm[0] not in self.stopwords and len(ck[0]) > 1:
                        comment_concept_drift_score_dict[cm[0]
                                                        ] += cm[1] * time_weight
            else:
                all_concept_drift_score_dict = {
                    **content_concept_drift_score_dict, **comment_concept_drift_score_dict}
                sorted_content_concept_drift_score_dict = sorted(
                    content_concept_drift_score_dict.items(), key=operator.itemgetter(1), reverse=True)
                sorted_comment_concept_drift_score_dict = sorted(
                    comment_concept_drift_score_dict.items(), key=operator.itemgetter(1), reverse=True)
                sorted_all_concept_drift_score_dict = sorted(
                    all_concept_drift_score_dict.items(), key=operator.itemgetter(1), reverse=True)
                concept_drift_score_date_list.append(
                    [sorted_content_concept_drift_score_dict, sorted_comment_concept_drift_score_dict, sorted_all_concept_drift_score_dict])
                date_list.append([previos_date, previos_date+margin])
        #       change to next era, fuck
                previos_date = previos_date + margin

        #         reset dict
                content_concept_drift_score_dict = defaultdict(int)
                comment_concept_drift_score_dict = defaultdict(int)

        all_concept_drift_score_dict = {
            **content_concept_drift_score_dict, **comment_concept_drift_score_dict}
        sorted_content_concept_drift_score_dict = sorted(
            content_concept_drift_score_dict.items(), key=operator.itemgetter(1), reverse=True)
        sorted_comment_concept_drift_score_dict = sorted(
            comment_concept_drift_score_dict.items(), key=operator.itemgetter(1), reverse=True)
        sorted_all_concept_drift_score_dict = sorted(
            all_concept_drift_score_dict.items(), key=operator.itemgetter(1), reverse=True)
        concept_drift_score_date_list.append(
            [sorted_content_concept_drift_score_dict, sorted_comment_concept_drift_score_dict, sorted_all_concept_drift_score_dict])
        date_list.append([previos_date, previos_date+margin])
        return (date_list, concept_drift_score_date_list, interval)
