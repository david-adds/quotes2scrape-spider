import scrapy
from scrapy_splash import SplashRequest


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
        
    script = '''
        function main(splash,args)
            splash.private_mode_enable = false
            url = args.url
            assert(splash:go(url))
            assert(splash:wait(1))
            quotes = assert(splash:select_all('.row'))
            assert(splash:wait(1))
            splash:set_viewport_full()
            return splash:html()
        end
    '''
    def start_requests(self):
        yield SplashRequest(url='http://quotes.toscrape.com',callback=self.parse,endpoint='execute',args={
            'lua_source': self.script
        })

    def parse(self, response):
        for quote in response.xpath("//div[contains(@class,'quote')]"):
            yield{
                'quote':quote.xpath(".//span[1]/text()").get(),
                'author':quote.xpath(".//small/text()").get(),
                'tags':quote.xpath(".//div[contains(@class,'tag')]/a/text()").getall()
            }
            
        next_page = response.xpath(
             "//li[@class='next']/a/@href").get()
        if next_page:
            absolute_url = f"http://quotes.toscrape.com{next_page}"
            yield SplashRequest(url=absolute_url, callback=self.parse, endpoint='execute', args={
                'lua_source': self.script
            })
        
