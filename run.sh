#!/bin/sh
source /home/ubuntu/.virtualenvs/tzscrape/bin/activate
cd /home/ubuntu/projects/tzscrape
scrapy crawl citizen
scrapy crawl mwananchi
scrapy crawl daily_news