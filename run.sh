#!/bin/sh
source /home/ubuntu/.virtualenvs/tzscrape/bin/activate
cd /home/ubuntu/projects/tzscrape
scrapy crawl citizen
scrapy crawl mwananchi
scrapy crawl daily_news
scrapy crawl habarileo
scrapy crawl guardian
scrapy crawl nipashe