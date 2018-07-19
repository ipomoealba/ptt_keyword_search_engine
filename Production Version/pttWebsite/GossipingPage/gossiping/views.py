# -*- coding: utf-8 -*-
import json
import logging
import operator
import os
import subprocess
import sys
import traceback
import uuid
from collections import Counter
from collections import OrderedDict
from datetime import datetime
from datetime import timedelta
from functools import reduce
from hashlib import md5
from operator import __and__ as AND
from operator import __or__ as OR

from bson import json_util
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .models import UserSavePost, Gossiping, GossipingContent, GossipingReply, Newkeywords

logger = logging.getLogger(__name__)


@login_required
def myFolder(request):
    if request.POST:
        user_id = request.user.id
        user_save_post = UserSavePost.objects.filter(user_id=user_id)
        user_save_post_class = []
        for u in user_save_post:
            user_save_post_class.append(u.class_id)

        return render(request, "myFolder.html", {
            "user_save_post_class": set(user_save_post_class),
            "user_save_post": user_save_post

        })
    return HttpResponse(status=404)


@login_required
def save_post(request):
    if request.POST:
        user_id = request.user.id
        data = request.POST.getlist("posts[]")
        dataset_name = request.POST.get("dataset_name")
        logger.info("[%s] Save Data (%s) to %s " %
                    (user_id, data, dataset_name))
        for p in data:
            pid = p.split("||")[0]
            post_name = p.split("||")[1]
            s = UserSavePost(pid=pid, user_id=user_id,
                             class_id=dataset_name, post_name=post_name)
            s.save()
        payload = {'success': True}
    return HttpResponse(json.dumps(payload), content_type='application/json')


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
        month_date_freq = {}
        week_date_freq = {}
        if new_start_time:
            base = new_end_time
        else:
            base = datetime.today()
        for x in range(0, 30):
            month_date_freq[(base - timedelta(days=x)).date()] = 0
        for x in range(0, 7):
            week_date_freq[(base - timedelta(days=x)).date()] = 0
        for r in raw_data:
            if r.ptime.date() in list(month_date_freq.keys()):
                month_date_freq[r.ptime.date()] = month_date_freq[
                                                      r.ptime.date()] + 1
            if r.ptime.date() in list(week_date_freq.keys()):
                week_date_freq[r.ptime.date()] = week_date_freq[
                                                     r.ptime.date()] + 1

        def sort_dict_data(data):
            return OrderedDict((datetime.strftime(k, '%d-%m-%Y'), v)
                               for k, v in sorted(data.items()))

        all_month_date_freq = sort_dict_data(month_date_freq)
        all_week_date_freq = sort_dict_data(week_date_freq)
        filename = str(uuid.uuid1())
        all_content_data_file = os.path.join(
            "cache/data/month/" + filename + ".json")
        all_reply_data_file = os.path.join(
            "cache/data/week/" + filename + ".json")
        with open(all_content_data_file, 'w') as outfile:
            json.dump(all_month_date_freq, outfile,
                      default=json_util.default)
        with open(all_reply_data_file, 'w') as outfile:
            json.dump(all_week_date_freq, outfile, default=json_util.default)
        code_file = os.path.join('lib/graph.py')
        process_month = subprocess.Popen(
            ['python2', code_file, str(all_month_date_freq), filename, "month"], stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        out1, err1 = process_month.communicate()
        process_week = subprocess.Popen(
            ['python2', code_file, str(all_week_date_freq), filename, "week"], stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        out2, err2 = process_week.communicate()
        logger.info(err1, err2)
        content_result = {}
        reply_result = {}
        for i in raw_data:
            content_keywords = i.content_keywords
            reply_keywords = i.comment_keywords
            if i.sheee == None or i.arrow == None or i.push == None:
                i.all_reply = "err"
            else:
                i.all_reply = i.sheee + i.push + i.arrow
            for ck in content_keywords[2:len(content_keywords) - 2].split('], ['):
                ckeyword = ck.split(', ')
                if ckeyword[0] in content_result:
                    #  print(u"".join(ckeyword[0]))
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
        post_classes = [u.class_id for u in UserSavePost.objects.filter(
            user_id=request.user.id)]
        return render(request, 'home.html', {'all_data': raw_data,
                                             'all_reply_counter': _all_reply_counter,
                                             'all_content_counter': _all_content_counter,
                                             'urls': urls,
                                             'post_classes': set(post_classes)
                                             })

    else:
        return render(request, 'home.html', {'all_data': "",
                                             'all_reply_counter': "",
                                             'all_content_counter': ""})


@login_required()
def add_new_keyword(request):
    def _get_urlmd5id(keyword):
        return md5(keyword).hexdigest()

    if request.POST:
        try:
            keyword_class = request.POST['keywordClass']
            print(keyword_class)
            new_word = request.POST['new_word']
            print(new_word)
            try:
                tmp = Newkeywords.objects.get(keyword=new_word)
                print("this data was in the db")
            except Newkeywords.DoesNotExist:
                kid = _get_urlmd5id(new_word.encode('utf-8'))
                k = Newkeywords(id=kid, keyword=new_word.encode('utf-8'),
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
            reply_raw = GossipingReply.objects.get(
                pid=request.GET['pid']).reply
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
                        #  w[w.index(""", "push_tag": """) + len(""", "push_tag": \""""):w.index("""", "push_date":""")],
                        #  w[w.index(""", "push_user": """) +
                          #  len(""", "push_user": \""""):w.index("""", "push_tag""")],
                        #  w[w.index("""push_content": ":""") +
                          #  len("""push_content": ":"""):w.index('", "push_user": ')],
                        #  w[w.index(""", "push_date": """) + len(""", "push_date": \""""):w.index("\n")]])
                        w[w.index(""""push_tag": """) + len("""\"push_tag": \""""):w.index("""\", "push_date\":""")],
                        w[w.index(""", "push_user": """) + len(""", \"push_user\": \""""):w.index("""\", "push_content": \"""")],
                        w[w.index("""push_content\": \":""") + len("""push_content": ":"""):],
                        w[w.index(""", "push_date": """) + len(""", \"push_date\": \""""):w.index("\n")]
                        ])
            post.sorted_hash = sorted(
                content_result.items(), key=operator.itemgetter(1), reverse=True)[:25]
            post.sorted_reply = sorted(
                reply_result.items(), key=operator.itemgetter(1), reverse=True)[:50]

            post.re_sorted_content = sorted(re_content_result.items(
            ), key=operator.itemgetter(1), reverse=True)[:25]
            post.re_sorted_reply = sorted(re_reply_result.items(
            ), key=operator.itemgetter(1), reverse=True)[:50]
            post.content = GossipingContent.objects.get(
                pid=request.GET['pid']).content
            print(post.push)
            return render(request, 'result.html', {'post': post, 're_post': re_post, 'reply': reply})
        else:
            return HttpResponse(status=404)
    else:
        return HttpResponse(status=404)
