# - * - coding: utf-8 - * -

from scrapy.spiders import CrawlSpider
from cheaa.items import CheaaItem
import scrapy
import time

class cheaaSpider(CrawlSpider):
    name = "cheaa_news"
    allowed_domains = ["cheaa.com"]
    start_urls = [
        # 'http://news.cheaa.com/renwu.shtml',
        'http://news.cheaa.com/hangye.shtml'
    ]

    def parse(self, response):
        start_url= response.url
        for sel in response.xpath('//div[@class="ListPageBox  list"]/ul/li/div[@class="hbox-r"]/h2'):
            links=sel.xpath('a/@href').extract()[0]
            if_belong =links.startswith('http://news.cheaa.com/')  ##
            if(if_belong):
                link=links
                yield scrapy.Request(url=link,callback=self.parse_ccontent,meta={'start_url':start_url}) ##meta方法传值start_url
        #
        ##下一页
        next_page=sel.xpath('//*[@id="ListPage"]/ul/li[9]/a/@href').extract()[0]
        if next_page:
            next_link=next_page
            yield scrapy.Request(url=next_link, callback=self.parse)

    ##解析详情页面
    def parse_ccontent(self,response):
        for url in response.xpath('//*[@id="main-l1"]'):
            item=CheaaItem()
            item['LinkUrl'] =response.url
            item['Title']=url.xpath('//div[@id="NewsTitle"]/h1/text()').extract()[0]
            NewsInfo=url.xpath('//div[@id="NewsInfo"]/text()').extract()[0].strip()##来源+时间
            item['Time']=NewsInfo[0:16]
            item['InfoFrom']=NewsInfo
            item['ArtcleContent']=url.xpath('//*[@id="ctrlfscont"]/p/text()').extract()
            item['startUrl']= response.meta['start_url']  ##meta方法获取传过来的值
            yield item



