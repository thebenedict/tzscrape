import scrapy
import datetime
from tzscrape.items import DailyNewsItem

class DailyNewsSpider(scrapy.Spider):
    name = 'daily_news'
    allowed_domains = ['dailynews.co.tz']
    start_urls = ['http://dailynews.co.tz/']

    def parse(self, response):
        # headlines
        for href in response.xpath('//*[@class="article-title"]/*/*[@itemprop="url"]/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_article)


    def parse_article(self, response):
        item = DailyNewsItem()
        item['body'] = response.xpath('//section[@itemprop="articleBody"]/p/text()').extract()

        if not item['body']:
            yield None
        #skip photo galleries
        if "gallery" in response.url:
            yield None
        else :
            item['url'] = response.url
            item['publication'] = 'daily_news'
            item['title'] = [response.css('h1').xpath('a/text()').extract()[0].strip()]
            item['description'] = response.xpath('//blockquote[@itemprop="description"]/p/text()').extract()
            item['byline'] = response.xpath('//dd[@itemprop="author"]/span[@itemprop="name"]/text()').extract()
            item['scraped_at'] = datetime.datetime.utcnow().isoformat()
            yield item