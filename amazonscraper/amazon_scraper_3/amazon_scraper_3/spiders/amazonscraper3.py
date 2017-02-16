# -*- coding: utf-8 -*-
import scrapy
from ..items import AmazonScraper3Item
from scrapy.spiders import Spider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy import Request
import time
import sys
from scrapy.conf import settings

class AmazonScraper3(scrapy.Spider):
    name = "amazonscraper"
    allowed_domans = ["amazon.com"]
    handle_httpstatus_list = [404, 302, 301, 429]
    #https://www.amazon.com/health-personal-care-nutrition-fitness/b?ie=UTF8&node=3760901
    start_urls = ["https://www.amazon.com/health-personal-care-nutrition-fitness/b?ie=UTF8&node=3760901"]

    def parse(self, response):
	item = AmazonScraper3Item()
	hrefs = resonse.xpath()
	sel = Selector(response)
	hrefs_1 = response.xpath('//div[h3[contains(text(), "Household Supplies")]]/p[@class="seeMore"]/a/@href').extract()
	hrefs_1 = map(unicode.strip, hrefs_1)
	base_url = "https://www.amazon.com"
	for href1 in hrefs_1:
	    url = baseurl + str(href1)
	    print url
	    yield scrapy.Request(url, callback=self.parse_2nd_level)



    def parse_2nd_level(self, response):
	hrefs_2 = response.xpath('//div[@class="categoryRefinementsSection"]/ul/li/a/@href').extract()
	#level = response.xpath('//div[@class="categoryRefinementsSection"]/ul/li/a/@href').extract()
	hrefs_2 = map(unicode.strip, hrefs_2)
	for href2 in hrefs_2:
	    print href2
	    url = base_url + str(href2)
	    yield scrapy.Request(url, callback=self.parse_3rd_level)

    ###################################### Navigate to 3rd level #########################################
    """
    https://www.amazon.com/b/ref=s9_acss_bw_ct_refTest_ct2_cta_w?_encoding=UTF8&ie=UTF8&node=15342841&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-4&pf_rd_r=8MZZC2RNQ790XYNM5EPF&pf_rd_t=101&pf_rd_p=93e09301-f0a3-5f0b-901e-6f09b7730143&pf_rd_i=15342811
    Trash Bags (8,406)
    Bath Tissue (7,639)
    Paper Towels (8,048)
    Napkins (7,645)
    Facial Tissues (5,868)
    Plates & Cutlery (26,727)
    Cups & Straws (25,060)
    Food Storage (13,998)
    Coffee Filters (4,325)
    """
    def parse_3rd_level(self, response):
        hrefs_3 = response.xpath('//div[@class="categoryRefinementsSection"]/ul/li[a[span[@class="refinementLink"]]]/a/@href').extract()
        hrefs_3 = map(unicode.strip, hrefs_3)
        for href3 in hrefs_3:
            print href3
            url = base_url + str(href3)
            yield scrapy.Requests(url, callback=self.parse_4th_level)


    ####################################Navigate to 4th Level##########################################
    """
    HTTPS://www.amazon.com/s/ref=lp_15342841_nr_n_0/164-8988282-8343319?fst=as%3Aoff&rh=n%3A3760901%2Cn%3A%213760931%2Cn%3A15342811%2Cn%3A15342841%2Cn%3A15342971&bbn=15342841&ie=UTF8&qid=1487173350&rnid=15342841
    """
    def parse_4th_level(self, response):
        #hrefs_4 = response.xpath('').extract()
        #hrefs_4 = response.xpath('//div[@id="mainResults"]/ul/li[starts-with(@id, "result")]/div[@class="s-item-container"]/div/div/a[contains(@class, "a-link-normal s-access-detail-page  a-text-normal")]/@href').extract()
        hrefs_4 = response.xpath('//div[@id="mainResults"]/ul/li[starts-with(@id, "result")]/div[@class="s-item-container"]/\
                div/div/a[contains(@class, "a-link-normal s-access-detail-page  a-text-normal") and contains(@href, "https://www.amazon.com")]/@href').extract()
        hrefs_4 = map(unicode.strip, hrefs_4)
        for href4 in hrefs4:
            print href4
            yield scrapy.Request(href4, callback=self.parse_pagination_level)
    """
    Pagination:
    It will keep crawling until all the pages exhausted

    """
    def parse_pagination_level(self, response):

    """
    Detail product Page
    """
    def parse_detail_product(self, response):

        sel = Selector(response)
        item = AmazonScraper3Item()
        productTitle = response.xpath('//span[@id="productTitle"]/text()').extract_first().replace('\n', '').strip()

	try:
	    item['Product_title'] = productTitle
	except:
	    pass
        price = :
	#productPrice = response.xpath("")
	#item['Price'] = '$123'
	#yield item


