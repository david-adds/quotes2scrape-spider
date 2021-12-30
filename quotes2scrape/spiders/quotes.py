import scrapy
from scrapy_splash import SplashRequest


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']
    
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
        print(response.body)
        
