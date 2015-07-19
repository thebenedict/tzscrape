import scrapy
import datetime
from tzscrape.items import CitizenItem

class CitizenSpider(scrapy.Spider):
    name = 'citizen'
    allowed_domains = ['thecitizen.co.tz']
    start_urls = ['http://www.thecitizen.co.tz/']

    def parse(self, response):
        # editor's choice
        for href in response.css('.ec_item_inner a').xpath('@href[1]'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_article)

        # latest news and single column (opinion, business) panels
        for href in response.css('.newslist li a').xpath('@href[1]'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_article) 

        # sections with "split panels"
        for href in response.css('.dn2LeftOverall h3 a').xpath('@href[1]'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_article) 

        for href in response.css('.topDN2List li a').xpath('@href[1]'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_article) 

    def parse_article(self, response):
        item = CitizenItem()
        item['url'] = response.url
        item['publication'] = 'citizen'
        item['title'] = response.css('h1').xpath('text()').extract()
        item['body'] = []
        item['meta'] = response.css('#articlemeta').xpath('text()').extract()
        item['scraped_at'] = datetime.datetime.utcnow().isoformat()

        pages = set(response.css('#article_pages a').xpath('@href').extract())
        if len(pages):
            pages = enumerate(pages)
            idx, page = pages.next()
            yield scrapy.Request(response.urljoin(page), callback = self.parse_pages,
                meta = {'item': item, 'pages': pages})
        else:
            item['body'] = response.css('#article_text p').xpath('text()').extract()[1:]
            yield item


    def parse_pages(self, response):
        partial_item = response.request.meta['item']
        partial_item['body'] += response.css('#article_text p').xpath('text()').extract()[1:]
        try:
            idx, page = response.request.meta['pages'].next()
            yield scrapy.Request(response.urljoin(page), callback = self.parse_pages,
                meta = {'item': partial_item, 'pages': response.request.meta['pages']})
        except StopIteration:
            yield partial_item