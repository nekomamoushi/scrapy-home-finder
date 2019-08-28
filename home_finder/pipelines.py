# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
import csv

from .items import HomeFinderItem
from .utils import get_dropbox_object, yaml_load, csv_load, Notifier

class HomeFinderPipeline(object):
    def __init__(self, crawler):
        self._load_settings(crawler)
        self._filename = "{name}.csv".format(name=crawler.spider.name)
        if os.path.exists(self._filename):
            annonces = csv_load(self._filename, delimiter='|')
            self._annonce_ids = [annonce[0] for annonce in annonces]
            os.remove(self._filename)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def _load_settings(self, crawler):
        self._dropbox_token = crawler.settings.get("DROPBOX_TOKEN")
        self._dbx = get_dropbox_object(self._dropbox_token)
        self._settings_file = crawler.settings.get("DROPBOX_SETTINGS_FILENAME")
        self._settings = yaml_load(self._dbx, self._settings_file)
        self._notifier = Notifier(
            crawler.settings.get("NOTIFIER_TOKEN"),
            crawler.settings.get("NOTIFIER_TRIGGER")
        )

    def open_spider(self, spider):
        spider.pipeline = self
        self._fp = open(self._filename, 'w', encoding='utf8')
        self._writer = csv.writer(self._fp, delimiter='|')
        item = HomeFinderItem()
        self._fields = [name for name in item.fields]
        self._item_processed = 0
        self._news = []

    def check_annonce(self, item):
        annonce_id = item['annonce_id']
        if annonce_id in self._annonce_ids:
            self._news.append(item)

    def process_item(self, item, spider):
        self._writer.writerow([item[name] for name in self._fields])
        self._item_processed = self._item_processed + 1
        self.check_annonce(item)
        return item

    def close_spider(self, spider):
        spider.logger.info("Items processes = {}".format(self._item_processed))
        spider.logger.info("You have {number} new annonces.".format(number=len(self._news)))
        if os.path.exists(self._filename) and self._news:
            for item in self._news:
                self._notifier.notify(item)
        self._fp.close()
