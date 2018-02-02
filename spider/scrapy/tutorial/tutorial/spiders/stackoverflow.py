# -*- coding: utf-8 -*-
# @Author: mwl
import scrapy
class StackOverflowSpider(scrapy.Spider):
    name = "stackoverflow"
    start_urls = ["http://stackoverflow.com/questions?sort=votes"]
    def parse(self):
        pass
