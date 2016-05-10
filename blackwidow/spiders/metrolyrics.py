import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import Song

class MetroSpider(CrawlSpider):
  name = 'metrolyrics'
  custom_settings = {
        'FEED_URI' : './output/metrolyrics.csv',
        'FEED_FORMAT' : 'CSV'
    }
  allowed_domains = ['metrolyrics.com']
  start_urls = ['http://www.metrolyrics.com']
  rules = [
    Rule(LinkExtractor(allow=(r'/artists-[a-z1](-\d+)?\.html',))),
    Rule(LinkExtractor(allow=(r'/[a-z0-9-]+-(lyrics|overview|alpage-\d+)\.html',))),
    Rule(LinkExtractor(allow=(r'/[a-z0-9-]+-lyrics-[a-z0-9-]+\.html',),
                       deny=(r'/news-story-',)), callback='parse_song'),
  ]

  def parse_song(self, response):
    song = Song()
    song['provider'] = 'metrolyrics'
    song['url'] = response.url
    song['title'] = re.sub(r'(.*) Lyrics', r'\1', response.xpath('//h1/text()').extract()[0].strip())
    song['artist'] = re.sub(r'(.*) Lyrics', r'\1', response.xpath('//h2/text()').extract()[0].strip())
    song['lyrics'] = ''.join(response.css('#lyrics-body-text').extract())
    yield song
