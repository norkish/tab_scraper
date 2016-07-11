import scrapy
from scrapy.crawler import CrawlerProcess
from blackwidow.spiders.echords import EchordsSpider
from blackwidow.spiders.lyricsnet import LyricsnetSpider
from blackwidow.spiders.metrolyrics import MetroSpider
from blackwidow.spiders.songlyrics import SonglyricsSpider
from blackwidow.spiders.ultimate_guitar import UltimateGuitarSpider


process = CrawlerProcess()
#process.crawl(EchordsSpider)
process.crawl(LyricsnetSpider)
#process.crawl(MetroSpider)
#process.crawl(SonglyricsSpider)
#process.crawl(UltimateGuitarSpider)
process.start() # the script will block here until all crawling jobs are finished
