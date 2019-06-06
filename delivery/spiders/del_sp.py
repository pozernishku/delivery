# -*- coding: utf-8 -*-
import scrapy

import hashlib
import os, json
import io
from PIL import Image
import pytesseract
from wand.image import Image as wi
from delivery.read_data import convert_pdf_to_txt, document_to_text


class DelSpSpider(scrapy.Spider):
    name = 'del_sp'
    allowed_domains = ['online.hunterexpress.com.au']
    start_urls = ['https://online.hunterexpress.com.au/']

    def parse(self, response):
        pass
