# -*- coding: utf-8 -*-

from math import ceil

from scrapy import Spider
from scrapy_splash import SplashRequest
from scrapy_selenium import SeleniumRequest

from lxml import html

from ..utils import csv_load
from ..items import HomeFinderItem


BASE_URL = "https://www.seloger.com/list.htm?{parameters}"


class SelogerSpider(Spider):
    name = 'seloger'
    allowed_domains = ['seloger.com']

    def parse(self, response):
        root = html.fromstring(response.body)

        nb_annonces = root.cssselect('div.title_nbresult')[0].text_content().strip().split(" ")[0]
        nb_pages = ceil(int(nb_annonces) / 20)

        for annonce in self.parse_page(response):
            yield annonce

        for n in range(2, nb_pages):
            url = "&".join([response.url, "LISTING-LISTpg={page}".format(page=n)])
            yield SeleniumRequest(url=url, callback=self.parse_page, wait_time=15)

    def parse_page(self, response):
        root = html.fromstring(response.body)
        annonces_by_page = root.xpath('//section[@class="liste_resultat"]/div[contains(@class, "c-pa-list")]')
        for annonce in annonces_by_page:
            yield self.parse_annonce(annonce)

    def parse_annonce(self, element):
        item = HomeFinderItem()
        item['url'] = element[1][0].get('href')
        item['size'] = element[1][1][2].text_content()
        item['price'] = element[1][2][1].text_content().strip()
        item['city'] = element[1][4].text_content().strip()
        item['annonce_id'] = element[1][5].get('data-idannonce')
        return item

    # overriding start_requests means that the urls defined in start_urls are ignored.
    def start_requests(self):
        for url in self.search_url:
            yield SeleniumRequest(url=url, callback=self.parse, wait_time=15)

    @property
    def search_url(self):
        return [
            BASE_URL.format(parameters=self.parameters())
        ]

    def parameters(self):

        types, projects, enterprise, picture, natures, qsversion = self.parameters_seloger()

        surface = "surface={surfaces}".format(
            surfaces=self.parameters_surface()
        )

        price = "price={prices}".format(
            prices=self.parameters_price()
        )

        rooms = "rooms={total}".format(
            total=self.parameters_rooms()
        )

        bedrooms = "bedrooms={total}".format(
            total=self.parameters_bedrooms()
        )

        places = "places=[{places}]".format(
            places=self.parameters_places()
        )

        parameters = [
            types,
            projects,
            enterprise,
            picture,
            natures,
            surface,
            rooms,
            bedrooms,
            price,
            places,
            qsversion
        ]

        return "&".join(parameters)

    def parameters_seloger(self):
        seloger_settings = self.pipeline._settings['seloger']
        types = "types={}".format(seloger_settings['types'])
        projects = "projects={}".format(seloger_settings['projects'])
        enterprise = "enterprise={}".format(seloger_settings['enterprise'])
        picture = "picture={}".format(seloger_settings['picture'])
        natures = "types={}".format(seloger_settings['natures'])
        qsversion = "qsVersion={}".format(seloger_settings['qsversion'])
        return (types, projects, enterprise, picture, natures, qsversion)

    def parameters_surface(self):
        s = self.pipeline._settings['search']['surface']
        min_surface = "NaN" if s['min'] == 0 else s['min']
        max_surface = "NaN" if s['max'] == 0 else s['max']
        return "{min}/{max}".format(min=min_surface, max=max_surface)

    def parameters_price(self):
        p = self.pipeline._settings['search']['price']
        min_price = "NaN" if p['min'] == 0 else p['min']
        max_price = "NaN" if p['max'] == 0 else p['max']
        return "{min}/{max}".format(min=min_price, max=max_price)

    def parameters_rooms(self):
        return self.pipeline._settings['search']['rooms']

    def parameters_bedrooms(self):
        return self.pipeline._settings['search']['bedrooms']

    def parameters_places(self):

        def find_row(codes, city):
            for code in codes:
                if city == code[0]:
                    break
            else:
                error_msg = "ERROR: <{}> does not exists".format(city)
                raise Exception(error_msg)
            return code

        def process_code(code):
            if code == "75":
                return "{" + "cp:" + code + "}"
            code = "{0}0{1}".format(code[0:2], code[2:])
            return "{" + "ci:" + code + "}"

        places = []
        insee_code_city_filename = self.settings["INSEE_CODE_FILENAME"]
        insee_codes = csv_load(insee_code_city_filename)
        cities = self.pipeline._settings['search']['cities']
        for city in cities:
            found_row = find_row(insee_codes, city.upper())
            processed_row = process_code(found_row[2])
            places.append(processed_row)

        return "|".join(places)
