# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
import csv

from .items import HomeFinderItem
from .utils import get_dropbox_object, yaml_load, csv_load

class HomeFinderPipeline(object):
    def __init__(self, crawler):
        self._load_settings(crawler)
        self._filename = "{name}.csv".format(name=crawler.spider.name)
        if os.path.exists(self._filename):
            self._annonces = csv_load(self._filename)
            os.remove(self._filename)

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
        self._fp = open(self._filename, 'w', encoding='utf8')
        self._writer = csv.writer(self._fp, delimiter='|')
        item = HomeFinderItem()
        self._fields = [name for name in item.fields]
        self._writer.writerow(self._fields)
        del item
        self._item_processed = 0

    def process_item(self, item, spider):
        self._writer.writerow([item[name] for name in self._fields])
        self._item_processed = self._item_processed + 1
        return item

    def close_spider(self, spider):
        print("Items processes = {}".format(self._item_processed))
        self._fp.close()
