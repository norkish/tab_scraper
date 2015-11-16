# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from slugify import slugify

class TabItem(scrapy.Item):
    title = scrapy.Field()
    body = scrapy.Field()
    url = scrapy.Field()
    raw_html = scrapy.Field()
    raw_tab = scrapy.Field()
    contributor = scrapy.Field()
    difficulty = scrapy.Field()
    artist = scrapy.Field()
    rating = scrapy.Field()
    type = scrapy.Field()
    comments = scrapy.Field()
    key = scrapy.Field()
    youtube = scrapy.Field()
    provider = scrapy.Field()

    def filename(self):
        return slugify(unicode(self['provider']) + ' - ' + unicode(self['artist']) + ' - ' + unicode(self['title']))

    def encodeTab(self):

        output = u""
        for key in self.keys():
            if key not in {'raw_html', 'raw_tab'}:
                output += u"%%%% " + unicode(key) + ":" + unicode(self[key]) + u" %%%%\n"

        output += u"%%%% Tab:" + unicode(self['raw_tab']) + u"\n"

        return unicode(output)



class Song(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    artist = scrapy.Field()
    lyrics = scrapy.Field()
    match = scrapy.Field()
    provider = scrapy.Field()
