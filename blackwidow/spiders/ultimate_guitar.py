# -*- coding: utf-8 -*-
import HTMLParser
import scrapy
from blackwidow.items import TabItem
from string import ascii_lowercase

parser = HTMLParser.HTMLParser()

class UltimateGuitarSpider(scrapy.Spider):
    custom_settings = {
        'FEED_URI' : './output/ultimate-guitar.csv',
        'FEED_FORMAT' : 'CSV'
    }
    name = "ultimate-guitar"
    allowed_domains = ["ultimate-guitar.com"]
    start_urls = [
        # A manual list of urls to start parsing from
	'https://www.ultimate-guitar.com/bands/0-9.htm'
                 ] + [
	
        # Add all of the letters a-z to the list of urls to start
        'https://www.ultimate-guitar.com/bands/' + c + '.htm' for c in ascii_lowercase
    ]

    # Parse the initial search page
    def parse(self, response):
        # Make a list of all artists on the page, and call parse_artist on them
        for link in response.css('table.b3 + table a'):
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
        # The following conditional prevents the first page from being downloaded
        # remove this and the "req.meta['additional'] = True" line in the subseqent
        # loop to download all pages for all artists
        #if 'additional' in response.meta:
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

        for href in response.css("table table table a.ys::attr('href')"):
            absoluteUrl = response.urljoin(href.extract())
            req = scrapy.Request(absoluteUrl, callback=self.parse_artist)
            #req.meta['additional'] = True
            req.meta['artist'] = response.meta['artist']
            yield req

    def parse_tab(self, response):

        item = TabItem()
        #item['raw_html'] = response.body
        item['raw_tab'] = parser.unescape(''.join(response.xpath("//pre[2]/node()").extract()))
        
        labels = '\n'.join(response.css('.t_dt').xpath('.//text()').extract()).strip().lower().split('\n')
        values = '\n'.join(response.css('.t_dtd').xpath('.//text()').extract()).strip().split('\n')

	values = [x.strip() for x in values]
	labels = [x.strip() for x in labels]
	values = filter(None,values)
	labels = filter(None, labels)

        for label, value in zip(labels, values):
            if label == 'difficulty':
                item['difficulty'] = value
            elif label == 'contributor':
                item['contributor'] = value
	    elif label == 'key':
                item['key'] = value
        item['artist'] = parser.unescape(response.meta['artist'])
        #item['rating'] = response.meta['rating']
        item['type'] = response.meta['type']
        item['url'] = response.url
        #item['comments'] = parser.unescape([comment.strip() for comment in response.css('.comment_content p').extract()])
        item['provider'] = 'ultimate-guitar'
        item['title'] = parser.unescape(response.meta['title'])

        yield item
