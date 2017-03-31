# -*- coding: utf-8 -*-
import scrapy

#create the KabumItem class with item's attributes to save in database
class KabumItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    price_cash = scrapy.Field()
    url = scrapy.Field()
    data_id = scrapy.Field()
    status = scrapy.Field()
    url_photo = scrapy.Field()
    stars = scrapy.Field()
