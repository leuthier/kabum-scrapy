# -*- coding: utf-8 -*-
import scrapy
import logging
from kabum.items import KabumItem
from kabum.login import LoginSpider
from scrapy.item import Item, Field
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser

class KbSpider(scrapy.Spider):
    name = "kb"

    def start_requests(self):
        logar = LoginSpider()
        allowed_domains = ["kabum.com.br"]
        urls = [
            'http://www.kabum.com.br/computadores/computadores/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        computers = response.xpath('//div[@class="listagem-box"]')
            
        ## O indice dos computadores começa em 3
        start = 3
        for computer in computers:
            item = KabumItem()
            
            item['name'] = computer.xpath(
                '//*[@id="BlocoConteudo"]/div[2]/div/div['+str(start)+']/div[2]/span[1]//text()').extract()[0]

            ## Sometimes computer's prices doesn't have "De R$ xx,xx por..." at beginning, we check below
            price_query = computer.xpath(
                '//*[@id="BlocoConteudo"]/div[2]/div/div['+str(start)+']/div[3]/div[2]//text()').extract()[0]
            if "EM" in price_query:
                item['price'] = computer.xpath(
                    '//*[@id="BlocoConteudo"]/div[2]/div/div['+str(start)+']/div[3]/div[1]//text()').extract()[0]
            else:
                item['price'] = price_query
                
            price_cash_query = computer.xpath(
                    '//*[@id="BlocoConteudo"]/div[2]/div/div['+str(start)+']/div[3]/div[4]//text()').extract()[0]
            if "%" in price_cash_query:
                item['price_cash'] = computer.xpath(
                    '//*[@id="BlocoConteudo"]/div[2]/div/div['+str(start)+']/div[3]/div[3]//text()').extract()[0]
            else:
                item['price_cash'] = price_cash_query
 
            item['url'] = computer.xpath(
              '//*[@id="BlocoConteudo"]/div[2]/div/div['+str(start)+']/div[2]/span//@href').extract()[0]
            item['data_id'] = computer.xpath(
              '//*[@id="BlocoConteudo"]/div[2]/div/div['+str(start)+']/div[2]/span//@data-id').extract()[0]
            
            start += 1
            yield item

            logging.info('COMPUTERS SCRAPY FINISHED')

##            next_page = response.xpath(
##                '//*[@id="BlocoConteudo"]/div[2]/div/div[2]/form/table/tbody/tr/td[6]/span//a[1]/@href'
##            ).extract_first()
##            if next_page:
##                self.log('Next Page: {0}'.format(next_page))
##                yield scrapy.Request(url=next_page, callback=self.parse)
