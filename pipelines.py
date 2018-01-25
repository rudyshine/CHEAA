# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings

class CheaaPipeline(object):
    def __init__(self):
        # 连接数据库
        self.client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
        # 数据库登录需要帐号密码的话,在settings.py底部追加
        # MINGO_USER = "username"
        # MONGO_PSW = "password"
        # self.client.admin.authenticate(settings['MINGO_USER'], settings['MONGO_PSW'])
        self.db = self.client[settings['MONGO_DB']]  # 获得数据库的句柄
        self.coll = self.db[settings['MONGO_COLL']]  # 获得collection的句柄

    def process_item(self, item, spider):
        insert_item = dict(item)  # 把item转化成字典形式
        # 插入之前查询text是否存在，不存在的时候才插入。
        self.coll.update({"LinkUrl": insert_item['LinkUrl']}, {
                         '$setOnInsert': insert_item}, True)
        # self.coll.insert(insert_item)  # 向数据库插入一条记录
        return item  # 会在控制台输出原item数据，可以选择不写
