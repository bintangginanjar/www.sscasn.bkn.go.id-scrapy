# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy.item import Item, Field
from itemloaders.processors import MapCompose, TakeFirst, Join


class CpnsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    instansi = Field()
    pengadaan = Field()
    jabatan = Field()
    lokasi = Field()
    pendidikan = Field()
    jenisFormasi = Field()
    disabilitas = Field()
    kebutuhan = Field()

    pass
