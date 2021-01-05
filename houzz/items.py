# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Field, Item


class HouzzItem(Item):
    # define the fields for your item here like:
    url = Field()
    name = Field()
    image_1 = Field()
    image_2 = Field()
    tag = Field()
    page = Field()
    datetime = Field()
    category = Field()
