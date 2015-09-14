# -*- coding: utf-8 -*-

import scrapy

class CitizenItem(scrapy.Item):
  publication = scrapy.Field()
  title = scrapy.Field()
  scraped_at = scrapy.Field()
  byline = scrapy.Field()
  body = scrapy.Field()
  url = scrapy.Field()

class MwananchiItem(scrapy.Item):
  publication = scrapy.Field()
  title = scrapy.Field()
  scraped_at = scrapy.Field()
  byline = scrapy.Field()
  body = scrapy.Field()
  url = scrapy.Field()

class DailyNewsItem(scrapy.Item):
  publication = scrapy.Field()
  title = scrapy.Field()
  description = scrapy.Field()
  scraped_at = scrapy.Field()
  byline = scrapy.Field()
  body = scrapy.Field()
  url = scrapy.Field()

class HabarileoItem(scrapy.Item):
  publication = scrapy.Field()
  title = scrapy.Field()
  scraped_at = scrapy.Field()
  byline = scrapy.Field()
  body = scrapy.Field()
  url = scrapy.Field()
