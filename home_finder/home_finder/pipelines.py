# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class HomeFinderPipeline(object):
    def __init__(self, crawler):
        self._dropbox_token = crawler.settings.get("DROPBOX_TOKEN")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_item(self, item, spider):
        return item
