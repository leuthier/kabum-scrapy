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
            
        ## the computer's list index start at 3
        start = 3
        for computer in computers:
            item = KabumItem()
            
            item['name'] = computer.xpath(
                'normalize-space(//*[@id="BlocoConteudo"]/div[2]/div/div['+str(start)+']/div[2]/span[1]//text())').extract()[0]

            ## Sometimes computer's prices doesn't have "De R$ xx,xx por..." at beginning, we check below
            price_query = computer.xpath(
                'normalize-space(//*[@id="BlocoConteudo"]/div[2]/div/div['+str(start)+']/div[3]/div[2]//text())').extract()[0]
            if "EM" in price_query:
                item['price'] = computer.xpath(
                    'normalize-space(//*[@id="BlocoConteudo"]/div[2]/div/div['+str(start)+']/div[3]/div[1]//text())').extract()[0]
            else:
                item['price'] = price_query
                
            price_cash_query = computer.xpath(
                    'normalize-space(//*[@id="BlocoConteudo"]/div[2]/div/div['+str(start)+']/div[3]/div[4]//text())').extract()[0]
            if "%" in price_cash_query:
                item['price_cash'] = computer.xpath(
                    'normalize-space(//*[@id="BlocoConteudo"]/div[2]/div/div['+str(start)+']/div[3]/div[3]//text())').extract()[0]
            else:
                item['price_cash'] = price_cash_query
 
            item['url'] = computer.xpath(
              'normalize-space(//*[@id="BlocoConteudo"]/div[2]/div/div['+str(start)+']/div[2]/span//@href)').extract()[0]
            item['data_id'] = computer.xpath(
              'normalize-space(//*[@id="BlocoConteudo"]/div[2]/div/div['+str(start)+']/div[2]/span//@data-id)').extract()[0]

            ## Verifies thats computer is available to purchase            
            purchase_status = computer.xpath(
                'normalize-space(//*[@id="BlocoConteudo"]/div[2]/div/div['+str(start)+']/div[4]/div/a/img/@src)').extract()[0]
            if "_off" in purchase_status:
                item['status'] = "Indisponivel"
            else:
                item['status'] = "Disponivel"

            item['url_photo'] = computer.xpath(
                '//*[@id="BlocoConteudo"]/div[2]/div/div['+str(start)+']/div[1]/a/img/@src').extract()[0]

            stars = computer.xpath(
                '//*[@id="BlocoConteudo"]/div[2]/div/div['+str(start)+']/div[2]/div/ul/li[3]/div/@class').extract()[0]
            if stars[len(stars)-1] == "e":
                item['stars'] = 0
            else:
                item['stars'] = stars[len(stars)-1]

            start += 1
            yield item
        
        next_pages=[]
        #next_pages = response.xpath('//*[@id="BlocoConteudo"]/div[2]/div/div[2]/form/table/tbody/tr/td[6]/span/a/@href').extract()
        next_pages.append("?string=&dep=04&sec=34&cat=&sub=&pagina=2&ordem=5&limite=30")
        next_pages.append("?string=&dep=04&sec=34&cat=&sub=&pagina=3&ordem=5&limite=30")
        for i in next_pages:
            next_url = "http://www.kabum.com.br/computadores/computadores/"+i
            #logging.info('NEXT_URL: '+next_url)
            yield scrapy.Request(url=next_url, callback=self.parse)
            
