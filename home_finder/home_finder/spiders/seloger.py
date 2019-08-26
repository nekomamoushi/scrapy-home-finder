# -*- coding: utf-8 -*-
import scrapy


class SelogerSpider(scrapy.Spider):
    name = 'seloger'
    allowed_domains = ['seloger.com']
    start_urls = ['https://www.seloger.com/']

    def parse(self, response):
        pass
