# -*- coding: utf-8 -*-
import scrapy
from jd.items import JdItem
from selenium import webdriver

class IphoneSpider(scrapy.Spider):
    name = 'iphone'
    allowed_domains = ['jd.com']
    start_urls = ['https://search.jd.com/Search?keyword=iphone&enc=utf-8&wq=iphone']

    def __init__(self):
        # 创建浏览器
        self.browser = webdriver.Firefox(executable_path='C:\Program Files\Mozilla Firefox\geckodriver.exe')
        # 设定浏览器大小（半屏）
        self.browser.set_window_size(960,1080)
        # 控制加载时间，超时会在中间件中停止
        self.browser.set_page_load_timeout(30)

    # 复写关闭爬虫时触发关闭浏览器
    def closed(self,spider):
        print('*****************爬虫关闭啦*****************')
        self.browser.close()

    def parse(self, response):
        item = JdItem()
        print('*****************爬虫开启啦*****************')
        # print('当前请求User-Agent是 ====> ' + str(response.request.headers['User-Agent']))
        # print('当前请求头是 ====> ' + str(response.request.headers['User-Agent']))
        li_list = response.xpath('//*[@id="J_goodsList"]/ul/li')
        for li in li_list:
            # 京东真不错，商品名称竟然分开写,此处应该判断下拆分的姓名是不是返回了None。
            name_0 = li.xpath('./div/div/a/em/text()[1]').extract_first()
            name_1 = li.xpath('./div/div/a/em/text()[2]').extract_first()
            if name_0 or name_1 is None:
                if name_0 is None:
                    item['name'] = name_1
                else:
                    item['name'] = name_0                
            else:
                item['name'] = name_0 + name_1
            item['spid'] = li.xpath('./@data-sku').extract_first()
            item['jiage'] = li.xpath('./div/div[3]/strong/i/text()').extract_first()
            item['url_x'] = 'https://item.jd.com/'+ item['spid'] + '.html'
            yield scrapy.Request(item['url_x'], callback=self.parse_ziye,meta=item)
            # print(item)

        # 读取下一页的URL，进行翻页。这里不详述了。

    def parse_ziye(self, response):
        item = response.meta
        item['xiangqing'] = response.xpath('//*[@id="p-ad"]/text()').extract_first()
        item['zhongliang'] = response.xpath('//*[@id="summary-weight"]/div[2]/text()').extract_first()
        # print(item)
        yield item

