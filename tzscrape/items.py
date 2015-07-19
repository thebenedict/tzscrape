# -*- coding: utf-8 -*-

import scrapy

class CitizenItem(scrapy.Item):
  publication = scrapy.Field()
  title = scrapy.Field()
  scraped_at = scrapy.Field()
  meta = scrapy.Field()
  body = scrapy.Field()
  url = scrapy.Field()
