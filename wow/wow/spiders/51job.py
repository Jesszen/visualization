# -*- coding: utf-8 -*-
import scrapy
from wow.items import WowItem



class LagouSpider(scrapy.Spider):
    name = '51job'
    allowed_domains = ['51job.com']
    start_urls = ['https://m.51job.com/search/joblist.php?keyword=数据分析']

    def parse(self, response):
        result=response.xpath('//div[@class="items"]//a[@class="e eck "]')
        for m in result:
            detail_job_url=m.xpath('./@href').extract_first()
            yield scrapy.Request(detail_job_url,self.parse_detail)

        #选取当前页最后一个
        page_on=''.join(response.xpath('//div[@class="items"]//a[last()]//h3//text()').extract()).strip()
        if '数据分析'in page_on:
            next_page=response.xpath('//div[@class="paging"]//a[last()]/@href').extract_first()
            yield scrapy.Request(next_page,self.parse)

    def parse_detail(self,response):
        item = WowItem()
        item['job']=response.xpath('//div[@class="jt"]/p/text()').extract_first()
        item['job_url']=response.url
        item['salary']=response.xpath('//p[@class="jp"]/text()').extract_first()
        item['ddate']=response.xpath('//div[@class="jt"]/span/text()').extract_first()
        item['location']=response.xpath('//div[@class="jt"]/em/text()').extract_first()
        item['education']=''.join(response.xpath('//div[@class="jd"]//text()').extract()).strip()
        #如果元素class在变化，但知道位置在第一个。直接用/替代//【@class=】
        item['company']=response.xpath('//div[@class="rec"]/a/p/text()').extract_first()
        item['company_url']=response.xpath('//div[@class="rec"]/a/@href').extract_first()
        item['applicate_person']=''.join(response.xpath('//div[@class="ain"]/article//text()').extract()).strip()
        #item['job_content']=response.xpath('//div[@class="ain"]/article//p[2]//text()').extract()
        yield item



    # def parse(self, response):
    #     result=response.xpath('//div[@class="items"]')
    #     for m in result:
    #         item=WowItem()
    #         item['job']=''.join(m.xpath('.//h3//text()').extract()).strip()
    #         item['salary']=m.xpath('.//em/text()').extract_first()
    #         item['company']=m.xpath('.//aside/text()').extract_first()
    #         item['location']=m.xpath('.//i/text()').extract_first()
    #         yield item
    #     #选取当前页最后一个
    #     page_on=''.join(response.xpath('//div[@class="items"]//a[last()]//h3//text()').extract()).strip()
    #     if '数据分析'in page_on:
    #         next_page=response.xpath('//div[@class="paging"]//a[class="next"]/@href').extract_first()
    #         yield scrapy.Request(next_page,self.parse)
