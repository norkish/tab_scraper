# -*- coding: utf-8 -*-
import scrapy
from blackwidow.items import TabItem
from string import ascii_lowercase

class UltimateGuitarSpider(scrapy.Spider):
    name = "ultimate-guitar"
    allowed_domains = ["ultimate-guitar.com"]
    start_urls = [
        # A manual list of urls to start parsing from
        'http://www.ultimate-guitar.com/bands/0-9.htm'
                 ] + [

        # Add all of the letters a-z to the list of urls to start
        'http://www.ultimate-guitar.com/bands/' + c + '.htm' for c in ascii_lowercase
    ]

    # Parse the initial search page
    def parse(self, response):
        # Make a list of all artists on the page, and call parse_artist on them
        for link in response.css("table.b3 + table a"):
            absoluteUrl = response.urljoin(link.xpath('./@href').extract_first())

            req = scrapy.Request(absoluteUrl, callback=self.parse_artist)

            # pass along some data to the next step
            req.meta['artist'] = link.xpath('./text()').extract_first()

            yield req

        # Recursively call this function on all pagination links
        for href in response.css("table table table tr:nth-child(4) a.ys::attr('href')"):
            absoluteUrl = response.urljoin(href.extract())

            yield scrapy.Request(absoluteUrl, callback=self.parse)


    def parse_artist(self, response):
        for item in response.css("table.b3 + table tr"):
            absoluteUrl = response.urljoin(item.css("a::attr('href')").extract_first())

            req = scrapy.Request(absoluteUrl, callback=self.parse_tab)

            # pass along some more information to the song page
            req.meta['artist'] = response.meta['artist']
            req.meta['absoluteUrl'] = absoluteUrl
            req.meta['title'] = item.css('a::text').extract_first()
            req.meta['rating'] = item.css("td:nth-child(2) span:first-child::attr('class')").extract_first()
            req.meta['type'] = item.css("td:nth-child(3) b::text").extract_first()

            yield req

        for href in response.css("table table table tr:nth-child(4) a.ys::attr('href')"):
            absoluteUrl = response.urljoin(href.extract())

            yield scrapy.Request(absoluteUrl, callback=self.parse)

    def parse_tab(self, response):

        item = TabItem()
        item['raw_html'] = response.body
        item['raw_tab'] = ''.join(response.xpath("//pre[2]/node()").extract())
        item['contributor'] = response.css('.t_dtd div::text').extract_first()
        item['difficulty'] = response.css('.t_dtd div + div::text').extract_first()
        item['artist'] = response.meta['artist']
        item['rating'] = response.meta['rating']
        item['type'] = response.meta['type']
        item['url'] = response.url
        item['comments'] = [comment.strip() for comment in response.css('.comment_content p').extract()]
        item['provider'] = 'ultimate-guitar'
        item['title'] = response.meta['title']

        yield item
