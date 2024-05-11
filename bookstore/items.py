# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookstoreItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    bookURL = scrapy.Field()
    bookName = scrapy.Field()
    price = scrapy.Field()
    stock = scrapy.Field()
    descrip = scrapy.Field()
    rating = scrapy.Field()

    pass
