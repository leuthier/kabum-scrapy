import scrapy
import logging
from scrapy.item import Item, Field
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser


class LoginSpider(scrapy.Spider):
    name = "kabum"
    allowed_domains = ["kabum.com.br"]
    start_urls = [
        "https://www.kabum.com.br/cgi-local/site/login/login.cgi"
    ]

    def parse(self, response):
        # this is a fake kabum account created just for educational purpose
        formdata = {'login': 'scrapy.kabum@hotmail.com',
                'senha': 'testescrapy' }
        yield FormRequest.from_response(response,
                                formnumber = 1,
                                formdata = formdata,
                                clickdata = {'name': 'commit'},
                                callback = self.parse1)

    def parse1(self, response):
        # when user try to login in the website if fails has "msg" at url to show a error at browser
        if "msg=" in response.url:
            logging.info("-----------------------------")
            logging.info("        LOGIN FAILED         ")
            logging.info("-----------------------------")
        else:
            logging.info("-----------------------------")
            logging.info("       LOGIN SUCCESSFUL      ")
            logging.info("-----------------------------")
        open_in_browser(response)
          
