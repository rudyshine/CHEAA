# - * - coding: utf-8 - * -

from scrapy.spiders import CrawlSpider
from cheaa.items import CheaaItem
import scrapy
import time
import requests

class cheaaSpider(CrawlSpider):
    name = "cheaa_spider"
    allowed_domains = ["cheaa.com"]
    start_urls = [
        # 'http://news.cheaa.com/renwu.shtml',
        # 'http://news.cheaa.com/hangye.shtml'
        "http://news.cheaa.com/renwu_18.shtml"
    ]

    def parse(self, response):
        for sel in response.xpath('//div[@class="ListPageBox  list"]/ul/li/div[@class="hbox-r"]/h2'):
            start_url = response.url
            links=sel.xpath('a/@href').extract()[0]
            if_belong =links.startswith('http://news.cheaa.com/')  ##
            if(if_belong):
                link=links
                print(link)
                yield scrapy.Request(url=link, callback=self.parse_ccontent,meta={'start_url': start_url})  ##meta方法传值start_url
    #     #
    #     ##下一页
    #     next_page=sel.xpath('//*[@id="ListPage"]/ul/li[9]/a/@href').extract()[0]
    #     if next_page:
    #         next_link=next_page
    #         print(next_link)
    #         # yield scrapy.Request(url=next_link, callback=self.parse_ccontent)

        ##xpath不能取到下一页面的连接
        next_links=response.url.replace('.shtml','')
        for i in range(2,3784):
            next_link = next_links + '_' + str(i) + '.shtml'
            # print(next_link)
            r=requests.get(next_link)
            if r.status_code==404:
                break
            yield scrapy.Request(url=next_link, callback=self.parse)


    ##解析详情页面
    def parse_ccontent(self,response):
        start_url=response.meta['start_url']
        for url in response.xpath('//*[@id="main-l1"]'):
            item=CheaaItem()
            item['LinkUrl'] =response.url
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
            item['startUrl'] = start_url  ##meta方法获取传过来的值
            ProgramStarttime=time.strftime('%Y-%m-%d', time.localtime(time.time()))
            item['ProgramStarttime']=ProgramStarttime
            yield item

            for i in range(2,5):
                next_content_page=response.url.replace('.shtml','')
                next_content_link=next_content_page+'_'+str(i)+'.shtml'
                r=requests.get(next_content_link)
                if r.status_code==404:
                    break
                yield scrapy.Request(url=next_content_link, callback=self.parse_ccontent,meta={'start_url': start_url})

