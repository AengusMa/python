# -*- coding: utf-8 -*-
import scrapy
from tutorial1.items import Tutorial1Item

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['toscrape.com']
    start_urls = ['http://quotes.toscrape.com/page/1/']

    def parse(self, response):
        for quote in response.css('div .quote'):
            item = Tutorial1Item()
            item['text'] = quote.css('span.text::text').extract_first()
            item['author'] = quote.css('small.author::text').extract_first()
            item['tags'] = quote.css('div.tags a.tag::text').extract(),
            yield item
        for a in response.css('li.next a'):
            yield response.follow(a, callback=self.parse)
