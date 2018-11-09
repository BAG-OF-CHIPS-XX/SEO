import requests
from bs4 import BeautifulSoup


def count_words(url, the_word):
    r = requests.get(url, allow_redirects=False)
    soup = BeautifulSoup(r.content, 'lxml')
    words = soup.find(text=lambda text: text and the_word in text)
    try:
    	return len(words)
    except:
    	return ('0')


def main():
	keyword ='xbox clips'
	serp = requests.get('https://www.google.com/search?q={}'.format(keyword)).content 
	soup = BeautifulSoup(serp, 'lxml')#.encode("utf-8")
	#print (soup)
	ser = soup.findAll("div", class_="g")

	for i in ser:
		# print (i)
		
		serp_title = i.find("h3").get_text()
		url = i.find("cite").get_text()
		snip =  i.find("span",class_="st").get_text()

		soup = BeautifulSoup(requests.get(url).content, 'lxml')
		words = soup.find(text=lambda text: text and keyword in text)
	    try:
	    	word_count = str(len(words))
	    except:
	    	word_count = str(0)
		try:
			page_title = soup.find("title").get_text()
		except AttributeError:
			page_title = 'None'
		try:
			first_h1   = soup.find("h1").get_text()
		except AttributeError:
			first_h1 = 'None'

		print ('SERP:')
		print (url)
		print (serp_title)
		print (snip)
		print ('')
		print ('PAGE:')
		print ('Title tag: ' + page_title)
		print ('First h1 tag: ' + first_h1)
		print ('Keyword count: ' + word_count)
		print ("-----------------")
		print ('')

if __name__ == '__main__':
    main()