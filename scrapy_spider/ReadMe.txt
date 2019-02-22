pip install pandas,scrapy
Run "scrapy crawl link_checker" from cmd line as admin.

For 301 and 302s:
Run python script to get the final destination url of all urls in the url column of invalid_urls.csv
Update the hrefs on all urls in the from column of invalid_urls.csv with the newly found final destination urls.

For 404s:
Make those pages 301 to a similar page or 301 to the homepage.
Update hrefs to reflect the newly selected page.


