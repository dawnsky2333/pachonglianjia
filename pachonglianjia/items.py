# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy
from scrapy import Field, Item


class PachonglianjiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # define the fields for your item here like:
    # name = scrapy.Field()
    district = Field()
    region = Field()
    id = Field()
    layout = Field()
    floor = Field()
    year = Field()
    size = Field()
    elevator = Field()
    renovation = Field()
    price = Field()