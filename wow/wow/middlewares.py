# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from wow.phone_user_agent import PHONE_USER_ANGET
import random
import requests
import logging
import scrapy

class WowSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class WowDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class phone_middle(object):
    def __init__(self):
        self.phone_ua=PHONE_USER_ANGET
    # 如果在scrapy.Request()
    # 中设置了headers参数，中间件中使用setdefault，则不会修改原有的user - agent
    def process_request(self,request,spider):
        request.headers['User-Agent']=random.choice(self.phone_ua)
        #没有返回值，则会继续执行其他的process_request

class use_proxy(object):
    def __init__(self,web_proxy):
        self.proxy_url=web_proxy
        self.logger=logging.getLogger(__name__)
    @classmethod
    def from_crawler(cls,crawler):
        return cls(web_proxy=crawler.settings.get('WEB_PROXY'))
    def get_random_proxy(self):
        """
        requests 专门import的包，而非scrapy的request实例
        :return:
        """
        try:
            response=requests.get(self.proxy_url)
            if response.status_code==200:
                proxy=response.text
                return proxy
        except requests.ConnectionError:
            return False
    def process_request(self,request,spider):
        #相当于获取meta中retry times的值
        #也可以直接request.meta['retry_times']
        #但是为了统一，我们都用get
        #重点啊   要是用get就是执行方法，圆括号，而非直接引用的[]方括号
        #如果第一次request失败
        if request.meta.get('retry_times'):
            proxy=self.get_random_proxy()
            #如果成功拿到代理
            if proxy:
               self.logger.debug('启用代理')
               url='https://{proxy}'.format(proxy=proxy)
               request.meta['proxy']=url







