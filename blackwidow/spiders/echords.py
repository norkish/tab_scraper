# -*- coding: utf-8 -*-
import HTMLParser
import scrapy
from blackwidow.items import TabItem
from string import ascii_lowercase
import time

class EchordsSpider(scrapy.Spider):
    name = "echords"
    custom_settings = {
        'FEED_URI' : './output/echords.csv',
        'FEED_FORMAT' : 'CSV'
    }
    allowed_domains = ["e-chords.com"]
    start_urls = [
        # A manual list of urls to start parsing from
        'http://www.e-chords.com/browse/[0-9]'
    ] + [

        # Add all of the letters a-z to the list of urls to start
        'http://www.e-chords.com/browse/' + c for c in ascii_lowercase
    ]

    def parse(self, response):
        for link in response.css('.pages p a'):
            absoluteUrl = response.urljoin(link.xpath('./@href').extract_first())
    
            req = scrapy.Request(absoluteUrl, callback=self.parse_artist)

            req.meta['artist'] = link.xpath('.//text()').extract_first()
            #req.meta['country'] = link.xpath('')
            
            yield req

    def parse_artist(self, response):
        for item in response.css('.lista'):
            title = item.css('p a::text').extract_first()
            if len(response.css(".types")) > 0:
                for href in response.css(".types a:not(.tu):not(.tb2):not(.td2):not(.tf2):not(.tt2):not(.th2):not(.ti2)::attr(href)").extract():
                    absoluteUrl = response.urljoin(href)
                    req = scrapy.Request(absoluteUrl, callback=self.parse_tab)

                    req.meta['artist'] = response.meta['artist']
                    req.meta['title'] = title

                    yield req
            else:
                print('No types : ', absoluteUrl)

    def parse_tab(self, response):

        item = TabItem()
        item['title'] = response.meta['title']
        item['artist'] = response.meta['artist']
        #item['title'] = response.xpath("//h1/text()[normalize-space()]").extract_first()
        #item['artist'] = response.xpath("//h2[@id='artistname']/a/text()").extract_first()
        #item['raw_html'] = response.body
        item['raw_tab'] = HTMLParser.HTMLParser().unescape(''.join(response.xpath("//div[@class='coremain']/pre[@class='core']/node()").extract()))
        item['contributor'] = response.xpath("//div[@class='topo_cifra']/p[contains(., 'by')]/a/text()").extract_first()
        item['difficulty'] = response.xpath("//*[contains(., 'Difficulty')]/span/text()").extract_first()
        item['type'] = response.xpath("//div[@class='subopcoes']/span[@class='aba_active']/text()").extract_first()
        item['url'] = response.url
        item['key'] = response.xpath("//span[@class='actualkey']/text()").extract_first()
        item['provider'] = 'echords'

        yield item
