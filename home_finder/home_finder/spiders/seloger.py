# -*- coding: utf-8 -*-
from scrapy import Spider

from scrapy_splash import SplashRequest

from ..utils import csv_load


BASE_URL = "https://www.seloger.com/list.htm?{parameters}"


class SelogerSpider(Spider):
    name = 'seloger'
    allowed_domains = ['seloger.com']
    start_urls = ['https://www.seloger.com/']

    def parse(self, response):
        print(BASE_URL.format(parameters=self.parameters()))

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, callback=self.parse,args={'wait':'5'})

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
