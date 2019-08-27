# -*- coding: utf-8 -*-
from scrapy import Spider

from scrapy_splash import SplashRequest



class SelogerSpider(Spider):
    name = 'seloger'
    allowed_domains = ['seloger.com']
    start_urls = ['https://www.seloger.com/']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, callback=self.parse,args={'wait':'5'})

    def parse(self, response):
        pass
