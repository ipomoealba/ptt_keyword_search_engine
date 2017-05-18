# -*- coding: utf-8 -*-
import uuid
import os
import re
import json
from bson import json_util
import operator
import sys
import traceback
import subprocess

from functools import reduce
from collections import OrderedDict
from collections import Counter
from datetime import datetime
from django.contrib.auth import authenticate
from datetime import timedelta, date, datetime
from django.shortcuts import render, render_to_response, redirect
from .models import Gossiping, Content, Keywords, Reply, NewKeywords
from django.db.models import Q
from GossipingPage import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from operator import __or__ as OR
from operator import __and__ as AND
from hashlib import md5


@login_required
def home(request):
    def change_date_form(_date):
        _time_query = datetime.strptime(_date, '%Y-%m-%d %H:%M')
        return _time_query
    if request.POST:
        start_time = request.POST['start_day']
        end_time = request.POST['end_day']
        arthor = request.POST['arthorID']
        keywordANDs = request.POST.getlist('keywordAND[]')
        keywordORs = request.POST.getlist('keywordOR[]')
        if " " in keywordANDs:
            keywordANDs.remove(" ")
        if " " in keywordORs:
            keywordORs.remove(" ")
        article_class = request.POST['articleClass']
        sql_query = []
        or_query = []
        new_start_time = None
        if start_time and end_time:
            new_end_time = change_date_form(end_time)
            new_start_time = change_date_form(start_time)
            start_time_query = Q(ptime__range=[new_start_time, new_end_time])
            sql_query.append(start_time_query)
        elif start_time:
            new_start_time = change_date_form(start_time)
            new_end_time = datetime.strftime(
                datetime.now(), '%Y-%m-%d %H:%M:%S')
            start_time_query = Q(ptime__range=[new_start_time, new_end_time])
            sql_query.append(start_time_query)
        else:
            pass

        if arthor:
            arthor_query = Q(arthor=request.POST['arthorID'])
            sql_query.append(arthor_query)
        for keyword_AND in keywordANDs:
            keyword_and_query = Q(title__contains=keyword_AND)
            sql_query.append(keyword_and_query)
        for keyword_OR in keywordORs:
            keyword_or_query = Q(title__contains=keyword_OR)
            or_query.append(keyword_or_query)

        if article_class != u'[全選]':
            article_class_query = Q(
                title__contains=request.POST['articleClass'])
            sql_query.append(article_class_query)
        sql_query.append(Q(first_page=1))
        _all_reply_counter = {}
        _all_content_counter = {}
        t = {}
        d = {}
        raw_data = None
        if (sql_query != [] and or_query != []):
            raw_data = Gossiping.objects.filter(
                reduce(AND, sql_query), reduce(OR, or_query))
        elif (sql_query != [] and or_query == []):
            raw_data = Gossiping.objects.filter(reduce(AND, sql_query))
        elif (sql_query == [] and or_query != []):
            raw_data = Gossiping.objects.filter(reduce(OR, or_query))
        # print([r.ptime.date() for r in raw_data])
        month_date_freq = {}
        week_date_freq= {}
        month_all_date_freq = {}
        week_all_date_freq = {}
        all_keywords = keywordANDs + keywordORs
        # numdays = 30
        if new_start_time:
            base = new_end_time
        else:
            base = datetime.today()
        month_date_freq["all"] = {}
        week_date_freq["all"] = {}
        for k in all_keywords:
            month_date_freq[u''.join(k)] = {}
            week_date_freq[u''.join(k)] = {}
            for x in range(0, 30):
                month_date_freq["all"][(base - timedelta(days=x)).date()] = 0
                month_date_freq[k][(base - timedelta(days=x)).date()] = 0
            for x in range(0, 7):
                week_date_freq["all"][(base - timedelta(days=x)).date()] = 0
                week_date_freq[k][(base - timedelta(days=x)).date()] = 0

        for r in raw_data:
            for k in month_date_freq.keys():
                if k in r.title:
                    if r.ptime.date() in list(month_date_freq['all'].keys()):
                        month_date_freq[k][r.ptime.date()] += 1
                    if r.ptime.date() in list(week_date_freq['all'].keys()):
                        week_date_freq[k][r.ptime.date()] += 1
                 
            if r.ptime.date() in list(month_date_freq["all"].keys()):
                month_date_freq["all"][r.ptime.date()] = month_date_freq["all"][
                    r.ptime.date()] + 1
            
            if r.ptime.date() in list(week_date_freq["all"].keys()):
                week_date_freq["all"][r.ptime.date()] = week_date_freq["all"][
                    r.ptime.date()] + 1

        def sort_dict_data(data):
            return OrderedDict((datetime.strftime(k, '%d-%m-%Y'), v)
                               for k, v in sorted(data.iteritems()))
        for k in month_date_freq.keys():
            month_date_freq[k] = sort_dict_data(month_date_freq[k])
        for k in week_date_freq.keys():
            week_date_freq[k] = sort_dict_data(week_date_freq[k])    
        # week_date_freq["all"] = sort_dict_data(week_all_date_freq)
        print(month_date_freq)
        filename = str(uuid.uuid1())
        month_data_file = os.path.join(
            "cache/data/month/" + filename + ".json")
        week_data_file = os.path.join(
            "cache/data/week/" + filename + ".json")
        with open(month_data_file, 'w') as outfile:
            json.dump(month_date_freq, outfile,
                      default=json_util.default)
        with open(week_data_file, 'w') as outfile:
            json.dump(week_date_freq, outfile, default=json_util.default)
        code_file = os.path.join('lib/graph.py')
        process_month = subprocess.Popen(
            ['python2', code_file, str(month_date_freq), filename, "month"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        out1, err1 = process_month.communicate()
        process_week = subprocess.Popen(
            ['python2', code_file, str(week_date_freq), filename, "week"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        out2, err2 = process_week.communicate()
        print(out1, out2)
        print(err1, err2)
        content_result = {}
        reply_result = {}
        for i in raw_data:
            content_keywords = i.content_keywords
            reply_keywords = i.comment_keywords

            for ck in content_keywords[2:len(content_keywords) - 2].split('], ['):
                ckeyword = ck.split(', ')
                if ckeyword[0] in content_result:
                    content_result[ckeyword[0]] += int(ckeyword[1])
                elif ckeyword[0] != '' and len(ckeyword[0]) > 3:
                    content_result[ckeyword[0]] = int(ckeyword[1])

            for rk in reply_keywords[2:len(reply_keywords) - 2].split('], ['):
                rkeyword = rk.split(', ')
                if rkeyword[0] in reply_result:
                    reply_result[rkeyword[0]] += int(rkeyword[1])
                elif rkeyword[0] != '' and len(rkeyword[0]) > 3:
                    reply_result[rkeyword[0]] = int(rkeyword[1])
        if '""' in content_result:
            del content_result['""']
        if '""' in reply_result:
            del reply_result['""']

        _all_reply_counter = sorted(
            reply_result.items(), key=operator.itemgetter(1), reverse=True)
        _all_content_counter = sorted(
            content_result.items(), key=operator.itemgetter(1), reverse=True)

        if d != {}:
            _all_reply_counter = d[:10]
        if t != {}:
            _all_content_counter = t[:10]

        img_list = os.path.join("cache/urls/" + filename + ".txt")
        urls = {"all_content": "static/cache/img/month/" + filename + ".png",
                "all_reply": "static/cache/img/week/" + filename + ".png", }
        print(urls)
        return render(request, 'home.html', {'all_data': raw_data,
                                             'all_reply_counter': _all_reply_counter[:100],
                                             'all_content_counter': _all_content_counter[:200],
                                             'urls': urls
                                             })

    else:
        return render(request, 'home.html', {'all_data': "",
                                             'all_reply_counter': "",
                                             'all_content_counter': ""})


@login_required()
def add_new_keyword(request):
    # add_type = 0

    def _get_urlmd5id(keyword):
        return md5(keyword).hexdigest()

    if request.POST:
        try:
            keyword_class = request.POST['keywordClass']
            print(keyword_class)
            new_word = request.POST['new_word']
            print(new_word)
            try:
                tmp = NewKeywords.objects.get(keyword=new_word)
                print("this data was in the db")
            except NewKeywords.DoesNotExist:
                kid = _get_urlmd5id(new_word.encode('utf-8'))
                k = NewKeywords(id=kid, keyword=new_word.encode('utf-8'),
                                category=keyword_class)
                k.save()
        except Exception as e:
            print(str(e))
            exc_info = sys.exc_info()
            traceback.print_exception(*exc_info)
    # return render(request, 'home.html', {'all_data': "",
    #                                      'all_reply_counter': "",
    #                                      'all_content_counter': "",
    #                                      'add_sucess': add_type})
    return HttpResponseRedirect('/')


@login_required()
def result(request):
    if request.GET:
        if request.GET['pid']:
            post = Gossiping.objects.get(pid=request.GET['pid'])
            content_keywords = post.content_keywords
            reply_keywords = post.comment_keywords
            content_result = Counter()
            reply_result = Counter()
            re_content_result = Counter()
            re_reply_result = Counter()
            reply_raw = Reply.objects.get(pid=request.GET['pid']).reply
            for ck in content_keywords[2:len(content_keywords) - 2].split('], ['):
                ckeyword = ck.split(', ')
                if ckeyword[0] in content_result:
                    content_result[ckeyword[0]] += int(ckeyword[1])
                elif ckeyword[0] != '' and len(ckeyword[0]) > 3:
                    content_result[ckeyword[0]] = int(ckeyword[1])
            for rk in reply_keywords[2:len(reply_keywords) - 2].split('], ['):
                rkeyword = rk.split(', ')
                if rkeyword[0] in reply_result:
                    reply_result[rkeyword[0]] += int(rkeyword[1])
                elif rkeyword != '' and len(rkeyword[0]) > 3:
                    reply_result[rkeyword[0]] = int(rkeyword[1])
            re_post = Gossiping.objects.filter(
                Q(title__contains="Re: " + post.title))
            if re_post:
                re_content_result += Counter(content_result)
                re_reply_result += Counter(reply_result)
                for rep in re_post:
                    re_content_keywords = rep.content_keywords[:-2]
                    re_reply_keywords = rep.comment_keywords[:-2]
                    for ck in re_content_keywords[2:len(content_keywords) - 2].split('], ['):
                        ckeyword = ck.split(', ')
                        try:
                            if ckeyword[0] in re_content_result:
                                re_content_result[
                                    ckeyword[0]] += int(ckeyword[1])
                            elif ckeyword[0] != '' and len(ckeyword[0]) > 3:
                                re_content_result[
                                    ckeyword[0]] = int(ckeyword[1])
                        except:
                            exc_info = sys.exc_info()
                            traceback.print_exception(*exc_info)

                    for rk in re_reply_keywords[2:len(reply_keywords) - 2].split('], ['):
                        rkeyword = rk.split(', ')
                        try:
                            if rkeyword[0] in re_reply_result:
                                re_reply_result[
                                    rkeyword[0]] += int(rkeyword[1])
                            elif rkeyword != '' and len(rkeyword[0]) > 3:
                                re_reply_result[rkeyword[0]] = int(rkeyword[1])
                        except:
                            exc_info = sys.exc_info()
                            traceback.print_exception(*exc_info)

            if '""' in content_result:
                del content_result['""']
            if '""' in reply_result:
                del reply_result['""']
            if '""' in re_content_result:
                del re_content_result['""']
            if '""' in re_reply_result:
                del re_reply_result['""']

            reply = []

            if reply_raw != u'[]':
                tmp = reply_raw[2:-2].split('}, {')
                for i, w in enumerate(tmp):
                    reply.append([
                        w[w.index(""", "push_tag": """) + len(""", "push_tag": \"""")
                          :w.index("""", "push_date":""")],
                        w[w.index(""", "push_user": """) +
                          len(""", "push_user": \""""):w.index("""", "push_tag""")],
                        w[w.index("""push_content": ":""") +
                          len("""push_content": ":"""):w.index('", "push_user": ')],
                        w[w.index(""", "push_date": """) + len(""", "push_date": \""""):w.index("\n")]])

            post.sorted_hash = sorted(
                content_result.items(), key=operator.itemgetter(1), reverse=True)[:25]
            post.sorted_reply = sorted(
                reply_result.items(), key=operator.itemgetter(1), reverse=True)[:50]

            post.re_sorted_content = sorted(re_content_result.items(
            ), key=operator.itemgetter(1), reverse=True)[:25]
            post.re_sorted_reply = sorted(re_reply_result.items(
            ), key=operator.itemgetter(1), reverse=True)[:50]
            post.content = Content.objects.get(pid=request.GET['pid']).content
            print(post.push)
            return render(request, 'result.html', {'post': post, 're_post': re_post, 'reply': reply})
        else:
            return HttpResponse(status=404)
    else:
        return HttpResponse(status=404)