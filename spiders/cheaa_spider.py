# - * - coding: utf-8 - * -

from scrapy.spiders import CrawlSpider
from cheaa.items import CheaaItem
import scrapy
import time

class cheaaSpider(CrawlSpider):
    name = "cheaa_spider"
    allowed_domains = ["cheaa.com"]
    start_urls = [
        'http://news.cheaa.com/renwu_18.shtml',
        # 'http://news.cheaa.com/hangye.shtml'
        # 'http://news.cheaa.com/2007/1016/100445.shtml'
    ]

    def parse(self, response):
        for sel in response.xpath('//div[@class="ListPageBox  list"]/ul/li/div[@class="hbox-r"]/h2'):
            start_url = response.url
            links=sel.xpath('a/@href').extract()[0]
            if_belong =links.startswith('http://news.cheaa.com/')  ##
            if(if_belong):
                link=links
                yield scrapy.Request(url=link, callback=self.parse_ccontent,meta={'start_url': start_url})  ##meta方法传值start_url
    #     #
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
            # print(item['LinkUrl'])
            item['Title']=url.xpath('//div[@id="NewsTitle"]/h1/text()').extract()[0]
            NewsInfo=url.xpath('//div[@id="NewsInfo"]/text()').extract()[0].strip()##来源+时间
            item['Time']=NewsInfo[0:16]
            item['InfoFrom']=NewsInfo
            SpanContent=url.xpath('//*[@id="ctrlfscont"]/p/span/text()').extract()
            Span2Content=url.xpath('//*[@id="ctrlfscont"]/span/text()').extract()
            PContent=url.xpath('//*[@id="ctrlfscont"]/p/text()').extract()
            p2Content=url.xpath('//*[@id="newsmemo"]/p/text()').extract()
            TextContent=url.xpath('//*[@id="ctrlfscont"]/text()').extract()
            Text2Content=url.xpath('//*[@id="font_word"]/text()').extract()
            CenterContent=url.xpath('//*[@id="ctrlfscont"]/center/p/text()').extract()
            EmContent=url.xpath('//*[@id="ctrlfscont"]/p/em/text()').extract()
            DivContent=url.xpath('//*[@id="ctrlfscont"]/div/text()').extract()
            FontContent=url.xpath('//*[@id="ctrlfscont"]/p/font/text()').extract()
            Font2Content=url.xpath('//*[@id="ctrlfscont"]/font/p/text()').extract()
            item['ArtcleContent']=FontContent+Span2Content+SpanContent+TextContent+DivContent+EmContent+PContent+CenterContent+p2Content+Text2Content+Font2Content
            item['startUrl'] = response.meta['start_url']  ##meta方法获取传过来的值
            ProgramStarttime=time.strftime('%Y-%m-%d', time.localtime(time.time()))
            item['ProgramStarttime']=ProgramStarttime
            yield item

            # next_content_page=url.xpath('//*[@id="show-all-cont"]/span/@href').extract()[0]
            # if next_content_page:
            #     next_content_link=next_content_page
            #     print("next_content_link:",next_content_link)
            #     yield scrapy.Request(url=next_content_link, callback=self.parse_ccontent)

