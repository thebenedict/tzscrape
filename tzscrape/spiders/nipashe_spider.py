import scrapy
import datetime
from tzscrape.items import NipasheItem

class NipasheSpider(scrapy.Spider):
    name = 'nipashe'
    allowed_domains = ['ippmedia.com']
    start_urls = ['http://www.ippmedia.com/?m=54&lang=SW']
    def parse(self, response):
        # lists of artcles
        feed_xpath = '//ul[@class="feed"]//a/@href'

        #top level articles in section boxes
        featured_xpath = '//a[text()="Habari Kamili"]/@href'

        #columns (editorials?)
        columns_xpath = response.xpath('//span[@class="column_name"]//a/@href').extract()

        xpaths = [feed_xpath, featured_xpath, columns_xpath]

        for xp in xpaths:
            for href in response.xpath(xp):
                url = response.urljoin(href.extract())
                yield scrapy.Request(url, callback=self.parse_article)


    def parse_article(self, response):
        item = NipasheItem()
        
        # The first paragraph of the body is in a <p> tag, the rest are <divs>, separated
        # by divs containing only &nbsp;
        first_para = response.xpath('//div[@class="article_content"]//p/text()').extract()

        # remaining paragraphs except the photo caption
        remaining_paras = response.xpath('//div[@class="article_content"]//div[not(@class="cap")]/text()[normalize-space()]').extract()
        
        # remove &nbsp;
        filter(lambda a: a != u'\xa0', remaining_paras)

        item['body'] = first_para + remaining_paras

        if not item['body']:
            yield None
        else :
            item['url'] = response.url
            item['publication'] = 'nipashe'
            item['title'] = response.xpath('//div[@class="content_title"]/h2/text()').extract()
            item['byline'] = response.xpath('//div[@class="byline"]/text()').extract()
            item['scraped_at'] = datetime.datetime.utcnow().isoformat()
            yield item