# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DeliveryItem(scrapy.Item):
    name = scrapy.Field()
    address = scrapy.Field()
    description = scrapy.Field()
    weight = scrapy.Field()
    phone = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()