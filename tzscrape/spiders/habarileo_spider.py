import scrapy
import datetime
from tzscrape.items import HabarileoItem

class HabarileoSpider(scrapy.Spider):
    name = 'habarileo'
    allowed_domains = ['habarileo.co.tz']
    start_urls = ['http://www.habarileo.co.tz/']

    def parse(self, response):
        top_slider_xpath = '//div[@id="Mod124"]//h4[@class="ja-zintitle"]//@href'
        side_accordion_xpath = '//div[@id="ja-accordion114"]//@href'
        section_boxes_xpath = '//div[@id="Mod120"]//div[@class="ja-box-inner clearfix"]//@href'
        bottom_slider_xpath = '//div[@id="Mod122"]//@href'
        xpaths = [top_slider_xpath, side_accordion_xpath, section_boxes_xpath, bottom_slider_xpath]

        for xp in xpaths:
            for href in response.xpath(xp):
                url = response.urljoin(href.extract())
                yield scrapy.Request(url, callback=self.parse_article)


    def parse_article(self, response):
        item = HabarileoItem()
        item['body'] = response.xpath('//section[@itemprop="articleBody"]/p/text()').extract()

        if not item['body']:
            yield None
        else :
            item['url'] = response.url
            item['publication'] = 'habarileo'
            item['title'] = response.xpath('//h1[@itemprop="name"]/a/text()').extract()
            item['byline'] = response.xpath('//dd[@itemprop="author"]/span/text()').extract()
            item['scraped_at'] = datetime.datetime.utcnow().isoformat()
            yield item