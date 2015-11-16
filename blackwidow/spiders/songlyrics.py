import re

import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

from ..items import Song

class SonglyricsSpider(CrawlSpider):
  name = 'songlyrics'
  custom_settings = {
        'FEED_URI' : './output/songlyrics.csv',
        'FEED_FORMAT' : 'CSV'
    }
  allowed_domains = ['songlyrics.com']
  start_urls = ['http://www.songlyrics.com/']
  rules = [
    Rule(LinkExtractor(allow=(r'/[a-z0]/(\d+)?',))),
    Rule(LinkExtractor(allow=(r'/[a-z-]+/[a-z-]+-lyrics/',),
                       deny=(r'/news/',)), callback='parse_song'),
    Rule(LinkExtractor(allow=(r'/[a-z-]+-lyrics/',))),
  ]

  def parse_song(self, response):
    song = Song()
    song['provider'] = 'songlyrics'
    song['url'] = response.url
    song['title'] = re.sub(r'(.*) Lyrics', r'\1', response.css('.current').xpath('text()').extract()[0])
    song['artist'] = response.css('.pagetitle').xpath('.//a/text()').extract()[0]
    song['lyrics'] = ''.join(response.css('#songLyricsDiv').extract())
    yield song
