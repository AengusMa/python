# -*- coding: utf-8 -*-
# @Author: mwl
import scrapy

class ZhaoBao(scrapy.Spider):
    name="zaobao"
    start_urls = ['http://www.zaobao.com/special/report/politic/fincrisis']
    def parse(self,response):
        for i in range(18):
            url = response.xpath('//*[@id="DressUp"]/div[2]/div[1]/div['+str(i+1)+']/div/div/a/@href').extract()[0]
            full_url = full_url = response.urljoin(url)
            yield scrapy.Request(full_url,callback=self.parse_detail)
    def parse_detail(self,response):
        yield {
            ##.body-content .article-content-container
            #MainCourse > div .media-holder.main  .loadme  picture  img
			'title':response.css('div h1::text').extract()[0],
			'dt':response.css("div aside.trackme  span.datestamp::text").extract()[0],
			'body':response.css(".body-content .article-content-container p::text").extract(),
			'link': response.url,
		}
