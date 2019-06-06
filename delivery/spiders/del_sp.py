# -*- coding: utf-8 -*-
import scrapy
import os, io, re
from delivery.read_data import convert_pdf_to_txt
from delivery.items import DeliveryItem


class DelSpSpider(scrapy.Spider):
    name = 'del_sp'
    allowed_domains = ['online.hunterexpress.com.au']

    def start_requests(self):
        url = 'https://online.hunterexpress.com.au/'
        start = getattr(self, 'start', None)
        end = getattr(self, 'end', None)
        preffix = 'XX'

        if start and end:
            start = int(start)
            end = int(end)
            for i in range(start, end):
                pdf_ref = os.path.join(url, 'tmp', preffix + str(i) + '.pdf')
                yield scrapy.Request(pdf_ref, self.parse, errback=self.errback_httpbin, meta={'start': start, 'end': end})
        else:
            print('Please set the starting and ending parameters for supposed file name')

    def errback_httpbin(self, failure):
        request = failure.request
        yield DeliveryItem(name='',
                           address='',
                           description='',
                           weight='',
                           phone='',
                           url=request.url,
                           status='error ' + repr(failure))

    def parse(self, response):
        if response.status >= 500 and response.status < 600:
            yield DeliveryItem(name='',
                               address='',
                               description='',
                               weight='',
                               phone='',
                               url=response.url,
                               status='server error ' + str(response.status))
        else:
            has_doc = False
            content_type = response.headers.get('Content-Type', def_val=b'').decode()
            for typ in ['application/pdf', 'application/octet-stream', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
                has_doc = True if typ in content_type else False
                if has_doc: 
                    break

            if has_doc:
                # pdf parse here
                bytesio = io.BytesIO(response.body)
                bfr = io.BufferedReader(bytesio)
                doc_pdf_text = convert_pdf_to_txt(bfr)



                # regex parse here
                yield DeliveryItem(name=doc_pdf_text, #change here
                                address='',
                                description='',
                                weight='',
                                phone='',
                                url=response.url,
                                status='success')
            
            else:
                yield DeliveryItem(name='',
                                address='',
                                description='',
                                weight='',
                                phone='',
                                url=response.url,
                                status='not a pdf')
            