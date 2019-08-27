# scrapy api
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from home_finder.spiders.seloger import SelogerSpider


settings = get_project_settings()

# crawl responsibly
crawler = CrawlerProcess(settings=settings)

crawler.crawl(SelogerSpider)
crawler.start()
