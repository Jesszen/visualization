# -*- coding: utf-8 -*-
import scrapy


class TianyandSpider(scrapy.Spider):
    name = 'tianyand'
    allowed_domains = ['tainyan.com']
    start_urls = ['http://tainyan.com/']

    def parse(self, response):
        pass
