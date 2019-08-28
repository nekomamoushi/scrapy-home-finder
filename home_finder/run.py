
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
    settings.set("DROPBOX_TOKEN", retrieve_environ("DROPBOX_TOKEN"))
    settings.set("DROPBOX_SETTINGS_FILENAME", "/home-finder/settings.yml")
    settings.set("INSEE_CODE_FILENAME", os.getcwd() + "/resources/insee_city_codes.csv")
    settings.set("NOTIFIER_TOKEN", retrieve_environ("NOTIFIER_TOKEN"))
    settings.set("NOTIFIER_TRIGGER", "seloger")
    return settings

home_finder_settings = settings=setup_settings()
crawler = CrawlerProcess(settings=home_finder_settings)
crawler.crawl(SelogerSpider)
crawler.start()
