from __future__ import with_statement
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess

"""
simple crawler to find pages on a website that include a specified keyword or phrase
"""



website_to_crawl = 'website.com' 		#website.com  -do not include 'www.'' or 'http'
keyword_to_search_for = 'this is my keyword phrase' #keyword or phrase


class someSpider(CrawlSpider):
	keyword = keyword_to_search_for
	custom_settings = {'JOBDIR': './job',}
	name = 'crawltest'
	allowed_domains = [website_to_crawl]
	start_urls = ['http://' + website_to_crawl]
	rules = (Rule(LinkExtractor(allow=(),unique=True), callback='parse_obj', follow=True),)



	def parse_obj(self,response):
	    text = response.xpath('//body//text()').extract()
	    text = ''.join(text)
	    link = response.request.url
	    with open('urls.txt', "a") as f:
	        if self.keyword in text:
    			f.write(link+'\n') 



if __name__ == "__main__":
	process = CrawlerProcess({
	    'USER_AGENT': 'Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 5.1)'
	})
	process.crawl(someSpider)
	process.start() # the script will block here until the crawling is finished