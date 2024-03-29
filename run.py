
import os

from pathlib import Path
from dotenv import load_dotenv
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings

from home_finder.spiders.seloger import SelogerSpider
from home_finder.utils import retrieve_environ



def load_environ():
    load_if_dotenv()
    return from_environ()


def load_if_dotenv():
    env_path = Path(".") / ".env"
    load_dotenv(dotenv_path=env_path, verbose=False)


def from_environ():
    dropbox = retrieve_environ("DROPBOX_TOKEN")
    notifier = retrieve_environ("NOTIFIER_TOKEN")
    return (dropbox, notifier)


def setup_settings(dropbox, notifier):
    settings = Settings()
    settings_module_path = 'home_finder.settings'
    settings.setmodule(settings_module_path, priority='project')
    settings.set("HOME_FINDER_DROPBOX_TOKEN", dropbox)
    settings.set("HOME_FINDER_NOTIFIER_TOKEN", notifier)
    return settings


def main():
    dropbox, notifier = load_environ()
    home_finder_settings = setup_settings(dropbox, notifier)
    crawler = CrawlerProcess(settings=home_finder_settings)
    crawler.crawl(SelogerSpider)
    crawler.start()


if __name__ == "__main__":
    main()
