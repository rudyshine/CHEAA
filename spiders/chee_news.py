# - * - coding: utf-8 - * -

from scrapy.spiders import CrawlSpider
from cheaa.items import CheaaItem
import requests
import scrapy
import time
import re

class cheaaSpider(CrawlSpider):
    name = "cheaa_news"
    allowed_domains = ["cheaa.com"]
    start_urls = [
        'http://news.cheaa.com/2008/0221/117484.shtml']

    def parse(self,response):
        for next_content_url in response.xpath('//*[@id="main-l1"]'):
            item=CheaaItem()
            # item['LinkUrl'] =response.url
            # print(item['LinkUrl'])
            item['Title']=next_content_url.xpath('//div[@id="NewsTitle"]/h1/text()').extract()[0]
            print(item['Title'])
            NewsInfo=next_content_url.xpath('//div[@id="NewsInfo"]/text()').extract()[0].strip()##来源+时间
            item['Time']=NewsInfo[0:16]
            item['InfoFrom']=NewsInfo
            item['ArtcleContent']=next_content_url.xpath('//*[@id="ctrlfscont"]/p/text()').extract()
            # item['startUrl']= response.meta['start_url']  ##meta方法获取传过来的值
            yield item




            for i in range(2,6):
                next_content_page=response.url.replace('.shtml','')
                next_content_link=next_content_page+'_'+str(i)+'.shtml'
                r=requests.get(next_content_link)
                if r.status_code==404:
                    break
                yield scrapy.Request(url=next_content_link, callback=self.parse)
