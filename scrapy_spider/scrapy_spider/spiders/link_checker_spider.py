# -*- coding: utf-8 -*-
from scrapy.crawler import CrawlerProcess
from scrapy import signals
import scrapy
import pandas as pd
import sys
import codecs
if sys.stdout.encoding != 'UTF-8':
	sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'ignore')


class LinkCheckerSpider(scrapy.Spider):
	name = "link_checker"
	allowed_domains = ['www.example.com']
	start_urls = ['https://www.example.com']
	# Set the HTTP error codes that should be handled
	handle_httpstatus_list = [301,302,303,304,305,306,400,401,402,403,404,405,406,407,408,409,410,411,412,413,414,415,416,417,500,501,502,503,504,505]
	# Initialize array for valid/invalid links
	valid_url = []
	invalid_url = []
	maxdepth = 1
	custom_settings = {
	'LOG_LEVEL': 'WARNING',
	'FEED_EXPORT_ENCODING': 'utf-8',

  # ... other settings...
  }


	def parse(self, response):
		from_url = ''
		from_text = ''
		depth = 0;
		if 'from' in response.meta: 
			from_url = response.meta['from']
		if 'text' in response.meta: 
			from_text = response.meta['text']
		if 'depth' in response.meta: 
			depth = response.meta['depth']
		if 'href' in response.meta:
			href = response.meta['href']

		print(depth, response.url, '<-', from_url, from_text, sep=' ')
		# 404 error, populate the broken links array
		if response.status in self.handle_httpstatus_list:
			self.invalid_url.append({'url': response.url,
									 'response': response.status,
									 'from': from_url,
									 'href': href,
									 'text': from_text})
		else:
			# Populate the working links array
			self.valid_url.append({'url': response.url,
								   'from': from_url,
								   'text': from_text})
			if depth < self.maxdepth:
				a_selectors = response.xpath("//a".replace(u'\u2212', '-'))
				for selector in a_selectors:
					text = selector.xpath("text()").extract_first()
					link = selector.xpath("@href").extract_first()
					request = response.follow(link, callback=self.parse)
					request.meta['from'] = response.url;
					request.meta['text'] = text
					request.meta['href'] = link
					yield request


	@classmethod
	def from_crawler(cls, crawler, *args, **kwargs):
		spider = super(LinkCheckerSpider, cls).from_crawler(crawler, *args, **kwargs)
		# Register the spider_closed handler on spider_closed signal
		crawler.signals.connect(spider.spider_closed, signals.spider_closed)
		return spider

	def spider_closed(self):
		""" Handler for spider_closed signal."""
		print('There are', len(self.valid_url), 'working links and',
			  len(self.invalid_url), 'broken links.', sep=' ')

		if len(self.invalid_url) > 0:
			df = pd.DataFrame(self.invalid_url)
			print (df)
			df.to_csv('invalid_urls.csv', index=False)

		df = pd.DataFrame(self.valid_url)
		print (df)
		df.to_csv('valid_urls.csv', index=False)


if __name__ == "__main__":
	process = CrawlerProcess({
		'USER_AGENT': 'Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 5.1)'
	})
	process.crawl(LinkCheckerSpider)
	process.start() # the script will block here until the crawling is finished