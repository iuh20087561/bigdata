from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from bookstore.spiders.bookscrawl import BookscrawlSpider


process = CrawlerProcess(get_project_settings())
process.crawl(BookscrawlSpider)
process.start()
