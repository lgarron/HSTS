# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class HSTSItem(Item):
    index = Field()
    url = Field()
    status = Field()
    hsts = Field()
    location = Field()
    protocol = Field()
    www = Field()
