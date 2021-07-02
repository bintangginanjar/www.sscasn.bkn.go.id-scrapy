import scrapy
import json

from scrapy_splash import SplashRequest
from scrapy.loader import ItemLoader
from cpns.items import CpnsItem

class CpnsSpider(scrapy.Spider):
    name = 'cpns'
    
    custom_settings = {
        'FEED_EXPORT_FIELDS': [
            'instansi',
            'pengadaan',
            'jabatan',
            'lokasi',
            'pendidikan',
            'jenisFormasi',
            'disabilitas',
            'kebutuhan'
        ]
    }


    def start_requests(self):
        self.logger.info('Start requests')
        
        targetUrl = 'https://data-sscasn.bkn.go.id/spf'
        yield scrapy.Request(targetUrl, callback=self.reqPengadaan)


    def reqPengadaan(self, response):
        self.logger.info('Request pengadaan')

        dropdownList = []
        numOfList = 0

        for row in response.xpath('//select[@id="jenisPengadaan"]'):            
            jenisPengadaanList = row.xpath('option/text()').extract()
            del jenisPengadaanList[0]
            dropdownList.append(jenisPengadaanList)

            idPengadaanList = row.xpath('option/@value').extract()
            del idPengadaanList[0]
            dropdownList.append(idPengadaanList)

            numOfList = len(idPengadaanList)

        for i in range(numOfList):            
            targetUrl = 'https://data-sscasn.bkn.go.id/spf/getInstansi?jenisPengadaan=' + idPengadaanList[i]
            yield scrapy.Request(targetUrl, method='GET', callback=self.reqInstansi, meta={'jenisPengadaan': dropdownList[0][i], 'idPengadaan': dropdownList[1][i]})
        
    
    def reqInstansi(self, response):
        self.logger.info('Request instansi')
        resp = json.loads(response.text)

        for row in resp:            
            targetUrl = 'https://data-sscasn.bkn.go.id/spf?jenisPengadaan=' + response.meta['idPengadaan'] + '&instansi=' + row['kode']
            yield scrapy.Request(targetUrl, method='GET', callback=self.parseLowongan, meta={'jenisPengadaan': response.meta['jenisPengadaan'], 'idPengadaan': response.meta['idPengadaan'], 'namaInstansi': row['nama']})            


    def parseLowongan(self, response):
        self.logger.info('Parse lowongan')     
        
        for row in response.xpath('//*[@class="table"]//tbody//tr'):            
            loader = ItemLoader(item = CpnsItem(), selector = row)
            loader.add_value('instansi', response.meta['namaInstansi'])
            loader.add_value('pengadaan', response.meta['jenisPengadaan'])
            loader.add_xpath('jabatan', 'td[1]//text()')
            loader.add_xpath('lokasi', 'td[2]//text()')
            loader.add_xpath('pendidikan', 'td[3]//text()')
            loader.add_xpath('jenisFormasi', 'td[4]//text()')
            loader.add_xpath('disabilitas', 'td[5]//text()')
            loader.add_xpath('kebutuhan', 'td[6]//text()')

            yield loader.load_item()       