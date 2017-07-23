# -*- coding: utf-8 -*-
import scrapy
import logging
from ptt.items import PostItem
from datetime import datetime


class PTTSpider(scrapy.Spider):
    name = "pttSpider"
    # allowed_domains = ["ptt.cc/bbs/Gossiping"]
    start_urls = (
        'https://www.ptt.cc/bbs/Gossiping/index.html',
    )
    custom_settings = {
        'ITEM_PIPELINES': {
            'ptt.pipelines.PttMongoPipeline': 300,
#            'ptt.pipelines.MySQLStorePipeline': 300,
            # 'ptt.pipelines.PttMysqlPipeline': 300
        }
    }

    def __init__(self):
        self._retries = 0
        self.MAX_RETRY = 5
        self._pages = 0
        self.MAX_PAGES = 50

    def parse(self, response):
        if len(response.xpath('//div[@class="over18-notice"]')) > 0:
            if self._retries < self.MAX_RETRY:
                self._retries += 1
                logging.warning('retry {} times...'.format(self._retries))
                yield scrapy.FormRequest.from_response(response,
                                                       formdata={'yes': 'yes'},
                                                       callback=self.parse)
            else:
                logging.warning('you cannot pass')

        else:
            self._pages += 1
            for href in response.css('.r-ent > div.title > a::attr(href)'):
                url = response.urljoin(href.extract())
                yield scrapy.Request(url, callback=self.parse_post)

            if self._pages < self.MAX_PAGES:
                # print ""
                next_page = response.xpath(
                    '//div[@class="btn-group btn-group-paging"]/a[2]/@href')
                if next_page:
                    url = response.urljoin(next_page[0].extract())
                    logging.warning('follow {}'.format(url))
                    yield scrapy.Request(url, self.parse)
                else:
                    logging.warning('no next page')
            else:
                logging.warning('max pages reached')

    def parse_post(self, response):
        title = response.xpath(
            '//meta[@property="og:title"]/@content')[0].extract()
        author = response.xpath(
            u'//div[@class="article-metaline"]/span[text()="作者"]/following-sibling::span[1]/text()')[
            0].extract().split(' ')[0]
        content = response.xpath('//div[@id="main-content"]/text()')[
            0].extract()
        item = PostItem()
        item['title'] = title
        item['author'] = author
        datetime_str = response.xpath(
            u'//div[@class="article-metaline"]/span[text()="時間"]/following-sibling::span[1]/text()')[
            0].extract()
        item['date'] = datetime.strptime(datetime_str, '%a %b %d %H:%M:%S %Y')

        item['content'] = ''
        for i in response.xpath('//div[@id="main-content"]/text()'):
            item['content'] += i.extract()
        item['author_ip'] = response.xpath('//div[@id="main-content"]/span[@class="f2"]/text()[contains(.,"ptt.cc")]')[
                                0].extract()[27:]
        comments = []
        # total_score = 0
        for comment in response.xpath('//div[@class="push"]'):
            push_tag = comment.css('span.push-tag::text')[0].extract()
            push_user = comment.css('span.push-userid::text')[0].extract()
            push_date = comment.css('span.push-ipdatetime::text')[0].extract()
            push_content = comment.css('span.push-content::text')[0].extract()

            #     if '推' in push_tag:
            #         score = 1
            #     elif '噓' in push_tag:
            #         score = -1
            #     else:
            #         score = 0
            #
            #     total_score += score
            #
            # item['score'] = total_score
            comments.append({'push_tag': push_tag,
                             'push_date': push_date,
                             'push_user': push_user,
                             'push_content': push_content})

        item['comments'] = comments

        item['url'] = response.url

        yield item
