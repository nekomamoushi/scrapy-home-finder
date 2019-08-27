# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from .utils import get_dropbox_object, yaml_load

class HomeFinderPipeline(object):
    def __init__(self, crawler):
        self._load_settings(crawler)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def _load_settings(self, crawler):
        self._dropbox_token = crawler.settings.get("DROPBOX_TOKEN")
        self._dbx = get_dropbox_object(self._dropbox_token)
        self._settings_file = crawler.settings.get("DROPBOX_SETTINGS_FILENAME")
        self._settings = yaml_load(self._dbx, self._settings_file)

    def open_spider(self, spider):
        spider.pipeline = self

    def process_item(self, item, spider):
        return item
