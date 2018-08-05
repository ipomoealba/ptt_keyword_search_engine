# -*- coding: utf-8 -*-

def sort_dict_data(data):
    return OrderedDict((datetime.strftime(k, '%d-%m-%Y'), v)
                       for k, v in sorted(data.iteritems()))
