# -*- coding: utf-8 -*-
import scrapy
import os, io, re
from delivery.read_data import convert_pdf_to_txt
from delivery.items import DeliveryItem


class DelSpSpider(scrapy.Spider):
    name = 'del_sp'
    allowed_domains = ['online.hunterexpress.com.au']

    phone_regex = re.compile(r'.*\d{5,}.*', re.MULTILINE)

    def start_requests(self):
        url = 'https://online.hunterexpress.com.au/'
        start = getattr(self, 'start', None)
        end = getattr(self, 'end', None)
        verbose = getattr(self, 'verbose', None)
        preffix = 'XX'

        if start and end and (verbose == 'true' or verbose == 'false'):
            start = int(start)
            end = int(end)
            verbose = True if verbose == 'true' else False
            for i in range(start, end):
                pdf_ref = os.path.join(url, 'tmp', preffix + str(i) + '.pdf')
                yield scrapy.Request(pdf_ref, self.parse, errback=self.errback_httpbin, meta={'start': start, 'end': end, 'verbose': verbose})
        else:
            print('Please set the starting and ending parameters for supposed file name. Also set correct verbose=true/false argument.')

    def errback_httpbin(self, failure):
        pass
        # request = failure.request
        # yield DeliveryItem(sender='',
        #                    text='',
        #                    phone='',
        #                    url=request.url,
        #                    status='error ' + repr(failure))

    def parse(self, response):
        if response.status >= 500 and response.status < 600:
            yield DeliveryItem(sender='',
                               text='',
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

                sender_name = os.linesep.join(doc_pdf_text.split(os.linesep + os.linesep)[1:6]).replace(
                    'Receiver :', '').replace(
                    'Phone: ', '').replace(
                    'Instr uctions:', '').replace(
                    'Sender :', '').replace(
                    os.linesep + os.linesep, os.linesep
                )

                phone = os.linesep.join(self.phone_regex.findall(sender_name))
                sender_name = self.phone_regex.sub('', sender_name).replace(os.linesep + os.linesep, os.linesep)

                yield DeliveryItem(sender=sender_name,
                                text=doc_pdf_text if response.meta.get('verbose') else '',
                                phone=phone,
                                url=response.url,
                                status='success')
            
            else:
                yield DeliveryItem(sender='',
                                text='',
                                phone='',
                                url=response.url,
                                status='not a pdf')
            
