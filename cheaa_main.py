from scrapy import cmdline
# cmdline.execute("scrapy crawlall".split())  ##同时执行

cmdline.execute("scrapy crawl cheaa_spider".split()) ##单个执行
#
# cmdline.execute("scrapy crawl cheaa_news".split()) ##单个执行


