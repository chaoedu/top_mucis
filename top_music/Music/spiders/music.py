# !usr/bin/python
# -*- coding: utf-8 -*-


import json

import scrapy
from Music.items import MusicItem


class QuotesSpider(scrapy.Spider):
    name = "Music"

    def start_requests(self):
        netease_urls = [
            'http://music.163.com/discover/toplist?id=19723756',
            'http://music.163.com/discover/toplist?id=3779629',
            'http://music.163.com/discover/toplist?id=3778678'
        ]
        qq_urls = [
            'https://c.y.qq.com/v8/fcg-bin/fcg_v8_toplist_cp.fcg?topid=4',
            'https://c.y.qq.com/v8/fcg-bin/fcg_v8_toplist_cp.fcg?topid=26',
            'https://c.y.qq.com/v8/fcg-bin/fcg_v8_toplist_cp.fcg?topid=27',
            'https://c.y.qq.com/v8/fcg-bin/fcg_v8_toplist_cp.fcg?topid=33',
            'https://c.y.qq.com/v8/fcg-bin/fcg_v8_toplist_cp.fcg?topid=30'
        ]
        xiami_urls = [
            'http://www.xiami.com/chart/data?c=103',
            'http://www.xiami.com/chart/data?c=102',
            'http://www.xiami.com/chart/data?c=104'
        ]
        kugou_urls = [
            'http://mobilecdngz.kugou.com/api/v3/rank/song?rankid=6666&pagesize=100&plat=2&version=8930',
            'http://mobilecdngz.kugou.com/api/v3/rank/song?rankid=8888&pagesize=500&plat=2&version=8930',
            'http://mobilecdngz.kugou.com/api/v3/rank/song?rankid=31308&pagesize=100&plat=2&version=8930'
        ]
        for url in netease_urls:
            yield scrapy.Request(url=url, callback=self.parse_netease)
        for url in qq_urls:
            yield scrapy.Request(url=url, callback=self.parse_qq)
        for url in xiami_urls:
            yield scrapy.Request(url=url, callback=self.parse_xiami)
        for url in kugou_urls:
            yield scrapy.Request(url=url, callback=self.parse_kugou)

    def parse_netease(self, response):
        item = MusicItem()
        json_response = json.loads(response.css('textarea::text').extract()[0])
        list_name = u"网易云音乐-" + response.css('title::text').extract()[0].split('-')[0].strip()[3:]
        for num in range(len(json_response)):
            song = json_response[num]["name"]
            singer = json_response[num]["artists"][0]["name"]
            item['list_name'] = list_name
            item['num'] = num + 1
            item['song'] = song
            item['singer'] = singer
            yield item
        self.log('Saved top list %s' % list_name)

    def parse_qq(self, response):
        item = MusicItem()
        json_response = json.loads(response.body_as_unicode())
        list_name = u"QQ音乐-" + json_response["topinfo"]["ListName"]
        for num in range(json_response["total_song_num"]):
            song = json_response["songlist"][num]["data"]["songname"]
            singer = json_response["songlist"][num]["data"]["singer"][0]["name"]
            item['list_name'] = list_name
            item['num'] = num + 1
            item['song'] = song
            item['singer'] = singer
            yield item
        self.log('Saved top list %s' % list_name)

    def parse_xiami(self, response):
        item = MusicItem()
        title = {'102': u'新歌榜', '103': u'音乐榜', '104': u'原创榜'}
        result = response.xpath('//tr/@data-title').extract()
        list_name = u"虾米音乐-" + title[response.url[-3:]]
        for num in range(len(result)):
            song = result[num].split('-')[0].strip()
            singer = result[num].split('-')[1].strip()
            item['list_name'] = list_name
            item['num'] = num + 1
            item['song'] = song
            item['singer'] = singer
            yield item
        self.log('Saved top list %s' % list_name)

    def parse_kugou(self, response):
        item = MusicItem()
        title = {'6666': u'飙升榜', '8888': u'TOP500', '31308': u'华语新歌榜'}
        json_response = json.loads(response.body_as_unicode())
        list_name = u"酷狗音乐-" + title[response.url.split('?')[-1].split('&')[0].split('=')[-1]]
        for num in range(json_response['data']['total']):
            song = json_response['data']['info'][num]['filename'].split('-')[1].strip()
            singer = json_response['data']['info'][num]['filename'].split('-')[0].strip()
            item['list_name'] = list_name
            item['num'] = num + 1
            item['song'] = song
            item['singer'] = singer
            yield item
        self.log('Saved top list %s' % list_name)