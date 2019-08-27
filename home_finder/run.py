
import os

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings

from home_finder.spiders.seloger import SelogerSpider
from home_finder.utils import retrieve_environ


def setup_settings():
    settings = Settings()
    settings_module_path = 'home_finder.settings'
    settings.setmodule(settings_module_path, priority='project')
    dropbox_token = retrieve_environ("DROPBOX_TOKEN")
    settings.set("DROPBOX_TOKEN", dropbox_token)
    return settings

home_finder_settings = settings=setup_settings()

crawler = CrawlerProcess(settings=home_finder_settings)

crawler.crawl(SelogerSpider)
crawler.start()
