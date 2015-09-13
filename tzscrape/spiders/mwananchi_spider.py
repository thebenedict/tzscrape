import scrapy
import datetime
from tzscrape.items import MwananchiItem

class MwananchiSpider(scrapy.Spider):
    name = 'mwananchi'
    allowed_domains = ['mwananchi.co.tz']
    start_urls = ['http://www.mwananchi.co.tz/']

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
        item = MwananchiItem()
        item['body'] = response.xpath('//div[@itemprop="articleBody"]/div/p//text()').extract()

        if not item['body']:
            yield None
        else :
            item['url'] = response.url
            item['publication'] = 'Mwananchi'
            item['title'] = response.css('h1').xpath('text()').extract()
            item['byline'] = response.css('section.author').xpath('text()').extract()
            item['scraped_at'] = datetime.datetime.utcnow().isoformat()
            yield item