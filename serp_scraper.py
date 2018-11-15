import requests
import textstat
from bs4 import BeautifulSoup
from bs4.element import Comment


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)



def count_words(url, the_word):
	r = requests.get(url, allow_redirects=False)
	soup = BeautifulSoup(r.content, 'lxml')
	words = soup.find(text=lambda text: text and the_word in text)
	try:
		return len(words)
	except:
		return ('0')

def text_analysis(test_data):
	#flesch_reading_ease: higher scores indicate material that is easier to read. aim for >60.0
	print ('flesch_reading_ease: '+str(textstat.flesch_reading_ease(test_data)))
	#smog_index: Calculates US grade level
	print ('smog_index: '+str(textstat.smog_index(test_data)))
	#flesch_kincaid_grade: Calculates US grade level
	print ('flesch_kincaid_grade: '+str(textstat.flesch_kincaid_grade(test_data)))
	#Colman Liau: Calculates US grade level
	print ('coleman_liau_index: '+str(textstat.coleman_liau_index(test_data)))
	#automated_readability_index: Calculates US grade level
	print ('automated_readability_index: '+str(textstat.automated_readability_index(test_data)))
	#Dale Chall Readability Score: 0.1579(dificult words / words *100) + 0.0496(words/sentences)
	print ('dale_chall_readability_score: '+str(textstat.dale_chall_readability_score(test_data)))
	#number of difficult words
	print ('difficult_words: '+str(textstat.difficult_words(test_data)))
	#Linsear Write: Calculates the U.S. grade level of a text sample based on sentence length and the number of words with three or more syllables. 
	print ('linsear_write_formula: '+str(textstat.linsear_write_formula(test_data)))
	#gunning_frog: The text can be understood by someone who left full-time education at a later age than the index
	print ('gunning_fog: '+str(textstat.gunning_fog(test_data)))
	#text_standard: Calculates US grade level
	print ('text_standard: '+str(textstat.text_standard(test_data)))


def main():
	##setup##
	keyword ='insta followers'
	serp = requests.get('https://www.google.com/search?q={}'.format(keyword)).content 
	soup = BeautifulSoup(serp, 'lxml')#.encode("utf-8")
	#print (soup)
	ser = soup.findAll("div", class_="g")
	rank = 1
	print ("____"+keyword.upper()+' SERP RESULTS____')
	##extract info for each url in SERP##
	for i in ser:
		# print (i)
		#google info
		print ('Position: {}').format(str(rank))
		rank +=1
		try:
			serp_title = i.find("h3").get_text()
		except:
			serp_title = 'None'
		try:
			url = i.find("cite").get_text()
		except:
			url = 'None'
		try:
			snip =  i.find("span",class_="st").get_text()
		except:
			snip = 'None'
		#page info	
		try:
			soup = BeautifulSoup(requests.get(url).content, 'lxml')
			words = soup.find(text=lambda text: text and keyword in text)
		except:
			print 'error with url must be complicated serp'

		
		html = requests.get(url).text

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

		##print results##
		print ('URL: '+url)
		print ('SEO Title: '+serp_title)
		print ('Meta Description: ')
		print (snip)
		print ('Title Tag: ' + page_title)
		print ('H1 Tag: ' + first_h1)
		print ('Keyword Count: ' + word_count)
		print ('\nBody text analysis: ')
		text_analysis(text_from_html(html))
		print ('')
		print ("-----------------")
		print ('')

if __name__ == '__main__':
	main()