#### Utilizando Scrapy para extrair dados da KaBuM
#### Site: http://www.kabum.com.br/

#### Tutorial


```
$ rethinkdb
$ git clone https://github.com/leuthier/kabum-scrapy
$ pip install -r requirements.txt
$ cd kabum-scrapy
$ scrapy crawl kb -o computers.json
$ scrapy runspider login.py
``` 

#### Índice
  * [Objetivos](https://github.com/leuthier/kabum-scrapy/blob/master/README.md#objetivos)
  * Arquivos:
      * [/kabum/spiders/kb.py](https://github.com/leuthier/kabum-scrapy#arquivo-kabumspiderskbpy)
      * [/kabum/pipelines.py](https://github.com/leuthier/kabum-scrapy#arquivo-kabumpipelinespy)
      * [/kabum/settings.py](https://github.com/leuthier/kabum-scrapy#arquivo-kabumsettingspy)
      * [/kabum/items.py](https://github.com/leuthier/kabum-scrapy#arquivo-kabumitemspy)
  * [Tempo gasto](https://github.com/leuthier/kabum-scrapy/blob/master/README.md#tempo-gasto)
  * [Programas utilizados](https://github.com/leuthier/kabum-scrapy/blob/master/README.md#programas-utilizados)
  * [Referências](https://github.com/leuthier/kabum-scrapy/blob/master/README.md#material)


#### Objetivos
- [x] Utilização de ```xpath``` nas buscas por links
- [x] Persistência das informações (RethinkDB)
- [x] Submissão de formulários
- [x] Utilização de logs para sinalizar ocorrências durante o scraping


#### Arquivo: [/kabum/spiders/kb.py](../blob/master/kabum/spiders/kb.py)
```python 
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

            logging.info('COMPUTERS SCRAPY FINISHED'
```

#### Arquivo: [/kabum/pipelines.py](../blob/master/kabum/pipelines.py)
```python
# -*- coding: utf-8 -*-

import rethinkdb as r

class RethinkdbPipeline(object):

    conn = None
    rethinkdb_settings = {}
    
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings

        ## get rethinkdb settings from settings.py
        rethinkdb_settings = settings.get('RETHINKDB', {})

        return cls(rethinkdb_settings)

    def __init__(self, rethinkdb_settings):
        self.rethinkdb_settings = rethinkdb_settings

    def open_spider(self, spider):
        if self.rethinkdb_settings:
            
            self.table_name = self.rethinkdb_settings['table_name']
            self.db_name = self.rethinkdb_settings['db']
            self.conn = r.connect('localhost', 28015)
            table_list = r.db(self.db_name).table_list().run(self.conn)
            
            ## verify if table already exists and creates a table in database              
            if self.table_name not in table_list:
                r.db(self.db_name).table_create(self.table_name).run(self.conn)

    def close_spider(self, spider):
        if self.conn:
            self.conn.close()

    def process_item(self, item, spider):
        if self.conn:
            r.db(self.db_name).table(self.table_name).insert(item).run(self.conn)
        return item 
```

#### Arquivo: [/kabum/settings.py](../blob/master/kabum/settings.py)
```python
# -*- coding: utf-8 -*-

# Scrapy settings for kabum project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html


BOT_NAME = 'kabum'

SPIDER_MODULES = ['kabum.spiders']
NEWSPIDER_MODULE = 'kabum.spiders'

RETHINKDB = {
    'table_name': 'computers', 'db': 'kabum'
}

ITEM_PIPELINES = {
    'kabum.pipelines.RethinkdbPipeline': 1
}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'kabum (+http://www.yourdomain.com)'

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 0.5
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'kabum.middlewares.KabumSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'kabum.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'kabum.pipelines.KabumPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
```

#### Arquivo: [/kabum/items.py](../blob/master/kabum/items.py)
```python
# -*- coding: utf-8 -*-
import scrapy

#create the KabumItem class with item's attributes to save in database
class KabumItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    price_cash = scrapy.Field()
    url = scrapy.Field()
    data_id = scrapy.Field()
```
 
 
#### Tempo gasto
  * Estudando:
  * Implementando:


#### Programas utilizados
  * [XPath Helper](https://chrome.google.com/webstore/detail/xpath-helper/hgimnogjllphhhkhlmebbmlgjoejdpjl)
  * [RethinkDB](https://www.rethinkdb.com/docs/install/)
  
  
#### Referências
  * [Guia de 10min com RethinkDB e Python [ENG]](https://www.rethinkdb.com/docs/guide/python/)
  * [Parte I - Configurando e rodando o Scrapy](http://www.gilenofilho.com.br/usando-o-scrapy-e-o-rethinkdb-para-capturar-e-armazenar-dados-imobiliarios-parte-i/)
  * [Instalando, configurando e armazenando os dados no Rethinkdb](http://www.gilenofilho.com.br/usando-o-scrapy-e-o-rethinkdb-para-capturar-e-armazenar-dados-imobiliarios-parte-ii/)
  * [XPath Tutorial [ENG]](https://www.w3schools.com/xml/xpath_intro.asp)
