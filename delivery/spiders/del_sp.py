# -*- coding: utf-8 -*-
import scrapy


class DelSpSpider(scrapy.Spider):
    name = 'del_sp'
    allowed_domains = ['online.hunterexpress.com.au']
    start_urls = ['http://online.hunterexpress.com.au/']

    def parse(self, response):
        pass
