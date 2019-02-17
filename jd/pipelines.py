# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from jd import settings


class JdPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host = settings.MYSQL_HOST,
            port = settings.MYSQL_PORT,
            db = settings.MYSQL_DBNAME,
            user = settings.MYSQL_USER,
            passwd = settings.MYSQL_PASSWORD,
            charset = 'utf8',
            use_unicode = True )
        self.cursor = self.connect.cursor()

    # 数据入库方法
    def insertData(self, item):
        sql = "insert into iphone(spid, url_x, name, xiangqing, jiage, zhongliang) VALUES(%s, %s, %s, %s, %s, %s);"
        params = (item['spid'], item['url_x'], item['name'], item['xiangqing'], item['jiage'], item['zhongliang'])
        self.cursor.execute(sql, params)
        self.connect.commit()

    # 数据清洗方法
    def cls(self, item):
        spid_cls = item['spid']
        if spid_cls:
            item['spid'] = spid_cls.strip().replace('\n','').replace(' ','')

        url_x_cls = item['url_x']
        if url_x_cls:
            item['url_x'] = url_x_cls.strip().replace('\n','').replace(' ','')

        name_cls = item['name']
        if name_cls:
            item['name'] = name_cls.strip().replace('\n','').replace(' ','')

        xiangqing_cls = item['xiangqing']
        if xiangqing_cls:
            item['xiangqing'] = xiangqing_cls.strip().replace('\n','').replace(' ','')

    # 执行    
    def process_item(self, item, spider):
        self.cls(item)
        self.insertData(item)
        return item