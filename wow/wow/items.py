# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WowItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection='51job'
    job=scrapy.Field()
    job_url=scrapy.Field()
    ddate=scrapy.Field()
    salary=scrapy.Field()
    company=scrapy.Field()
    company_url = scrapy.Field()
    location=scrapy.Field()
    applicate_person=scrapy.Field()
    job_content=scrapy.Field()
    education=scrapy.Field()


