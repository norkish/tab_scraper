import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import Song

class LyricsnetSpider(CrawlSpider):
  name = 'lyricsnet'
  custom_settings = {
        'FEED_URI' : './output/lyricsnet.csv',
        'FEED_FORMAT' : 'CSV'
    }
  allowed_domains = ['lyrics.net']
  start_urls = ['http://www.lyrics.net/']
  rules = [
    Rule(LinkExtractor(allow=(r'/artists/[0A-Z](/99999)?',))),
    Rule(LinkExtractor(allow=(r'/artist/[^/]+(/\d+)?',))),
    Rule(LinkExtractor(allow=(r'/album/\d+',))),
    Rule(LinkExtractor(allow=(r'/lyric/\d+',)), callback='parse_song'),
  ]

  def parse_song(self, response):
    song = Song()
    song['provider'] = 'lyricsnet'
    song['url'] = response.url
    song['title'] = response.css('.lyric-title').xpath('text()').extract()[0]
    song['artist'] = response.css('.lyric-artist a').xpath('text()').extract()[0]
    song['lyrics'] = ''.join(response.css('.lyric-body').extract())
    yield song
