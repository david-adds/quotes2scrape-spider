import scrapy
from scrapy.selector import Selector
from shutil import which
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class QuotesSpiderSelenium(scrapy.Spider):
    name = 'quotes_selenium'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = [
        'http://quotes.toscrape.com'
    ]
    
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        
        chrome_path = which("./chromedriver")
        driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)
        driver.set_window_size(1920,1080)
        driver.get("http://quotes.toscrape.com")
        
        quotes = driver.find_elements_by_class_name('row')
        
        self.html = driver.page_source
        driver.close()
        
    def parse(self, response):
        resp = Selector(text=self.html)
        for quote in resp.xpath("//div[contains(@class,'quote')]"):
            yield{
                'quote':quote.xpath(".//span[1]/text()").get(),
                'author':quote.xpath(".//small/text()").get(),
                'tags':quote.xpath(".//div[contains(@class,'tag')]/a/text()").getall()
            }
        
