import scrapy
import datetime
from tzscrape.items import CitizenItem

class CitizenSpider(scrapy.Spider):
    name = 'citizen'
    allowed_domains = ['thecitizen.co.tz']
    start_urls = ['http://www.thecitizen.co.tz/']

    def parse(self, response):
        # headlines
        for href in response.xpath('//*[@itemprop="headline"]/a/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_article)

        #teasers
        for href in response.css('li.story-teaser').xpath('a/@href[1]'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_article)


    def parse_article(self, response):
        item = CitizenItem()
        item['body'] = response.xpath('//div[@itemprop="articleBody"]/div/p//text()').extract()

        if not item['body']:
            yield []
        else :
            item['url'] = response.url
            item['publication'] = 'citizen'
            item['title'] = response.css('h1').xpath('text()').extract()
            item['byline'] = response.css('section.author').xpath('text()').extract()
            item['scraped_at'] = datetime.datetime.utcnow().isoformat()
            yield item