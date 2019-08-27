
import os

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from home_finder.spiders.seloger import SelogerSpider
from home_finder.utils import retrieve_environ


settings = get_project_settings()
dropbox_token = retrieve_environ("DROPBOX_TOKEN")
settings.set("DROPBOX_TOKEN", dropbox_token)
print(list(settings.keys()))
exit()
crawler = CrawlerProcess(settings=settings)

crawler.crawl(SelogerSpider)
crawler.start()
