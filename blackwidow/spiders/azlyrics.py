import re
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

from ..items import Song

class AzlyricsSpider(CrawlSpider):
  name = 'azlyrics'
  custom_settings = {
        'FEED_URI' : './output/azlyrics.csv',
        'FEED_FORMAT' : 'CSV'
    }
  allowed_domains = ['azlyrics.com']
  start_urls = ['http://www.azlyrics.com']
  rules = [
    Rule(LinkExtractor(allow=(r'/lyrics/[a-z0-9_-]+/[a-z0-9_-]+\.html')),
         callback='parse_song'),
    Rule(LinkExtractor(allow=(r'/([a-z]|19)\.html',))),
    Rule(LinkExtractor(allow=(r'/([a-z]|19)/[a-z0-9_-]+\.html')))
  ]

  def parse_song(self, response):
    song = Song()
    song['provider'] = 'azlyrics'
    song['url'] = response.url
    song['title'] = response.xpath('//script').re(r'SongName = "([^"]+)"')[0]
    song['artist'] = response.xpath('//script').re(r'ArtistName = "([^"]+)"')[0]
    song['lyrics'] = ''.join(response.xpath("//div[@class='lyricsh']/following-sibling::div[not(self::*[@class='ringtone']) and position() < 3]").extract())
    
    yield song
